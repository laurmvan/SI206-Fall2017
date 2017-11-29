import os
import json
import facebook
from argparse import ArgumentParser

#Name: Lauren Van Vlierbergen
def get_parser():
	parser = ArgumentParser()
	parser.add_argument('--page') #in terminal run python3 word_cloud.py --page tigerstylecodeacademy
	return parser

if __name__ == '__main__':
	parser = get_parser()
	args = parser.parse_args()

	token = os.environ.get('EAACEdEose0cBANSniNZBcuKkpz0nx27bdp9LMtZBtZBNGMTtewH51rzbkxThZAZAmPEAj6k4gQSzjJAxC2EATwFZCsDufXyO2INmVIpuqG3ZBU5Mx2bAQ7gx2B82muTjRHMz6x5I2gf1LZCfD2kvdz8TRKcqg2RQqvhYCqWvqouraKtF0ZBBM2Q0Xkx63LFEZBrUNCL2VVnZBYX3wZDZD') #assigned token to a variable
	fields = ['id',
	'name',
	'about',
	'likes',
	'website',
	'link',]

	fields = ','.join(fields)

	graph = facebook.GraphAPI(token)
	page = graph.get_object(args.page, fields=fields)

	print(json.dumps(page, indent=4))