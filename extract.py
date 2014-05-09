import os, codecs

from lxml import etree

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

print "{} gismu found".format(len(gismu))

for valsi in gismu:
    word = valsi.get('word')
    rafsi = [rafsi.text for rafsi in valsi.xpath("rafsi")]
    _definition = valsi.xpath('definition')
    if _definition:
        definition = _definition[0].text
    else:
        definition = u'No definition available.'
    definition = definition.replace(u"$x_{1}$", u"x1")
    definition = definition.replace(u"$x_{2}$", u"x2")
    definition = definition.replace(u"$x_{3}$", u"x3")
    definition = definition.replace(u"$x_{4}$", u"x4")
    definition = definition.replace(u"$x_{5}$", u"x5")

    _notes = valsi.xpath('notes')
    if _notes:
        notes = _notes[0].text
    else:
        notes = u'No notes available.'
    print "{} ({}) : {}".format(word, rafsi, definition)

    parent_path = os.path.join(EXPORT_PATH, word[0])

    if not os.path.isdir(parent_path):
        os.makedirs(parent_path)

    with codecs.open(os.path.join(parent_path, "{}.txt".format(word)), 'w', 'utf-8') as fobj:
        fobj.write(u"""
Word: {}
Rafsi: {}
Definition: {}

Notes:
{}

Examples:
""".format(word, u", ".join(rafsi), definition, notes))
