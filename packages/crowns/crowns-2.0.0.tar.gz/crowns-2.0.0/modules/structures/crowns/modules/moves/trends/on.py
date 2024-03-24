


import crowns.climate as crowns_climate
import law_dictionary
import subprocess
def the_process (params):
	law_dictionary.check (	
		allow_extra_fields = True,
		laws = {
			"DB_directory": {
				"required": True,
				"type": str
			},
			"port": {
				"required": True,
				"type": str
			},
			"CWD": {
				"required": True,
				"type": str
			}
		},
		dictionary = params
	)

	port = params ["port"]
	DB_directory = params ["DB_directory"]
	CWD = params ["CWD"]

	subprocess.run (
		f"mongod --dbpath '{ DB_directory }' --port '{ port }'", 
		shell = True, 
		check = True,
		cwd = CWD
	)

	return;

from multiprocessing import Process
import rich
def turn_on ():
	mongo_climate = crowns_climate.find ("mongo")
	edited_config = crowns_climate.find ("edited_config")

	rich.print_json (data = {
		"mongo": mongo_climate,
		"edited_config": edited_config
	})
	

	'''
	return;
	mongo_DB_directory = move ["mongo directory"]
	mongo_port = move ["mongo port"]
	'''

	nodes = edited_config ["trends"] ["nodes"]
	for node in nodes:
		mongo = Process (
			target = the_process,
			args = (),
			kwargs = {
				"params": {
					"CWD": edited_config ["CWD"], 
					"DB_directory": node ["data path"],
					"port": str (node ["port"])
				}
			}
		)
		mongo.start ()


	