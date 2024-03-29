"""Command line interface of the BYOA tool"""

import click

from byoa import __version__
from byoa.cli.build import build
from byoa.cli.context import context
from byoa.cli.delete import delete
from byoa.cli.deploy import deploy
from byoa.cli.init import init_processor
from byoa.cli.manifest import update_manifest
from byoa.cli.run import run_processor


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(
    __version__, "--version", "-V", package_name="byoa", message="%(package)s %(version)s"
)
def main():
    """A command-line utility to Build Your Own Analytic"""


main.add_command(build)
main.add_command(context)
main.add_command(delete)
main.add_command(deploy)
main.add_command(init_processor)
main.add_command(update_manifest)
main.add_command(run_processor)
