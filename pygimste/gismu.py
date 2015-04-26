# 2-clause BSD license
"""
Copyright (c) 2014, Andrew Browne <dersaidin@dersaidin.net>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project.
"""

# Morphology utilities
class Morph:
    def isCorV(ch):
        CONSONANTS = ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'x', 'z']
        VOWELS = ['a', 'e', 'i', 'o', 'u']
        if ch.lower() in CONSONANTS:
            return 'c'
        if ch.lower() in VOWELS:
            return 'v'
        if ch.lower() is 'y':
            # sort of a consonant
            return 'y'
        if ch is '\'':
            return '\''
        if ch is ',':
            return ','
        if ch is '.':
            return '.'
        # character is not in lojban word
        return '#'

    def getCVstring(str):
        cvString = ''
        for l in str:
            cvString += Morph.isCorV(l)
        return cvString

class YamlParseException(Exception):
    def __init__(self, exc, msg, line=0, col=0):
        self.exc = exc
        self.message = msg
        self.line = line
        self.col = col

class GismuValidationException(Exception):
    def __init__(self, gismu, message):
        self.gismu = gismu
        self.message = message

class GismuExampleTranslation:
    def __init__(self, lang, text):
        self.lang = lang
        self.text = text

    def getLang(self):
        return self.lang

    def getText(self):
        return self.text

class GismuExample:
    def __init__(self, jboText):
        self.jbo = jboText
        # Not a map, because one lang could have multile variant translations
        self.translations = []

    def addTranslation(self, lang, text):
        t = GismuExampleTranslation(lang, text)
        self.translations.append(t)

    def getLojbanText(self):
        return self.jbo

    def getTranslations(self):
        return self.translations

class GismuDefinition:
    def __init__(self, lang):
        self.lang = lang
        self.placeStructure = None
        self.notes = []
        self.glosses = []

    def getLang(self):
        return self.lang

    def setPlace(self, place):
        self.placeStructure = place

    def addGlosses(self, glosses):
        self.glosses.extend(glosses)

    def addNotes(self, notes):
        self.notes.extend(notes)

class Gismu:
    def __init__(self, gismu):
        # The gismu itself
        self.gismu = gismu

        # Is this gismu experimental
        self.experimental = False

        # The yaml text representing this gismu
        self.textYaml = None

        # A string representing the consonant/vowel pattern in the gismu. Morphology requires 'cvccv' or 'ccvcv'.
        self.gismuCV = Morph.getCVstring(self.gismu)

        # A list of rafsi associated with this gismu
        self.rafsi = []

        self.examples = []
        self.definitions = {}


        # A list of all possible valid rafsi forms. Not all of these are used.
        # Only access this via getPossibleRafsi().
        # None => not cached.
        self._rafsiForms = None

    def __lt__(self, other):
        return self.gismu < other.gismu
    def __le__(self, other):
        return self.gismu <= other.gismu
    def __eq__(self, other):
        return self.gismu == other.gismu
    def __ge__(self, other):
        return self.gismu >= other.gismu
    def __gt__(self, other):
        return self.gismu > other.gismu
    def __ne__(self, other):
        return self.gismu != other.gismu
    def __hash__(self):
        return hash(self.gismu)

    def __str__(self):
        result = self.gismu
        if self.experimental:
            result += ' [experimental]'
        return result

    def setExperimental(self, experi):
        self.experimental = experi

    def get(self):
        return self.gismu

    def setTextYaml(self, text):
        self.textYaml = text

    def addRafsi(self, rafsi):
        self.rafsi.append(rafsi)

    # Returns a list of rafsi associated with this gismu
    def getRafsi(self):
        return self.rafsi

    # Returns a list of all valid rafsi forms.
    # This must be is a superset of the rafsi associated with this gismu.
    # Not all possible valid forms are associated with this gismu.
    def getPossibleRafsi(self):
        if self._rafsiForms is None:
            g = self.gismu
            # CLL 4.6 - the 5-letter-rafsi, and the 4-letter-rafsi
            forms = [g, g[0:4]]
            if self.gismuCV == 'cvccv':
                # CLL 4.6 - valid short rafsi forms for cvccv
                forms.extend([
                (g[0] + g[1] + g[2]),
                (g[0] + g[1] + g[3]),
                (g[0] + g[1] + '\'' + g[4]),
                (g[0] + g[1] + g[4]),
                (g[2] + g[3] + g[4]),
                (g[0] + g[2] + g[1])])
            elif self.gismuCV == 'ccvcv':
                # CLL 4.6 - valid short rafsi forms for ccvcv
                forms.extend([
                (g[0] + g[2] + g[3]),
                (g[1] + g[2] + g[3]),
                (g[0] + g[2] + '\'' + g[4]),
                (g[0] + g[2] + g[4]),
                (g[1] + g[2] + '\'' + g[4]),
                (g[1] + g[2] + g[4]),
                (g[0] + g[1] + g[2])])
            else:
                raise GismuValidationException(self.gismu, "gismu form is invalid: %s" % (self.gismuCV))
            self._rafsiForms = forms
        return self._rafsiForms

    # Return variations on the gismu form that cannot also be gismu because they are too similar
    def getSimilarForms(self):
        SIMILAR_CONSONANT = {
            'b': ['p', 'v'],
            'c': ['j', 's'],
            'd': ['t'],
            'f': ['p', 'v'],
            'g': ['k', 'x'],
            'j': ['c', 'z'],
            'k': ['g', 'x'],
            'l': ['r'],
            'm': ['n'],
            'n': ['m'],
            'p': ['b', 'f'],
            'r': ['l'],
            's': ['c', 'z'],
            't': ['d'],
            'v': ['b', 'f'],
            'x': ['g', 'k'],
            'z': ['j', 's'],
                }

        # CLL 4.14 - conflicting gismu: too similar
        result = []
        for i in range(0, len(self.gismu)):
            origLetter = self.gismu[i]
            replacements = SIMILAR_CONSONANT.get(origLetter, [])
            for r in replacements:
                similarForm = self.gismu[:i] + r + self.gismu[i+1:]
                # Results are tuple of (similar form, letter index, original letter, new letter)
                result.append((similarForm, i, origLetter, r))
        return result


    def addExample(self, example):
        self.examples.append(example)

    def addDefinition(self, definition):
        lang = definition.getLang()
        if lang not in self.definitions.keys():
            self.definitions[lang] = []
        self.definitions[lang].append(definition)

    def getDefinitions(self):
        return self.definitions

    def validateForms(self):
        # CLL 4.4 - always have five letters
        if len(self.gismu) != 5:
            raise GismuValidationException(self.gismu, "gismu must always have five letters")

        # CLL 4.4 - start with a consonant and end with a single vowel
        # CLL 4.4 - always contain exactly one consonant pair
        if self.gismuCV not in ['ccvcv', 'cvccv']:
            raise GismuValidationException(self.gismu, "gismu form is invalid: %s" % (self.gismuCV))

        shortRafsi = self.getPossibleRafsi()
        for r in self.rafsi:
            if r not in shortRafsi:
                raise GismuValidationException(self.gismu, "rasfi form is invalid: %s" % (r))


    def validateExamples(self):
        # TODO: check examples are well formed
        pass

    def validateDefinitions(self):
        # TODO: check definitions are well formed
        pass

    def validate(self):
        self.validateForms()
        self.validateExamples()
        self.validateDefinitions()

def yaml2Gismu(gismu, text):
    import yaml
    y = None
    try:
        y = yaml.load(text)
    except yaml.YAMLError as exc:
        line = 0
        col = 0
        if hasattr(exc, 'problem_mark'):
            mark = exc.problem_mark
            print("Error position: (%s:%s)" % (mark.line+1, mark.column+1))
            line = mark.line+1
            col = mark.column+1
        raise YamlParseException(exc, str(exc), line, col)
    if y is None:
        return None

    result = Gismu(gismu)

    if y['word'] != gismu:
        raise YamlParseException(None, "gismu word does not match")


    rafsiData = y['rafsi']
    if rafsiData == ['No rafsi.']:
        pass
    else:
        for r in rafsiData:
            result.addRafsi(r)

    for ex in y['examples']:
        result.addExample(ex)

    for lang,v in y['definitions'].items():
        gd = GismuDefinition(lang)
        gd.setPlace(v['place structure'])
        gd.addGlosses(v['glosses'])
        gd.addNotes(v['notes'])
        result.addDefinition(gd)

    result.validate()
    result.setTextYaml(text)
    return result

def Gismu2yaml(g):
    if g.getTextYaml():
        return g.getTextYaml()

    import yaml
    try:
        t = yaml.dump(g)
        return t
    except yaml.YAMLError as exc:
        pass
    return None

