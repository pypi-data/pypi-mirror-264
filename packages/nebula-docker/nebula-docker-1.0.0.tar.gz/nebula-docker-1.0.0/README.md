# nebula-docker

<p align="center">
    <a href="https://pypi.python.org/pypi/nebula-docker/" alt="PyPI version">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/nebula-docker?color=26272B&labelColor=090422"></a>
    <a href="https://github.com/kozmoai/nebula-docker/" alt="Stars">
        <img src="https://img.shields.io/github/stars/kozmoai/nebula-docker?color=26272B&labelColor=090422" /></a>
    <a href="https://pepy.tech/badge/nebula-docker/" alt="Downloads">
        <img src="https://img.shields.io/pypi/dm/nebula-docker?color=26272B&labelColor=090422" /></a>
    <a href="https://github.com/kozmoai/nebula-docker/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/kozmoai/nebula-docker?color=26272B&labelColor=090422" /></a>
    <br>
    <a href="https://nebula-community.slack.com" alt="Slack">
        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=26272B&labelColor=090422&logo=slack" /></a>

</p>

## Welcome!

Nebula integrations for working with Docker.

Note! The `DockerRegistryCredentials` in `nebula-docker` is a unique block, separate from the `DockerRegistry` in `nebula` core. While `DockerRegistry` implements a few functionality from both `DockerHost` and `DockerRegistryCredentials` for convenience, it does not allow much configuration to interact with a Docker host.

Do not use `DockerRegistry` with this collection. Instead, use `DockerHost` and `DockerRegistryCredentials`.

## Getting Started

### Python setup

Requires an installation of Python 3.8+.

We recommend using a Python virtual environment manager such as pipenv, conda, or virtualenv.

These tasks are designed to work with Nebula 2. For more information about how to use Nebula, please refer to the [Nebula documentation](https://docs.nebula.io/).

### Installation

Install `nebula-docker` with `pip`:

```bash
pip install nebula-docker
```

Then, register to [view the block](https://docs.nebula.io/concepts/blocks/) on Nebula Cloud:

```bash
nebula block register -m nebula_docker
```

Note, to use the `load` method on Blocks, you must already have a block document [saved through code](https://docs.nebula.io/concepts/blocks/#saving-blocks) or saved through the UI.

### Pull image, and create, start, log, stop, and remove Docker container

```python
from nebula import flow, get_run_logger
from nebula_docker.images import pull_docker_image
from nebula_docker.containers import (
    create_docker_container,
    start_docker_container,
    get_docker_container_logs,
    stop_docker_container,
    remove_docker_container,
)


@flow
def docker_flow():
    logger = get_run_logger()
    pull_docker_image("kozmoai/nebula", "latest")
    container = create_docker_container(
        image="kozmoai/nebula", command="echo 'hello world!' && sleep 60"
    )
    start_docker_container(container_id=container.id)
    logs = get_docker_container_logs(container_id=container.id)
    logger.info(logs)
    stop_docker_container(container_id=container.id)
    remove_docker_container(container_id=container.id)
    return container
```

### Use a custom Docker Host to create a Docker container
```python
from nebula import flow
from nebula_docker import DockerHost
from nebula_docker.containers import create_docker_container

@flow
def create_docker_container_flow():
    docker_host = DockerHost(
        base_url="tcp://127.0.0.1:1234",
        max_pool_size=4
    )
    container = create_docker_container(
        docker_host=docker_host,
        image="kozmoai/nebula",
        command="echo 'hello world!'"
    )

create_docker_container_flow()
```

## Resources

If you encounter any bugs while using `nebula-docker`, feel free to open an issue in the [nebula-docker](https://github.com/kozmoai/nebula-docker) repository.

If you have any questions or issues while using `nebula-docker`, you can find help in the [Nebula Slack community](https://nebula.io/slack).

Feel free to ⭐️ or watch [`nebula-docker`](https://github.com/kozmoai/nebula-docker) for updates too!

## Development

If you'd like to install a version of `nebula-docker` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/kozmoai/nebula-docker.git

cd nebula-docker/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
