import os.path
import os
import datetime
import re

#TODO: Description file for 'neat' 'design' etc.
#TODO: Date created. This indicates i have to store some metadata about the file.
#TODO: Should be some notion of order, so that index can be ordered generally.

"""

You make files of the form [somename]1, [somename]2, etc. You also make a file just called [somename].

The file [somename] contains a (typically) one line description of the rest of the similarly named files. It is used in the index page to describe them.

The files like [somename]1 contain HEADING: followed by lines of text. HEADING is, for example, the title, or the body. The skeleton file is rendered as a template, with {{ HEADING }} being replaced with the lines of text. 
"""

# Constants

INDEX = "index.html" # Name of the index file
SKELETON = "skeleton.html" # Name of the skeleton file
ENTRY_DIR = "entries/" # Where are the entries?
OUTPUT_DIR = "" # Where to output the entries?

# Utility functions

def get_all_types(directory):
	""" Finds all words such that word1 exists in the current directory. """
	types = []
	files = os.listdir(directory)

	for file in files:
		if re.match(r'^[a-zA-Z0-9]+1$', file):
			types.append(file[:-1])

	return types

def file_of_type(type, num):
	return "%s%d" % (type, num)

def is_keyword(line):
	""" is the line passed in a keyword line? """
	return re.match(r'^[A-Z]+:', line)

def get_section(line):
	""" 'NAME:\n' -> 'NAME' """

	return line[:-2]

def render_template(template, sections):
	"""Renders an incredibly simple template format found in TEMPLATE, replacing each {{ KEY }} 
	with sections[KEY]."""

	# Add in a DATE section (generate it ourselves) if we haven't hardcoded one.
	if "DATE" not in sections:
		sections["DATE"] = datetime.datetime.now().strftime("%A, %B %d %Y")
	
	# Special case section: Don't show twitter message. 
	# This might not actually be best abstracted as a section.
	if "NOTWITTER" in sections:
		# Remove twitter message.
		template = template.replace('You should follow me on twitter <a href="http://twitter.com/thedayturns">here.</a>', '')
		del sections["NOTWITTER"]

	# Replace each templatized section in the skeleton with its contents.
	for section in sections:
	  template = template.replace("{{ %s }}" % section, sections[section])
	
	return template

# The big function

def process_files(type):
	""" Creates each file of type TYPE. Returns a list of tuples of the form (created_file, title). """
	built_files = []
	paragraphed_sections = ["BODY"]
	result = "".join([line for line in open(SKELETON)])
	num = 1

	# Check each file until one doesn't exist. design1, design2...
	while os.path.exists(ENTRY_DIR + file_of_type(type, num)):
		# TODO: TOP is a hack just for the index. Remove eventually.
		sections = { "TOP" : "" } #Each section of the file.
		current_section = ""
		paragraphed = False #Should we surround each para in <p> tags?
		result_file = file_of_type(type, num) + ".html" #Where we're writing to.

		# Scan the file.
		lines = [line for line in open(ENTRY_DIR + file_of_type(type, num))]
		for line in lines:
			if is_keyword(line):
				# Close the final paragraph tag if necessary.
				if paragraphed: sections[current_section] += "</p>"

				# If it's a keyword, add it to the dictionary
				current_section = get_section(line)
				sections[current_section] = ""
				paragraphed = current_section in paragraphed_sections

				if paragraphed: sections[current_section] += "<p>"
			else:
				# Otherwise, add it to the current section.
				sections[current_section] += line

				if line == "\n" and paragraphed: sections[current_section] += "</p> <p>"


		sections["POSTTYPE"] = type

		result = render_template(result, sections)

		# Result now contains the full HTML.

		# Remove the old one, if necessary.
		if os.path.exists(OUTPUT_DIR + result_file):
			os.unlink(result_file)

		output = open(OUTPUT_DIR + result_file, 'w')
		output.write(result)
		output.close()

		built_files.append((result_file, sections["TITLE"]))

		num += 1
	
	return built_files

def generate_index_chunk(files, type):
	""" Generate one of the lists on the index. """
	body = "" #section of the index
	desc = "".join([l for l in open(ENTRY_DIR + type)]) #description of this type of file

	body += "<p> %s </p>" % (desc)
	body += "<ol reversed>"

	files = ["<li><a href='%s'>%s</a>" % (f[0], f[1]) for f in files]

	body += "\n".join(files)
	body += "</ol> <p> </p>"

	return body

def get_index_sections(body):
	""" Build sections of index for templatizing. """
	sections = {}

	sections = {}
	sections["TOP"] = """
			Thoughts.
      <ol reversed> <!-- super sexy html5 -->
        <li><a href="post2.html"> Be direct. </a> (Under construction)
        <li><a href="post1.html"> Are you a technical person? </a>
      </ol>"""
	sections["BODY"] = body
	sections["POSTTYPE"] = "index"
	sections["TITLE"] = "johnfn's blog"
	sections["FOOTER"] = "Nothing to see here. Move along, citizen."
	sections["NOTWITTER"] = True

	return sections


def generate_all_files():
	body = ""
	#Generate the index page
	for type in get_all_types(ENTRY_DIR):
		files_created = process_files(type)
		body += generate_index_chunk(files_created, type)
	
	sections = get_index_sections(body)

	index = render_template("\n".join([l for l in open("skeleton.html")]), sections)

	if os.path.exists(INDEX):
		os.unlink(INDEX)
	
	index_file = open(INDEX, 'w')
	index_file.write(index)

# I can't imagine when this wouldn't be the case...
if __name__ == "__main__": 
	generate_all_files()
