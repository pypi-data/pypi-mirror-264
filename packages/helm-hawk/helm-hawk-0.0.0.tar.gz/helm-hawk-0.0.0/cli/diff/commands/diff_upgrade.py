import click
from cli.utils.helm import Helm




@click.command(name='upgrade')
@click.argument('release_name',type=click.types.STRING,required=True)
@click.argument('chart_path',type=click.Path(exists=True),required=True)
@click.option('--values','-f',help=f"Provide values file path",type=click.Path(exists=True),multiple=True)
@click.option('--context','-c',help="Context that you want to use",type=click.STRING)
@click.option('--namespace','-n',help="Namespace you want to use",type=click.STRING)
def diff_upgrade(chart_path,release_name,values,context,namespace):
    '''Show a diff explaining what a helm upgrade would change.'''
    helm=Helm(context=context,namespace=namespace)
    click.echo("Validating charts...")
    validation=helm.validate_chart(chart_path)
    if validation is not True:
        return click.echo(validation)
    output=helm.diff(release_name,chart_path,values)
    click.echo(output)
    # show prompt for to upgrade from diff
    prompt=input("enter Yes to perform the upgrade: ")
    if prompt.lower() == "yes":
        output=helm.upgrade(release_name,chart_path,values,False)
        click.echo(output)

