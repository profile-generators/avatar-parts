#! /usr/bin/python3

"""
extract_svg.py extracts relevant layers from an svg to individuals svgs
Copyright (C) 2021 Xavier "Crashoz" Launey

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom
import os, sys

# register useful namespaces
ns = {
	'': 'http://www.w3.org/2000/svg',
	'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
	'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
	'xlink': 'http://www.w3.org/1999/xlink',
	'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
	'cc': 'http://creativecommons.org/ns#',
	'dc': 'http://purl.org/dc/elements/1.1/'
}

for key, url in ns.items():
	ET.register_namespace(key, url)

def tag(k, v):
	"returns a tag/attribute scoped name"
	return f'{{{ns[k]}}}{v}'

# list of sodipodi attributes
sodipodiAttrs = [
	'absref', 'arg1', 'arg2', 'argument', 'cx', 'cy', 'docbase', 'docname',
	'end', 'expansion', 'insensitive', 'linespacing', 'modified', 'nodetypes',
	'nonprintable', 'open', 'original', 'r1', 'r2', 'radius', 'revolution',
	'role', 'rx', 'ry', 'sides', 'spiral', 'star', 'start', 't0', 'type',
	'version'
]

def	prepareNode(node, partName):
	"prepare svg node (layer)"

	# Make layer visible if it was hidden
	if 'style' in node.attrib:
		style = node.attrib['style']
		style = style.replace('display:none', '')
		if style == '':
			del node.attrib['style']
		else:
			node.attrib['style'] = style

	# Remove sodipodi stuff
	for name in sodipodiAttrs:
		attr = tag('sodipodi', name)
		elts = node.findall(f'.//*[@{attr}]')
		for elt in elts:
			del elt.attrib[attr]
		if attr in node.attrib:
			del node.attrib[attr]

	# Add a partName class to access it easily in the final svg
	node.attrib['class'] = partName


def makeSvg(node, author, keywords):
	"wrap an svg node in a standalone svg"

	# Svg root element
	root = ET.Element('svg')
	root.set('width', "124.19042mm")
	root.set('height', "124.19042mm")
	root.set('viewBox', "0 0 124.19042 124.19042")
	root.set('version', "1.1")
	root.set('id', "svg151")

	root.append(node)

	# Add metadata (license, author and keywords)
	metadata = ET.Element('metadata')
	rdf = ET.SubElement(metadata, tag('rdf', 'RDF'))
	work = ET.SubElement(rdf, tag('cc', 'Work'))
	creator = ET.SubElement(work, tag('dc', 'creator'))
	creatorAgent = ET.SubElement(creator, tag('cc', 'Agent'))
	creatorTitle = ET.SubElement(creatorAgent, tag('dc', 'title'))
	creatorTitle.text = author

	source = ET.SubElement(work, tag('dc', 'source'))
	source.text = 'https://github.com/profile-generators/avatar-parts'

	subject = ET.SubElement(work, tag('dc', 'subject'))
	bag = ET.SubElement(subject, tag('rdf', 'Bag'))
	for keyword in keywords:
		kw = ET.SubElement(bag, tag('rdf', 'li'))
		kw.text = keyword

	license = ET.SubElement(rdf, tag('cc', 'License'))
	license.set(tag('rdf', 'about'), 'http://creativecommons.org/licenses/by/4.0/')
	permits1 = ET.SubElement(license, tag('cc', 'permits'))
	permits1.set(tag('rdf', 'resource'), 'http://creativecommons.org/ns#Reproduction')
	permits2 = ET.SubElement(license, tag('cc', 'permits'))
	permits2.set(tag('rdf', 'resource'), 'http://creativecommons.org/ns#Distribution')
	requires1 = ET.SubElement(license, tag('cc', 'requires'))
	requires1.set(tag('rdf', 'resource'), 'http://creativecommons.org/ns#Notice')
	requires2 = ET.SubElement(license, tag('cc', 'requires'))
	requires2.set(tag('rdf', 'resource'), 'http://creativecommons.org/ns#Attribution')
	permits3 = ET.SubElement(license, tag('cc', 'permits'))
	permits3.set(tag('rdf', 'resource'), 'http://creativecommons.org/ns#DerivativeWorks')

	root.append(metadata)

	tree = ET.ElementTree(root)
	return tree

def processLayer(part, partid, number, g):
	# Ask for keywords
	print(f'extracting {part}_{partid} as {part}_{number:04d}.svg')
	response = input(f'enter keywords for {part}_{partid}: ')
	keywords = list(map(str.strip, response.split(',')))

	# prepare node
	prepareNode(g, part)

	# wrap and export
	svg = makeSvg(g, author, keywords)

	filename = f'{dst}/{part}/{part}_{number:04d}.svg'
	svg.write(filename, encoding='utf-8', xml_declaration=True)

	# prettify
	dom = xml.dom.minidom.parse(filename) 
	pretty_xml = dom.toprettyxml()

	lines = pretty_xml.splitlines()
	filtered = list(filter(lambda x: x.strip() != '', lines))
	output = '\n'.join(filtered)
	
	with open(filename, 'w') as f:
		f.write(output)

# list of accepted drawing parts
parts_list = [
	"backhair", "hair", "neck", "bust",
    "ears", "head", "eyes", "eyebrows",
    "nose", "mouth", "freckles", "glasses",
    "hat"
]

if len(sys.argv) < 3:
	print(f'usage: {sys.argv[0]} src_svg dst_folder author tags')
	print('src_svg		- an avatar with each part on a layer')
	print('dst_folder	- the root folder to export to')
	print('author		- will be stored as creator in metadata')
	sys.exit(1)

src = sys.argv[1]
dst = sys.argv[2]
author = sys.argv[3]

print(f'extracting parts from {src} to {dst}')
print(f'author: {author}')

if not os.path.exists(dst):
	os.makedirs(dst)

part_numbers = {}
for part in parts_list:
	partfolder = f'{dst}/{part}'
	if not os.path.exists(partfolder):
		os.makedirs(partfolder)

	number = -1
	for filename in os.listdir(partfolder):
		if not filename.endswith('.svg'):
			continue
		n = int(filename.split('_')[1].split('.')[0])
		number = max(number, n)
	part_numbers[part] = number + 1

# parse svg input
tree = ET.parse(src)
root = tree.getroot()
backhairs = []
for g in root.findall('{http://www.w3.org/2000/svg}g'):
	# select relevant layers
	label = g.attrib['{' + ns['inkscape'] + '}label']
	try:
		part, partid = label.split('_')
		if part not in parts_list or partid == 'box' or int(partid) == 0:
			continue
	except:
		continue

	# select next number available for filename
	if len(partid) != 4:
		if part == 'backhair':
			backhairs.append([part, partid, g])
			continue
		number = part_numbers[part]
		part_numbers[part] += 1
	else:
		# if partid is exactly 4 digits, override previous file
		number = int(partid)
		if number == 0:
			# skip template 0000 parts
			continue

	processLayer(part, partid, number, g)

for part, partid, g in backhairs:
	# ask which hair matched backhair

	response = input(f'enter matching hair id (4 digits) for {part}_{partid}: ')
	number = int(response)

	processLayer(part, partid, number, g)