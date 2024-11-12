import datetime
import os

from fabric import task, Connection

"""
The remote server needs to have docker and nginx installed

Example usages:

docker-compose run --rm server fab deploy
"""

code_dir = "/home/asplab/sens-server/"
host = "asplab@fs-labs.s.upf.edu"
pem_file = "/ssh/id_rsa"


def print_banner(messages):
    print("...........................................")
    if type(messages) == list:
        for message in messages:
            print(message)
    else:
        print(messages)
    print("...........................................")
    print("")


@task
def deploy(ctx, branch="main"):
    messages = ["Deploying...", "Host: %s" % host, "Using pem: %s" % pem_file, "Branch: %s" % branch]
    print_banner(messages)

    with Connection(host=host, connect_kwargs={"key_filename": pem_file}) as c:
        with c.cd(code_dir):
            # Checkout code
            c.run(f"git fetch")
            c.run(f"git checkout -f {branch}")
            c.run("git pull")

            # Copy the local_settings.py file for proiduction deployment
            c.put("deploy/local_settings.py", code_dir + 'sens_server/local_settings.py')

            compose_file = "docker-compose.prod.yml"
            server_service_name = "web"

            # Build docker image
            c.run(f"docker compose -f {compose_file} build")

            # Migrate
            c.run(f"docker compose -f {compose_file} run --rm {server_service_name} python manage.py migrate")
            

            # Restart
            c.run(f"docker compose -f {compose_file} stop")
            c.run(f"docker compose -f {compose_file} up -d")


@task
def stop(ctx):
    messages = ["Stopping...", "Host: %s" % host, "Using pem: %s" % pem_file]
    print_banner(messages)

    with Connection(host=host, connect_kwargs={"key_filename": pem_file}) as c:
        with c.cd(code_dir):
            # Stop
            compose_file = "docker-compose.prod.yml" 
            c.run(f"docker compose -f {compose_file} stop")


@task
def restart(ctx):
    messages = ["Stopping...", "Host: %s" % host, "Using pem: %s" % pem_file]
    print_banner(messages)

    with Connection(host=host, connect_kwargs={"key_filename": pem_file}) as c:
        with c.cd(code_dir):
            # Restart
            compose_file = "docker-compose.prod.yml"
            c.run(f"docker compose -f {compose_file} stop")
            c.run(f"docker compose -f {compose_file} up -d")
