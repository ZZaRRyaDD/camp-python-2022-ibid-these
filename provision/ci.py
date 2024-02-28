##############################################################################
# Commands used in ci for code validation
##############################################################################
from invoke import task

from . import common, django, docker, linters, open_api, project, tests


@task
def prepare(context):
    """Prepare ci environment for check."""
    common.success("Preparing CI")
    docker.up(context)
    set_up_hosts(context)
    project.copylocal(context=context)
    project.install_requirements(context)


def set_up_hosts(context):
    """Add services to hosts."""
    common.success("Setting up hosts")
    context.run("echo \"127.0.0.1 postgres\" | sudo tee -a /etc/hosts")
    context.run("echo \"127.0.0.1 redis\" | sudo tee -a /etc/hosts")


@task
def start(context, check):
    """Perform ci check."""
    common.success("Perform CI check")
    checks_map = dict(
        style=linters.all,
        migrations=django.check_new_migrations,
        open_api=open_api.validate_swagger,
        tests=tests.run_ci,
    )
    checks_map[check](context)
