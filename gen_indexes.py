#! /usr/bin/python3

"""
gen_indexes.py creates indexes for each part folder
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
import os

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

# list of accepted drawing parts
parts_list = [
	"backhair", "hair", "neck", "bust",
    "ears", "head", "eyes", "eyebrows",
    "nose", "mouth", "freckles", "glasses",
    "hat"
]

# minimal valid html5 template
template = """<!doctype html>
<html lang=en>
    <head>
        <meta charset=utf-8>
        <title>Eyes</title>
    </head>
    <body>
        <ul>
"""

parts_root = 'parts'
for part in parts_list:
    html = template

    counter = 0
    for filename in os.listdir(f'{parts_root}/{part}'):
        # skip non svg files
        if not filename.endswith('.svg'):
            continue
        counter += 1

        path = f'{parts_root}/{part}/{filename}'

        # parse svg input
        tree = ET.parse(path)
        root = tree.getroot()

        # extract tags and creator
        work = root.find(f'./{tag("", "metadata")}/rdf:RDF/cc:Work', ns)
        tagsList = work.findall('./dc:subject/rdf:Bag/rdf:li', ns)
        tags = list(map(lambda tag: tag.text, tagsList))
        creator = work.find('./dc:creator/cc:Agent/dc:title', ns).text

        html += f'            <li><a href="{filename}" data-tags="{" ".join(tags)}" data-creator="{creator}">{filename}</a></li>\n'

    html += '        </ul>\n    </body>\n</html>'

    # output index as index.html
    with open(f'{parts_root}/{part}/index.html', 'w') as f:
        f.write(html)

    # stats
    print(f'found {counter} {part} parts')