


import crowns.modules.moves.trends_to_mint as trends_to_mint

import crowns.modules.moves.trends.find as find_trend
import crowns.modules.moves.trends.forget as forget_trend
import crowns.modules.moves.trends.on as on
import crowns.modules.moves.trends.show as show_trends

import click

def add ():
	
	@click.group ("trends")
	def group ():
		pass


	@group.command ("turn-on")
	def turn_on ():
		on.turn_on ()
	
	@group.command ("turn-off")
	def turn_off ():
		print ('not yet implemented')

	@group.command ("find")
	@click.option ('--name', required = True)
	def search (name):
		find_trend.find (name = name)
	
	@group.command ("list")
	def list_ ():
		show_trends.show ()
	
	@group.command ("show")
	def show ():
		show_trends.show ()
	
	@group.command ("forget")
	@click.option ('--id', required = True)
	@click.option ('--delete-if-file-gone', is_flag = True, default = False)
	def forget (id, delete_if_file_gone):		
		forget_trend.forget (
			id = id,
			delete_if_file_gone = delete_if_file_gone
		)
		
		

	'''
		crowns trends to-minds --name folder
	'''
	@group.command ("to-minds")
	@click.option ('--name', required = True)
	@click.option ('--id', required = False, default = '')
	def retrieve_command (name, id):
		trends_to_mint.start (
			name = name,
			id = id
		)

	return group




#



