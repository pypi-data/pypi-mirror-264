import asyncio
import datetime
import json
import os
import signal
import time
import click

from cli.fingerprint import get_fingerprint
from .lib import create_venv, get_and_download_plugin, get_current_user, get_inference_job, get_my_workers, install_requirements, install_torch_requirements, login_with_token, post_register_worker, process_inference_job, run_plugin

@click.group()
def cli():
    pass

@click.command(help="Share my AI CLI - Help")
def help():
    click.echo(f'Help:')
    click.echo(f'  - help: Show this help message')
    return

@click.command(help="Login with a token")
@click.option('--token', required=True, help='Your login token')
def login(token):
    logged_in_user = login_with_token(token)
    if not logged_in_user:
        click.echo('Login failed, please try again.')
        return
    click.echo(f'Logged in successfully as {logged_in_user["name"]} - {logged_in_user["id"]}')
    return

@click.command(help="Get the current user")
def current_user():
    user = get_current_user()
    formatted_json = json.dumps(user, indent=4, sort_keys=True)
    click.echo(f'Current user:\n{formatted_json}')
    return

@click.command(help="Get the current machines fingerprint")
def fingerprint():
    fingerprint_bytes = asyncio.run(get_fingerprint())
    fingerprint_str = fingerprint_bytes.hex()
    click.echo(f'Fingerprint: {fingerprint_str}')
    return

@click.command(help="Register new worker")
@click.option('--plugin_id', required=True, help='The plugin id to work on')
def register_worker(plugin_id):
    worker = post_register_worker(plugin_id)
    formatted_json = json.dumps(worker, indent=4, sort_keys=True)
    click.echo(f'Worker:\n{formatted_json}')
    return

@click.command(help="Get my workers")
def my_workers():
    workers = get_my_workers()
    formatted_json = json.dumps(workers, indent=4, sort_keys=True)
    click.echo(f'Workers:\n{formatted_json}')
    return

@click.command(help="Run worker")
@click.option('--plugin_id', required=True, help='The plugin id to work on')
def run_worker(plugin_id):
    # first, register a worker
    worker = post_register_worker(plugin_id)
    formatted_json = json.dumps(worker, indent=4, sort_keys=True)
    click.echo(f'Worker:\n{formatted_json}')
    # then, download the plugin
    plugin, plugin_path = get_and_download_plugin(plugin_id)
    click.echo(f'Plugin downloaded to {plugin_path}')
    # then, create a venv for the plugin
    venv_path = create_venv(plugin_path)
    click.echo(f'Venv created at {venv_path}')
    # then, install the plugin requirements
    install_torch_requirements(venv_path, plugin['torchRequirements'])
    install_requirements(venv_path, plugin['requirements'])
    click.echo(f'Requirements installed')
    # then, run the plugin
    pid = run_plugin(venv_path, plugin_path, plugin['name'])
    try:
        while True:
            click.echo(f'Checking for jobs - {datetime.datetime.now()}...')
            job = get_inference_job(worker['id'])
            if not job:
                click.echo(f'No job found - {datetime.datetime.now()}...')
                time.sleep(5)
                continue
            click.echo(f'Job found: {job}')
            # process it 
            process_inference_job(job['params']['prompt'], job['params']['image'], job['params'], plugin['params'], job['id'])
            time.sleep(5)
    except KeyboardInterrupt:
        click.echo(f'Stopping plugin - {datetime.datetime.now()}...')
        os.kill(pid, signal.SIGTERM)
    click.echo(f'Plugin stopped - {datetime.datetime.now()}...')
    return

cli.add_command(help)
cli.add_command(login)
cli.add_command(current_user)
cli.add_command(fingerprint)
cli.add_command(register_worker)
cli.add_command(my_workers)
cli.add_command(run_worker)



