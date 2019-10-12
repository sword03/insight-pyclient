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

utxos = client.get_unsent_outputs('n3jYBjCzgGNydQwf83Hz6GBzGBhMkKfgL1')
#p(utxos)


print('************************get_unsent_outputs_ex************************************************')
utxos = client.get_unsent_outputs_ex('n3jYBjCzgGNydQwf83Hz6GBzGBhMkKfgL1')
#utxos = client.get_unsent_outputs_ex('n3jYBjCzgGNydQwf83Hz6GBzGBhMkKfgL1', 0.00001000)
p(utxos)
