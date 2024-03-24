





import io
import zipfile
import pymongo
from gridfs import GridFS
import os
import shutil
import tempfile
'''
	from crowns.modules.freight.save import zip_and_save_to_gridfs
	zip_and_save_to_gridfs (
		directory_path = str (normpath (join (this_directory, 'folder'))), 
		metadata = None,
		
		GridFS_driver = None,
		GridFS_collection_files = None
	)
'''

def zip_shutil_temp (directory_path):
	with tempfile.TemporaryDirectory() as temp_dir:
		temp_zip_path = os.path.join (temp_dir, 'temp_zipfile.zip')

		shutil.make_archive (temp_zip_path[:-4], 'zip', directory_path)

		# Read the zip file into memory if needed
		with open (temp_zip_path, 'rb') as zip_file:
			#zip_data = zip_file.read ()
			zip_data = io.BytesIO (zip_file.read ())

	return zip_data

def zip_walk (directory_path):
	zip_buffer = io.BytesIO ()
	with zipfile.ZipFile (zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
		for root, dirs, files in os.walk (directory_path):
			for file in files:
				file_path = os.path.join (root, file)
				zipf.write (
					file_path, 
					os.path.relpath (file_path, directory_path)
				)
				
	zip_buffer.seek (0)

	return zip_buffer

def zip_and_save_to_gridfs (
	directory_path, 
	name = 'unnamed_archive',
	
	metadata = {},
	
	GridFS_collection = None,
	GridFS_collection_files = None
):
	zip_buffer = zip_shutil_temp (directory_path)

	id = GridFS_collection.put (
		zip_buffer, 
		filename = name + '.zip', 
		metadata = metadata
	)
	
	GridFS_collection_files.update_one (
		{'_id': id }, 
		{'$set': {'uploadDate': '' }}
	)
	
	print ("id:", id)
	return id;




