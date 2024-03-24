from functools import partial
from functools import wraps
from itertools import cycle
from itertools import repeat
import logging
import time
import typing as t


logger = logging.getLogger(__package__)


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
    error_callback: t.Optional[t.Callable[[int, Exception, DelayT, RetriesT], None]] = None,
    sleep: t.Callable[[float], None] = time.sleep,
    delays: SingleOrIterable[DelayT] = 0,
    first_delay: t.Optional[DelayT] = None,
    chain_exception: bool = False,
    logger: t.Union[logging.Logger, t.Callable] = logger,
):
    if not isinstance(delays, t.Iterable):
        delays = repeat(delays)
    delays = cycle(delays)
    if first_delay is None:
        first_delay = next(delays)
    if not isinstance(logger, logging.Logger):
        logger = DummyLogger(logger)

    def _default_error_callback(
        index: int,
        exception: Exception,
        delay: DelayT,
        retries: RetriesT,
    ):
        log_prefix = f'tried {index} of {retries} -> {exception!r}'
        is_last = index == retries
        if not is_last:
            logger.info(f'{log_prefix} -> sleep {delay} seconds')
        else:
            logger.warning(log_prefix)

    error_callback = error_callback or _default_error_callback

    def callback(index: int, exception: Exception, delay: DelayT, retries: RetriesT):
        error_callback(index, exception, delay, retries)
        if index != retries:
            sleep(delay)

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            function_retrying = partial(f, *args, **kwargs)
            try:
                # execute once
                return function_retrying()
            except exceptions as e:
                # start retrying
                i = 0
                callback(i, e, first_delay, retries)
                # retrying
                while True:
                    try:
                        return function_retrying()
                    except exceptions as e:
                        # check first
                        if i == retries:
                            if chain_exception:
                                raise
                            raise e from None
                        # then ++
                        i += 1
                        delay = next(delays)
                        callback(i, e, delay, retries)

        return wrapper

    return decorator


if __name__ == '__main__':
    from random import random

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-7s %(message)s (%(name)s)')

    class Error(Exception):
        pass

    @retry(
        retries=3,
        exceptions=(ValueError, ZeroDivisionError, Error),
        # error_callback=lambda i, e, d, r: print(i),
        # error_callback=lambda i, e, d, r: logger.error(i),
        sleep=lambda x: print('.' * int(x * 10)),
        # delays=cycle([1 / 3, 2 / 3]),
        delays=2.1,
        first_delay=1.5,
        # chain_exception=True,
        # logger=logger,
        # logger=print,
    )
    def f():
        1 / 0  # type: ignore[reportUnusedExpression]

        if random() < 0.2:
            return

        if random() < 0.8:
            # return
            1 / 0  # type: ignore[reportUnusedExpression]
        if random() < 0.8:
            raise Error('??')

    f()
