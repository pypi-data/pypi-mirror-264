import os
import re
import subprocess
import sys
from dataclasses import field, dataclass
from functools import partial
from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional, cast
from .project import ProjectContext

import click
from noneprompt import (
    Choice,
    ListPrompt,
    InputPrompt,
    ConfirmPrompt,
    CancelledError,
)

from detensor_cli import _
from detensor_cli.cli import CLI_DEFAULT_STYLE, ClickAliasedCommand, ClickAliasedGroup, run_sync, run_async
from detensor_cli.config import ConfigManager
from detensor_cli.exceptions import ModuleLoadFailed
from detensor_cli.handlers import (
    Reloader,
    FileFilter,
    run_project,
    create_project,
    get_project_root,
    create_virtualenv,
    terminate_process,
    generate_run_script,
    list_project_templates,

)


async def prompt_test_execution_exec_context(context: ProjectContext) -> ProjectContext:
    members = await InputPrompt(
        _("参与同步计算的节点（例如：'org0'或者'org0 org1'）:"),
        validator=node_name_validator,
        error_message=_("Invalid node name!"),
    ).prompt_async(style=CLI_DEFAULT_STYLE)
    context.variables["members"] = members

    uid = await InputPrompt(
        _("计算的合约ID（请输入整数,目前仅支持0、1、2）:"),
        validator=node_num_validator,
        error_message=_("Invalid uid!"),
    ).prompt_async(style=CLI_DEFAULT_STYLE)
    context.variables["uid"] = uid
    return context


async def prompt_test_count_num_context(context: ProjectContext) -> ProjectContext:
    count = await InputPrompt(
        _("开启的节点个数:"),
        validator=count_num_validator,
        error_message=_("Invalid count num!"),
    ).prompt_async(style=CLI_DEFAULT_STYLE)
    context.variables["count"] = count
    return context


def node_num_validator(num: str) -> bool:
    try:
        a = int(num)
        return a >= 0 and True
    except ValueError:
        return False


def count_num_validator(num: str) -> bool:
    try:
        a = int(num)
        return a > 0 and True
    except ValueError:
        return False


def node_name_validator(name: str) -> bool:
    try:
        a = name.split()
        for t in a:
            if len(t) < 4:
                return False
            else:
                t1 = t[:3]
                t2 = t[3:]
                if t1 != "org":
                    return False
                try:
                    b = int(t2)
                    if b < 0:
                        return False
                except ValueError:
                    return False
        return True
    except ValueError:
        return False


def contract_id_validator(uid: str) -> bool:
    try:
        a = int(uid)
        return a >= 0 and True
    except ValueError:
        return False


@click.group(
    cls=ClickAliasedGroup, invoke_without_command=True, help=_("本地开发项目测试.")
)
@click.pass_context
@run_async
async def test_execution(ctx: click.Context):
    if ctx.invoked_subcommand is not None:
        return

    command = cast(ClickAliasedGroup, ctx.command)

    choices: List[Choice[click.Command]] = []
    for sub_cmd_name in await run_sync(command.list_commands)(ctx):
        if sub_cmd := await run_sync(command.get_command)(ctx, sub_cmd_name):
            choices.append(
                Choice(
                    sub_cmd.help
                    or _("Run subcommand {sub_cmd.name!r}").format(sub_cmd=sub_cmd),
                    sub_cmd,
                )
            )

    try:
        result = await ListPrompt(
            _("What do you want to do?"), choices=choices
        ).prompt_async(style=CLI_DEFAULT_STYLE)
    except CancelledError:
        ctx.exit()

    sub_cmd = result.data
    await run_sync(ctx.invoke)(sub_cmd)


@test_execution.command(
    cls=ClickAliasedCommand, aliases=["exec"], help=_("同步计算")
)
@click.option(
    '-H',
    '--host',
    type=str,
    default='http://localhost:3000',
    help='http endpoint of compute user service',
)
@click.option(
    '-u',
    '--uid',
    type=int,
    default=1,
    help='contract uid'
)
@click.option(
    '-a',
    '--args',
    type=str,
    nargs='+',
    help='execute arguments'
)
@click.option(
    '-m',
    '--members',
    type=str,
    nargs="+",
    help='members involved in this execution'
)
@click.option(
    '-v',
    '--verbose',
    default=None,
    type=str,
    help='print debug information'
)
@click.pass_context
@run_async
async def test_exec(
        ctx: click.Context,
        host: Optional[str],
        uid: Optional[int],
        args: Optional[str],
        members: Optional[str],
        verbose: Optional[str]
):
    context = ProjectContext()
    try:
        context = await prompt_test_execution_exec_context(context)
        uid = context.variables["uid"]
        members = context.variables["members"]
    except ModuleLoadFailed as e:
        click.secho(repr(e), fg="red")
        ctx.exit()
    except CancelledError:
        ctx.exit()

    # click.secho(os.getcwd())
    # 启动python_exec脚本
    command = f'scripts/python_exec -u {uid} -m {members}'
    process = subprocess.run(command, shell=True, check=False)
    if process.returncode == 0:
        print('python_exec run successfully')

    else:
        print('python_exec failed with return code:', process.returncode)


@test_execution.command(
    cls=ClickAliasedCommand, aliases=["exec_sync"], help=_("异步计算")
)
@click.option(
    '-H',
    '--host',
    type=str,
    default='http://localhost:3000',
    help='http endpoint of compute user service',
)
@click.option(
    '-u',
    '--uid',
    type=int,
    default=1,
    help='contract uid'
)
@click.option(
    '-a',
    '--args',
    type=str,
    nargs='+',
    help='execute arguments'
)
@click.option(
    '-m',
    '--members',
    type=str,
    nargs="+",
    help='members involved in this execution'
)
@click.option(
    '-v',
    '--verbose',
    default=None,
    type=str,
    help='print debug information'
)
@click.pass_context
@run_async
async def test_exec_sync(
        ctx: click.Context,
        host: Optional[str],
        uid: Optional[int],
        args: Optional[str],
        members: Optional[str],
        verbose: Optional[str]
):
    context = ProjectContext()
    try:
        context = await prompt_test_execution_exec_context(context)
        uid = context.variables["uid"]
        members = context.variables["members"]
    except ModuleLoadFailed as e:
        click.secho(repr(e), fg="red")
        ctx.exit()
    except CancelledError:
        ctx.exit()

    # click.secho(os.getcwd())
    # 启动python_exec_sync脚本
    command = f'scripts/python_exec_sync -u {uid} -m {members}'
    process = subprocess.run(command, shell=True, check=False)
    if process.returncode == 0:
        print('python_exec_sync run successfully')

    else:
        print('python_exec_sync failed with return code:', process.returncode)


@test_execution.command(
    cls=ClickAliasedCommand, aliases=["start"], help=_("开启节点")
)
@click.option(
    '-c',
    '--count',
    type=int,
    default=1,
    help='http endpoint of compute user service',
)
@click.pass_context
@run_async
async def test_start(
        ctx: click.Context,
        count: Optional[int]
):
    context = ProjectContext()
    try:
        context = await prompt_test_count_num_context(context)
        count = context.variables["count"]
    except ModuleLoadFailed as e:
        click.secho(repr(e), fg="red")
        ctx.exit()
    except CancelledError:
        ctx.exit()

    # click.secho(os.getcwd())
    # 启动python_exec_sync脚本
    command = f'scripts/start -c {count}'
    process = subprocess.run(command, shell=True, check=False)
    if process.returncode == 0:
        print('start run successfully')

    else:
        print('start failed with return code:', process.returncode)


@test_execution.command(
    cls=ClickAliasedCommand, aliases=["stop"], help=_("关闭节点")
)
@click.pass_context
@run_async
async def test_stop(
        ctx: click.Context,
):
    # click.secho(os.getcwd())
    # 启动python_exec_sync脚本
    command = f'scripts/stop'
    process = subprocess.run(command, shell=True, check=False)
    if process.returncode == 0:
        print('stop run successfully')

    else:
        print('stop failed with return code:', process.returncode)
