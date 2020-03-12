from argparse import ArgumentParser
from DataLoader import DataLoader
from indicators.BollingerBand import BollingerBand
import datetime



if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('--stock_id', required=True, dest="stock_id")
	parser.add_argument('--start', default="", dest="start")
	parser.add_argument('--end', default="", dest="end")
	args = vars(parser.parse_args())

	if args['end'] == "":
		end_date = datetime.datetime.today()
	else:
		end_date = datetime.datetime.strptime(args['end'], '%d/%m/%Y')

	if args['start'] == "":
		start_date = end_date - datetime.timedelta(days = 100)
	else:
		start_date = datetime.datetime.strptime(args['start'], '%d/%m/%Y')

	stock_id = args['stock_id']
	end_date = end_date.strftime('%d/%m/%Y')
	start_date = start_date.strftime('%d/%m/%Y')

	data_loader = DataLoader(from_date=start_date, to_date=end_date, stock_list=stock_id)
	data = data_loader.load()

	bb = BollingerBand(data)
	bb.graph()
