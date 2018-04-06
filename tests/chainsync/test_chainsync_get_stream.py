from test_base import ChainSyncBaseTestCase


class ChainSyncGetStreamTestCase(ChainSyncBaseTestCase):

    def test_get_stream_blocks(self):
        stream_data = list(self.chainsync.get_stream(['blocks'], start_block=1))
        # Should only retrive the blocks within the initial batch size
        self.assertEqual(len(stream_data), 10)
        # Should only be returning the data type requested
        self.assertTrue(stream_data[0][0] in ['block'])
        # Should be block 1 - 10 (default batch size is 10)
        self.assertTrue(stream_data[0][1]['block_num'] <= 10)

    def test_get_stream_blocks_with_batch_size(self):
        stream_data = list(self.chainsync.get_stream(['blocks'], start_block=1, batch_size=3))
        # Should only retrive the blocks within the initial batch size
        self.assertEqual(len(stream_data), 3)
        # Should only be returning the data type requested
        self.assertTrue(stream_data[0][0] in ['block'])
        # Should be block 1 - 10 (default batch size is 10)
        self.assertTrue(stream_data[0][1]['block_num'] <= 3)

    def test_get_stream_blocks_with_end(self):
        stream_data = list(self.chainsync.get_stream(['blocks'], start_block=1, end_block=4))
        # Should only retrieve a single event
        self.assertEqual(len(stream_data), 4)
        # Should only be returning the data types requested
        self.assertTrue([d[0] for d in stream_data][0] in ['block'])
        # Should be returning both blocks 1 & 2
        for block in [d[1] for d in stream_data]:
            self.assertTrue(block['block_num'] in [1, 2, 3, 4])

    def test_get_stream_ops(self):
        stream_data = list(self.chainsync.get_stream(['ops'], start_block=1))
        # Should only retrieve a single event (op) - even though there's 10 blocks
        self.assertEqual(len(stream_data), 1)
        # Should only be returning the data type requested
        self.assertTrue(stream_data[0][0] in ['op'])
        # Should be block 1 - 10 (default batch size is 10)
        self.assertTrue(stream_data[0][1]['block_num'] <= 10)

    def test_get_stream_ops_with_batch_size(self):
        stream_data = list(self.chainsync.get_stream(['ops'], start_block=3000000, batch_size=4))
        # Should retrieve 23 events (ops)
        self.assertEqual(len(stream_data), 23)
        self.assertEqual(len([d[1] for d in stream_data if d[0] == 'op']), 23)
        # Should only be returning the data type requested
        self.assertTrue(stream_data[0][0] in ['op'])
        for op in [d[1] for d in stream_data]:
            # Should be blocks 3000000 - 3000003
            self.assertTrue(op['block_num'] in [3000000, 3000001, 3000002, 3000003])

    def test_get_stream_ops_with_whitelist(self):
        stream_data = list(self.chainsync.get_stream(['ops'], start_block=3000000, whitelist=['vote', 'comment']))
        # Should retrieve 8 events (ops, 6 vote and 2 comment)
        self.assertEqual(len(stream_data), 8)
        self.assertEqual(len([d[1] for d in stream_data if d[0] == 'op' and d[1]['operation_type'] == 'vote']), 6)
        self.assertEqual(len([d[1] for d in stream_data if d[0] == 'op' and d[1]['operation_type'] == 'comment']), 2)
        # Should only be returning the data type requested
        self.assertTrue(stream_data[0][0] in ['op'])
        for op in [d[1] for d in stream_data]:
            # Should be blocks 3000000 - 3000003
            self.assertTrue(op['block_num'] in range(3000000, 3000010))
            # Should all be votes
            self.assertTrue(op['operation_type'] in ['vote', 'comment'])

    def test_get_stream_ops_with_end(self):
        stream_data = list(self.chainsync.get_stream(['ops'], start_block=3000000, end_block=3000003))
        # Should be retrieving a total of 23 ops from these 4 blocks
        self.assertEqual(len(stream_data), 23)
        # Should only be returning the data types requested
        self.assertTrue([d[0] for d in stream_data][0] in ['op'])
        # Should be returning ops from all blocks requested
        for op in [d[1] for d in stream_data]:
            self.assertTrue(op['block_num'] in [3000000, 3000001, 3000002, 3000003])

    def test_get_stream_ops_per_blocks(self):
        stream_data = list(self.chainsync.get_stream(['ops', 'ops_per_blocks'], start_block=1))
        # Should retrieve two events (1 op and 1 ops_per_blocks)
        self.assertEqual(len(stream_data), 2)
        # Should only be returning the data types requested
        self.assertTrue([
            d[0] for d in stream_data
        ][0] in ['op', 'ops_per_block'])
        # The ops should return the proper block number
        for op in [d[1] for d in stream_data if d[0] == 'op']:
            # Should be block 1 - 10 (default batch size is 10)
            self.assertTrue(op['block_num'] <= 10)
        # The ops_per_block should return the number of ops in the block
        for counter in [d[1] for d in stream_data if d[0] == 'ops_per_block']:
            self.assertEqual(counter[1], 1)

    def test_get_stream_ops_per_blocks_with_end(self):
        stream_data = list(self.chainsync.get_stream(['ops', 'ops_per_blocks'], start_block=3000000, end_block=3000003))
        # Should retrieve 24 events (23 ops and 1 ops_per_blocks)
        self.assertEqual(len(stream_data), 24)
        self.assertEqual(len([d[1] for d in stream_data if d[0] == 'op']), 23)
        self.assertEqual(len([d[1] for d in stream_data if d[0] == 'ops_per_block']), 1)
        # Should only be returning the data types requested
        self.assertTrue([
            d[0] for d in stream_data
        ][0] in ['op', 'ops_per_block'])
        # The ops should return the proper block number
        for op in [d[1] for d in stream_data if d[0] == 'op']:
            # Should be block 1 - 10 (default batch size is 10)
            self.assertTrue(op['block_num'] in [3000000, 3000001, 3000002, 3000003])
        # The ops_per_block should return the number of ops in the block
        for counter in [d[1] for d in stream_data if d[0] == 'ops_per_block']:
            print(counter)
            for height in [3000000, 3000001, 3000002, 3000003]:
                self.assertTrue(counter[height] in [3, 15, 4, 1])

    def test_get_stream_all_events(self):
        stream_data = list(self.chainsync.get_stream(start_block=3000000, batch_size=3))
        types_expected = ['config', 'block', 'op', 'ops_per_block']
        types_returned = [d[0] for d in stream_data]
        self.assertTrue(all([data_type in types_returned for data_type in types_expected]))
