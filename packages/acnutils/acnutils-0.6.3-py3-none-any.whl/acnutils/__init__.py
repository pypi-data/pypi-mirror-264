#!/usr/bin/env python3
# coding: utf-8
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2021 AntiCompositeNumber

import pywikibot  # type: ignore
import logging
import logging.handlers
import logging.config
import time
import os
import json
import importlib.util

from typing import Callable, Any, Dict

__version__ = "0.6.3"

logger = logging.getLogger(__name__)

if importlib.util.find_spec("toolforge"):
    from acnutils.db import get_replag  # noqa: F401


class RunpageError(Exception):
    """The on-wiki runpage is False or missing."""

    pass


class PageNotSaved(Exception):
    """An error occurred while saving the page."""

    def __init__(self, page: pywikibot.Page, message: str = ""):
        self.page = page
        self.message = message


def logger_config(
    module: str,
    level: str = "INFO",
    filename: str = "",
    tool: str = "",
    thread: bool = False,
) -> Dict:
    """Create a logging configuration dict for logging.config.dictConfig.

    This function makes some assumptions about the environment, and is partially
    designed for use on Toolforge.

    :param module: Name of the module being logged. Should be the same as the module
        name used in ``logging.getLogger()``.
    :param level: String form of the log level. ``VERBOSE`` is a special value
        that will set the root logger to ``INFO`` and the module logger to ``DEBUG``.
    :param filename:
        - An absolute path to the log file (starts with ``/``)
        - A relative path; on Toolforge this is relative to ``$HOME/logs``, elsewhere
            it is relative to the current working directory
        - ``stderr``: A special value, streams to stderr instead of writing to a file.
    :param tool: Name of the Toolforge tool, used for SMTP logging.
    :param thread: Include thread name in log entries.

    :Environment variables:
    - `LOG_LEVEL`: Overrides the log level set with ``level``
    - `LOG_FILE`: Overrides the filename set with ``filename``
    - `LOG_SMTP`: Enables logging of errors to SMTP (off by default). Does not have
        an equivalent param, as it should not be hardcoded. Only has an effect when
        running on Toolforge, as the Toolforge mailserver is hard-coded. The to and
        from addresses are ``tools.{tool}@toolforge.org``
    """
    loglevel = os.environ.get("LOG_LEVEL", level).upper()
    if loglevel == "VERBOSE":
        module_level = "DEBUG"
        root_level = "INFO"
    else:
        module_level = loglevel
        root_level = loglevel

    if os.environ.get("LOG_FILE"):
        log_file = os.environ["LOG_FILE"]
    elif filename:
        log_file = filename
    else:
        log_file = f"{module}.log"

    if thread:
        formatstr = "%(asctime)s %(name)s %(threadName)s %(levelname)s: %(message)s"
    else:
        formatstr = "%(asctime)s %(name)s %(levelname)s: %(message)s"

    conf: Dict = {
        "version": 1,
        "formatters": {
            "log": {
                "format": formatstr,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {},
        "loggers": {"pywiki": {"level": root_level}, module: {"level": module_level}},
        "root": {"level": root_level},
    }
    if log_file.lower() == "stderr":
        conf["handlers"]["console"] = {
            "class": "logging.StreamHandler",
            "formatter": "log",
        }
        conf["root"].setdefault("handlers", []).append("console")
    else:
        conf["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": get_log_location(log_file),
            "maxBytes": 10 * 1024**2,  # 10 MiB
            "backupCount": 5,
            "formatter": "log",
        }
        conf["root"].setdefault("handlers", []).append("file")

    if os.environ.get("LOG_SMTP") and on_toolforge():
        if not tool and os.environ.get("HOME"):
            tool = os.environ["HOME"].rpartition("/")[2]
        conf["handlers"]["smtp"] = {
            "class": "logging.handlers.SMTPHandler",
            "mailhost": "mail.tools.wmflabs.org",
            "fromaddr": f"tools.{tool}@toolforge.org",
            "toaddrs": [f"tools.{tool}@toolforge.org"],
            "subject": f"{tool} {module} error",
            "level": "ERROR",
            "formatter": "log",
        }
        conf["root"].setdefault("handlers", []).append("smtp")

    return conf


def getInitLogger(module: str, **kwargs) -> logging.Logger:
    """Configure and initialize logging, then return a Logger for ``module``.

    Parameters are passed to `logger_config`.
    :param module: Name of module to be logged
    """
    pywikibot.bot.init_handlers()
    logging.config.dictConfig(logger_config(module, **kwargs))
    return logging.getLogger(module)


def get_log_location(filename: str) -> str:
    """Return a log location depending on system.

    On Toolforge, uses ``$HOME/logs``, creating if needed.
    If ``$HOME`` is not set or the bot is not running on Toolforge,
    the current directiory is used instead.

    Absolute paths (starting with ``/``) are returned without modification.
    """
    if filename.startswith("/"):
        return filename
    elif on_toolforge() and os.environ.get("HOME"):
        logdir = os.path.join(os.environ["HOME"], "logs")
        try:
            os.mkdir(logdir)
        except FileExistsError:
            pass
    else:
        logdir = os.getcwd()

    return os.path.join(logdir, filename)


def on_toolforge() -> bool:
    """Detect if this is a Wikimedia Cloud Services environment.

    While this function is ``on_toolforge``, it will also detect Cloud VPS.
    """
    try:
        f = open("/etc/wmcs-project")
    except FileNotFoundError:
        wmcs = False
    else:
        wmcs = True
        f.close()
    return wmcs


def check_runpage(
    site: pywikibot.Site, task: str = "", title: str = "", override: bool = False
) -> None:
    """Raise `RunpageError` if on-wiki runpage is not True.

    Runpage title is ``User:<username>/Run`` or ``User:<username>/<task>/Run``
    if ``task`` is given.

    :param site: Pywikibot site for the runpage
    :param task: Optional subpage for bots with multiple tasks
    :param title: Full runpage title
    :param override: Skip runpage check entirely if True
    """
    if override:
        return
    if task and title:
        raise ValueError("task and title can not be used together")
    if not title:
        titleparts = [f"User:{site.username()}"]
        if task:
            titleparts.append(task)
        titleparts.append("Run")
        title = "/".join(titleparts)

    page = pywikibot.Page(site, title)
    if not page.text.endswith("True"):
        raise RunpageError(f"Runpage {page.title(as_link=True)} is disabled")


def save_page(
    text: str,
    page: pywikibot.Page,
    summary: str,
    bot: bool = True,
    minor: bool = False,
    mode: str = "replace",
    force: bool = False,
    new_ok: bool = False,
    no_change_ok: bool = False,
    edit_redirect: bool = False,
) -> None:
    """Helper for saving a page using Pywikibot.

    :param text: New page text
    :param page: Pywikibot page to be saved
    :param summary: Edit summary
    :param bot: Flag this edit as a bot edit, default True
    :param minor: Flag this edit as a minor edit, default False
    :param mode: Must be one of the following:
        - ``replace``: Replace the current text with ``text`` (default)
        - ``append``: Add ``text`` to the bottom of the page
        - ``prepend``: Add ``text`` to the top of the page
    :param force: Ignore bot exclusion protocol, default False
    :param new_ok: Allow the creation of new pages, default False
    :param no_change_ok: Do not raise `PageNotSaved` if there is no change between
        the current text and the new text.
    :param edit_redirect: Edit redirect pages instead of raising an exception
    """
    logger.info(f"Saving to {page.title()}")
    if not text:
        if no_change_ok:
            return
        raise PageNotSaved(
            page, message="New page text is blank, page %s was not saved"
        )

    try:
        old_text = page.get(force=True, get_redirect=edit_redirect)
    except pywikibot.exceptions.NoPageError as err:
        logger.exception(err)
        if new_ok:
            old_text = ""
        else:
            raise

    if mode == "replace":
        pass
    elif mode == "append":
        text = old_text + text
    elif mode == "prepend":
        text = text + old_text
    else:
        raise ValueError("mode must be 'replace', 'append', or 'prepend', not {mode}")

    if old_text == text:
        if not no_change_ok:
            raise PageNotSaved(
                page, message="Page text did not change, page %s was not saved"
            )
    else:
        page.text = text
        page.save(
            summary=summary,
            minor=minor,
            botflag=bot,
            quiet=True,
            force=force,
        )
        logger.info(f"Page {page.title(as_link=True)} saved")


def retry(function: Callable, retries: int, *args, **kwargs) -> Any:
    """Retry a function call if an exception occurs.

    :param function: Function to be called
    :param retries: Number of times to retry

    All other args are passed to the called function.
    """
    if retries < 1:
        raise ValueError("Retry called with retries < 1")
    for i in range(retries):
        try:
            out = function(*args, **kwargs)
        except Exception as e:
            err = e
        else:
            break
    else:
        raise err
    return out


class Throttle:
    """Enforce a time of ``delay`` seconds between calls to `throttle`.

    Different instances can be used to throttle different actions.
    Note: This throttle is not parallelism-safe.
    """

    def __init__(self, delay: float) -> None:
        """:param delay: Seconds between `throttle` calls"""
        self.delay = delay
        self.last_edit = 0.0

    def throttle(self) -> None:
        now = time.monotonic()
        diff = round(self.delay - (now - self.last_edit), 2)
        if diff > 0:
            logger.debug(f"Sleeping for {diff} seconds")
            time.sleep(diff)
        self.last_edit = time.monotonic()


def load_config(namespace: str, filepath: str) -> dict:
    """Load JSON configuration data stored in the parent directory.

    Load order:
    1. "*" in default_config.json
    2. ``namespace`` in default_config.json
    3. "*" in config.json
    4. ``namespace`` in config.json

    Configuation data loaded last takes precedence.

    :param namespace: Configuration namespace to use
    :param filepath: Set to ``__file__``
    """
    # XXX: Requiring that __file__ be passed every time isn't great. Calling __file__
    # here doesn't work, because it's now relative to this file in some site_packages
    # somewhere.
    conf_dir = os.path.realpath(os.path.dirname(filepath) + "/..")

    config = {}
    with open(os.path.join(conf_dir, "default_config.json")) as f:
        default_config = json.load(f)

    config.update(default_config.get("*", {}))
    config.update(default_config.get(namespace, {}))

    try:
        with open(os.path.join(conf_dir, "config.json")) as f:
            conf_file = json.load(f)
    except FileNotFoundError:
        pass
    else:
        config.update(conf_file.get("*", {}))
        config.update(conf_file.get(namespace, {}))

    return config
