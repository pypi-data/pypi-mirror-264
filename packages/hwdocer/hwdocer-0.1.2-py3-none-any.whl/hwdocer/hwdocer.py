#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import shutil
import argparse
import pathlib
import time
from time import sleep

# logging
from multiprocessing import Process, Queue, current_process
from logging.handlers import TimedRotatingFileHandler, QueueHandler
import logging


class HwDocer(object):

    diaOutFormat = 'png'
    __def_output__ = '_build'
    __def_input__ = './'
    __search_folder__ = '/**/'
    __search_hrs__ = '*.yml'
    __search_dia__ = '*.drawio'
    __verb_levels__ = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]

    """docstring for HwDocer"""

    def __init__(self, arg):
        super(HwDocer, self).__init__()
        self.arg = arg  # save passed arguments

        # Arguments
        argParse = argparse.ArgumentParser()
        argParse.add_argument("-v", "--verbose", help="Increase the verbosity level (can be used upto 4 times)", action='count', default=0)
        argParse.add_argument("-i", "--input", help="input directory to search for docs to build", default=self.__def_input__, type=pathlib.Path)
        argParse.add_argument("-o", "--output", help="output build directory", default=self.__def_output__, type=pathlib.Path)
        self.args = argParse.parse_args()  # Parse & save all arguments

        # region Logger
        self.verbosity = self.__verb_levels__[min(self.args.verbose, len(self.__verb_levels__) - 1)]
        self.q_log = Queue()

        # main object logger
        self.logger = logging.getLogger('hwdocer')
        self.logger.setLevel(self.verbosity)
        self.logger.addHandler(QueueHandler(self.q_log))

        logger_p = Process(target=self.logger_process, args=(self.q_log,))
        logger_p.start()
        # endregion

        # param - input files
        current_directory = os.getcwd()
        if not os.path.isabs(self.args.input):
            self.src_path = os.path.join(current_directory, self.args.input)
        else:
            self.src_path = self.args.input

        # param - output files
        # make output path absolute
        if os.path.isabs(self.args.output):
            self.dst_path = self.args.output
        else:
            self.dst_path = os.path.join(current_directory, self.args.output)
        self.logger.debug(f'input path: {self.src_path}, output path: {self.dst_path}')

        # start with empty work lists
        self.diaList = []
        self.hrsList = []
        self.builtList = []

        self.logger.debug(f'{__name__} created successfully')
        self.logger.info(f'started pid: {current_process().pid}')

    def searchFiles(self):
        self.logger.debug(f'starting input file searching')
        self.logger.debug(f'searching in {self.src_path} for {self.__search_folder__}')

        for folder in glob.iglob(self.src_path + self.__search_folder__, recursive=True):
            self.logger.debug(f'folder found: {folder}')
            self.logger.debug(f'searching in {folder} for {self.__search_hrs__}')
            for file in glob.iglob(folder + self.__search_hrs__):
                self.logger.debug(f'harness found: {os.path.basename(file)}')
                self.hrsList.append(file)
            self.logger.debug(f'searching in {folder} for {self.__search_dia__}')
            for file in glob.iglob(folder + self.__search_dia__):
                self.logger.debug(f'diagram found: {os.path.basename(file)}')
                self.diaList.append(file)

        self.logger.info(f'harnesses found: {self.hrsList}')
        self.logger.info(f'diagrams found: {self.diaList}')
        self.logger.debug(f'stopping input file searching')

    def prepFolder(self):
        self.logger.debug(f'starting folder preparation')
        try:
            # ensure root folder exists
            if not os.path.exists(self.dst_path):
                self.logger.info(f'creating folder: {self.dst_path}')
                os.makedirs(self.dst_path)
            else:
                self.logger.debug(f'folder: {self.dst_path} already existed')

            # ensure subfolder are ready
            for dia in self.diaList:
                commonPath = os.path.commonpath([self.src_path, dia])
                folder = os.path.dirname(dia).replace(commonPath, '')
                folder = folder[1:]
                folder = os.path.join(self.dst_path, folder)
                if not os.path.exists(folder):
                    self.logger.debug(f'creating folder: {folder}')
                    os.makedirs(folder)
                else:
                    self.logger.debug(f'folder: {folder} already existed')
            for hrs in self.hrsList:
                commonPath = os.path.commonpath([self.src_path, hrs])
                folder = os.path.dirname(hrs).replace(commonPath, '')
                folder = folder[1:]
                folder = os.path.join(self.dst_path, folder)
                if not os.path.exists(folder):
                    self.logger.debug(f'creating folder: {folder}')
                    os.makedirs(folder)
                else:
                    self.logger.debug(f'folder: {folder} already existed')
        except Exception as e:
            raise e
        self.logger.debug(f'stopping folder preparation')

    def buildHrs(self):
        self.logger.debug(f'starting building harnesses')
        for hrs in self.hrsList:                        # and we'll build each member of it
            self.logger.debug(f'building harness \'{hrs}\'')

            # path preparation
            commonPath = os.path.commonpath([self.src_path, hrs])
            outPath = os.path.dirname(hrs).replace(commonPath, '')
            outPath = outPath[1:]
            outPath = os.path.join(self.dst_path, outPath)

            # actual building
            resultCode = os.system("wireviz {}".format(hrs))
            if resultCode == 0:   # Try to build this harness
                self.builtList.append(str(hrs))      # Add it to the built list if successful
            else:
                self.logger.error(f'failed with code: {resultCode}\n')

            # move to build folder and cleanup
            try:
                name, extension = os.path.basename(hrs).split('.')
                os.chdir(os.path.dirname(hrs))
                shutil.copy(name + '.bom.tsv', outPath)
                os.remove(name + '.bom.tsv')
                shutil.copy(name + '.gv', outPath)
                os.remove(name + '.gv')
                shutil.copy(name + '.html', outPath)
                os.remove(name + '.html')
                shutil.copy(name + '.png', outPath)
                os.remove(name + '.png')
                shutil.copy(name + '.svg', outPath)
                os.remove(name + '.svg')
            except Exception as e:
                print(e)
                pass
        self.logger.debug(f'stopping building harnesses')

    def buildDia(self):
        self.logger.debug(f'starting building diagrams')
        for dia in self.diaList:
            commonPath = os.path.commonpath([self.src_path, dia])
            outPath = os.path.dirname(dia).replace(commonPath, '')
            outPath = outPath[1:]
            outPath = os.path.join(self.dst_path, outPath)
            self.logger.debug(f'Building diagram \'{dia}\' into {outPath}')

            # Try to build this diagram
            try:
                resultCode = os.system("drawio -x -t -f {} -o {} {}".format(self.diaOutFormat, outPath, dia))
                # Add it to the built list if successful
                if resultCode == 0:
                    self.builtList.append(str(dia))
                else:
                    self.logger.error('failed with code: {resultCode}')
            except Exception as e:
                raise e
        self.logger.debug(f'stopping building diagrams')

    def run(self):
        status = 0

        self.logger.debug(f'starting')

        # 1. Search all supported files
        self.searchFiles()

        # 2. Prepare build folder
        self.prepFolder()

        # 3. Generate harness
        self.buildHrs()

        # 4. Generate diagrams
        self.buildDia()

        # graceful end of exec
        self.logger.info(f'all done, stopping pid: {current_process().pid}')
        self.q_log.put(None)
        return status

    def logger_process(self, queue):
        """ logging isolated process

        Args:
            queue (Queue): logging queue receiving all logs to be saved
        """

        logger = logging.getLogger('logger')
        logger.setLevel(self.verbosity)

        # Create a separate folder for logs if it doesn't exist
        log_dir = 'log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Formater
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d | %(name)-15s | %(levelname)-8s | %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')

        # File logging
        log_filename = os.path.join(log_dir, f'hwdocer_{time.strftime("%Y-%m-%d_%H-%M-%S")}.log')
        file_handler = TimedRotatingFileHandler(log_filename, when='midnight', backupCount=4)
        file_handler.setFormatter(formatter)

        # Console logging
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(self.verbosity)  # Set the level as needed
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        logger.info(f'started pid: {current_process().pid}')

        # process loop
        while True:
            msg = queue.get()       # pull new message from queue
            if msg is None:         # exit process on special None message
                break
            logger.handle(msg)      # log the message

        logger.info(f'stopped pid: {current_process().pid}')
        return 0
