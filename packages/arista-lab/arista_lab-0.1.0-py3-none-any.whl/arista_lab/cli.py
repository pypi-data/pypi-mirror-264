import nornir
import click
import yaml
import sys

from nornir.core.task import Result
from rich.console import Console
from pathlib import Path
from typing import List
from nornir.core.filter import F

from arista_lab import config, ceos, docker

console = Console()


def _init_nornir(ctx: click.Context, param, value) -> nornir.core.Nornir:
    try:
        return nornir.InitNornir(config_file=value)
    except Exception as exc:
        ctx.fail(f"Unable to initialize Nornir with config file '{value}': {str(exc)}")


def _parse_topology(ctx: click.Context, param, value) -> dict:
    try:
        t = yaml.safe_load(value)
        t.update({"_topology_path": value.name})
        return t
    except Exception as exc:
        ctx.fail(
            f"Unable to read Containerlab topology file '{value.name}': {str(exc)}"
        )


@click.group()
@click.option(
    "-n",
    "--nornir",
    "nornir",
    default="nornir.yaml",
    type=click.Path(exists=True),
    callback=_init_nornir,
    help="Nornir configuration in YAML format.",
)
@click.pass_context
def cli(ctx, nornir: nornir.core.Nornir):
    ctx.ensure_object(dict)
    ctx.obj["nornir"] = nornir


# Backup on flash


@cli.command(help="Create or delete device configuration backups to flash")
@click.pass_obj
@click.option(
    "--delete/--no-delete", default=False, help="Delete the backup on the device flash"
)
def backup(obj: dict, delete: bool) -> Result:
    if delete:
        return config.delete_backups(obj["nornir"])
    else:
        return config.create_backups(obj["nornir"])


@cli.command(help="Restore configuration backups from flash")
@click.pass_obj
def restore(obj: dict) -> Result:
    return config.restore_backups(obj["nornir"])


# Backup locally


@cli.command(help="Save configuration to a folder")
@click.pass_obj
@click.option(
    "--folder",
    "folder",
    type=click.Path(writable=True, path_type=Path),
    required=True,
    help="Configuration backup folder",
)
def save(obj: dict, folder: Path) -> Result:
    return config.save(obj["nornir"], folder)


@cli.command(help="Load configuration from a folder")
@click.pass_obj
@click.option(
    "--folder",
    "folder",
    type=click.Path(writable=True, path_type=Path),
    required=True,
    help="Configuration backup folder",
)
def load(obj: dict, folder: Path) -> List[Result]:
    r = []
    r.append(config.create_backups(obj["nornir"]))
    r.append(config.load(obj["nornir"], folder))
    return r


# Containerlab


@cli.command(help="Start containers")
@click.option(
    "-t",
    "--topology",
    "topology",
    default="topology.clab.yml",
    type=click.File("r"),
    callback=_parse_topology,
    help="Containerlab topology file.",
)
@click.pass_obj
def start(obj: dict, topology: dict) -> Result:
    return docker.start(obj["nornir"], topology)


@cli.command(help="Stop containers")
@click.option(
    "-t",
    "--topology",
    "topology",
    default="topology.clab.yml",
    type=click.File("r"),
    callback=_parse_topology,
    help="Containerlab topology file.",
)
@click.pass_obj
def stop(obj: dict, topology: dict) -> Result:
    return docker.stop(obj["nornir"], topology)


@cli.command(
    help="Configure cEOS serial number, system MAC address and copy CloudVision token to flash"
)
@click.option(
    "--token",
    "token",
    type=click.Path(exists=True, readable=True, path_type=Path),
    required=False,
    help="CloudVision onboarding token",
)
@click.pass_obj
@click.option(
    "-t",
    "--topology",
    "topology",
    default="topology.clab.yml",
    type=click.File("r"),
    callback=_parse_topology,
    help="Containerlab topology file.",
)
def init_ceos(obj: dict, topology: dict, token: Path) -> Result:
    return ceos.init_ceos_flash(obj["nornir"], topology, token)


# Configuration


@cli.command(
    help="Onboard to CloudVision (N.B: TerminAttr uses default VRF and CVaaS cv-staging cluster)"
)
@click.pass_obj
def onboard(obj: dict) -> List[Result]:
    r = []
    r.append(config.create_backups(obj["nornir"]))
    r.extend(config.onboard_cloudvision(obj["nornir"]))
    return r


@cli.command(help="Apply configuration templates")
@click.pass_obj
@click.option(
    "--folder",
    "folder",
    type=click.Path(writable=True, path_type=Path),
    required=True,
    help="Configuration template folder",
)
@click.option(
    "--groups/--no-groups",
    default=False,
    help="The template folder contains subfolders with Nornir group names",
)
def apply(obj: dict, folder: Path, groups: bool) -> List[Result]:
    r = []
    r.append(config.create_backups(obj["nornir"]))
    r.append(config.apply_templates(obj["nornir"], folder, groups=groups))
    return r


@cli.command(help="Configure point-to-point interfaces")
@click.pass_obj
@click.option(
    "--links",
    "links",
    type=click.Path(exists=True, readable=True, path_type=Path),
    required=True,
    help="YAML File describing lab links",
)
def interfaces(obj: dict, links: Path) -> List[Result]:
    r = []
    r.append(config.create_backups(obj["nornir"]))
    r.append(config.configure_interfaces(obj["nornir"], links))
    return r


@cli.command(help="Configure peering devices")
@click.pass_obj
@click.option(
    "--group", "group", type=str, required=True, help="Nornir group of peering devices"
)
@click.option(
    "--backbone",
    "backbone",
    type=str,
    required=True,
    help="Nornir group of the backbone",
)
def peering(obj: dict, group: str, backbone: str) -> List[Result]:
    r = []
    r.append(config.create_backups(obj["nornir"].filter(F(groups__contains=group))))
    r.append(config.configure_peering(obj["nornir"], group, backbone))
    return r


def main() -> int:
    try:
        sys.exit(cli(max_content_width=120))
    except Exception:
        console.print_exception(show_locals=True)
        sys.exit(1)
