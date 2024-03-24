




from .group import clique as clique_group

def clique ():
	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("sphene")
	def open_sphene ():	
		import pathlib
		from os.path import dirname, join, normpath
		this_folder_path = pathlib.Path (__file__).parent.resolve ()
		this_module_path = normpath (join (this_folder_path, ".."))

		import sphene
		sphene.start ({
			"extension": ".s.HTML",
			"directory": str (this_module_path),
			"relative path": str (this_module_path)
		})

		import time
		while True:
			time.sleep (1000)


	import click
	@click.command ("ETFs")
	def example_command ():	
		#
		#	rollercoaster/structures/ride/season_1/TV_technicals_shares/ETF/rise.proc.py
		#
	
		import rich
		import rollercoaster.clouds.TradingView.treasure.technicals as TV_treasure_tech
		symbols_indicators = TV_treasure_tech.scan_symbols (
			symbols = [
				symbol ("Cruise", "Travel"),
				symbol ("DFEN", "peace"),
			
			{
				"symbol": "JETS",
				"screener": "america",
				"exchange": "AMEX",
				
				"description": "airlines"
			},{
				"symbol": "KIE",
				"screener": "america",
				"exchange": "AMEX",
				
				"description": "insurance"
			},{
				"symbol": "MSOS",
				"screener": "america",
				"exchange": "AMEX",
				
				"description": "cannabis"
			},{
				"symbol": "PJP",
				"screener": "america",
				"exchange": "AMEX",
				
				"description": "pharmaceuticals"
			},{
				"symbol": "LABU",
				"screener": "america",
				"exchange": "AMEX",
				
				"descriptions": "biotech x3"
			},{
				"symbol": "VOO",
				"screener": "america",
				"exchange": "AMEX",
				
				"descriptions": ""
			}]
		)

		rich.print_json (data = symbols_indicators)

		TV_treasure_tech.print_symbols_table (symbols_indicators)

	group.add_command (example_command)
	group.add_command (open_sphene)

	group.add_command (clique_group ())
	group ()




#
