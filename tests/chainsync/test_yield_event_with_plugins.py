from test_base import ChainSyncBaseTestCase

from datetime import datetime
from abc import ABC, abstractmethod

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter

class ChainSyncYieldEventTestCase(ChainSyncBaseTestCase):

    def test_yield_event_plugin(self):
        # configure with adapter + plugin
        chainsync = ChainSync(adapter=SteemAdapter(), plugins=[SamplePlugin1()])
        # sample 'what' and 'data' for the event
        what = 'block'
        data = {
            'timestamp': '2018-02-19T23:54:09'
        }
        # yield the data in an event
        tupled = chainsync.yield_event(what, data)
        eventType, eventData = tupled
        # they should still match
        self.assertEqual(eventType, what)
        self.assertEqual(eventData, data)
        # ensure a datetime is returned
        self.assertIsInstance(eventData['timestamp'], datetime)

    def test_yield_event_plugin(self):
        # configure with adapter + plugin
        chainsync = ChainSync(adapter=SteemAdapter(), plugins=[SamplePlugin1(), SamplePlugin2()])
        # sample 'what' and 'data' for the event
        what = 'block'
        data = {
            'string': 'convert to upper',
            'timestamp': '2018-02-19T23:54:09'
        }
        # yield the data in an event
        tupled = chainsync.yield_event(what, data)
        eventType, eventData = tupled
        # they should still match
        self.assertEqual(eventType, what)
        # ensure a datetime is returned (via SamplePlugin1)
        self.assertIsInstance(eventData['timestamp'], datetime)
        # ensure the string is now upper (via SamplePlugin2)
        self.assertEqual(eventData['string'], data['string'].upper())

class AbstractPlugin(ABC):

    @abstractmethod
    def block(self, data):
        """ a method name matching the 'what' value and transforms
            the data as needed.
        """
        pass

class SamplePlugin1(AbstractPlugin):

    """ a plugin that will convert a timestamp string into a datetime
    """
    def block(self, data):
        ts = data['timestamp']
        data['timestamp'] = datetime(int(ts[:4]), int(ts[5:7]), int(ts[8:10]), int(ts[11:13]), int(ts[14:16]), int(ts[17:19]))
        return data

class SamplePlugin2(AbstractPlugin):

    """ a plugin that will upper() a single field
    """
    def block(self, data):
        data['string'] = data['string'].upper()
        return data
