"""Deploy command"""

import click
import docker
import docker.errors
import requests

from byoa.config.context import ENDPOINT_KEY, REGISTRY_KEY, get_context_value
from byoa.config.manifest import Manifest, check_manifest
from byoa.exceptions import APIError, ImagePushError, MissingContextValue
from byoa.importer import get_variable


def _login_to_docker(docker_client: docker.DockerClient, registry: str):
    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)

    click.echo("Login to registry... ", nl=False)
    result_login = docker_client.login(username=username, password=password, registry=registry)
    click.echo(result_login["Status"])


def _save_processor(processor_id: str, data: dict, endpoint: str):
    try:
        click.echo(f"Saving processor {processor_id}... ", nl=False)
        response = requests.put(f"{endpoint}/process_graphs/{processor_id}", json=data, timeout=60)
        response.raise_for_status()
        click.echo("Done!")

    except requests.HTTPError as e:
        raise APIError(f'Cannot save processor {processor_id}: "{e}"') from e


def _delete_processor(processor_id: str, endpoint: str):
    try:
        response = requests.delete(f"{endpoint}/process_graphs/{processor_id}", timeout=60)
        response.raise_for_status()

    except requests.HTTPError as e:
        raise APIError(f'Cannot delete processor {processor_id}: "{e}"') from e


@click.command("deploy", short_help="deploys the processor")
@click.option(
    "--registry",
    help="Container registry name",
    envvar="BYOA_CONTAINER_REGISTRY",
    show_envvar=True,
    default=lambda: get_context_value(REGISTRY_KEY),
)
@click.option(
    "--endpoint",
    help="BYOA API endpoint",
    envvar="BYOA_ENDPOINT",
    show_envvar=True,
    default=lambda: get_context_value(ENDPOINT_KEY),
)
@click.option("--profile", help="Profile to use for environment values")
@check_manifest
def deploy(profile: str, registry: str, endpoint: str):
    """Saves and deploys the processor"""

    if profile:
        _registry = get_context_value(REGISTRY_KEY, profile, registry)
        _endpoint = get_context_value(ENDPOINT_KEY, profile, endpoint)

        if _endpoint is None:
            raise MissingContextValue(ENDPOINT_KEY)
        if _registry is None:
            raise MissingContextValue(REGISTRY_KEY)

        endpoint = _endpoint
        registry = _registry

    manifest = Manifest()

    with open("VERSION", "r", encoding="utf-8") as f:
        version = f.read()

    output_files = get_variable("schemas.output_schema", "OUTPUT_FILES")
    links = [
        {"rel": "output_file", "href": file.local_path, "title": file.name, "type": file.type}
        for file in output_files
    ]

    links.append(
        {
            "rel": "image",
            "href": f"{registry}/byoa/processor/{manifest.slug}:v{version}",
        }
    )

    data = {
        "id": manifest.slug,
        "summary": manifest.summary,
        "description": manifest.description,
        "categories": ["byoa"],
        "parameters": [
            {"name": "input_data", "description": "Input data", "schema": {"type": "object"}}
        ],
        "returns": {"description": "Output data", "schema": {"type": "object"}},
        "process_graph": {},
        "links": links,
    }

    _save_processor(manifest.slug, data, endpoint)

    docker_client = docker.from_env()

    click.echo("Building image... ", nl=False)
    docker_client.images.build(
        path="./", tag=f"{registry}/byoa/processor/{manifest.slug}:v{version}"
    )
    click.echo("DONE !")

    if click.confirm("Do you need to login to your container registry ?", True):
        _login_to_docker(docker_client, registry)

    try:
        click.echo("Pushing the image... ", nl=False)
        docker_client.images.push(f"{registry}/byoa/processor/{manifest.slug}", tag=f"v{version}")
        click.echo("DONE !")
    except docker.errors.APIError as e:
        click.echo("Reverting...")
        _delete_processor(manifest.slug, endpoint)
        raise ImagePushError(e.response.text) from e
