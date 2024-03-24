

import rich

import crowns.climate as crowns_climate

def show ():
	mongo = crowns_climate.connect ()


	documents = mongo ['safety'] ['passes'].find ()

	# Iterate over the documents and print them
	data = []
	for document in documents:	
		data.append ({
			"_id": str (document ["_id"]),
			"legal": document ["legal"]
		})

	rich.print_json (data = data)