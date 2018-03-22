import threading
import multiprocessing
import os
import signal
import time
import datetime

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter

from chainmodel import ChainModel
from chainmodel.models.steem.schema import Schema

from pymongo import MongoClient

# Setup ChainSync + Steem adapter
adapter = SteemAdapter(endpoints=['https://api.steemit.com/'])
chainsync = ChainSync(adapter)

# establish models with schema
chainmodel = ChainModel(schema=Schema())

class Example():

    def __init__(self):
        # Handling KeyboardInterrupt so the pool doesn't override
        # https://stackoverflow.com/questions/11312525/catch-ctrlc-sigint-and-exit-multiprocesses-gracefully-in-python
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

        self.requests = multiprocessing.Queue()
        self.responses = multiprocessing.Queue()

        self.requests_pool = multiprocessing.Pool(None, self.worker, (self.requests,))
        self.responses_pool = multiprocessing.Pool(None, self.saver, (self.responses,))

        # Reassign signal
        signal.signal(signal.SIGINT, original_sigint_handler)

        # Get chain config
        self.config = chainsync.get_config()

    def worker(self, queue):
        while True:
            # get the height and limit from the requests queue
            height, limit = queue.get(True)

            # retrieve the requested blocks
            for dataType, data in chainsync.get_stream(['ops', 'ops_per_block'], start_block=height, end_block=(height + limit)):
                self.responses.put((dataType, data))

    def saver(self, queue):
        # each saver gets it's own mongoclient
        mongo = MongoClient('mongodb://localhost', connect=False)
        db = mongo['steemindex']
        while True:
            # get any opData waiting in the responses queue
            dataType, data = queue.get(True)

            dataHeader = "{} #{}: {}".format(datetime.datetime.now(), data['block_num'], dataType)

            # if this was an op, save it
            if dataType == "op":
                print("{} {} {}".format(dataHeader, data['transaction_id'], data['operation_type']))
                # model data based on schema
                model = chainmodel.get(data)
                # insert in database
                db.ops.update(model.query(), model.data(), upsert=True)

            # if this was an ops_per_block response, save the counts per block
            #     (this data can be used to validate that every operation in a block was successfully saved)
            if dataType == "ops_per_block":
                for height in data:
                    print("{} - #{}: {}".format(dataHeader, height, data[height]))
                    db.ops_per_block.update({'_id': height}, {'v': data[height]}, upsert=True)

    def run(self, start_block=1, batch_size=10):
        while True:
            # Get blockchain status
            status = chainsync.get_status()

            # Determine the current head block
            head_block = status['head_block_number']

            # If no start block is specified, start streaming from head
            if start_block is None:
                start_block = head_block

            # Set initial remaining blocks for this stream
            remaining = head_block - start_block + 1

            # While remaining blocks exist - batch load them
            while remaining > 0:
                # Determine how many blocks to load with this request
                limit = batch_size

                # Modify the amount of blocks to load if lower than the batch_size
                if remaining < batch_size:
                    limit = remaining

                # Track the last block successfully processed
                last_block_processed = start_block

                # Queue the requested block + limit
                self.requests.put((start_block, limit))

                # Remaining blocks to process
                remaining = head_block - start_block

                # Next block to start on
                if remaining > batch_size:
                    start_block = start_block + batch_size
                else:
                    start_block = last_block_processed + 1

            # Pause loop based on the blockchain block time
            block_interval = self.config[chainsync.adapter.config['BLOCK_INTERVAL']] if 'BLOCK_INTERVAL' in chainsync.adapter.config else 3
            time.sleep(block_interval)

if __name__ == '__main__':

    batch_size = 10
    start_block = 1000000

    example = Example()
    example.run(start_block=start_block, batch_size=batch_size)
