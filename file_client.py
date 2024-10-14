import click
import requests
import sys

# Default configuration
DEFAULT_BASE_URL = "http://localhost/"
REST_BACKEND = "rest"

# Function to retrieve file metadata
def get_file_metadata(base_url, uuid):
    url = f"{base_url}file/{uuid}/stat/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        click.echo(f"File Name: {data['name']}")
        click.echo(f"Creation Date: {data['create_datetime']}")
        click.echo(f"Size: {data['size']} bytes")
        click.echo(f"MIME Type: {data['mimetype']}")
    elif response.status_code == 404:
        click.echo("File not found (404).")
    else:
        click.echo(f"Error retrieving metadata: {response.status_code}")

# Function to retrieve file content
def get_file_content(base_url, uuid, output):
    url = f"{base_url}file/{uuid}/read/"
    response = requests.get(url)
    if response.status_code == 200:
        if output == "-":
            sys.stdout.buffer.write(response.content)
        else:
            with open(output, 'wb') as f:
                f.write(response.content)
            click.echo(f"File saved to {output}")
    elif response.status_code == 404:
        click.echo("File not found (404).")
    else:
        click.echo(f"Error retrieving file content: {response.status_code}")

# Main CLI group
@click.group()
@click.option('--backend', default=REST_BACKEND, help="Backend to use, choices are grpc and rest (default: rest).")
@click.option('--base-url', default=DEFAULT_BASE_URL, help="Base URL for the REST server (default: http://localhost/).")
@click.option('--output', default='-', help="File to save output, default is stdout.")
@click.pass_context
def file_client(ctx, backend, base_url, output):
    """CLI to retrieve file metadata and content from a REST API."""
    ctx.ensure_object(dict)
    ctx.obj['backend'] = backend
    ctx.obj['base_url'] = base_url
    ctx.obj['output'] = output

    if backend != REST_BACKEND:
        click.echo("Only REST backend is supported.")
        ctx.exit()

# Subcommand for 'stat'
@file_client.command()
@click.argument('uuid')
@click.pass_context
def stat(ctx, uuid):
    """Prints the file metadata in a human-readable manner."""
    base_url = ctx.obj['base_url']
    get_file_metadata(base_url, uuid)

# Subcommand for 'read'
@file_client.command()
@click.argument('uuid')
@click.pass_context
def read(ctx, uuid):
    """Outputs the file content."""
    base_url = ctx.obj['base_url']
    output = ctx.obj['output']
    get_file_content(base_url, uuid, output)

if __name__ == '__main__':
    file_client()
