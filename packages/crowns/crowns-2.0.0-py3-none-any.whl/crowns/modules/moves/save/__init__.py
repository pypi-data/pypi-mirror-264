



'''
	import crowns.modules.moves.save as save
	save.save ()
'''

import pymongo
from gridfs import GridFS
import pathlib
from os.path import dirname, join, normpath
import os

import crowns.climate as crowns_climate
from .modules.zip_and_save_to_gridfs import zip_and_save_to_gridfs

def save (
	name = ''
):
	climate_mongo = crowns_climate.find ("mongo")

	DB_name = climate_mongo ["DB_name"]
	DB_collection_zips = climate_mongo ["passes"] ['GridFS_zips']
	DB_collection_zips_files = climate_mongo ["passes"] ['GridFS_zips_files']
	mongo_connection = climate_mongo ["connection"]
	
	client = pymongo.MongoClient (mongo_connection)
	DB = client [ DB_name ]
	GridFS_collection = GridFS (DB, collection = DB_collection_zips)
	GridFS_collection_files = DB [ DB_collection_zips_files ]

	id = zip_and_save_to_gridfs (
		name = name,
		directory_path = str (normpath (join (os.getcwd (), name))), 
		
		metadata = None,
		
		GridFS_collection = GridFS_collection,
		GridFS_collection_files = GridFS_collection_files
	)

	proceeds = crowns_climate.link ().insert_one ({
		"legal": {
			"name": name,
			"tags": [],
			"locks": [] 
		},
		"zip": id
	})

	'''
		Figure out is inserted.
	'''
	found = crowns_climate.link ().find_one({ "_id": proceeds.inserted_id })
	assert (
		str (found ["_id"]) == str (proceeds.inserted_id)
	), [ str (found ["_id"]), str (proceeds.inserted_id)]
	
