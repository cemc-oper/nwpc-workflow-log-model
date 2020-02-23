import click
from nwpc_workflow_log_model.analytics.node_status_change_dfa import NodeStatusChangeDFA


@click.command()
@click.option("--name", default="ecflow", help="DFA's name")
@click.option("--output-file", help="output file path", required=True)
def cli(name, output_file):
    dfa = NodeStatusChangeDFA(name)
    dfa.node_situation.get_graph().draw(output_file, prog='dot')


if __name__ == "__main__":
    cli()
