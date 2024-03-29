"""Run command"""

import shlex
import subprocess

import click
import docker

from byoa.config.manifest import Manifest, check_manifest


@click.command("run", short_help="executes the processor")
@click.option(
    "--entrypoint",
    "-e",
    type=click.Choice(["api", "cli"], case_sensitive=False),
    default="cli",
    help="How the processor is started",
)
@click.option(
    "--port",
    "-p",
    default=8081,
    help="Redirection port when using api mode",
)
@click.option("--build", "-b", is_flag=True, help="Build the image before running")
@click.option(
    "--args",
    "-a",
    help="Additional arguments to pass to the command",
)
@check_manifest
def run_processor(entrypoint: str, build: bool, args: str, port: int):
    """Runs the processor's Docker image"""

    manifest = Manifest()
    docker_client = docker.from_env()

    if build:
        click.echo("Building image...", nl=False)
        image, _ = docker_client.images.build(path="./", tag=manifest.slug)
        click.echo("DONE !")
    else:
        image = docker_client.images.get(manifest.slug)

    click.echo(f"Running image {image.tag}")
    if entrypoint == "api":
        docker_client.containers.run(
            image, environment=["RUN_MODE_ENV=API"], ports={"80": port}, detach=True
        )
        click.echo(
            f"API running on http://localhost:{port}. "
            f"Swagger UI available at http://localhost:{port}/docs",
        )

    else:
        if args:
            arg_list = shlex.split(args)
        else:
            arg_list = []

        command = ["docker", "run", image.id] + arg_list

        raw_output = subprocess.run(command, capture_output=True, text=True, check=True).stdout
        click.echo(raw_output)
