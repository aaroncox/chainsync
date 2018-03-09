from abc import ABC, abstractmethod

class AbstractAdapter(ABC):

    @abstractmethod
    def get_block(self, height):
        pass

    @abstractmethod
    def get_blocks(self, start_block, limit):
        pass

    @abstractmethod
    def get_status(self):
        pass
