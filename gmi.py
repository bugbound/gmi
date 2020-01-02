#!/bin/python
"""Usage: 
	gmi.py <filepath> [--https]
	gmi.py -h | --help
	gmi.py --version
	
Options:
	-h --help                  show this
	--version                  shows the current version
	
Arguments
	<filepath>		Path to file containing hosts to check
	--https			Use https instead of http
"""
from docopt import docopt
import requests
import re
from urllib3.exceptions import InsecureRequestWarning


def run_scan(hosts, use_https):
	for host in hosts:
		if use_https:
			print("https://%s"%host)
		else:
			print("http://%s"%host)
		requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) 
		s = requests.Session()
		for hostToTry in hosts:
			urlToTry = ''
			
			if(use_https):
				urlToTry = "https://%s/"%hostToTry
			else:
				urlToTry = "http://%s/"%hostToTry
			
			response_code= 'Not Set'
			page_title = "Not Set"
			#first_100_chars = "Not Set"
			try:
				http_response = s.get(urlToTry, headers={'Host': host}, verify=False, allow_redirects=False)
				response_code = http_response.status_code
				page_title = extract_page_title(http_response.text)
				if response_code >= 300 and response_code < 400:
					page_title = "%s -> %s"%(page_title, http_response.headers['location'])
				
				#first_100_chars = http_response.text[0:100]
			except:
				response_code = -1
				page_title = "Error with connection"
				pass
			
			print("\t%s = %d (%s)"%(hostToTry, response_code, page_title))
		print('')

	
	print('All done son.')
	print('')

def extract_page_title(http_response_text):
	title = "Title Not Found"
	try:
		title = re.search('<title>(.*?)</title', http_response_text, re.IGNORECASE).group(1)
	except:
		pass
	return title
		

def readfile(filepath):
	hosts = []
	with open(filepath) as fp:
		hosts = fp.read().splitlines() 
		
	return hosts
	


if __name__ == "__main__":
	arguments = docopt(__doc__, version='gmi 0.1 BETA')
	use_https = arguments['--https']
	hosts_file = arguments['<filepath>']
	hosts = readfile(hosts_file)
	run_scan(hosts, use_https)



