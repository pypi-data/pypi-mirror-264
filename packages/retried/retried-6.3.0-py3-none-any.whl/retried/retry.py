from functools import partial
from functools import wraps
from itertools import cycle
from itertools import repeat
import logging
import time
import typing as t


try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec  # type: ignore[assignment]


logger = logging.getLogger(__package__)


P = ParamSpec('P')  # https://docs.python.org/zh-tw/3/library/typing.html#typing.ParamSpec
T = t.TypeVar('T')
SingleOrTuple = t.Union[T, tuple[T, ...]]
SingleOrIterable = t.Union[T, t.Iterable[T]]

DelayT = float
RetriesT = t.Optional[int]


class DummyLogger(logging.Logger):
    def __init__(self, f: t.Callable):
        self._f = f
        super().__init__(__package__)

    def _log(self, level, msg, *args, **kwargs):
        self._f(msg)


def retry(
    retries: RetriesT = None,
    *,
    exceptions: SingleOrTuple[t.Type[Exception]] = Exception,
    error_callback: t.Optional[
        t.Callable[[int, Exception, DelayT, RetriesT, t.Callable[P, T]], None]
    ] = None,
    sleep: t.Callable[[float], None] = time.sleep,
    delays: SingleOrIterable[DelayT] = 0,
    first_delay: t.Optional[DelayT] = None,
    chain_exception: bool = False,
    logger: t.Union[logging.Logger, t.Callable[[t.Any], None]] = logger,
):
    if not isinstance(delays, t.Iterable):
        delays = repeat(delays)
    delays = cycle(delays)
    if first_delay is None:
        first_delay = next(delays)
    if not isinstance(logger, logging.Logger):
        logger = DummyLogger(logger)

    def _default_error_callback(i: int, e: Exception, d: DelayT, r: RetriesT, f: t.Callable[P, T]):
        log_prefix = f'tried {i} of {r}. {f.__code__.co_filename}:{f.__code__.co_firstlineno} {e!r}'
        is_last = i == r
        if not is_last:
            logger.info(f'{log_prefix} -> sleep {d} seconds')
        else:
            logger.warning(log_prefix)

    error_callback = error_callback or _default_error_callback

    def callback(i: int, e: Exception, d: DelayT, r: RetriesT, f: t.Callable[P, T]):
        error_callback(i, e, d, r, f)
        if i != r:
            sleep(d)

    def decorator(f: t.Callable[P, T]) -> t.Callable[P, T]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            function_retrying = partial(f, *args, **kwargs)
            try:
                # execute once
                result = function_retrying()
            except exceptions as e:
                # start retrying
                i = 0
                callback(i, e, first_delay, retries, f)
                # retrying
                while True:
                    try:
                        result = function_retrying()
                    except exceptions as e:
                        # check if should retry
                        if i == retries:
                            if chain_exception:
                                raise
                            raise e from None
                        # then ++
                        i += 1
                        delay = next(delays)
                        callback(i, e, delay, retries, f)
                    else:
                        return result
            else:
                return result

        return wrapper

    return decorator
