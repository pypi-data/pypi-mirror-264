import click
import subprocess
import os
from jinja2 import Environment, FileSystemLoader
from importlib import resources
import shlex
import tempfile
class CommandError(click.ClickException):
    def __init__(self, message, exit_code=1):
        super().__init__(message)
        self.exit_code = exit_code

def execute_command(command,end_message=None):
    command = shlex.split(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        for line in process.stdout:
            click.echo(line.strip())
            if end_message and end_message in line:
                click.echo('End message detected, terminating now.')
                if process.poll() is None:
                    click.echo("Process poll is None, attempting to terminate.")
                    process.terminate()
                    process.wait(timeout=10)
                return 
    except subprocess.TimeoutExpired:
        click.echo("Process did not terminate in time, force killing.")
        process.kill() 
                  
    process.wait()
    
    if process.returncode != 0:
        error_output = "\n look for error message above"
        raise CommandError(f"Command failed with exit code {process.returncode}: {error_output}")


def get_template_path(filename):
    with resources.path('oetcloudmodule.templates', filename) as file_path:
        return file_path
    
def get_templates_dir():
    try:
        templates_path = resources.files('oetcloudmodule').joinpath('templates')
        return templates_path
    except Exception as e:
        print(f"Failed to locate templates directory: {e}")

def render_yaml_from_template(template_file_name='k8-jinja.yaml',variables=None):
    """
    Renders a YAML file from a Jinja2 template.

    :param template_file_name: The name of the template file.
    :param variables: A dictionary of variables to replace in the template.
    :return: The rendered YAML content as a string.
    """
    file_loader = FileSystemLoader(get_templates_dir())
    env = Environment(loader=file_loader)
    template = env.get_template(template_file_name)
    rendered_yaml = template.render(variables)

    return rendered_yaml


def apply_k8s_yaml(yaml_content):
    with tempfile.NamedTemporaryFile(delete=False, mode='w+') as tmpfile:
        tmpfile_name = tmpfile.name
        tmpfile.write(yaml_content)
        tmpfile.flush()
        command = f"kubectl apply -f {tmpfile_name}"
        try:
            execute_command(command)
        finally:
            os.remove(tmpfile_name)


@click.command()
@click.option('--bucket_name', required=True, prompt='Please enter the bucket name',help='The name of the GCP bucket used for storing data.')
@click.option('--source', required=True, prompt='Please enter the input directory path',help='The local directory path whose contents will be copied. This directory will be overwritten.')
@click.option('--endpoint', required=True, prompt='Please enter the output directory path',help='The destination directory path where the processed results will be written.')
@click.option('--dockerimage', required=True, prompt='Please enter the Docker image name',help='The name of the Docker image to be used for processing')
def exe(bucket_name, source, endpoint, dockerimage):
    try:
        click.echo(f"Creating Google Cloud Storage bucket named {bucket_name} ...")
        execute_command(f"gcloud storage buckets create gs://{bucket_name} --uniform-bucket-level-access")
        
        click.echo("Copying files to the bucket...")
        current_dir = os.getcwd()
        source_path = os.path.join(current_dir, source)
        execute_command(f"gcloud storage cp --recursive {source_path} gs://{bucket_name}/")
        click.echo("Files copied successfully.")
        
        execute_command("kubectl get pods")
        
        template_file_name='k8-jinja.yaml'
        variables = {'bucket_name': bucket_name, 
                    'input_dir':source,
                    'output_dir': endpoint,
                    'docker_image': dockerimage
                    }
        rendered_yaml = render_yaml_from_template(template_file_name, variables)
        apply_k8s_yaml(rendered_yaml)

        execute_command("ktail cal-img --since-start" ,end_message='Container left (terminated)')
        
        click.echo(f"process finished sucessfully veiw output folder in bucket {bucket_name}")
        
        if click.confirm('Do you want to download results from the bucket ?'):
            execute_command(f"gcloud storage cp --recursive gs://{bucket_name}/{endpoint}/ {current_dir}")
        
    except CommandError as e:
        e.show()
        ctx = click.get_current_context()
        ctx.exit(e.exit_code)


