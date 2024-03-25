# isort: skip_file

# Setup version and path constants

from . import _version
import importlib
import pathlib
import warnings
import sys

__version_info__ = _version.get_versions()
__version__ = __version_info__["version"]

# The absolute path to this module
__module_path__ = pathlib.Path(__file__).parent
# The absolute path to the root of the repository, only valid for use during development
__development_base_path__ = __module_path__.parents[1]

# The absolute path to the built UI within the Python module, used by
# `nebula server start` to serve a dynamic build of the UI
__ui_static_subpath__ = __module_path__ / "server" / "ui_build"

# The absolute path to the built UI within the Python module
__ui_static_path__ = __module_path__ / "server" / "ui"

del _version, pathlib

if sys.version_info < (3, 8):
    warnings.warn(
        (
            "Nebula dropped support for Python 3.7 when it reached end-of-life"
            " . To use new versions of Nebula, you will need"
            " to upgrade to Python 3.8+. See https://devguide.python.org/versions/ for "
            " more details."
        ),
        FutureWarning,
        stacklevel=2,
    )


# Import user-facing API
from nebula.runner import Runner, serve
from nebula.deployments import deploy
from nebula.states import State
from nebula.logging import get_run_logger
from nebula.flows import flow, Flow
from nebula.tasks import task, Task
from nebula.context import tags
from nebula.manifests import Manifest
from nebula.utilities.annotations import unmapped, allow_failure
from nebula.results import BaseResult
from nebula.engine import pause_flow_run, resume_flow_run, suspend_flow_run
from nebula.client.orchestration import get_client, NebulaClient
from nebula.client.cloud import get_cloud_client, CloudClient
import nebula.variables
import nebula.runtime

# Import modules that register types
import nebula.serializers
import nebula.deprecated.data_documents
import nebula.deprecated.packaging
import nebula.blocks.kubernetes
import nebula.blocks.notifications
import nebula.blocks.system
import nebula.infrastructure.process
import nebula.infrastructure.kubernetes
import nebula.infrastructure.container

# Initialize the process-wide profile and registry at import time
import nebula.context

nebula.context.initialize_object_registry()

# Perform any forward-ref updates needed for Pydantic models
import nebula.client.schemas

nebula.context.FlowRunContext.update_forward_refs(Flow=Flow)
nebula.context.TaskRunContext.update_forward_refs(Task=Task)
nebula.client.schemas.State.update_forward_refs(
    BaseResult=BaseResult, DataDocument=nebula.deprecated.data_documents.DataDocument
)
nebula.client.schemas.StateCreate.update_forward_refs(
    BaseResult=BaseResult, DataDocument=nebula.deprecated.data_documents.DataDocument
)


nebula.plugins.load_extra_entrypoints()

# Configure logging
import nebula.logging.configuration

nebula.logging.configuration.setup_logging()
nebula.logging.get_logger("profiles").debug(
    f"Using profile {nebula.context.get_settings_context().profile.name!r}"
)

# Ensure moved names are accessible at old locations
import nebula.client

nebula.client.get_client = get_client
nebula.client.NebulaClient = NebulaClient


from nebula._internal.compatibility.deprecated import (
    inject_renamed_module_alias_finder,
    register_renamed_module,
)

register_renamed_module(
    "nebula.client.orchestration",
    "nebula.client.orchestration",
    start_date="Feb 2023",
)
register_renamed_module(
    "nebula.docker",
    "nebula.utilities.dockerutils",
    start_date="Mar 2023",
)
register_renamed_module(
    "nebula.infrastructure.docker",
    "nebula.infrastructure.container",
    start_date="Mar 2023",
)
register_renamed_module("nebula.projects", "nebula.deployments", start_date="Jun 2023")
register_renamed_module(
    "nebula.packaging", "nebula.deprecated.packaging", start_date="Mar 2024"
)
inject_renamed_module_alias_finder()


# Attempt to warn users who are importing Nebula 1.x attributes that they may
# have accidentally installed Nebula 2.x

NEBULA_1_ATTRIBUTES = [
    "nebula.Client",
    "nebula.Parameter",
    "nebula.api",
    "nebula.apply_map",
    "nebula.case",
    "nebula.config",
    "nebula.context",
    "nebula.flatten",
    "nebula.mapped",
    "nebula.models",
    "nebula.resource_manager",
]


class Nebula1ImportInterceptor(importlib.abc.Loader):
    def find_spec(self, fullname, path, target=None):
        if fullname in NEBULA_1_ATTRIBUTES:
            warnings.warn(
                f"Attempted import of {fullname!r}, which is part of Nebula 1.x, while"
                f" Nebula {__version__} is installed. If you're upgrading you'll need"
                " to update your code, see the Nebula 2.x migration guide:"
                " `https://orion-docs.nebula.io/migration_guide/`. Otherwise ensure"
                " that your code is pinned to the expected version."
            )


if not hasattr(sys, "frozen"):
    sys.meta_path.insert(0, Nebula1ImportInterceptor())


# Declare API for type-checkers
__all__ = [
    "allow_failure",
    "flow",
    "Flow",
    "get_client",
    "get_run_logger",
    "Manifest",
    "State",
    "tags",
    "task",
    "Task",
    "unmapped",
    "Runner",
    "serve",
    "deploy",
    "pause_flow_run",
    "resume_flow_run",
    "suspend_flow_run",
]
