##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.11.7                                                             #
# Generated on 2024-03-27T23:22:58.029174                                        #
##################################################################################

from __future__ import annotations


class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class StorageExecutor(object, metaclass=type):
    def __init__(self, use_processes = False):
        ...
    def warm_up(self):
        ...
    def submit(self, *args, **kwargs):
        ...
    ...

def handle_executor_exceptions(func):
    """
    Decorator for handling errors that come from an Executor. This decorator should
    only be used on functions where executor errors are possible. I.e. the function
    uses StorageExecutor.
    """
    ...

