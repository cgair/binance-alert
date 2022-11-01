#!/usr/bin/env python
import logging
import os
import threading
import toml

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

lock = threading.Lock()

class Config(object):
    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), 'config/config.toml')
        self.config = self._from_toml()
        self._init_config_observer()

    def _init_config_observer(self):
        """Reload the target based on file changes in the directory"""
        observer = Observer()
        this = self
        class ConfigModifyHandler(FileSystemEventHandler):
            def on_modified(self, event):
            # All files within the watched directory will trigger
            # an event, so we filter to only reload when the target
            # file is changed.
                if os.path.relpath(event.src_path) == 'config/config.toml':
                    this._reload()

        # Sadly, watchdog only operates on directories and not on a file
        # level, so any change within the directory will trigger a reload.
        observer.schedule(ConfigModifyHandler(), path=os.path.dirname(self.config_path), recursive=False)
        observer.setDaemon(True)
        observer.start()

    def _from_toml(self):
        return toml.load(self.config_path)

    def _reload(self):
        """Manually reload the class with its new config."""
        logging.debug("reload the class with its new config")
        try:
            lock.acquire()
            self.config = self._from_toml()
        finally:
            lock.release()

    # A static method does not receive an implicit first argument. 
    # A static method is also a method that is bound to the class and not the object of the class. 
    # This method can’t access or modify the class state.
    # @staticmethod