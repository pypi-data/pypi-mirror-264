import click

from . import policies
from ..output.table import output_entry


@click.command(name="set-multifactor-policy")
@click.option("--name", required=True)
@click.option("--label", multiple=True, type=str)
@click.option("--duration", required=True, type=int)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_set_multifactor_policy(ctx, **kwargs):
    output_entry(ctx, policies.set_multifactor_policy(ctx, **kwargs).to_dict())


@click.command(name="list-multifactor-policies")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_multifactor_policies(ctx, **kwargs):
    results = policies.list_multifactor_policies(ctx, **kwargs)
    print(policies.format_multifactor_policies(ctx, results))


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
