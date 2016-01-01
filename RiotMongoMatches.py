# Script por UnforgivenCL (Guillermo Lobos Parada)
# memolob@gmail.com


import sys
import json
import os.path
import time
import argparse
from riotwatcher import RiotWatcher
from pymongo import MongoClient






def readApiKey():
	try:
		file = open('api_key.txt', 'r')
		return file.read()				
	except Exception:
		print "Error, no existe archivo api_key.txt"



def initChallengerTierList(server):
	key = readApiKey()
	if os.path.isfile('data.json') == False:
		with open('data.json', 'w') as f:
			w = RiotWatcher(key, server)
			challenger_tier = w.get_challenger(server)
			json.dump(challenger_tier, f)
			print 'CACHE NOT FOUND, CREATING JSON..'
			data = challenger_tier			
			return data
	else:
	    with open('data.json') as data_file:
	      print 'CACHE FOUND, LOADING...'
	      data = json.load(data_file)
	      return data	


def extractSummonersId(server):

	info = initChallengerTierList(server)
	lista = []

	#Create List with Summoners ID
	for ids in info['entries']:
		lista.append(ids['playerOrTeamId'])
	return lista
	



def getSummonerMatchList(summonerId, server, queue, season):
	key = readApiKey()
	w = RiotWatcher(key, server)
	try:
		info = w.get_match_list(summonerId, server, champion_ids=None, #Aqui obtiene las partidas jugadasde un jugador (son muchas)
                          ranked_queues=queue,
                          season=season)
	except Exception:
		pass

	return info['matches']



def getMatch(matchList, server):
	key = readApiKey()
	w = RiotWatcher(key, server)
	try:
		match = w.get_match(matchList['matchId'], server)
	except Exception:
		pass
	
	return match


def doTheJobForAll(summoners, server, queue, season, ipmongo):
	try:
		for s in summoners:
			info = getSummonerMatchList(s, server, queue, season)
			time.sleep(3) # Time Wait de 3 segundos
			for m in info:
				dataMatch = getMatch(m, server)
				storeInMongo(dataMatch, ipmongo)
				print "Match Obtenido, esperando 3 segundos"
				time.sleep(3) # Time Wait de 3 segundos
	except Exception:
		print "VERIFICA TU API_KEY (api_key.txt)"
		print "Recuerda borrar data.json si cambias de servidor o no podra ejecutarse."
		pass			


def doTheJobForOne(summonerId, server, queue, season):
	try:
		info = getSummonerMatchList(summonerId, server, queue, season)
		for m in info:
			dataMatch = getMatch(m, server)
			storeInMongo(dataMatch)
			print "Match Obtenido, esperando 3 segundos"
			time.sleep(3)
	except Exception as e:
		print "VERIFICA TU API_KEY (api_key.txt)"
		print "Error en los parametros, quizas el jugador no pertence al servidor, o no cumple los parametros"
		pass			


def storeInMongo(match, ipmongo):
	try:
		client = MongoClient(ipmongo, 27017)
		db = client.matchs
		matchs = db.matches_stored
		matchs.insert_one(match).inserted_id
	except Exception as e:
		print e



def main():

	parser = argparse.ArgumentParser(
        usage="python RiotMongoMatches.py -t [target] -s [servidor-lol] -q [cola] -a [season] -i [ipMongo]",
        add_help=False,        
	)

	parser.add_argument("-h", "--help", action="help", help="Mostrar Mensaje de Ayuda")
	parser.add_argument("-t", dest='target', help="Id de Summoner a extraer matches, 0 para los Challenger")
	parser.add_argument("-s", dest='server', help="Servidor (na,las,lan,euw) ")
	parser.add_argument("-q", dest='queue', help="Cola (RANKED_SOLO_5x5, NORMAL) ")
	parser.add_argument("-a", dest='season', help="SEASON (SEASON2014, SEASON2015) ")
	parser.add_argument("-i", dest='ipmongo', help="Ip Servidor Mongo ")
	args = parser.parse_args()

	#summoners = extractSummonersId()
	#doTheJobForAll(summoners)
	if args.target == '0' and args.server and args.queue and args.season and args.ipmongo:
		try:
			summoners = extractSummonersId(args.server)
			doTheJobForAll(summoners, args.server, args.queue, args.season, args.ipmongo)

		except Exception as e:
			print "Error en los parametros."
			print "VERIFICA TU API_KEY (api_key.txt)"
			print e
			pass	

	elif args.target and args.server and args.queue and args.season and args.ipmongo:
		try:
			doTheJobForOne(args.target, args.server, args.queue, args.season, args.ipmongo)
		except Exception as e:
			print e
			pass	


	else:
		parser.print_help()	




if __name__ == '__main__':
    main()	