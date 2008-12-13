'''
    This file is part of Python-Slim.

    Python-Slim is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Python-Slim is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Python-Slim.  If not, see <http://www.gnu.org/licenses/>.
'''

def deserialize(serialized):
    return ListDeserializer(serialized).deserialize();

'''
 Uses Slim Serialization.  See ListSerializer for details.  Will deserialize lists of lists recursively.
'''

class ListDeserializer(object):
    def __init__(self, serialized):
        self.serialized = serialized
        self.result = []
        self.index = 0

    def deserialize(self):
        try:
            self.checkSerializedStringIsValid()
            return self.deserializeString()
        except Exception, e:
            raise SlimSyntaxError(e)

    def checkSerializedStringIsValid(self):
        if self.serialized == None:
            raise SlimSyntaxError("Can't deserialize null")
        elif len(self.serialized) == 0:
            raise SlimSyntaxError("Can't deserialize empty string")

    def deserializeString(self):
        self.checkForOpenBracket()
        result = self.deserializeList()
        self.checkForClosedBracket()
        return result
    
    def checkForClosedBracket(self):
        if (not self.charsLeft() or self.getChar() != ']'):
            raise SlimSyntaxError("Serialized list has no ending ]");

    def charsLeft(self):
        return self.index < len(self.serialized)

    def checkForOpenBracket(self):
        if self.getChar() != '[':
            raise SlimSyntaxError("Serialized list has no starting [")

    def deserializeList(self):

        itemCount = self.getLength()
        for i in range(0, itemCount):
            self.deserializeItem()
        
        return self.result

    def deserializeItem(self):
        itemLength = self.getLength()
        item = self.getString(itemLength)
        try:
            sublist = deserialize(item)
            self.result.append(sublist)
        except SlimSyntaxError, e:
            self.result.append(item)

    def getString(self, length):
        result = self.serialized[self.index:self.index + length]
        self.index += length
        self.checkForColon("String")
        return result

    def checkForColon(self, itemType):
        if self.getChar() != ':':
            raise SlimSyntaxError(itemType + " in serialized list not terminated by colon.")

    def getChar(self):
        c = self.serialized[self.index]
        self.index += 1
        return c

    def getLength(self):
        return self.tryGetLength()
        try:
            return self.tryGetLength()
        except NumberFormatException, e:
            raise SyntaxError(e)

    def tryGetLength(self):
        lengthSize = 6
        lengthString = self.serialized[self.index:self.index + lengthSize]
        length = int(lengthString)
        self.index += lengthSize;
        self.checkForColon("Length")
        return length

class SlimSyntaxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

