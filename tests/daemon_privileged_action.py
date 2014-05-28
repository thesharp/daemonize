import logging
from sys import argv

from daemonize import Daemonize


pid = argv[1]
log = argv[2]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler(log, "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def privileged_action():
    logger.info("Privileged action.")


def action():
    logger.info("Action.")


daemon = Daemonize(app="issue-22", pid=pid, action=action,
                   privileged_action=privileged_action, logger=logger, keep_fds=keep_fds)
daemon.start()
