##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.11.6                                                             #
# Generated on 2024-03-23T22:37:23.098662                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.monitor

class DebugMonitor(metaflow.monitor.NullMonitor, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugMonitorSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

