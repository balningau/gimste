import os, codecs, re

import rtyaml as yaml
from lxml import etree
from collections import OrderedDict

IMPORT_FILE = 'xml-export.html'
EXPORT_PATH = 'gismu'

try:
    fileobj = codecs.open(IMPORT_FILE, 'r', 'utf-8')
except IOError as e:
    print e
    print "Failed to open import file:", IMPORT_FILE

try:
    tree = etree.parse(fileobj)
except Exception as e:
    print e
    print "Failed to parse import file."


gismu = tree.xpath("//valsi[@type='gismu']")
expgismu = tree.xpath("//valsi[@type='experimental gismu']")

print "{} gismu found ({} official, {} experimental)".format(len(gismu) + len(expgismu), len(gismu), len(expgismu))

for valsi in gismu:
    word = valsi.get('word')
    rafsi = [rafsi.text for rafsi in valsi.xpath("rafsi")]
    _definition = valsi.xpath('definition')
    if _definition:
        definition = _definition[0].text
    else:
        definition = u'No definition available.'
    definition = re.sub(r'\$x_\{?(\d+)\}?\$', r'x\1', definition)

    _notes = valsi.xpath('notes')
    if _notes:
        notes = _notes[0].text
    else:
        notes = u'No notes available.'
    print "{} ({}) : {}".format(word, rafsi, definition)

    parent_path = os.path.join(EXPORT_PATH, word[0])

    if not os.path.isdir(parent_path):
        os.makedirs(parent_path)

    with codecs.open(os.path.join(parent_path, "{}.yaml".format(word)), 'w', 'utf-8') as fobj:
        d = OrderedDict()
        d['Word'] = word
        d['Rafsi'] = ', '.join(rafsi)
        d['Definition'] = definition
        d['Notes'] = notes
        d['Examples'] = 'None'
        yaml.dump(d, fobj)

