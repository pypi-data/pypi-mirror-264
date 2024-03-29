from pathlib import Path
from typing import Annotated

import typer
from amsdal.configs.main import settings
from amsdal.manager import AmsdalManager
from amsdal.migration.data_classes import MigrationDirection
from amsdal.migration.data_classes import MigrationResult
from amsdal.migration.data_classes import ModuleTypes
from amsdal.migration.executors.default_executor import DefaultMigrationExecutor
from amsdal.migration.file_migration_executor import FileMigrationExecutorManager
from amsdal.migration.migrations import MigrationSchemas
from amsdal.migration.migrations_loader import MigrationsLoader
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print

from amsdal_cli.commands.migrations.app import sub_app
from amsdal_cli.commands.migrations.constants import MIGRATIONS_DIR_NAME
from amsdal_cli.utils.cli_config import CliConfig


@sub_app.command(name='apply')
def apply(
    ctx: typer.Context,
    number: Annotated[str, typer.Argument(...)] = None,  # type: ignore # noqa: RUF013
    build_dir: Annotated[Path, typer.Option('--build-dir', '-b')] = Path('.'),
    *,
    module_type: Annotated[ModuleTypes, typer.Option('--module', '-m')] = ModuleTypes.APP,
    fake: Annotated[bool, typer.Option('--fake')] = False,
    config: Annotated[Path, typer.Option('--config', '-c')] = None,  # type: ignore # noqa: RUF013
) -> None:
    """
    Apply migrations. Do not forget to build the project before applying migrations by `amsdal build` command.
    """
    cli_config: CliConfig = ctx.meta['config']

    settings.override(APP_PATH=build_dir)
    config_manager = AmsdalConfigManager()
    config_manager.load_config(config or cli_config.config_path)
    amsdal_manager = AmsdalManager()
    amsdal_manager.setup()
    amsdal_manager.authenticate()
    amsdal_manager.post_setup()

    app_migrations_loader = MigrationsLoader(
        migrations_dir=build_dir / MIGRATIONS_DIR_NAME,
        module_type=ModuleTypes.APP,
    )
    schemas = MigrationSchemas()
    executor = FileMigrationExecutorManager(
        app_migrations_loader=app_migrations_loader,
        executor=DefaultMigrationExecutor(schemas),
    )
    result: list[MigrationResult] = executor.execute(
        migration_number=int(number) if number else None,
        module_type=module_type,
        fake=fake,
    )

    if not result:
        print('[blue]Migrations are up to date[/blue]')
        return

    reverted = [item for item in result if item.direction == MigrationDirection.BACKWARD]
    applied = [item for item in result if item.direction == MigrationDirection.FORWARD]

    if reverted:
        print('[yellow]Migrations reverted[/yellow]')
        for item in reverted:
            print(f'  [yellow]{item.migration.number}[/yellow] - [yellow]{item.migration.path.name}[/yellow]')

    if applied:
        print('[green]Migrations applied[/green]')
        for item in applied:
            print(f'  [green]{item.migration.number}[/green] - [green]{item.migration.path.name}[/green]')
