#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import shutil
import argparse
import pathlib
import time
import yaml

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
            self.src_path = os.path.normpath(os.path.join(current_directory, self.args.input))
        else:
            self.src_path = os.path.normpath(self.args.input)

        # param - output files
        # make output path absolute
        if os.path.isabs(self.args.output):
            self.dst_path = os.path.normpath(self.args.output)
        else:
            self.dst_path = os.path.normpath(os.path.join(current_directory, self.args.output))
        self.logger.debug(f'input path: {self.src_path}')
        self.logger.debug(f'output path: {self.dst_path}')

        # start with empty work lists
        self.dia_list = []
        self.hrs_list = []
        self.hrs_img_list = []
        self.built_list = []

        self.logger.debug(f'{__name__} created successfully')

    def search_files(self):
        self.logger.debug(f'S input file searching')
        self.logger.debug(f'searching in {self.src_path} for {self.__search_folder__}')

        # searching for compatible files
        for folder in glob.iglob(self.src_path + self.__search_folder__, recursive=True):
            self.logger.debug(f'folder found: {folder}')
            self.logger.debug(f'searching in {folder} for {self.__search_hrs__}')
            for file in glob.iglob(folder + self.__search_hrs__):
                self.logger.debug(f'harness found: {os.path.basename(file)}')
                self.hrs_list.append(file)
                # find all image in this harness and prepare for copy
                self.hrs_img_list.append(self._get_all_img_path_from_hrs(file))
            self.logger.debug(f'searching in {folder} for {self.__search_dia__}')
            for file in glob.iglob(folder + self.__search_dia__):
                self.logger.debug(f'diagram found: {os.path.basename(file)}')
                self.dia_list.append(file)

        # Condition lists
        self.hrs_list = self._flatten_and_remove_duplicate_from_list(self.hrs_list)
        self.hrs_img_list = self._flatten_and_remove_duplicate_from_list(self.hrs_img_list)
        self.dia_list = self._flatten_and_remove_duplicate_from_list(self.dia_list)

        self.logger.info(f'harnesses found: {self.hrs_list}')
        self.logger.debug(f'images found: {self.hrs_img_list}')
        self.logger.info(f'diagrams found: {self.dia_list}')
        self.logger.debug(f'P input file searching')

    def prep_folder(self):
        self.logger.debug(f'S folder preparation')

        # Folder structure recreation
        try:
            # ensure root folder exists
            if not os.path.exists(self.dst_path):
                self.logger.info(f'creating folder: {self.dst_path}')
                os.makedirs(self.dst_path)
            else:
                self.logger.debug(f'folder: {self.dst_path} already existed')

            # ensure subfolder are ready
            for dia in self.dia_list:
                commonPath = os.path.commonpath([self.src_path, dia])
                folder = os.path.dirname(dia).replace(commonPath, '')
                folder = folder[1:]
                folder = os.path.join(self.dst_path, folder)
                if not os.path.exists(folder):
                    self.logger.debug(f'creating folder: {folder}')
                    os.makedirs(folder)
                else:
                    self.logger.debug(f'folder: {folder} already existed')
            for hrs in self.hrs_list:
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

        # Copy all source file and all image in harness
        try:
            for image in self.hrs_img_list:
                self.logger.debug(f'copying {image} to {self.dst_path}')
                shutil.copy2(image, self.dst_path)
        except Exception as e:
            raise e
        # end try

        self.logger.debug(f'P folder preparation')

    def build_hrs(self):
        self.logger.debug(f'S building harnesses')
        for hrs in self.hrs_list:                        # and we'll build each member of it
            self.logger.debug(f'building harness \'{hrs}\'')

            # path preparation
            commonPath = os.path.commonpath([self.src_path, hrs])
            outPath = os.path.dirname(hrs).replace(commonPath, '')
            outPath = outPath[1:]
            outPath = os.path.join(self.dst_path, outPath)

            # actual building
            resultCode = os.system("wireviz {}".format(hrs))
            if resultCode == 0:   # Try to build this harness
                self.built_list.append(str(hrs))      # Add it to the built list if successful
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
        self.logger.debug(f'P building harnesses')

    def build_dia(self):
        self.logger.debug(f'S building diagrams')
        for dia in self.dia_list:
            commonPath = os.path.commonpath([self.src_path, dia])
            outPath = os.path.dirname(dia).replace(commonPath, '')
            outPath = outPath[1:]
            outPath = os.path.join(self.dst_path, outPath)
            self.logger.debug(f'Building diagram \'{dia}\'')

            # Try to build this diagram
            try:
                resultCode = os.system("drawio -x -t -f {} -o {} {}".format(self.diaOutFormat, outPath, dia))
                # Add it to the built list if successful
                if resultCode == 0:
                    self.built_list.append(str(dia))
                else:
                    self.logger.error('failed with code: {resultCode}')
            except Exception as e:
                raise e
        self.logger.debug(f'P building diagrams')

    def _get_all_img_path_from_hrs(self, hrs_path):
        image_list = []

        try:
            with open(hrs_path, 'r') as file:
                yaml_content = yaml.safe_load(file)
                for key, val in yaml_content.items():
                    if key == 'connectors' or key == 'cables':  # top level
                        for key2, val2 in val.items():          # connectors & cables listing level
                            for key3, val3 in val2.items():     # each conn/cable element level
                                if key3 == 'image':             # we only care for the image element
                                    for key4, val4 in val3.items():
                                        if key4 == 'src':       # we find the source path of it
                                            image = os.path.normpath(os.path.join(os.path.dirname(hrs_path), val4))
                                            self.logger.debug(f'image found: {image}')
                                            image_list.append(image)
        except Exception as e:
            self.logger.warning(f'failed to open {hrs_path}')
        # end try
        return image_list

    def _flatten_and_remove_duplicate_from_list(self, mylist=None):
        if mylist is not None:
            # flatten list
            flat_list = []
            for item in mylist:
                if type(item) == list:
                    flat_list.extend(item)
                else:
                    flat_list.append(item)

            # remove duplicate in list
            unique_list = []
            for item in flat_list:
                if item not in unique_list:
                    unique_list.append(item)

            return unique_list

    def run(self):
        status = 0

        self.logger.info(f'S execution, pid: {current_process().pid}')

        # 1. Search all supported files
        self.search_files()

        # 2. Prepare build folder
        self.prep_folder()

        # 3. Generate harness
        self.build_hrs()

        # 4. Generate diagrams
        self.build_dia()

        # graceful end of exec
        self.logger.info(f'P execution, pid: {current_process().pid}')
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

        logger.info(f'S execution, pid: {current_process().pid}')

        # process loop
        while True:
            msg = queue.get()       # pull new message from queue
            if msg is None:         # exit process on special None message
                break
            logger.handle(msg)      # log the message

        logger.info(f'P execution, pid: {current_process().pid}')
        return 0
