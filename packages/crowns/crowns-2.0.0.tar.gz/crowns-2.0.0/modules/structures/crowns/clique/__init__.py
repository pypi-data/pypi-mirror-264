




#from .group import clique as clique_group
from crowns.mints import clique as mints_group
from crowns.treasuries import clique as treasuries_group

import crowns.modules.moves.save as save





import crowns

import click

import crowns.clique.group.trends as group_trends

def clique ():
	'''
		This configures the crowns module.
	'''
	crowns.start ()

	@click.group ()
	def group ():
		pass
	
	@group.command ("help")
	def help ():
		import pathlib
		from os.path import dirname, join, normpath
		this_directory = pathlib.Path (__file__).parent.resolve ()
		this_module = str (normpath (join (this_directory, "..")))

		import somatic
		somatic.start ({
			"directory": this_module,
			"extension": ".s.HTML",
			"relative path": this_module
		})
		
		import time
		while True:
			time.sleep (1)

	
	
		

	


	group.add_command (mints_group.clique ())
	#group.add_command (treasuries_group.clique ())
	
	group.add_command (group_trends.add ())
	
	group ()




#
