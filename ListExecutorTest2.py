import unittest
from ListExecutor import ListExecutor
import ListSerializer
import ListDeserializer
from SlimError import SlimError
import sys

EXCEPTION_TAG = '__EXCEPTION__:'

def resultToMap(slimResults):
    m = {}
    for aResult in slimResults:
        resultList = aResult
        m[resultList[0]] = resultList[1]
    return m

class ListExecutorTest(unittest.TestCase):

    def setUp(self):
        self.executor = ListExecutor()
        self.statements = []
        self.expectedResults = []

    def testFoo(self):
        self.statements.append(["i1", "import", "xtest"])
	self.statements.append(["m1", "make", "testSlim", "TestSlim"])
        results = self.executor.execute(self.statements)
        print results

    def respondsWith(self, expected):
        self.expectedResults.extend(expected)
        result = self.executor.execute(self.statements)
        expectedMap = resultToMap(self.expectedResults)
        resultMap = resultToMap(result)
        self.assertEquals(expectedMap, resultMap)

    def assertExceptionReturned(self, message, returnTag):
        results = resultToMap(self.executor.execute(self.statements))
        result = results[returnTag]
        self.assert_(result.find(EXCEPTION_TAG) != -1)
        self.assert_(result.find(message) != -1)

if __name__ == '__main__':
    import sys
    unittest.main()

