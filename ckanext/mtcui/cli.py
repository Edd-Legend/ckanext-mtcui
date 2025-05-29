import click


@click.group(short_help="mtcui CLI.")
def mtcui():
    """mtcui CLI.
    """
    pass


@mtcui.command()
@click.argument("name", default="mtcui")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [mtcui]
