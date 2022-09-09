from __future__ import annotations

import logging
import traceback

from tribler.core.components.reporter.reported_error import ReportedError
from tribler.core.sentry_reporter.sentry_reporter import SentryStrategy
from tribler.core.sentry_reporter.sentry_scrubber import SentryScrubber
from tribler.gui import gui_sentry_reporter
from tribler.gui.app_manager import AppManager
from tribler.gui.dialogs.feedbackdialog import FeedbackDialog
from tribler.gui.exceptions import CoreError


# fmt: off


class ErrorHandler:
    def __init__(self, tribler_window):
        logger_name = self.__class__.__name__
        self._logger = logging.getLogger(logger_name)
        gui_sentry_reporter.ignore_logger(logger_name)

        self.tribler_window = tribler_window
        self.app_manager: AppManager = tribler_window.app_manager

        self._handled_exceptions = set()
        self._tribler_stopped = False

    def gui_error(self, exc_type, exc, tb):
        text = "".join(traceback.format_exception(exc_type, exc, tb))
        self._logger.error(text)

        if self._tribler_stopped:
            return

        if gui_sentry_reporter.global_strategy == SentryStrategy.SEND_SUPPRESSED:
            self._logger.info(f'GUI error was suppressed and not sent to Sentry: {exc_type.__name__}: {exc}')
            return

        if exc_type in self._handled_exceptions:
            return
        self._handled_exceptions.add(exc_type)

        is_core_exception = issubclass(exc_type, CoreError)
        if is_core_exception:
            text = f'{text}\n\nLast Core output:\n{self.tribler_window.core_manager.get_last_core_output()}'
            self._stop_tribler(text)

        reported_error = ReportedError(
            type=type(exc_type).__name__,
            text=text,
            event=gui_sentry_reporter.event_from_exception(exc),
        )

        if self.app_manager.quitting_app:
            return

        FeedbackDialog(
            parent=self.tribler_window,
            sentry_reporter=gui_sentry_reporter,
            reported_error=reported_error,
            tribler_version=self.tribler_window.tribler_version,
            start_time=self.tribler_window.start_time,
            stop_application_on_close=self._tribler_stopped,
            additional_tags={'source': 'gui'},
            retrieve_error_message_from_stacktrace=is_core_exception
        ).show()

    def core_error(self, reported_error: ReportedError):
        if self._tribler_stopped or reported_error.type in self._handled_exceptions:
            return
        self._handled_exceptions.add(reported_error.type)

        error_text = f'{reported_error.text}\n{reported_error.long_text}'
        self._logger.error(error_text)

        if reported_error.should_stop:
            self._stop_tribler(error_text)

        SentryScrubber.remove_breadcrumbs(reported_error.event)

        FeedbackDialog(
            parent=self.tribler_window,
            sentry_reporter=gui_sentry_reporter,
            reported_error=reported_error,
            tribler_version=self.tribler_window.tribler_version,
            start_time=self.tribler_window.start_time,
            stop_application_on_close=self._tribler_stopped,
            additional_tags={'source': 'core'}
        ).show()

    def _stop_tribler(self, text):
        if self._tribler_stopped:
            return

        self._tribler_stopped = True

        self.tribler_window.tribler_crashed.emit(text)
        self.tribler_window.delete_tray_icon()

        # Stop the download loop
        self.tribler_window.downloads_page.stop_loading_downloads()

        # Add info about whether we are stopping Tribler or not
        self.tribler_window.core_manager.stop(quit_app_on_core_finished=False)

        self.tribler_window.setHidden(True)

        if self.tribler_window.debug_window:
            self.tribler_window.debug_window.setHidden(True)
