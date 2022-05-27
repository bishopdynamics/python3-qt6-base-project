#!/usr/bin/env python3

# Thread Workers Module
#   workers to run in separate thread from UI, for long-running tasks that would otherwise freeze the UI

# Created 2022 by James Bishop (james@bishopdynamics.com)

import time
from abc import abstractmethod


from PyQt6.QtCore import QRunnable, pyqtSignal, QObject, QThreadPool

from Mod_Constants import *
from Mod_Util import print_traceback, print_obj


class ThreadWorkerSignals(QObject):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    error = pyqtSignal(str)
    success = pyqtSignal()
    result = pyqtSignal(object)


class ThreadWorker(QRunnable):
    # base ThreadWorker class
    def __init__(self):
        super().__init__()
        self.signals = ThreadWorkerSignals()

    def report_progress(self, progress: int):
        # report progress as 0-100 int
        self.signals.progress.emit(progress)

    def report_status(self, message: str):
        # report a status message
        self.signals.status.emit(message)

    def report_error(self, message: str):
        # report that worker failed, and why
        self.report_status('Error')
        self.signals.error.emit(message)

    def report_success(self):
        # report that worker completed successfully
        self.report_status('Success')
        self.signals.success.emit()

    def report_result(self, result: any):
        # report the output of the worker process, any object can be returned
        self.signals.result.emit(result)

    def run(self):
        # this is what gets run
        self.report_status('Starting')
        self.report_progress(0)
        self.thread_action()
        pass

    @abstractmethod
    def thread_action(self):
        # this is where long-running work goes
        #   this method is responsible for reporting progress:
        #       while working: report_progress, report_status
        #       if failure: report_error (no report_result called if error)
        #       if success: report_result, report_success
        pass


class ThreadWorkerCommunicator:
    # handles communication with a threadworker, progressbar, statuslabel, and handling result
    def __init__(self, name, worker: ThreadWorker, thread_pool: QThreadPool, message_function: callable, result_function: callable, progressbar=None, statuslabel=None):
        self.worker = worker
        self.log_msg = message_function
        self.progressbar = progressbar
        self.statuslabel = statuslabel
        self.thread_pool = thread_pool
        self.result_function = result_function
        self.name = name
        self.setup()

    def setup(self):
        try:
            self.worker.signals.progress.connect(self.on_progress)
            self.worker.signals.status.connect(self.on_status)
            self.worker.signals.error.connect(self.on_error)
            self.worker.signals.success.connect(self.on_success)
            self.worker.signals.result.connect(self.on_result)
        except Exception as ex:
            print('Error while setting up threadworkercommunicator: %s' % ex)
            print_traceback()

    def run(self):
        try:
            self.thread_pool.start(self.worker)
        except Exception as ex:
            print('error while running worker: %s' % ex)
            print_traceback()

    def on_progress(self, progress: int):
        # update a progress bar if assigned
        if self.progressbar:
            self.progressbar.setValue(progress)

    def on_status(self, status: str):
        # update a status label if assigned
        self.log_msg('ThreadWorker %s - Status: %s' % (self.name, status))
        if self.statuslabel:
            self.statuslabel.setText('Status: %s' % status)

    def on_error(self, error: str):
        self.log_msg('ThreadWorker %s - Error: %s' % (self.name, error))

    def on_success(self):
        self.log_msg('ThreadWorker %s - Success!' % self.name)

    def on_result(self, result):
        self.result_function(result)


class TicketCreator(ThreadWorker):
    # all the logic for creating JIRA tickets from selected contracts lives here
    def __init__(self, items: list):
        super().__init__()
        self.items = items

    def thread_action(self):
        # create tickets based on self.contracts_processed
        num_selected = len(self.items)
        num_created = 0
        num_skipped = 0
        if num_selected == 0:
            self.report_status('Creating 0 tickets, no contracts selected')
        else:
            count = 0
            self.report_status('Creating tickets for %s selected contracts' % num_selected)
            self.report_progress(5)
            for item in self.items:
                contract_id = item['id']
                progress = round(((count + 1) / num_selected) * 100)  # offset so that you can tell things have started
                # work starts here
                self.report_status('Creating tickets for Contract ID: %s' % contract_id)
                time.sleep(1)
                # work done
                self.report_progress(progress)
                print(progress)
                num_created += 1  # track how many we actually create
                count += 1
            self.report_progress(100)
            self.report_status('Of %s selected contracts, %s tickets were created, and %s were skipped' % (num_selected, num_created, num_skipped))
            self.report_result({
                'created': num_created,
                'selected': num_selected,
                'skipped': num_skipped,
            })
