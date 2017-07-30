# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 21:37:48 2017

@author: pg

AlphaSubDecrypt
Copyright (C) 2017  pg.developper.fr@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import re;

class Word:
	index = 0;
	length = 0;
	encrypted =  "";
	possibilities = set();
	inside = {};
	outside = [];

	def __init__(self, length):
		self.length = length;
		self.inside = {};

	def updatePossibilitiesWithAlphabet(self, alpha):
		# remove the possibilities that aren't actually possible with the curent dictionary of substitution
		# alpha is the dictionary of substitution
		for cypherChar, charPossibilities in alpha.items():
			index = self.encrypted.find(cypherChar);
			if index != -1 and charPossibilities != set(): # if the cypher char is used in the cypher word, reduce the number of loop
				loopset = self.possibilities.copy();
				for wordPossibility in loopset:
					if wordPossibility[index] not in charPossibilities: #if the char of the poossible decrypted word isn't in the possibility of the alphabet, then remove the word
						self.possibilities.discard(wordPossibility);

	def insidePattern(self, alpha):
		# not used anymore since Dict implement this for all the dictionary
		# get the pattern inside a word
		for char in alpha:
			if self.encrypted.count(char) >= 2:
				self.inside[char] = [x.start() for x in re.finditer(char, self.encrypted)];

	def outsidePattern(self, wordList):
		# get the pattern of this word with all the word in the array given
		# wordList is the array of all the words after this one (including himself)
		self.outside = [];
		wordList.pop(0); # remove himself from the list

		for char in set(self.encrypted): # set exclude redundance
			for word in wordList:
				res = word.encrypted.find(char);
				if res != -1:
					# if 2 letter only need to match 1 letter from each word dthank to inside pattern
					self.outside.append( {"char" : char, "wordIndex" : word.index, "insidePos" :  self.encrypted.find(char), "outsidePos" : res } );
				else :
					self.outside.append({});

	def matchInside(self):
		# no used anymore, dict return now all word with same pattern
		# remove the possibilities that didn't match with the inside pattern
		for key, value in self.inside.items():
			for i in range(len(value) - 1): #if 2ocu 1 eq needed, 3 ocu 2 eq needed etc
				self.possibilities = set([x for x in self.possibilities if x[value[i]] == x[value[i+1]] ]);

	def matchOther(self, otherWord, pos1, pos2):
		# no used to... I think ...
		validated1 = set();
		validated2 = set();

		for word1 in self.possibilities:
			for word2 in otherWord.possibilities:
				if word1[pos1] == word2[pos2]:
					validated1.add(word1);
					validated2.add(word2);

		self.possibilities = validated1;
		return validated2;







if __name__ == "__main__":
	print("Run tests");
	# create some tests here...