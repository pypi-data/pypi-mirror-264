# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

"""Hello World plugin for circfirm.

Author(s): Alec Delaney
"""

import click

# You could import circfirm if you need any of its functionalities:
# import cirfirm


# The plugin will be loaded by attaching cli() to the main circfirm CLI
# You can use name="XYZ" to give the command its own name
@click.command(name="hello-world")
def cli() -> None:
    """Say hi."""
    click.echo("Hello, world!")
