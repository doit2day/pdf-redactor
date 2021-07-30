#;encoding=utf-8
# Example file to redact Social Security Numbers from the
# text layer of a PDF and to demonstrate metadata filtering.

import re
from datetime import datetime

import pdf_redactor

## Set options.

options = pdf_redactor.RedactorOptions()

options.metadata_filters = {
	# Perform some field filtering --- turn the Title into uppercase.
	"Title": [lambda value : value.upper()],

	# Set some values, overriding any value present in the PDF.
	"Producer": [lambda value : "mwilliams@hotsprings.org"],
	"CreationDate": [lambda value : datetime.utcnow()],

	# Clear all other fields.
	"DEFAULT": [lambda value : None],
}

# Clear any XMP metadata, if present.
options.xmp_filters = [lambda xml : None]

# Redact things that look like social security numbers, replacing the
# text with X's.
options.content_filters = [
	# First convert all dash-like characters to dashes.
	(
		re.compile(u"[−–—~‐]"),
		lambda m : "-"
	),
	# Redact things that look like phonenumbers, replacing the
	# text with Z's.
	(	
		re.compile(r"(?:\d{1}\s)?\(?(\d{3})\)?-?\s?(\d{3})-?\s?(\d{4})"),
		lambda m : "(XXX)XXX-XXXX"
	),
	# Redact things that look like IPs, replacing the
	# text with P's.
	(	
		re.compile(r"\b(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))"),
		lambda m : "XXX.XXX.XXX.XXX"
	),
	# Redact things that look like url addresses, replacing the
	# text with LL's. not working, comment out and move on
	#(
#		re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"),
#		lambda m : "LLLLLLLLLLLLLLLLLLLLLLLLLLLL"
#	),	
	# Redact things that look like email addresses, replacing the
	# text with Y's.
	(
		re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"),
		lambda m : "XXXXXXXXXXXXXXXXXXXX"
	),
	# Then do an actual SSL regex.
	# See https://github.com/opendata/SSN-Redaction for why this regex is complicated.
	(
		re.compile(r"(?<!\d)(?!666|000|9\d{2})([OoIli0-9]{3})([\s-]?)(?!00)([OoIli0-9]{2})\2(?!0{4})([OoIli0-9]{4})(?!\d)"),
		lambda m : "XXX-XX-XXXX"
	),
	# Content filter that runs on the text comment annotation body.
	(
		re.compile(r"comment!"),
		lambda m : "annotation?"
	),
]

# Filter the link target URI.
options.link_filters = [
	lambda href, annotation : "https://www.google.com" 
]

# Perform the redaction using PDF on standard input and writing to standard output.
print (options)
pdf_redactor.redactor(options)
