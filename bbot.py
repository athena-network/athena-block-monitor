import discord
import asyncio
import turtlecoin
import json
import time
import random

#discord stuff
token = open('tokenfile').read()
client = discord.Client()


tc = turtlecoin.TurtleCoind(host='127.0.0.1', port=12001)

tclbh = tc.get_last_block_header()['result']

def getstats(height):

	tcgl = tc.get_last_block_header()['result']['block_header']

	#height of the latest block
	height = tcgl['height']
	#hash of latest block
	hash = tcgl['hash']
	# whether atest block is orphan or not
	orphan = tcgl['orphan_status']

	#reward of the latest block
	reward = tcgl['reward']
	breward = reward / 100

	#wheter the time the block took to make is acceptable or not
	timex = tcgl['timestamp']
	prevhash = tcgl['prev_hash']
	glb = tc.getblock(prevhash)
	time2 = glb['block']['timestamp']
	timed = (timex - time2) / 60
	rock = "388916188715155467"
	pingrock = "<@" + rock + ">"
	blocktime = ""
	if timed <= 1800:
		blocktime += "Block was too fast, {timed} minutes".format(timed=timed)
		pingrock += ""
	elif timed >= 7200:
		blocktime += 'Took too long, {timed} minutes.'
		pingrock += ""
	else:
		blocktime += "Took {timed} minutes to make, pretty nice".format(timed=timed)
		pingrock = ""

	#size of the block
	bsize = tc.getblock(hash)
	bsizes = bsize['block']['blockSize']

	# number of transaction hashes in the block
	txs = tc.getblock(hash)
	ntxs = len(txs['block']['transactions'])

	#each tx hash in the block
	hashes = [x['hash'] for x in txs['block']['transactions']]

	# size of each tx
	hahsizes = [z['size'] for z in txs['block']['transactions']]

	#size of all the txs
	txsize = txs['block']
	txsizes = txsize['transactionsCumulativeSize']


	for hash in hashes:
		#tx extra hash
		teta = tc.gettransaction(hash)['tx']['extra']
		#Decoded version of tx_extra:
		try:
			deteta = bytes.fromhex(teta).decode('utf-8')
		except UnicodeDecodeError:
			print("deta oops")
			#deteta = "unable to decode, probably nothing in there"

	#size of tx extra		
	txes =  bsizes-txsizes

	# % of txs in the block
	txp = txsizes/bsizes * 100

	# % of tx_extra in the block
	txep = txes/bsizes * 100

	return {'height': height, 'hash': hash, 'orphan': orphan, 'reward': breward, 'bsizes': bsizes, 'blocktime': blocktime, 'ntxs': ntxs, 'hashes': hashes, 'hahsizes': hahsizes, 'txsizes': txsizes, 'teta': teta, 'deteta': deteta, 'txes': txes, 'txp': txp, 'txep': txep, 'pingrock': pingrock}


def prettyPrintStats(blockstats):
	msg = "```WE FOUND A NEW BLOCK!\n"
	msg += "\nHeight: {} \n".format(blockstats['height'])
	msg += "Hash: {} \n".format(blockstats['hash'])
	msg += "Orphan: {} \n".format(blockstats['orphan'])
	msg += "Reward: {} \n".format(blockstats['reward'])
	msg += "Size: {} \n".format(blockstats['bsizes'])
	msg += "Time took to make: {} \n".format(blockstats['blocktime'])

	msg += " \nNo. of txs in the block: {} \n".format(blockstats['ntxs'])
	msg += "Tx hashes in the block: {} \n".format(blockstats['hashes'])
	msg += "Size of each tx: {} \n".format(blockstats['hahsizes'])
	msg += "Size of all the txs: {} \n \n".format(blockstats['txsizes'])

	msg += "tx_extra hash: {} \n".format(blockstats['teta'])
	msg += "Decoded version of tx_extra: {} \n".format(blockstats['deteta'])
	msg += "Size of tx_extra: {} \n \n".format(blockstats['txes'])

	msg += "Percentage of txs in the block: {} % \n".format(blockstats['txp'])
	msg += "Percentage of tx_extra in the block: {} % ```".format(blockstats['txep'])

	#msg += blockstats['pingrock']

	return msg
	print(msg)


@client.event
async def on_ready():
	print("connected")
	height = tclbh['height']
	while True:
		#prettyPrintStats(getstats(nheight))	
		nheight = tc.getblockcount()['count']
		if height != nheight:
			prettyPrintStats(getstats(nheight))
			await client.send_message(discord.Object(id='459931714471460864'), prettyPrintStats(getstats(nheight)))
			print("val changed")
			print(nheight)
			print(height)
			height = nheight
			print(height)
		await asyncio.sleep(0.5)


client.run(token)
