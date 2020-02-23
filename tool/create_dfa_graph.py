import click
from nwpc_workflow_log_model.analytics.node_status_change_dfa import NodeStatusChangeDFA


@click.group()
def cli():
    pass


@cli.command("node_status_change")
@click.option("--name", default="ecflow", help="DFA's name")
@click.option("--output-file", help="output file path", required=True)
def node_status_change(name, output_file):
    dfa = NodeStatusChangeDFA(name)
    dfa.get_graph().draw(output_file, prog='dot')


if __name__ == "__main__":
    cli()
