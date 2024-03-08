from abc import ABC, abstractmethod

def AutonomousRCControllerInterface(ABC):
    @property
    @abstractmethod
    def depth_camera(self):
        pass

    @abstractmethod
    def start(self, end_cords):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def get_status(self):
        pass