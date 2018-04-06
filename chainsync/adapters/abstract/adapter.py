from abc import ABC, abstractmethod

class AbstractAdapter(ABC):

    @property
    @abstractmethod
    def config(self):
        """ gets current configuration for the blockchain
        """
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
    def get_transaction(self, transaction_id=1):
        pass

    @abstractmethod
    def get_transactions(self, transaction_ids=[]):
        pass

    @abstractmethod
    def format_op_from_get_block(self, block, op, txIndex=False, opIndex=False):
        pass

    @abstractmethod
    def format_op_from_get_ops_in_block(self, op):
        pass

    @abstractmethod
    def format_op_from_get_transaction(self, tx, op, txIndex=False, opIndex=False):
        pass
