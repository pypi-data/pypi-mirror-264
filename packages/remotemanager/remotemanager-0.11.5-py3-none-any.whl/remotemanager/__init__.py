from remotemanager.dataset.dataset import Dataset
from remotemanager.connection.url import URL
from remotemanager.connection.computers.base import BaseComputer
from remotemanager.logging.log import Handler
from remotemanager.storage.remotefunction import RemoteFunction
from remotemanager.decorators.sanzufunction import SanzuFunction

__all__ = [
    "Dataset",
    "URL",
    "RemoteFunction",
    "BaseComputer",
    "SanzuFunction",
]  # noqa: F405
__version__ = "0.11.5"

# attach a global Logger to the manager
Logger = Handler()  # noqa: F405


# ipython magic
def load_ipython_extension(ipython):
    from remotemanager.decorators.magic import RCell

    ipython.register_magics(RCell)
