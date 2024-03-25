#!/usr/bin/env python3
import sys
from inspy_logger.common import PROG_NAME, DEFAULT_LOGGING_LEVEL
from inspy_logger.helpers import find_variable_in_call_stack, check_preemptive_level_set, find_argument_parser

from inspy_logger.helpers import (
    translate_to_logging_level,
    clean_module_name,
    CustomFormatter,
    determine_client_prog_name,
)

from inspy_logger.engine import Logger

__all__ = [
    "clean_module_name",
    "client_prog_name",
    "CustomFormatter",
    "DEFAULT_LOGGING_LEVEL",
    "determine_level",
    "InspyLogger",
    "LOG_DEVICE",
    "Logger",
    "PROG_NAME",
    "translate_to_logging_level",
]

LOG_DEVICE = Logger(PROG_NAME)

MODULE_OBJ = sys.modules[__name__]

client_prog_name = determine_client_prog_name()



def determine_level():
    """
    Determines the level at which to output logs to the console.

    Returns:
        int:
            The level at which to output logs to the console.
    """
    global client_prog_name
    level = DEFAULT_LOGGING_LEVEL

    if _preemptive_set := check_preemptive_level_set():
        level = translate_to_logging_level(_preemptive_set)

    if client_prog_name:
        if arg_parser := find_argument_parser():
            from inspy_logger.helpers.command_line import add_argument
            add_argument(arg_parser, level)
            args = arg_parser.parse_args()

            level = translate_to_logging_level(args.log_level)

    return level


LOG_DEVICE.set_level(determine_level())


if client_prog_name:
    PROG_LOGGER = Logger(client_prog_name, LOG_DEVICE.console_level, LOG_DEVICE.file_level)
    __all__.append('PROG_LOGGER')


InspyLogger = Logger


def _get_loggable():
    from inspy_logger.helpers.base_classes import Loggable
    import bisect
    # Add the `Loggable` class to `__all__` in alphabetical order.
    bisect.insort(__all__, 'Loggable')

    return Loggable


Loggable = _get_loggable()


LOG_DEVICE.replay_and_setup_handlers()
