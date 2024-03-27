import copy
import traceback
from typing import Any, Optional
from .dta_tracer_service import DtaLog, DtaTracer
from dataclasses import dataclass


## Custom exceptions ##
class DtaCustomError(Exception):
    """Base DTA Logging exceptions"""

    def __init__(self, message: str = "DTA Logging error"):
        self.message = message
        super().__init__(self.message)


class UnsupportedAppError(DtaCustomError):
    """Raised when no an unsupported handler is used to observing"""

    def __init__(self):
        self.message = "Invalid handler: You must use the Goblet app context"
        super().__init__(self.message)


@dataclass
class DtaObserverAppConfig:
    header_trace_id: Optional[str]
    header_session_id: Optional[str]
    input: Optional[bool]
    output: Optional[bool]
    intercept_exceptions: Optional[bool]


@dataclass
class DtaAppContext:
    payload: dict[str, Any]
    request: Any


class DtaObserverApp:
    def register_app(self, app) -> None:
        # Identify which app is managing requests
        self._app = app
        self._load_app_context()

    def _load_app_context(self) -> DtaAppContext:
        if self._app:
            context = DtaAppContext(
                request=None,
                payload={},
            )
            try:
                # Trying Goblet
                from goblet import Goblet

                if isinstance(self._app, Goblet):
                    context.request = self._app.current_request
                    if hasattr(context.request, "method"):
                        # Retrieving Goblet request payload
                        if context.request.method in ["GET", "DELETE"]:
                            context.payload = context.request.args
                        elif context.request.method in ["PUT", "POST"]:
                            context.payload = context.request.get_json()

                    return context
            except Exception:
                pass

            # NOTE: extend for more APP Handlers here if it's needed (Flask, FastAPI, etc)

            raise UnsupportedAppError()

    def _intercepting(
        self,
        main,
        tracer: DtaTracer,
        observer_config: DtaObserverAppConfig,
        *args,
        **kwargs,
    ):
        context = self._load_app_context()

        if observer_config.input:
            self._process_input(
                tracer=tracer, observer_config=observer_config, context=context
            )

        try:
            main_result = main(*args, **kwargs, tracer=tracer)
        except Exception as e:
            if observer_config.intercept_exceptions:
                self._process_exceptions(
                    e, tracer=tracer, observer_config=observer_config, context=context
                )

            raise e

        if observer_config.output:
            self._process_output(
                response=copy.deepcopy(main_result),
                tracer=tracer,
                observer_config=observer_config,
                context=context,
            )

        return main_result

    def _process_input(
        self,
        tracer: DtaTracer,
        observer_config: DtaObserverAppConfig,
        context: DtaAppContext,
    ):
        trace_id = (
            context.request.headers.get(observer_config.header_trace_id)
            if observer_config.header_trace_id
            else None
        )
        session_id = (
            context.request.headers.get(observer_config.header_session_id)
            if observer_config.header_session_id
            else None
        )

        # TRACER input
        tracer.trace(
            id=trace_id,
            session_id=session_id,
            input=context.payload,
        )

    def _process_exceptions(
        self,
        ex: Exception,
        tracer: DtaTracer,
        observer_config: DtaObserverAppConfig,
        context: DtaAppContext,
    ):
        ex_detail = "".join(
            traceback.format_exception(ex, value=ex, tb=ex.__traceback__)
        )
        trace_id = (
            context.request.headers.get(observer_config.header_trace_id)
            if observer_config.header_trace_id
            else None
        )
        session_id = (
            context.request.headers.get(observer_config.header_session_id)
            if observer_config.header_session_id
            else None
        )

        # TRACER event
        tracer.event(
            trace_id=trace_id,
            session_id=session_id,
            name="exception",
            input=context.payload,
            output=ex_detail,
        )

    def _process_output(
        self,
        response,
        tracer: DtaTracer,
        observer_config: DtaObserverAppConfig,
        context: DtaAppContext,
    ):
        trace_id = (
            context.request.headers.get(observer_config.header_trace_id)
            if observer_config.header_trace_id
            else None
        )
        session_id = (
            context.request.headers.get(observer_config.header_session_id)
            if observer_config.header_session_id
            else None
        )

        # TRACER output
        err_code = (
            response.body["code"]
            if "code" in response.body and response.body["code"] >= 300
            else None
        )
        tracer.trace(
            id=trace_id,
            session_id=session_id,
            output=response.body,
            tags=["error", f"error-{err_code}"] if err_code else None,
        )


class DtaObserver(DtaObserverApp):
    _initial_tracer_values: dict[str, Any] = {}

    def __init__(
        self,
        app: any = None,
        **kwargs,
    ) -> None:
        self._initial_tracer_values = {
            key: value for key, value in kwargs.items() if key != "handler"
        }

        if app:
            self.register_app(app)

    def observe(
        self,
        header_trace_id="X-Dta-Thread",
        header_session_id="X-Dta-Session",
        input=True,
        output=True,
        intercept_exceptions=True,
    ):
        observer_config = DtaObserverAppConfig(
            header_trace_id=header_trace_id,
            header_session_id=header_session_id,
            input=input,
            output=output,
            intercept_exceptions=intercept_exceptions,
        )

        def _register_observer(func):
            def wrapper(*args, **kwargs):
                tracer = DtaTracer(**self._initial_tracer_values)

                return self._intercepting(
                    main=func,
                    tracer=tracer,
                    observer_config=observer_config,
                    *args,
                    **kwargs,
                )

            return wrapper

        return _register_observer

    def trace(self, **kwargs):
        merged_args = {
            **self._initial_tracer_values,
            **kwargs,
        }
        return DtaLog.trace(**merged_args)

    def event(self, **kwargs):
        return DtaLog.event(**kwargs)

    def score(
        self,
        *,
        name=str,
        value=float,
        trace_id=str,
        comment=str,
    ):
        return DtaLog.score(
            name=name,
            value=value,
            trace_id=trace_id,
            comment=comment,
        )
