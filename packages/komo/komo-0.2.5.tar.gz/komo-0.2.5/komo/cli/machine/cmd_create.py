import time
from typing import Optional

import click

from komo import printing
from komo.core import create_machine, get_machine
from komo.types import Cloud, MachineStatus


@click.command("create")
@click.option("--gpus", type=str, default=None)
@click.option("--cloud", "-c", type=str, default=None)
@click.option("--detach", "-d", is_flag=True, default=False)
@click.argument("name", nargs=1)
def cmd_create(
    gpus: Optional[str],
    cloud: Optional[str],
    detach: bool,
    name: str,
):
    if cloud:
        cloud = Cloud(cloud)
    machine = create_machine(gpus, name, cloud)
    printing.success(f"Machine {machine.name} successfully created")

    if detach:
        return

    printing.info("Waiting for machine to start...")

    last_messsage = None
    while True:
        machine = get_machine(name)

        should_break = False
        error = False
        if machine.status in [MachineStatus.PENDING, MachineStatus.INITIALIZING]:
            pass
        elif machine.status == MachineStatus.RUNNING:
            should_break = True
        else:
            should_break = True
            error = True

        if machine.status_message and machine.status_message != last_messsage:
            if error:
                printing.error(machine.status_message)
            else:
                printing.info(machine.status_message)

            last_messsage = machine.status_message

        if should_break:
            break

        time.sleep(5)

    if machine.status == MachineStatus.RUNNING:
        printing.success(f"Machine {name} successfully created")
