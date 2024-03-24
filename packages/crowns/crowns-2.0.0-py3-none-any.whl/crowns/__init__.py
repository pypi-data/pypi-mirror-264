
import pathlib
import inspect
import os
from os.path import dirname, join, normpath

from crowns.clique import clique
import crowns.config.scan as config_scan
import crowns.climate as crowns_climate

print ("crowns @:", pathlib.Path (__file__).parent.resolve ())

configured = False

import rich

def is_configured ():
	return configured

def start ():
	crowns_config = config_scan.start ()
	if (crowns_config == False): 
		return;

	'''
	rich.print_json (data = {
		"crowns_config": crowns_config
	})
	'''
	
	'''
	crowns_climate.change ("mongo", {
		"directory": ""
	})
	'''
	
	'''
		get the absolute paths
	'''
	'''
	crowns_config ["configuration"] ["treasuries"] ["path"] = (
		normpath (join (
			crowns_config ["directory_path"], 
			crowns_config ["configuration"] ["treasuries"] ["path"]
		))
	)
	'''
	
	
	'''
		paths:
			trends
				mongo_data_1
	
	
		mongo:
			safety
				passes
				zips
				zips.files
	'''
	trends_path = normpath (join (
		crowns_config ["directory_path"], 
		crowns_config ["configuration"] ["trends"] ["path"]
	))
	edited_config = {
		"mints": {
			"path": normpath (join (
				crowns_config ["directory_path"], 
				crowns_config ["configuration"] ["mints"] ["path"]
			))
		},
		"trends": {
			"path": trends_path,
			
			"nodes": [{
				"host": "localhost",
				"port": "27017",
				"data path": normpath (join (
					trends_path, 
					"mongo_data_1"
				))
			}]
		},
		"CWD": crowns_config ["directory_path"]
	}
	
	'''
	config_template = {
		
	}
	'''
	
	rich.print_json (data = {
		"edited_config": edited_config
	})

	
	crowns_climate.change ("edited_config", edited_config)
	

	#print ('crowns configuration', crowns_config.configuration)

	'''
		Add the changed version of the basal config
		to the climate.
	'''
	'''
	config = crowns_config ["configuration"];
	for field in config: 
		crowns_climate.change (field, config [field])
	'''
	
	configured = True
	
	print ()
