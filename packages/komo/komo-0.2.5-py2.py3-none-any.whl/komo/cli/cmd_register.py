import os
from typing import List, Optional

import click

from komo import printing
from komo.core import register


@click.command("register")
def cmd_register():
    email = click.prompt("email")
    password = click.prompt("password", hide_input=True)

    register(email, password)
    printing.success("You are now registered and logged in!")
