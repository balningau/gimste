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

class VisitorBase:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def start(self):
        import datetime
        self.startTime = datetime.datetime.now()
        print("Running visitor %s ..." % (self.getName()), end="")

    def finish(self):
        import datetime
        self.finishTime = datetime.datetime.now()
        c = self.finishTime - self.startTime
        print(" %d ms" % (c.total_seconds() * 1000))

class CollectionVisitor(VisitorBase):
    def __init__(self, name):
        VisitorBase.__init__(self, name)

    def visitGismu(self, data):
        pass

class CollectionVisitorPair(VisitorBase):
    def __init__(self, name):
        VisitorBase.__init__(self, name)

    def visitGismuPair(self, a, b):
        pass

class CollectionVisitorAdjacent(VisitorBase):
    def __init__(self, name):
        VisitorBase.__init__(self, name)

    def visitGismuAdjacent(self, a, b):
        pass

class CollectionVisitorDuplicates(VisitorBase):
    def __init__(self, name):
        VisitorBase.__init__(self, name)

    def visitGismuDuplicates(self, dupList):
        pass

# Executes CollectionVisitor and CollectionVisitorPair on the collection
class CollectionVisitorManager:
    def __init__(self):
        self.visitors = []
        self.visitorsPairwise = []
        self.visitorsAdjacent = []
        self.visitorsDuplicates = []
        self.cacheClear()

    # Visitors

    def addVisitor(self, v):
        if hasattr(v, 'visitGismu'):
            self.visitors.append(v)
        if hasattr(v, 'visitGismuPair'):
            self.visitorsPairwise.append(v)
        if hasattr(v, 'visitGismuAdjacent'):
            self.visitorsAdjacent.append(v)
        if hasattr(v, 'visitGismuDuplicates'):
            self.visitorsDuplicates.append(v)

    def getVisitors(self):
        result = []
        result.extend(self.visitors)
        result.extend(self.visitorsPairwise)
        result.extend(self.visitorsAdjacent)
        result.extend(self.visitorsDuplicates)
        return result

    def getMetricVisitors(self):
        return [v for v in self.getVisitors() if hasattr(v, 'isMetric') and v.isMetric()]

    def getValidatorVisitors(self):
        return [v for v in self.getVisitors() if hasattr(v, 'isValidator') and v.isValidator()]

    # Cache

    def cacheClear(self):
        self.data = set()
        self.dataDuplicates = {}
        self.dataSorted = []

    def cacheCollection(self, main_gismu_list):
        self.cacheClear()
        for gismu,g in main_gismu_list.items():
            # Cache to find duplicates
            if g not in self.data:
                self.data.add(g)
            else:
                if gismu not in self.dataDuplicates.keys():
                    self.dataDuplicates[gismu] = []
                self.dataDuplicates[gismu].append(self.data.remove(gismu))
                self.dataDuplicates[gismu].append(g)

        # Get sorted list of gismu
        glist = []
        glist.extend(self.data)
        for k,v in self.dataDuplicates.items():
            glist.extend(v)
        self.dataSorted = sorted(glist)

    # Visiting

    def visit(self, main_gismu_list):
        self.cacheCollection(main_gismu_list)

        # Gismu visitors
        for check in self.visitors:
            check.start()
            for g in self.dataSorted:
                check.visitGismu(g)
            check.finish()

        # Duplicate Gismu visitors
        for check in self.visitorsDuplicates:
            check.start()
            for k,v in self.dataDuplicates.iteritems():
                assert(len(v) > 1)
                check.visitGismuDuplicates(v)
            check.finish()

        # Adjacent pairwise visitors
        for check in self.visitorsAdjacent:
            check.start()
            for i in range(1, len(self.dataSorted)):
                a = self.dataSorted[i-1]
                b = self.dataSorted[i]
                check.visitGismuAdjacent(a, b)
            check.finish()

        # Pairwise visitors
        for check in self.visitorsPairwise:
            check.start()
            for i in range(0, len(self.dataSorted)):
                for j in range(i+1, len(self.dataSorted)):
                    a = self.dataSorted[i]
                    b = self.dataSorted[j]
                    check.visitGismuPair(a,b)
            check.finish()


