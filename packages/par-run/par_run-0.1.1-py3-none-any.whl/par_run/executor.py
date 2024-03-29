"""Todo"""

import asyncio
import configparser
import enum
import multiprocessing as mp
import queue
import subprocess
from collections import OrderedDict
from concurrent.futures import Future, ProcessPoolExecutor
from pathlib import Path
from queue import Queue
from typing import Callable, List, Optional, Protocol, TypeVar, Union

import rich
from pydantic import BaseModel, ConfigDict, Field

# Type alias for a generic future.
GenFuture = Union[Future, asyncio.Future]

ContextT = TypeVar("ContextT")


class ProcessingStrategy(enum.Enum):
    """Enum for processing strategies."""

    AS_COMPLETED = "As Completed"
    ON_RECV = "On Receive"


class CommandStatus(enum.Enum):
    """Enum for command status."""

    NOT_STARTED = "Not Started"
    RUNNING = "Running"
    SUCCESS = "Success"
    FAILURE = "Failure"

    def completed(self) -> bool:
        """Return True if the command has completed."""
        return self in [CommandStatus.SUCCESS, CommandStatus.FAILURE]


class Command(BaseModel):
    """Holder for a command and its name."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    cmd: str
    status: CommandStatus = CommandStatus.NOT_STARTED
    unflushed: List[str] = []
    num_non_empty_lines: int = 0
    ret_code: Optional[int] = None
    fut: Optional[GenFuture] = Field(default=None, exclude=True)

    def incr_line_count(self, line: str) -> None:
        """Increment the non-empty line count."""
        if line.strip():
            self.num_non_empty_lines += 1

    def append_unflushed(self, line: str) -> None:
        """Append a line to the output and increment the non-empty line count."""
        self.unflushed.append(line)

    def set_ret_code(self, ret_code: int):
        """Set the return code and status of the command."""
        self.ret_code = ret_code
        if self.fut:
            self.fut.cancel()
            self.fut = None
        if ret_code == 0:
            self.status = CommandStatus.SUCCESS
        else:
            self.status = CommandStatus.FAILURE

    def set_running(self):
        """Set the command status to running."""
        self.status = CommandStatus.RUNNING


class CommandCB(Protocol):
    def on_start(self, cmd: Command) -> None: ...
    def on_recv(self, cmd: Command, output: str) -> None: ...
    def on_term(self, cmd: Command, exit_code: int) -> None: ...


class CommandAsyncCB(Protocol):
    async def on_start(self, cmd: Command) -> None: ...
    async def on_recv(self, cmd: Command, output: str) -> None: ...
    async def on_term(self, cmd: Command, exit_code: int) -> None: ...


class CommandGroup(BaseModel):
    """Holder for a group of commands."""

    name: str
    cmds: OrderedDict[str, Command]

    def cancel_running(self) -> int:
        """Cancel all running commands in the group and return the exit code."""
        exit_code = 999
        for _, cmd in self.cmds.items():
            if cmd.status == CommandStatus.RUNNING:
                rich.print(
                    f"[red bold]Command {cmd} timed out, cancelling, ret_code == {exit_code}[/]"
                )
                if cmd.fut:
                    cmd.fut.cancel()
                    cmd.fut = None
                cmd.set_ret_code(exit_code)
        return exit_code

    async def run_async(
        self,
        strategy: ProcessingStrategy,
        callbacks: CommandCB,
    ):
        q = mp.Manager().Queue()
        pool = ProcessPoolExecutor()
        futs = [
            asyncio.get_event_loop().run_in_executor(
                pool, run_command, cmd.name, cmd.cmd, q
            )
            for _, cmd in self.cmds.items()
        ]

        for (_, cmd), fut in zip(self.cmds.items(), futs):
            cmd.fut = fut
            cmd.set_running()

        return await self._process_q_async(q, strategy, callbacks)

    def run(
        self,
        strategy: ProcessingStrategy,
        callbacks: CommandCB,
    ):
        q = mp.Manager().Queue()
        pool = ProcessPoolExecutor()
        futs = [
            pool.submit(run_command, cmd.name, cmd.cmd, q)
            for _, cmd in self.cmds.items()
        ]
        for (_, cmd), fut in zip(self.cmds.items(), futs):
            cmd.fut = fut
            cmd.set_running()

        return self._process_q(q, strategy, callbacks)

    def _process_q(
        self,
        q: Queue,
        strategy: ProcessingStrategy,
        callbacks: CommandCB,
    ) -> int:
        grp_exit_code = 0

        if strategy == ProcessingStrategy.ON_RECV:
            for _, cmd in self.cmds.items():
                callbacks.on_start(cmd)

        while True:
            try:
                q_result = q.get(block=True, timeout=10)
            except queue.Empty:
                continue

            # Can only get here with a valid message from the Q
            cmd_name = q_result[0]
            # print(q_result, type(q_result[0]), type(q_result[1]))
            exit_code: Optional[int] = (
                q_result[1] if isinstance(q_result[1], int) else None
            )
            output_line: Optional[str] = (
                q_result[1] if isinstance(q_result[1], str) else None
            )
            # print(output_line, exit_code)
            if exit_code is None and output_line is None:
                raise ValueError("Invalid Q message")

            cmd = self.cmds[cmd_name]
            if strategy == ProcessingStrategy.ON_RECV:
                if exit_code is None:
                    cmd.incr_line_count(output_line)
                    callbacks.on_recv(cmd, output_line)
                else:
                    cmd.set_ret_code(exit_code)
                    callbacks.on_term(cmd, exit_code)
                    if exit_code != 0:
                        grp_exit_code = 1

            if strategy == ProcessingStrategy.AS_COMPLETED:
                if exit_code is None:
                    cmd.incr_line_count(output_line)
                    cmd.append_unflushed(output_line)
                else:
                    callbacks.on_start(cmd)
                    for line in cmd.unflushed:
                        callbacks.on_recv(cmd, line)
                    callbacks.on_term(cmd, exit_code)
                    cmd.set_ret_code(exit_code)
                    if exit_code != 0:
                        grp_exit_code = 1

            if all(cmd.status.completed() for _, cmd in self.cmds.items()):
                break
        return grp_exit_code

    async def _process_q_async(
        self,
        q: Queue,
        strategy: ProcessingStrategy,
        callbacks: CommandAsyncCB,
    ) -> int:
        grp_exit_code = 0

        if strategy == ProcessingStrategy.ON_RECV:
            for _, cmd in self.cmds.items():
                await callbacks.on_start(cmd)

        while True:
            await asyncio.sleep(0)
            try:
                q_result = q.get(block=True, timeout=10)
            except queue.Empty:
                continue

            # Can only get here with a valid message from the Q
            cmd_name = q_result[0]
            # print(q_result, type(q_result[0]), type(q_result[1]))
            exit_code: Optional[int] = (
                q_result[1] if isinstance(q_result[1], int) else None
            )
            output_line: Optional[str] = (
                q_result[1] if isinstance(q_result[1], str) else None
            )
            # print(output_line, exit_code)
            if exit_code is None and output_line is None:
                raise ValueError("Invalid Q message")

            cmd = self.cmds[cmd_name]
            if strategy == ProcessingStrategy.ON_RECV:
                if exit_code is None:
                    cmd.incr_line_count(output_line)
                    await callbacks.on_recv(cmd, output_line)
                else:
                    cmd.set_ret_code(exit_code)
                    await callbacks.on_term(cmd, exit_code)
                    if exit_code != 0:
                        grp_exit_code = 1

            if strategy == ProcessingStrategy.AS_COMPLETED:
                if exit_code is None:
                    cmd.incr_line_count(output_line)
                    cmd.append_unflushed(output_line)
                else:
                    await callbacks.on_start(cmd)
                    for line in cmd.unflushed:
                        await callbacks.on_recv(cmd, line)
                    await callbacks.on_term(cmd, exit_code)
                    cmd.set_ret_code(exit_code)
                    if exit_code != 0:
                        grp_exit_code = 1

            if all(cmd.status.completed() for _, cmd in self.cmds.items()):
                break
        return grp_exit_code


def read_commands_ini(filename: Union[str, Path]) -> list[CommandGroup]:
    """Read a commands.ini file and return a list of CommandGroup objects.

    Args:
        filename (Union[str, Path]): The filename of the commands.ini file.

    Returns:
        list[CommandGroup]: A list of CommandGroup objects.
    """
    config = configparser.ConfigParser()
    config.read(filename)

    command_groups = []
    for section in config.sections():
        if section.startswith("group."):
            group_name = section.replace("group.", "")
            commands = OrderedDict()
            for name, cmd in config.items(section):
                name = name.strip()
                commands[name] = Command(name=name, cmd=cmd.strip())
            command_group = CommandGroup(name=group_name, cmds=commands)
            command_groups.append(command_group)

    return command_groups


def write_commands_ini(filename: Union[str, Path], command_groups: list[CommandGroup]):
    """Write a list of CommandGroup objects to a commands.ini file.

    Args:
        filename (Union[str, Path]): The filename of the commands.ini file.
        command_groups (list[CommandGroup]): A list of CommandGroup objects.
    """
    config = configparser.ConfigParser()

    for group in command_groups:
        section_name = f"group.{group.name}"
        config[section_name] = {}
        for _, command in group.cmds.items():
            config[section_name][command.name] = command.cmd

    with open(filename, "w", encoding="utf-8") as configfile:
        config.write(configfile)


def run_command(name: str, command: str, q: Queue) -> None:
    """Run a command and put the output into a queue. The output is a tuple of the command
    name and the output line. The final output is a tuple of the command name and a dictionary
    with the return code.

    Args:
        name (str): Name of the command.
        command (str): Command to run.
        q (Queue): Queue to put the output into.
    """

    with subprocess.Popen(
        f"rye run {command}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ) as process:
        if process.stdout:
            for line in iter(process.stdout.readline, ""):
                q.put((name, line.strip()))
            process.stdout.close()
            process.wait()
            ret_code = process.returncode
            if ret_code is not None:
                q.put((name, int(ret_code)))
            else:
                raise ValueError("Process has no return code")
