import datetime
from argparse import ArgumentParser
from DataLoader import DataLoader
from indicators.BollingerBand import BollingerBand
from config import DATE_FORMAT_STRING


if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('--stock_id', required=True, dest="stock_id")
	parser.add_argument('--start', default="", dest="start")
	parser.add_argument('--end', default="", dest="end")
	parser.add_argument('--delta', default="", dest="delta")
	parser.add_argument('--save_graph', dest="save_graph", action='store_true')
	parser.add_argument('--show_nontrading', dest="show_nontrading", action='store_true')
	args = vars(parser.parse_args())

	if args['delta'] == "":
		delta = 365
	else:
		delta = int(args['delta'])

	if args['end'] == "":
		end_date = datetime.datetime.today()
	else:
		end_date = datetime.datetime.strptime(args['end'], DATE_FORMAT_STRING)

	if args['start'] == "":
		start_date = end_date - datetime.timedelta(days=delta)
	else:
		start_date = datetime.datetime.strptime(args['start'], DATE_FORMAT_STRING)

	stock_id = args['stock_id']
	end_date = end_date.strftime(DATE_FORMAT_STRING)
	start_date = start_date.strftime(DATE_FORMAT_STRING)

	data_loader = DataLoader(from_date=start_date, to_date=end_date, stock_list=stock_id)
	data = data_loader.load()

	bb = BollingerBand(stock_id, data)
	bb.graph(save_graph=args['save_graph'], show_nontrading=args['show_nontrading'])
