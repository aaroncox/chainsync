from abc import ABC, abstractmethod

class AbstractAdapter(ABC):

    @property
    @abstractmethod
    def config(self):
        """ gets current configuration for the blockchain
        """
        pass

    @abstractmethod
    def opData(self, block, opType, opData, txIndex):
        """ decorate the operation data with details from the block

            :param dict block: the block this operation was contained within
            :param string opType: the type of operation
            :param dict opData: the operation as returned by the blockchain
            :param int txIndex: the position of the operation in the transaction
                    for lookup against the block data
        """
        pass

    @abstractmethod
    def vOpData(self, vop):
        """ returns a formatted virtual op

            decorate the virtual operation data to match the format of a
            basic operation (most data exists, just arranged differently)

            :return:
        """
        pass

    @abstractmethod
    def get_block(self, height):
        """ retrieve a block using the `get_block` method

            :param int height: the block to retrieve
        """
        pass

    @abstractmethod
    def get_blocks(self, blocks=[]):
        """ retrieve a block using the `get_block` method

            :param int blocks: a list of the blocks to retrieve        
        """
        pass

    @abstractmethod
    def get_ops_in_block(self, block_num):
        pass

    @abstractmethod
    def get_ops_in_blocks(self, start_block, virtual_only, blocks):
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
