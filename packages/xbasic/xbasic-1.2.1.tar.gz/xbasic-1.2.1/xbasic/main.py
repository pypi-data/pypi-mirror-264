import click
import webbrowser
import platform
import datetime
from .init_interp import run


@click.group()
def cli():
    """XBasic CLI tool."""
    pass


@cli.command()
def report():
    """Open the GitHub page."""
    click.echo("Going to the Git page...")
    webbrowser.open("https://github.com/vivekkdagar/xbasic")


def entry_shell():
    """Starts an interactive shell."""
    while True:
        text = input('>> ')
        if text.strip() == "":
            continue
        result, error = run('<stdin>', text)

        if error:
            print(error.as_string())
        elif result:
            print("The process returned: ", result)


@cli.command()
@click.option('-f', type=click.Path(exists=True), default=None, help='Specify a file to execute within the shell.')
def shell(f):
    """Start an interactive shell or execute a file within the shell."""
    print_intro()
    if f:
        if not f.endswith('.bsx'):
            click.echo("Error: File must end with '.bsx'.")
            return
        result, error = run('<stdin>', f'RUN("{f}")')
        if error:
            print(error.as_string())
        elif result:
            print("The process returned ", result)
    else:
        entry_shell()


def print_intro():
    """Print introductory information."""
    version = "1.2.1"
    current_date_time = datetime.datetime.now().strftime("%b %d %Y, %H:%M:%S")
    os_name = platform.system()
    intro = f"XBasic {version} ({current_date_time}) on {os_name.lower()}"
    click.echo(intro)


if __name__ == '__main__':
    cli()
