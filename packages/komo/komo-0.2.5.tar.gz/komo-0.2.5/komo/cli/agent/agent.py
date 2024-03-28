import click

from komo.cli.agent.cmd_run import cmd_run
from komo.cli.agent.cmd_setup import cmd_setup


@click.group()
@click.pass_context
def agent(ctx: click.Context):
    pass


agent.add_command(cmd_run)
agent.add_command(cmd_setup)
