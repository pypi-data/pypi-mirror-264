from . import _version
from .host import DockerHost  # noqa
from .credentials import DockerRegistryCredentials  # noqa
from .worker import DockerWorker  # noqa

from nebula._internal.compatibility.deprecated import (
    register_renamed_module,
)

register_renamed_module(
    "nebula_docker.projects", "nebula_docker.deployments", start_date="Jun 2023"
)


__version__ = _version.get_versions()["version"]
