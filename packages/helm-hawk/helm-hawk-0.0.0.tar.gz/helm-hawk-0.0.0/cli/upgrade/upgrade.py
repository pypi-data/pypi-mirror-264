import click
from cli.utils.helm import Helm


@click.command(name="upgrade",help="This command upgrades a release to a new version of a chart.")
@click.argument('release_name',type=click.STRING,required=True)
@click.argument('chart_path', type=click.Path(exists=True),required=True)
@click.option("--values", "-f", multiple=True, help="Specify values in a YAML file (can specify multiple)")
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
@click.option('--dry-run',help="Simulate the upgrade",is_flag=True)
def upgrade_command(release_name,chart_path,values,context,namespace,dry_run):
    helm=Helm(namespace=namespace,context=context)
    validation=helm.validate_chart(chart_path)
    if validation is not True:
        return click.echo(validation)
    output=helm.upgrade(release_name,chart_path,values,dry_run)
    click.echo(output)

