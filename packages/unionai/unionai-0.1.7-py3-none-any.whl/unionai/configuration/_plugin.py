"""All imports to unionai in this file should be in the function definition.

This plugin is loaded by flytekit, so any imports to unionai can lead to circular imports.
"""

from typing import Optional

import click
from click import Group, Option
from flytekit.remote import FlyteRemote


class UnionAIPlugin:
    @staticmethod
    def get_remote(
        config: Optional[str],
        project: str,
        domain: str,
        data_upload_location: Optional[str] = None,
    ) -> FlyteRemote:
        from unionai._config import _get_config_obj, _is_serverless_endpoint
        from unionai.remote import UnionRemote

        cfg_obj = _get_config_obj(config)
        if _is_serverless_endpoint(cfg_obj.platform.endpoint) and project == "flytesnacks":
            project = "default"

        return UnionRemote(
            cfg_obj,
            default_project=project,
            default_domain=domain,
            data_upload_location=data_upload_location,
        )

    @staticmethod
    def configure_pyflyte_cli(main: Group) -> Group:
        """Configure pyflyte's CLI."""

        import unionai._config
        from unionai._config import _UNIONAI_CONFIG, _get_config_obj
        from unionai.cli._create import create
        from unionai.cli._delete import delete
        from unionai.cli._get import get
        from unionai.cli._update import update
        from unionai.ucimage._image_builder import _register_union_image_builder

        def _cli_main_config_callback(ctx, param, value):
            # Set org based on config from `pyflyte --config` for downstream cli
            # commands to use.
            if value is not None:
                _UNIONAI_CONFIG.config = value

            # Only register image builder for serverless
            cfg_obj = _get_config_obj(value)
            if unionai._config._is_serverless_endpoint(cfg_obj.platform.endpoint):
                _register_union_image_builder()
            return value

        for p in main.params:
            if p.name == "config":
                p.callback = _cli_main_config_callback

        # Configure org at the top level:
        def _set_org(ctx, param, value):
            _UNIONAI_CONFIG.org = value

        main.params.append(
            click.Option(
                ["--org"],
                help="Set organization",
                hidden=True,
                callback=_set_org,
                expose_value=False,
            )
        )

        from flytekit.clis.sdk_in_container.run import RunCommand, RunLevelParams, run

        class RunWithNewProjectDefault(RunCommand):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                for p in self.params:
                    if p.name == "image_config":
                        p.default = lambda: [unionai._config._get_default_image()]

            def get_command(self, ctx, filename):
                command = super().get_command(ctx, filename)
                run_params: RunLevelParams = ctx.obj
                if run_params.is_remote and run_params.project == "flytesnacks":
                    run_params.project = unionai._config._get_default_project(run_params.project)
                return command

        main.add_command(RunWithNewProjectDefault(name="run", help=run.help), "run")

        def update_or_create_group(new_group):
            try:
                main_group = main.commands[new_group.name]
                for name, command in new_group.commands.items():
                    main_group.add_command(command, name)
            except KeyError:
                main.add_command(new_group)

        new_groups = [create, delete, update, get]
        for group in new_groups:
            update_or_create_group(group)

        def yield_all_options():
            commands = [main]

            while commands:
                command = commands.pop()
                yield from (p for p in command.params if isinstance(p, Option))

                if isinstance(command, Group):
                    commands.extend(list(command.commands.values()))

        for p in yield_all_options():
            if p.name == "image_config" and p.default is not None:
                p.default = lambda: [unionai._config._get_default_image()]
            elif p.name == "project" and p.default is not None:
                p.default = lambda: unionai._config._get_default_project(p.default)

        return main

    @staticmethod
    def secret_requires_group() -> bool:
        """Return True if secrets require group entry."""
        return False

    @staticmethod
    def get_default_image() -> Optional[str]:
        """Return default image."""

        from unionai._config import _get_default_image

        return _get_default_image()

    @staticmethod
    def get_auth_success_html(endpoint: str) -> Optional[str]:
        """Get default success html. Return None to use flytekit's default success html."""
        from unionai._config import _get_auth_success_html

        return _get_auth_success_html(endpoint)
