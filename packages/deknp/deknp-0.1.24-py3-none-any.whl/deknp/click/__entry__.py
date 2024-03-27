from . import app
from . import env as env_command

app.add_typer(env_command.app, name='env')


def main():
    app()
