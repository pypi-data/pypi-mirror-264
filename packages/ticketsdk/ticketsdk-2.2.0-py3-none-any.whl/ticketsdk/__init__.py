import platform
import logging

__version__ = "2.2.0"
Version = __version__  # for backward compatibility

try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


UserAgent = "ticketSDK/{} Python/{} {}/{}".format(
    __version__,
    platform.python_version(),
    platform.system(),
    platform.release(),
)

log = logging.getLogger("ticketsdk")

if not log.handlers:
    log.addHandler(NullHandler())


def get_version():
    return __version__


def set_stream_logger(level=logging.DEBUG, format_string=None):
    log.handlers = []

    if not format_string:
        format_string = "%(asctime)s %(name)s [%(levelname)s]:%(message)s"

    log.setLevel(level)
    fh = logging.StreamHandler()
    fh.setLevel(level)
    formatter = logging.Formatter(format_string)
    fh.setFormatter(formatter)
    log.addHandler(fh)


# def seller(*args, **kwargs):
#     raise ImportError(
#         "SDK import must be changed as follows:\n\n- %s\n+ %s\n\n"
#         % (
#             "from ticketsdk import seller",
#             "from ticketsdk.seller import Connection as conn",
#         )
#     )
