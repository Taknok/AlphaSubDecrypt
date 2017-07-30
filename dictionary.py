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


from unidecode import unidecode;

class Dict:
	content = "";
	patternDict = {};
	alphabet = [];

	def __init__(self, filename, alphabet):
		# Load the dict file, unidecode remove all
		# accents. Put all in lower case
		with open(filename, 'r') as content_file:
			self.content = unidecode(content_file.read().lower()).splitlines();

		self.patternDict = {};
		self.alphabet = alphabet;

	def preCalculate(self):
		# register all word from the dictionary into a pattern dictionary
		# with that we will get all words that match for a pattern
		for word in self.content:
			pattern = self.getPattern(word);
			self.registerPattern(pattern, word);

	def getPattern(self, word):
		# encrypt the word to get the pattern of it
		# asume that all chars in word are lowers
		pattern = "";
		charUsed = {};
		index = 0;
		for char in word:
			if char not in charUsed:
				charUsed[char] = index;
				index += 1;
			pattern += self.alphabet[charUsed[char]];

		return pattern;

	def registerPattern(self, pattern, word):
		# add the word to the pattern dictionary, create a new entry if new
		if pattern in self.patternDict:
			self.patternDict[pattern].append(word);
		else :
			self.patternDict[pattern] = [word];






if __name__ == '__main__':
	import string;

	alphabet = list(string.ascii_lowercase);

	dico = Dict("full_dictionary_eng.txt", alphabet);

	wordTest = "alphasubdecrypt";
	patternCheck = "abcdaefghijklcm";
	patternOut = dico.getPattern(wordTest);
	if patternCheck != patternOut:
		print("Error on getPattern, in : " + wordTest + " - out : "
			 + patternOut + " - check : " + patternCheck);
	else:
		print("Test getPattern : passed");

	dico.registerPattern(patternOut, wordTest);
	wordOut = dico.patternDict[dico.getPattern(wordTest)];
	if wordTest not in wordOut:
		print("Error on registerPattern, in : " + wordTest + " - out : "
			 + wordOut[0] + " - dict : " + str(dico.patternDict));
	else:
		print("Test registerPattern : passed");

	wordListTest = "Earth should be preserved";
	wordListTest = wordListTest.lower().split();

	dico.preCalculate();

	for word in wordListTest:
		out = dico.patternDict[dico.getPattern(word)];
		if word not in out:
			print("Error dict, with : " + word);
			break;
		else:
			print("Test dict : passed");