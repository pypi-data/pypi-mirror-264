

'''
	#
	#	change
	#
	import crowns.climate as crowns_climate
	crowns_climate.change ("treasuries", {
		"path": treasuries_path
	})
	
	crowns_climate.change ("mongo", {
		"directory": ""
	})
'''


'''
	#
	#	find
	#
	import crowns.climate as crowns_climate
	mongo_climate = crowns_climate.find ("mongo")
'''

'''

'''

import copy

climate = {
	"mongo": {
		"directory": "",
		"connection": {
			"host": "localhost",
			"port": "27017"
		},
		"connection": "mongodb://localhost:27017/",
		"DB_name": 'safety',
		"passes": {
			"collection": "passes",
			"GridFS_zips": 'zips',
			"GridFS_zips_files": 'zips.files'
		}
	}	
}


'''
	import climate
	mongo = climate.connect ()
'''
from pymongo import MongoClient
import gridfs
def connect ():
	edited_config = find ("edited_config")
	
	nodes = edited_config ["trends"] ["nodes"]
	node_1 = nodes [0]
	
	host = node_1 ["host"]
	port = node_1 ["port"]

	mongo = MongoClient (f'mongodb://{ host }:{ port }/')
	
	return mongo;
	
def link ():
	return connect () ["safety"] ["passes"]


'''
	import climate
	GridFS = climate.link_FS ()
'''
def link_FS ():
	the_connection = connect ();
	DB = the_connection ["safety"]
	
	return gridfs.GridFS (DB)

def change (field, plant):
	#global CLIMATE;
	climate [ field ] = plant


def find (field):
	#print ("climate:", climate)

	return copy.deepcopy (climate) [ field ]