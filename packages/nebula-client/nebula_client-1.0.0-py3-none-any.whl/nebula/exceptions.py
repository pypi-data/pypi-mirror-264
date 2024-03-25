"""
Nebula-specific exceptions.
"""
import inspect
import traceback
from types import ModuleType, TracebackType
from typing import Callable, Dict, Iterable, List, Optional, Type

from nebula._internal.pydantic import HAS_PYDANTIC_V2

if HAS_PYDANTIC_V2:
    import pydantic.v1 as pydantic
else:
    import pydantic

from httpx._exceptions import HTTPStatusError
from rich.traceback import Traceback
from typing_extensions import Self

import nebula


def _trim_traceback(
    tb: TracebackType, remove_modules: Iterable[ModuleType]
) -> Optional[TracebackType]:
    """
    Utility to remove frames from specific modules from a traceback.

    Only frames from the front of the traceback are removed. Once a traceback frame
    is reached that does not originate from `remove_modules`, it is returned.

    Args:
        tb: The traceback to trim.
        remove_modules: An iterable of module objects to remove.

    Returns:
        A traceback, or `None` if all traceback frames originate from an excluded module

    """
    strip_paths = [module.__file__ for module in remove_modules]

    while tb and any(
        module_path in str(tb.tb_frame.f_globals.get("__file__", ""))
        for module_path in strip_paths
    ):
        tb = tb.tb_next

    return tb


def exception_traceback(exc: Exception) -> str:
    """
    Convert an exception to a printable string with a traceback
    """
    tb = traceback.TracebackException.from_exception(exc)
    return "".join(list(tb.format()))


class NebulaException(Exception):
    """
    Base exception type for Nebula errors.
    """


class CrashedRun(NebulaException):
    """
    Raised when the result from a crashed run is retrieved.

    This occurs when a string is attached to the state instead of an exception or if
    the state's data is null.
    """


class FailedRun(NebulaException):
    """
    Raised when the result from a failed run is retrieved and an exception is not
    attached.

    This occurs when a string is attached to the state instead of an exception or if
    the state's data is null.
    """


class CancelledRun(NebulaException):
    """
    Raised when the result from a cancelled run is retrieved and an exception
    is not attached.

    This occurs when a string is attached to the state instead of an exception
    or if the state's data is null.
    """


class PausedRun(NebulaException):
    """
    Raised when the result from a paused run is retrieved.
    """

    def __init__(self, *args, state=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state


class UnfinishedRun(NebulaException):
    """
    Raised when the result from a run that is not finished is retrieved.

    For example, if a run is in a SCHEDULED, PENDING, CANCELLING, or RUNNING state.
    """


class MissingFlowError(NebulaException):
    """
    Raised when a given flow name is not found in the expected script.
    """


class UnspecifiedFlowError(NebulaException):
    """
    Raised when multiple flows are found in the expected script and no name is given.
    """


class MissingResult(NebulaException):
    """
    Raised when a result is missing from a state; often when result persistence is
    disabled and the state is retrieved from the API.
    """


class ScriptError(NebulaException):
    """
    Raised when a script errors during evaluation while attempting to load data
    """

    def __init__(
        self,
        user_exc: Exception,
        path: str,
    ) -> None:
        message = f"Script at {str(path)!r} encountered an exception: {user_exc!r}"
        super().__init__(message)
        self.user_exc = user_exc

        # Strip script run information from the traceback
        self.user_exc.__traceback__ = _trim_traceback(
            self.user_exc.__traceback__,
            remove_modules=[nebula.utilities.importtools],
        )


class FlowScriptError(NebulaException):
    """
    Raised when a script errors during evaluation while attempting to load a flow.
    """

    def __init__(
        self,
        user_exc: Exception,
        script_path: str,
    ) -> None:
        message = f"Flow script at {script_path!r} encountered an exception"
        super().__init__(message)

        self.user_exc = user_exc

    def rich_user_traceback(self, **kwargs):
        trace = Traceback.extract(
            type(self.user_exc),
            self.user_exc,
            self.user_exc.__traceback__.tb_next.tb_next.tb_next.tb_next,
        )
        return Traceback(trace, **kwargs)


class ParameterTypeError(NebulaException):
    """
    Raised when a parameter does not pass Pydantic type validation.
    """

    def __init__(self, msg: str):
        super().__init__(msg)

    @classmethod
    def from_validation_error(cls, exc: pydantic.ValidationError) -> Self:
        bad_params = [f'{err["loc"][0]}: {err["msg"]}' for err in exc.errors()]
        msg = "Flow run received invalid parameters:\n - " + "\n - ".join(bad_params)
        return cls(msg)


class ParameterBindError(TypeError, NebulaException):
    """
    Raised when args and kwargs cannot be converted to parameters.
    """

    def __init__(self, msg: str):
        super().__init__(msg)

    @classmethod
    def from_bind_failure(
        cls, fn: Callable, exc: TypeError, call_args: List, call_kwargs: Dict
    ) -> Self:
        fn_signature = str(inspect.signature(fn)).strip("()")

        base = f"Error binding parameters for function '{fn.__name__}': {exc}"
        signature = f"Function '{fn.__name__}' has signature '{fn_signature}'"
        received = f"received args: {call_args} and kwargs: {list(call_kwargs.keys())}"
        msg = f"{base}.\n{signature} but {received}."
        return cls(msg)


class SignatureMismatchError(NebulaException, TypeError):
    """Raised when parameters passed to a function do not match its signature."""

    def __init__(self, msg: str):
        super().__init__(msg)

    @classmethod
    def from_bad_params(cls, expected_params: List[str], provided_params: List[str]):
        msg = (
            f"Function expects parameters {expected_params} but was provided with"
            f" parameters {provided_params}"
        )
        return cls(msg)


class ObjectNotFound(NebulaException):
    """
    Raised when the client receives a 404 (not found) from the API.
    """

    def __init__(self, http_exc: Exception, *args, **kwargs):
        self.http_exc = http_exc
        super().__init__(*args, **kwargs)


class ObjectAlreadyExists(NebulaException):
    """
    Raised when the client receives a 409 (conflict) from the API.
    """

    def __init__(self, http_exc: Exception, *args, **kwargs):
        self.http_exc = http_exc
        super().__init__(*args, **kwargs)


class UpstreamTaskError(NebulaException):
    """
    Raised when a task relies on the result of another task but that task is not
    'COMPLETE'
    """


class MissingContextError(NebulaException, RuntimeError):
    """
    Raised when a method is called that requires a task or flow run context to be
    active but one cannot be found.
    """


class MissingProfileError(NebulaException, ValueError):
    """
    Raised when a profile name does not exist.
    """


class ReservedArgumentError(NebulaException, TypeError):
    """
    Raised when a function used with Nebula has an argument with a name that is
    reserved for a Nebula feature
    """


class InvalidNameError(NebulaException, ValueError):
    """
    Raised when a name contains characters that are not permitted.
    """


class NebulaSignal(BaseException):
    """
    Base type for signal-like exceptions that should never be caught by users.
    """


class Abort(NebulaSignal):
    """
    Raised when the API sends an 'ABORT' instruction during state proposal.

    Indicates that the run should exit immediately.
    """


class Pause(NebulaSignal):
    """
    Raised when a flow run is PAUSED and needs to exit for resubmission.
    """

    def __init__(self, *args, state=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state


class ExternalSignal(BaseException):
    """
    Base type for external signal-like exceptions that should never be caught by users.
    """


class TerminationSignal(ExternalSignal):
    """
    Raised when a flow run receives a termination signal.
    """

    def __init__(self, signal: int):
        self.signal = signal


class NebulaHTTPStatusError(HTTPStatusError):
    """
    Raised when client receives a `Response` that contains an HTTPStatusError.

    Used to include API error details in the error messages that the client provides users.
    """

    @classmethod
    def from_httpx_error(cls: Type[Self], httpx_error: HTTPStatusError) -> Self:
        """
        Generate a `NebulaHTTPStatusError` from an `httpx.HTTPStatusError`.
        """
        try:
            details = httpx_error.response.json()
        except Exception:
            details = None

        error_message, *more_info = str(httpx_error).split("\n")

        if details:
            message_components = [error_message, f"Response: {details}", *more_info]
        else:
            message_components = [error_message, *more_info]

        new_message = "\n".join(message_components)

        return cls(
            new_message, request=httpx_error.request, response=httpx_error.response
        )


class MappingLengthMismatch(NebulaException):
    """
    Raised when attempting to call Task.map with arguments of different lengths.
    """


class MappingMissingIterable(NebulaException):
    """
    Raised when attempting to call Task.map with all static arguments
    """


class BlockMissingCapabilities(NebulaException):
    """
    Raised when a block does not have required capabilities for a given operation.
    """


class ProtectedBlockError(NebulaException):
    """
    Raised when an operation is prevented due to block protection.
    """


class InvalidRepositoryURLError(NebulaException):
    """Raised when an incorrect URL is provided to a GitHub filesystem block."""


class InfrastructureError(NebulaException):
    """
    A base class for exceptions related to infrastructure blocks
    """


class InfrastructureNotFound(NebulaException):
    """
    Raised when infrastructure is missing, likely because it has exited or been
    deleted.
    """


class InfrastructureNotAvailable(NebulaException):
    """
    Raised when infrastructure is not accessible from the current machine. For example,
    if a process was spawned on another machine it cannot be managed.
    """


class NotPausedError(NebulaException):
    """Raised when attempting to unpause a run that isn't paused."""


class FlowPauseTimeout(NebulaException):
    """Raised when a flow pause times out"""


class FlowRunWaitTimeout(NebulaException):
    """Raised when a flow run takes longer than a given timeout"""
