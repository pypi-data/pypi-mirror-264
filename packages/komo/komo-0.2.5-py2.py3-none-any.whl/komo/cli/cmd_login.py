import os
from typing import List, Optional

import click

from komo import printing
from komo.core import login


@click.command("login")
def cmd_login():
    email = click.prompt("email")
    password = click.prompt("password", hide_input=True)

    login(email, password)
    printing.success("You are now logged in!")
