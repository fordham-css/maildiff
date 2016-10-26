#! /usr/bin/python

# Nicholas DiBari

# Script to find email accounts in MailChimp account list
# that are not in the OrgSync accounts list
# Supports CSV Parsing for now

# -IMPORTANT- #
# Must pass the MailChimp file as first argument
# Must pass Orgsync file as second argument

# TODO: Extend file implementation
# 	-> xlsx

import csv
import re
import sys

# PRE: File name of CSV file to parse
# POST: Sorted list of Email Address attributes
def CSVParser(to_parse):
	results = []

	with open(to_parse) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			results.append(row['Email Address'])
	results.sort()

	return results

# PRE: Two lists of Email Addresses to search
# POST: One list of email addresses that are in MailChimp
#		and not in OrgSync
def GetTargets(Chimp, Org):
	targets = []

	for email in Chimp:
		if email not in Org:
			domain = re.search('@[\w.]+', email)
			if domain.group(0) == '@fordham.edu':
				targets.append(email)
	targets.sort()

	return targets

def main():
	if len(sys.argv) != 3:
		print('ERROR Usage ./main.py <MailChimp.csv> <OrgSync.csv>')
		exit(1)

	chimpFile = sys.argv[1]
	orgFile = sys.argv[2]

	print('Opened {0} to read..'.format(sys.argv[1]))
	print('Opened {0} to read..'.format(sys.argv[2]))

	MailChimp = CSVParser(chimpFile)
	OrgSync = CSVParser(orgFile)

	emails = GetTargets(MailChimp, OrgSync)

	with open('emails.txt', 'w') as f:
		# Write contents of target emails to text file
		for email in emails:
			f.write('{0}\n'.format(email))

	print('Done! Output file is emails.txt')

if __name__ == '__main__':
	main()
