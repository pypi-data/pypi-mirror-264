# -*- coding: utf-8 -*-
import logging
import os
from typing import List
from threading import Thread, Event

logger = logging.getLogger(__name__)


def force_exit_from_threads(code: int = -1):
    os._exit(code)  # noqa


def run_threads_until_any_exits(thread_list: List[Thread]):
    def _wrap_run(raw_run, event: Event):
        def _wrapper():
            self = raw_run.__self__
            try:
                raw_run()
                logger.critical(f"A thread has finished: {self}")
            except SystemExit:
                logger.critical(f"A thread has exited: {self}")
            except Exception as e:
                logger.critical(f"A thread has aborted by exception: {self}, {e}")
            event.set()

        return _wrapper

    shared_event = Event()
    for thread in thread_list:
        thread.daemon = True
        thread.run = _wrap_run(thread.run, shared_event)
        thread.start()

    shared_event.wait()
