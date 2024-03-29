import click
import os
import platform
import pkg_resources

from meerkat import email as send_email
from meerkat.api import get_user_token

@click.group()
def meerkat():
    pass

@meerkat.command()
def ping():
    resource_path = "ping_sounds/default_ping.mp3"
    full_path = pkg_resources.resource_filename(__name__, resource_path)
    print(full_path)
    play_sound(full_path)

@meerkat.command()
@click.argument('message', type=str)
def email(message):
    result = send_email(message=message)
    click.echo(f'{result}')

@meerkat.command()
def login():
    email = click.prompt("Enter Email")
    password = click.prompt("Enter Password", hide_input=True)
    token = get_user_token(email, password)

    if not token:
        click.echo("Invalid email or password.")
        return

    #save token to user HOME and set OS env
    with open(os.path.expanduser("~") + "/.meerkat", "w") as file:
        file.write(token)
    os.environ["MEERKAT_TOKEN"] = token

    click.echo(f"\nMeerkat initialized successfully.")

def play_sound(file_name: str):
    system = platform.system()
    if system == 'Darwin':  # macOS
        os.system(f'afplay {file_name}')
    elif system == 'Linux':
        os.system(f'aplay {file_name}')
    elif system == 'Windows':
        os.system(f'powershell -c "(New-Object Media.SoundPlayer \'{file_name}\').PlaySync();"')
    else:
        click.echo('Unsupported operating system.')

if __name__ == "__main__":
    meerkat()