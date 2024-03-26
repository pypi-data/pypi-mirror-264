import sys

import click

from tecton._internals import metadata_service
from tecton.cli import printer
from tecton.cli.command import TectonCommand
from tecton.cli.command import TectonGroup
from tecton_core.errors import TectonNotFoundError
from tecton_proto.secrets.secrets_service_pb2 import CreateSecretScopeRequest
from tecton_proto.secrets.secrets_service_pb2 import ListSecretScopesRequest
from tecton_proto.secrets.secrets_service_pb2 import ListSecretsRequest


@click.command("secrets", cls=TectonGroup)
def secrets():
    """Manage Tecton secrets and secret scopes."""


@secrets.command("create-scope", requires_auth=True, cls=TectonCommand)
@click.option("-s", "--scope", default=None, required=True, help="Secret scope name")
def create_scope(scope):
    """Create a new secret scope"""
    request = CreateSecretScopeRequest(scope=scope)
    response = metadata_service.instance().CreateSecretScope(request)


@secrets.command("list-scopes", requires_auth=True, cls=TectonCommand)
def list_scopes():
    """List secret scopes"""
    request = ListSecretScopesRequest()
    response = metadata_service.instance().ListSecretScopes(request)

    if response.scopes == []:
        printer.safe_print("No secret scopes found", file=sys.stderr)
    else:
        for scope in response.scopes:
            printer.safe_print(scope.name)


@secrets.command("list", requires_auth=True, cls=TectonCommand)
@click.option("-s", "--scope", default=None, required=True, help="Scope name")
def list_secrets(scope):
    """List secrets in a scope"""
    request = ListSecretsRequest(scope=scope)

    try:
        response = metadata_service.instance().ListSecrets(request)
    except TectonNotFoundError as e:
        printer.safe_print("Error: Secret scope not found", file=sys.stderr)
        return

    if response.keys == []:
        printer.safe_print("No secrets found")
    else:
        for key in response.keys:
            printer.safe_print(key.name)
