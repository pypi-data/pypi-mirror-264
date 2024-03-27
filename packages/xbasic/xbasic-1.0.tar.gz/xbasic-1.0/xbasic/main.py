import click
import webbrowser
import platform
import datetime
from shell import entry_shell


@click.group()
def cli():
    pass


@cli.command()
def report():
    """Open the GitHub page."""
    click.echo("Going to the Git page...")
    webbrowser.open("https://github.com/vivekkdagar/xbasic")


@cli.command()
@click.option('-f', type=click.Path(exists=True), default=None, help='Specify a file to execute within the shell.')
def shell(f):
    """Start an interactive shell."""
    print_intro()
    if f:
        if not f.endswith('.bsx'):
            click.echo("Error: File must end with '.bsx'.")
            return
        print(f)
    else:
        entry_shell()


def print_intro():
    version = "1.0"
    current_date_time = datetime.datetime.now().strftime("%b %d %Y, %H:%M:%S")
    os_name = platform.system()
    intro = f"XBasic {version} ({current_date_time}) on {os_name.lower()}"
    click.echo(intro)


if __name__ == '__main__':
    cli()
