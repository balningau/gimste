#!/usr/bin/env python3

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

PATHS_GISMU_DIRS = ['gismu', 'experimental_gismu']
#PATHS_GISMU_DIRS = ['experimental_gismu']

from pygimste import gismu
from pygimste import visitors

def getFileList(args, realpath=True, skipRegex=None):
    import os
    initial = []
    if args:
        # Start from the arguments
        for a in args:
            initial.append(a)
    else:
        # If no arguments are given, start from the current working directory
        initial.append(os.getcwd())

    # Build up the list of files under the initial paths
    result = []
    for init in initial:
        if os.path.isdir(init):
            # Recurse into directories
            for root, dirs, files in os.walk(init):
                for f in files:
                    path = os.path.join(root,f)
                    result.append(path)
        else:
            result.append(init)

    # Realpath results
    if realpath:
        result = [os.path.realpath(x) for x in result]

    if skipRegex:
        import re
        skipRE = re.compile(skipRegex)
        result = [x for x in result if not skipRE.match(x) ]

    return sorted(result)


def gismuFromFilename(gismuFile):
    import os
    import re
    gfile = os.path.basename(gismuFile)
    g = re.match('(.....)\.yaml', gfile)
    if g:
        return g.group(1)
    return None

def experimentalFromFilename(gismuFile):
    import re
    return re.search('experimental_gismu', gismuFile) is not None

GISMU = {}

def load_gismu_file(gismuFile):
    f = open(gismuFile, 'r')
    gStr = gismuFromFilename(gismuFile)
    t = f.read()
    gObj = gismu.yaml2Gismu(gStr, t)
    if experimentalFromFilename(gismuFile):
        gObj.setExperimental(True)
    GISMU[gObj.get()] = gObj

def getGismuDirs():
    import os
    root = os.path.dirname(os.path.realpath(__file__))
    return [os.path.join(root, d) for d in PATHS_GISMU_DIRS]

class GismuValidationError:
    def __init__(self, msg, args):
        self.msg = msg
        self.gismu = args

    def print(self):
        gismulist = ', '.join([str(g) for g in self.gismu])
        print("%s: %s" % (self.msg, gismulist))

class Validator:
    def __init__(self):
        self.validationErrors = []

    def isValidator(self):
        return True

    def addValidationError(self, msg, *args):
        self.failed = True
        self.validationErrors.append(GismuValidationError(msg, args))

    def print(self):
        for ve in self.validationErrors:
            ve.print()

    def isValid(self):
        return len(self.validationErrors) == 0

class Metric:
    def __init__(self, name):
        self.name = name
        pass

    def isMetric(self):
        return True

    def print(self):
        print("---- %s: ----" % (self.name))
        self.printResults()

    def printResults(self):
        pass

class LanguageMetrics(visitors.CollectionVisitor, Metric):
    def __init__(self):
        name = "Language Counts Metrics"
        Metric.__init__(self, name)
        visitors.CollectionVisitor.__init__(self, name)
        self.gismuCount = 0
        self.definitionLang = {}

    def visitGismu(self, gismu):
        self.gismuCount += 1
        for lang, defs in gismu.getDefinitions().items():
            for d in defs:
                assert(lang == d.getLang())
                self.addDefLang(d.getLang())

    def addDefLang(self, lang):
        if lang in self.definitionLang.keys():
            self.definitionLang[lang] += 1
        else:
            self.definitionLang[lang] = 1

    def printResults(self):
        print("%d gismu" % (self.gismuCount))
        for k,v in self.definitionLang.items():
            print("%d defs in language %s" % (v, k))

class ConflictingPairValidator(visitors.CollectionVisitorPair, Validator):
    def __init__(self):
        name = "Conflicting Gismu Validator"
        Validator.__init__(self)
        visitors.CollectionVisitorPair.__init__(self, name)

    def visitGismuPair(self, a, b):
        # CLL 4.14 - conflicting gismu: too similar
        for aSimilar, aIdx, aLetter, rLetter in a.getSimilarForms():
            if b.get() == aSimilar:
                msg = "gismu too similar (differs by %s to %s)" % (aLetter, rLetter)
                self.addValidationError(msg, a, b)
                return
        for bSimilar, bIdx, bLetter, rLetter in b.getSimilarForms():
            if a.get() == bSimilar:
                msg = "gismu too similar (differs by %s to %s)" % (bLetter, rLetter)
                self.addValidationError(msg, a, b)
                return

class ConflictingRafsiValidator(visitors.CollectionVisitorPair, Validator):
    def __init__(self):
        name = "Conflicting Rafsi Validator"
        Validator.__init__(self)
        visitors.CollectionVisitorPair.__init__(self, name)

    def visitGismuPair(self, a, b):
        # check for gismu that have the same rafsi
        intersect = set(a.getRafsi()).intersection(b.getRafsi())
        if intersect:
            msg = "gismu have same rafsi (common rafsi: %s)" % (str(intersect))
            self.addValidationError(msg, a, b)


class FinalVowelValidator(visitors.CollectionVisitorAdjacent, Validator):
    def __init__(self):
        name = "Final Vowel Validator"
        Validator.__init__(self)
        visitors.CollectionVisitorAdjacent.__init__(self, name)

    def visitGismuAdjacent(self, a, b):
        # CLL 4.4 - no two gismu differ only in the final vowel (exception: broda, brode, brodi, brodo, and brodu)
        if a.get()[0:4] == b.get()[0:4]:
            if (a.get()[0:4] == "brod") and (b.get()[0:4] == "brod"):
                return
            msg = "gismu only differ in final vowel" % (str(a), str(b))
            self.addValidationError(msg, a, b)

class DuplicateValidator(visitors.CollectionVisitorDuplicates, Validator):
    def __init__(self):
        name = "Duplicate Validator"
        Validator.__init__(self)
        visitors.CollectionVisitorDuplicates.__init__(self, name)

    def visitGismuDuplicates(self, dupList):
        # CLL 4.14 - conflicting gismu: identical
        msg = "gismu duplicate form"
        self.addValidationError(msg, *dupList)

class LevenshteinPairMetric(visitors.CollectionVisitorPair, Metric):
    def __init__(self):
        name = "Smallest Levenshtein Distances Metric"
        Metric.__init__(self, name)
        visitors.CollectionVisitorPair.__init__(self, name)
        self.top = []

    @staticmethod
    def levenshtein1(seq1, seq2):
        # Implementation from https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
        oneago = None
        thisrow = range(1, len(seq2) + 1) + [0]
        for x in xrange(len(seq1)):
            twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
            for y in xrange(len(seq2)):
                delcost = oneago[y] + 1
                addcost = thisrow[y - 1] + 1
                subcost = oneago[y - 1] + (seq1[x] != seq2[y])
                thisrow[y] = min(delcost, addcost, subcost)
        return thisrow[len(seq2) - 1]

    @staticmethod
    def levenshtein2(seq1, seq2):
        # Implementation from http://rosettacode.org/wiki/Levenshtein_distance#Python
        from functools import lru_cache
        @lru_cache(maxsize=4095)
        def ld(s, t):
            if not s: return len(t)
            if not t: return len(s)
            if s[0] == t[0]: return ld(s[1:], t[1:])
            l1 = ld(s, t[1:])
            l2 = ld(s[1:], t)
            l3 = ld(s[1:], t[1:])
            return 1 + min(l1, l2, l3)
        return ld(seq1, seq2)

    @staticmethod
    def levenshtein(seq1, seq2):
        return LevenshteinPairMetric.levenshtein2(seq1, seq2)

    def visitGismuPair(self, a, b):
        import heapq
        ldist = LevenshteinPairMetric.levenshtein(a.get(), b.get())
        heapq.heappush(self.top, (ldist, (a, b)))

    def printResults(self):
        import heapq
        if True:
            # Print all results < 3
            while self.top:
                (s, (a,b)) = heapq.heappop(self.top)
                if s >= 3:
                    break
                print("%d\t%s to %s" % (s, str(a), str(b)))
        else:
            # Print top 32 results
            small = heapq.nsmallest(32, self.top)
            for (s, (a,b)) in small:
                print("%d\t%s to %s" % (s, str(a), str(b)))


def LoadGismu(gismu_dirs):
    countFail = 0
    countProcessed = 0
    for x in getFileList(gismu_dirs, skipRegex='.*\.md$'):
        countProcessed += 1
        try:
            load_gismu_file(x)
        except gismu.YamlParseException as exc:
            countFail += 1
            print(exc)
        except gismu.GismuValidationException as exc:
            countFail += 1
            print(exc)
        except Exception as exc:
            # Unknowon/unexpected
            raise exc
        if countProcessed % 100 == 0:
            print("...loaded %d" % (countProcessed))

    print("...loaded %d" % (countProcessed))
    print("%d failed to load" % (countFail))

    return countFail

def main():
    # Load Gismu
    gismu_dirs = getGismuDirs()
    countFail = LoadGismu(gismu_dirs)

    # Create visitors
    visitMan = visitors.CollectionVisitorManager()
    visitMan.addVisitor(ConflictingPairValidator())
    visitMan.addVisitor(ConflictingRafsiValidator())
    visitMan.addVisitor(FinalVowelValidator())
    visitMan.addVisitor(LanguageMetrics())
    #visitMan.addVisitor(LevenshteinPairMetric())

    # Run visitors
    visitMan.visit(GISMU)

    # Output Results
    validators = visitMan.getValidatorVisitors()
    hasInvalid = False in [v.isValid() for v in validators]
    print("==== Validation: ====")
    for v in validators:
        v.print()
    if hasInvalid:
        print("FAIL")
    else:
        print("PASS")

    metrics = visitMan.getMetricVisitors()
    print("==== Summary: ====")
    for m in metrics:
        m.print()

    # Exit with error code
    exitcode = 0
    if countFail:
        exitcode = exitcode | 1
    if hasInvalid:
        exitcode = exitcode | 2
    import sys
    sys.exit(exitcode)

if __name__ == "__main__":
    main()

