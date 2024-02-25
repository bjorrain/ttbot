import telebot
import yaml
import logging
from rich.logging import RichHandler
from rich.traceback import install
from rich import print
import os

install()
logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)



