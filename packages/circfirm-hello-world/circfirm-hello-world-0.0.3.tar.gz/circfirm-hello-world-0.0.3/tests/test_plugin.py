# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for the plugin functionality."""


from click.testing import CliRunner

from circfirm_hello_world import cli


def test_plugin() -> None:
    """Tests the plugin functionality."""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert result.output == "Hello, world!\n"
