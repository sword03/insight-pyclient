from insight_pyclient.insight_api import InsightApi


def p(o):
    if isinstance(o, list):
        for item in o:
            print(str(item))
    else:
        print(o)


client = InsightApi('http://13.113.169.3/insight-api/')
block = client.get_block(
    '00000000cb5314d3d9bb7b8454dd567ba65a487f1022a9e8344cc49a25680795')
p(block)

#utxos = client.get_unsent_outputs('n3jYBjCzgGNydQwf83Hz6GBzGBhMkKfgL1')
#p(utxos)


print('************************get_unsent_outputs_ex************************************************')
#utxos = client.get_unsent_outputs_ex('n3jYBjCzgGNydQwf83Hz6GBzGBhMkKfgL1')
#utxos = client.get_unsent_outputs_ex('n3jYBjCzgGNydQwf83Hz6GBzGBhMkKfgL1', 0.00001000)
#p(utxos)

#txid = client.send_raw_transaction('020000000268bf1c110ced34ff9ee6d82a8923578dbda912882eb458d4709b3a1bd6fad3c6000000001716001472fb3ff2772c5bc11b571515e5a0621d5c25b8f3ffffffff68bf1c110ced34ff9ee6d82a8923578dbda912882eb458d4709b3a1bd6fad3c60100000017160014e240c1f374c1fbc22d0d779b633e2e471a13a1cbffffffff02640000000000000017a9147afd7488fae661a6dc57d6de7e38fae51645774e87da15d0000000000017a914de7550629380d44534cad333ce73b6d58653d7838700000000')
#p(txid)

#txs = client.get_address(address='n3jYBjCzgGNydQwf83Hz6GBzGBhMkKfgL1', no_transactions=False, transaction_from=0, transaction_to=5)
#txs = client.get_address(address='2MxQeB46hMJVFNCcTorb25DC2Kj4xdqhbXH', no_transactions=False, transaction_from=0, transaction_to=5)
txs = client.get_address(address='mmCevMVNNxDYPBJFbz21zLTUvoYBvAsrtc', no_transactions=False, transaction_from=0, transaction_to=1000)
p(txs)

class ReceiveSpend:
    def __init__(self, txid, index, amt, amt_unit, is_receive):
        self.txid = txid
        self.index = index
        self.amt = amt
        self.amt_unit = amt_unit
        self.is_receive = is_receive

def get_receive_spend(address, tx):
    for tx in txs.transactions:
        rs_list = []
        trans = client.get_transaction(tx)
        for input in trans.inputs:
            if not input.is_coinbase():
                if input.addr == address:
                    rs_list.append(ReceiveSpend(txid=input.txid, index=input.n, amt=input.value, amt_unit=input.valueSat, is_receive=False))
        for n, output in enumerate(trans.outputs):
            if output.include_address():
                if output.scriptPubKey.addresses.addr == address:
                    rs_list.append(ReceiveSpend(txid=tx, index=output.n, amt=output.value, amt_unit=output.value * 100000000, is_receive=True))

        return rs_list




for tx in txs.transactions:
    trans = client.get_transaction(tx)
    print(trans)
    for input in trans.inputs:
        print('is_coinbase():', input.is_coinbase())

s = client.get_block_summaries(max_number=3, date='2019-10-15')
print(s)

ret = client.get_height()
print(ret)