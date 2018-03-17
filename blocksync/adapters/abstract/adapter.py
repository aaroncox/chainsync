from abc import ABC, abstractmethod

class AbstractAdapter(ABC):

    @property
    @abstractmethod
    def config(self):
        pass

    @abstractmethod
    def opData(self, block, opType, opData, txIndex):
        pass

    @abstractmethod
    def vOpData(self, vop):
        pass

    @abstractmethod
    def get_block(self, height):
        pass

    @abstractmethod
    def get_blocks(self, start_block, limit):
        pass

    @abstractmethod
    def get_config(self):
        pass

    @abstractmethod
    def get_methods(self):
        pass

    @abstractmethod
    def get_status(self):
        pass
