from test_base import ChainSyncBaseTestCase


class ChainSyncGetStreamTestCase(ChainSyncBaseTestCase):

    def test_get_stream_blocks(self):
        stream_data = list(self.chainsync.get_stream(['blocks'],
                                                     start_block=1))
        # Should only retrieve a single event (block)
        self.assertEqual(len(stream_data), 1)
        # Should only be returning the data type requested
        self.assertTrue(stream_data[0][0] in ['block'])
        # Should be block #1
        self.assertEqual(stream_data[0][1]['block_num'], 1)

    def test_get_stream_ops(self):
        stream_data = list(self.chainsync.get_stream(['ops'], start_block=1))
        # Should only retrieve a single event (op)
        self.assertEqual(len(stream_data), 1)
        # Should only be returning the data type requested
        self.assertTrue(stream_data[0][0] in ['op'])
        # Should be block #1
        self.assertEqual(stream_data[0][1]['block_num'], 1)

    def test_get_stream_ops_per_blocks(self):
        stream_data = list(self.chainsync.get_stream(['ops', 'ops_per_blocks'],
                                                     start_block=1))
        # Should retrieve two events
        self.assertEqual(len(stream_data), 2)
        # Should only be returning the data types requested
        self.assertTrue([
            d[0] for d in stream_data
        ][0] in ['op', 'ops_per_block'])
        # The ops should return the proper block number
        for op in [d[1] for d in stream_data if d[0] == 'op']:
            self.assertEqual(op['block_num'], 1)
        # The ops_per_block should return the number of ops in the block
        for counter in [d[1] for d in stream_data if d[0] == 'ops_per_block']:
            self.assertEqual(counter[1], 1)

    def test_get_stream_blocks_with_end(self):
        stream_data = list(self.chainsync.get_stream(['blocks'], start_block=1,
                                                     end_block=4))
        # Should only retrieve a single event
        self.assertEqual(len(stream_data), 4)
        # Should only be returning the data types requested
        self.assertTrue([d[0] for d in stream_data][0] in ['block'])
        # Should be returning both blocks 1 & 2
        for block in [d[1] for d in stream_data]:
            self.assertTrue(block['block_num'] in [1, 2, 3, 4])

    def test_get_stream_ops_with_end(self):
        stream_data = list(self.chainsync.get_stream(['ops'],
                                                     start_block=3000000,
                                                     end_block=3000003))
        # Should be retrieving a total of 23 ops from these 4 blocks
        self.assertEqual(len(stream_data), 23)
        # Should only be returning the data types requested
        self.assertTrue([d[0] for d in stream_data][0] in ['op'])
        # Should be returning both blocks 1 & 2
        for op in [d[1] for d in stream_data]:
            self.assertTrue(op['block_num'] in [3000000, 3000001,
                                                3000002, 3000003])
