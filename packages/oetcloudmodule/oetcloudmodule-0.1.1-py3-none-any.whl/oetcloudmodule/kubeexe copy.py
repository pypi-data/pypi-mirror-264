import click
import subprocess
import os
from jinja2 import Environment, FileSystemLoader


class CommandError(click.ClickException):
    def __init__(self, message):
        super().__init__(message)

def execute_command(command,stream=False):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            click.echo(line, end='')
        process.wait()
        if process.returncode != 0:
            error_output = process.stderr.read()
            raise CommandError(f"Command failed: {error_output.strip()}")
        
    except subprocess.CalledProcessError as e:
        raise CommandError(f"Command failed: {e.stderr.decode().strip()}")


@click.command()
@click.argument('bucket_name')
@click.argument('source')
def exe(bucket_name, source):
    try:
        click.echo("current dir ")
        click.echo(f"Creating Google Cloud Storage bucket named {bucket_name} ...")
        execute_command(["gcloud", "storage", "buckets", "create", f"gs://{bucket_name}","--uniform-bucket-level-access"])
        click.echo("Copying files to the bucket...")
        current_dir = os.getcwd()
        source_path = os.path.join(current_dir, source)
        execute_command(["gcloud","storage", "cp","--recursive",f"{source_path}", f"gs://{bucket_name}/"])
        click.echo("Files copied successfully.")
        
        
        
        execute_command(["kubectl","get","pods"])
        
    except CommandError as e:
        e.show()
        ctx = click.get_current_context()
        ctx.exit(e.exit_code)


# ///////
def render_yaml_from_template(directory, template_file_name, variables):
    """
    Renders a YAML file from a Jinja2 template.

    :param directory: The directory where the template file is located.
    :param template_file_name: The name of the template file.
    :param variables: A dictionary of variables to replace in the template.
    :return: The rendered YAML content as a string.
    """
    # Set up the Jinja2 environment with the directory containing the template
    file_loader = FileSystemLoader(directory)
    env = Environment(loader=file_loader)

    # Load the template file
    template = env.get_template(template_file_name)

    # Render the template with the provided variables
    rendered_yaml = template.render(variables)

    return rendered_yaml



