import os
import re
import subprocess
import sys
from dataclasses import field, dataclass
from functools import partial
from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

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
from detensor_cli.log import ClickHandler

VALID_PROJECT_NAME = r"^[a-zA-Z][a-zA-Z0-9 _-]*$"
BLACKLISTED_PROJECT_NAME = {"mpcc", "bot"}
TEMPLATE_DESCRIPTION = {
    "development": _("develop (for developer)"),
}

METHOD_DESCRIPTION = {
    "python_exec": _("同步执行计算"),
    "python_exec_sync": _("异步执行计算"),
}

if sys.version_info >= (3, 10):
    BLACKLISTED_PROJECT_NAME.update(sys.stdlib_module_names)


@dataclass
class ProjectContext:
    """项目模板生成上下文

    参数:
        variables: 模板渲染变量字典
        packages: 项目需要安装的包
    """

    variables: Dict[str, Any] = field(default_factory=dict)
    packages: List[str] = field(default_factory=list)


def project_name_validator(name: str) -> bool:
    return (
            bool(re.match(VALID_PROJECT_NAME, name))
            and name not in BLACKLISTED_PROJECT_NAME
    )


async def prompt_common_context(context: ProjectContext) -> ProjectContext:
    project_name = await InputPrompt(
        _("Project Name:"),
        validator=project_name_validator,
        error_message=_("Invalid project name!"),
    ).prompt_async(style=CLI_DEFAULT_STYLE)
    context.variables["project_name"] = project_name
    return context


async def prompt_simple_context(context: ProjectContext) -> ProjectContext:
    dir_name = (
        context.variables["project_name"].lower().replace(" ", "-").replace("-", "_")
    )
    src_choices: List[Choice[bool]] = [
        Choice(_('1) In a "{dir_name}" folder').format(dir_name=dir_name), False),
        Choice(_('2) In a "src" folder'), True),
    ]
    context.variables["use_src"] = (
        await ListPrompt(_("Where to store the plugin?"), src_choices).prompt_async(
            style=CLI_DEFAULT_STYLE
        )
    ).data

    return context


TEMPLATE_PROMPTS = {
    "simple": prompt_simple_context,
}


@click.command(
    cls=ClickAliasedCommand,
    aliases=["init"],
    context_settings={"ignore_unknown_options": True},
    help=_("Create a DeTensor project."),
)
@click.option(
    "-o",
    "--output-dir",
    default=None,
    type=click.Path(exists=True, file_okay=False, writable=True),
)
@click.option("-t", "--template", default=None, help=_("The project template to use."))
@click.option(
    "-p",
    "--python-interpreter",
    default=None,
    help=_("The python interpreter virtualenv is installed into."),
)
@click.argument("pip_args", nargs=-1, default=None)
@click.pass_context
@run_async
async def create_dev(
        ctx: click.Context,
        output_dir: Optional[str],
        template: Optional[str],
        python_interpreter: Optional[str],
        pip_args: Optional[List[str]],
):
    if not template:
        templates = list_project_templates()
        try:
            template = (
                await ListPrompt(
                    _("Select a template to use:"),
                    [Choice(TEMPLATE_DESCRIPTION.get(t, t), t) for t in templates],
                ).prompt_async(style=CLI_DEFAULT_STYLE)
            ).data

            # click.echo(f"获得的template！：{template}")
        except CancelledError:
            ctx.exit()

    context = ProjectContext()
    try:
        context = await prompt_common_context(context)
        if inject_prompt := TEMPLATE_PROMPTS.get(template):
            context = await inject_prompt(context)
    except ModuleLoadFailed as e:
        click.secho(repr(e), fg="red")
        ctx.exit()
    except CancelledError:
        ctx.exit()

    create_project(template, {"detensor": context.variables}, output_dir)

    try:
        install_dependencies = await ConfirmPrompt(
            _("Install dependencies now?"), default_choice=True
        ).prompt_async(style=CLI_DEFAULT_STYLE)
    except CancelledError:
        ctx.exit()

    use_venv = False
    project_dir_name = context.variables["project_name"].replace(" ", "-")
    project_dir = Path(output_dir or ".") / project_dir_name
    venv_dir = project_dir / ".venv"

    if install_dependencies:
        try:
            use_venv = await ConfirmPrompt(
                _("Create virtual environment?"), default_choice=True
            ).prompt_async(style=CLI_DEFAULT_STYLE)
        except CancelledError:
            ctx.exit()

        if use_venv:
            click.secho(
                _("Creating virtual environment in {venv_dir} ...").format(
                    venv_dir=venv_dir
                ),
                fg="yellow",
            )
            await create_virtualenv(
                venv_dir, prompt=project_dir_name, python_path=python_interpreter
            )

        config_manager = ConfigManager(working_dir=project_dir, use_venv=use_venv)

        # 假设你的shell脚本路径是 /path/to/your/script.sh

        # print(os.getcwd())

        print("正在创建项目和下载依赖包，请耐心等候...")
        # 指定脚本位置和参数
        script_path = os.getcwd() / project_dir / "start.sh"
        cwd = os.getcwd() / project_dir

        # print(f"\033[31m{script_path}\033[0m")

        # # 在指定位置运行脚本
        # process = subprocess.run(
        #     ["/bin/bash", script_path],  # 使用split将参数分割成列表
        #     cwd=cwd,  # 指定工作目录
        #     text=True,  # 如果需要获取输出，设置为True
        #     capture_output=True  # 捕获输出和错误
        # )
        # 
        process = subprocess.Popen(
            ["/bin/bash", script_path],
            stdout=subprocess.PIPE,
            cwd=cwd,
            text=True
        )

        while True:
            output = process.stdout.readline()

            if not output and process.poll() is not None:
                break

            # 在这里处理输出结果或者更新进度条等操作
            print(output)

        returncode = process.returncode

        # 检查脚本是否成功执行
        if returncode == 0:
            click.secho(_("脚本执行成功!"), fg="green")
            click.secho(_("Run the following command to start your DeTensor:"), fg="green")
            click.secho(f"  cd {project_dir} && source .venv/bin/activate && cd compute-core && python3 ~/cli/main.py",
                        fg="green")
        else:
            print("脚本执行失败，错误信息：", process.stderr)

