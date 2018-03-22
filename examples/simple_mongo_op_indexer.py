from pymongo import MongoClient

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter

from chainmodel import ChainModel
from chainmodel.models.steem.schema import Schema

# define endpoints
endpoints = [
    'https://api.steemit.com/',
    'https://rpc.buildteam.io/',
    'https://steemd.privex.io/',
]

# setup adapter + chainsync
adapter = SteemAdapter(endpoints=endpoints)
chainsync = ChainSync(adapter)

# establish models with schema
chainmodel = ChainModel(schema=Schema())

# connect to database
mongo = MongoClient('mongodb://localhost', connect=False)
db = mongo['steem']

# stream all operations
for dataType, opData in chainsync.stream(['ops']):

    # model data based on schema
    model = chainmodel.get(opData)

    # insert in database
    db.ops.update(model.query(), model.data(), upsert=True)
