#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import abc
import logging
import threading
import time
import os
import gzip
import json
import shutil

from .alignment import MemoryQueue

logger = logging.getLogger(__file__)
BUF_SIZE = 1024


class Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        else:
            return cls.__instance


class ReplayRecorder(metaclass=abc.ABCMeta):
    def __init__(self, app, session=None):
        self.app = app
        self.session = session

    @abc.abstractmethod
    def record(self, data):
        """
        记录replay数据
        :param data: 数据 {
            "session": "",
            "data": "",
            "timestamp": ""
        }
        :return:
        """

    @abc.abstractmethod
    def session_start(self, session_id):
        print("Session start: {}".format(session_id))
        pass

    @abc.abstractmethod
    def session_end(self, session_id):
        print("Session end: {}".format(session_id))
        pass


class CommandRecorder:
    def __init__(self, app, session=None):
        self.app = app
        self.session = session

    def record(self, data):
        """
        :param data: 数据 {
            "session":
            "input":
            "output":
            "user":
            "asset":
            "system_user":
            "timestamp":
        }
        :return:
        """

    def session_start(self, session_id):
        print("Session start: {}".format(session_id))
        pass

    def session_end(self, session_id):
        print("Session end: {}".format(session_id))
        pass


class ServerReplayRecorder(ReplayRecorder):
    def __init__(self, app):
        super().__init__(app)
        self.file = None

    def record(self, data):
        """
        :param data:
        [{
            "session": session.id,
            "data": data,
            "timestamp": time.time()
        },...]
        :return:
        """
        # Todo: <liuzheng712@gmail.com>
        if len(data['data']) > 0:
            # print(json.dumps(
            #     data['data'].decode('utf-8', 'replace')))
            self.file.write(
                '"' + str(data['timestamp'] - self.starttime) + '":' + json.dumps(
                    data['data'].decode('utf-8', 'replace')) + ',')

    def session_start(self, session_id):
        self.starttime = time.time()
        self.file = open(os.path.join(
            self.app.config['LOG_DIR'], session_id + '.replay'
        ), 'a')
        self.file.write('{')

    def session_end(self, session_id):
        self.file.write('"0":""}')
        self.file.close()
        with open(os.path.join(self.app.config['LOG_DIR'], session_id + '.replay'), 'rb') as f_in, \
                gzip.open(os.path.join(self.app.config['LOG_DIR'], session_id + '.replay.gz'), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        if self.push_to_server(session_id):
            logger.info("Succeed to push {}'s {}".format(session_id, "record"))
        else:
            logger.error("Failed to push {}'s {}".format(session_id, "record"))

    def push_to_server(self, session_id):
        return self.app.service.push_session_replay(os.path.join(self.app.config['LOG_DIR'], session_id + '.replay.gz'),
                                                    session_id)

    def __del__(self):
        print("{} has been gc".format(self))
        del self.file


class ServerCommandRecorder(CommandRecorder, metaclass=Singleton):
    batch_size = 10
    timeout = 5
    no = 0

    def __init__(self, app):
        super().__init__(app)
        self.queue = MemoryQueue()
        self.stop_evt = threading.Event()
        self.push_to_server_async()
        self.__class__.no += 1

    def record(self, data):
        if data and data['input']:
            data['input'] = data['input'][:128]
            data['output'] = data['output'][:1024]
            data['timestamp'] = int(data['timestamp'])
            self.queue.put(data)

    def push_to_server_async(self):
        def func():
            while not self.stop_evt.is_set():
                data_set = self.queue.mget(self.batch_size, timeout=self.timeout)
                logger.debug("<Session command recorder {}> queue size: {}".format(
                    self.no, self.queue.qsize())
                )
                if not data_set:
                    continue
                logger.debug("Send {} commands to server".format(len(data_set)))
                ok = self.app.service.push_session_command(data_set)
                if not ok:
                    self.queue.mput(data_set)

        thread = threading.Thread(target=func)
        thread.daemon = True
        thread.start()

    def session_start(self, session_id):
        pass

    def session_end(self, session_id):
        pass

    def __del__(self):
        print("{} has been gc".format(self))


def get_command_recorder_class(app):
    command_engine = app.config["COMMAND_RECORD_ENGINE"]

    if command_engine == "server":
        return ServerCommandRecorder
    else:
        return ServerCommandRecorder


def get_replay_recorder_class(app):
    replay_engine = app.config["REPLAY_RECORD_ENGINE"]
    if replay_engine == "server":
        return ServerReplayRecorder
    else:
        return ServerReplayRecorder
