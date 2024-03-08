class StringEnum:
    def __init__(self, *args):
        self._enums = args

    def __getattr__(self, item):
        if item in self._enums:
            return item
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")


class Status(StringEnum):
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"