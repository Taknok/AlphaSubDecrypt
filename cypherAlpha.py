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

class CypherAlpha:
	cracked = False;
	alphabet = "";
	alpha = {};

	def __init__(self, alphabet):
		self.cracked = False;
		self.alphabet = alphabet;
		self.alpha = self.getBlankCipherletterMapping();

	def getBlankCipherletterMapping(self):
	    # Returns a dictionary value that is a blank cipherletter mapping.
		blank = {};
		for char in self.alphabet:
			blank[char] = set(); # enpty set correspond to all possibilities

		return blank

	def select(self, encrypted, possibility):
		# asume that all the letters in word are correct and update the alpha in consequence
		i = 0;
		for cypherChar in encrypted:
			self.alpha[cypherChar] = {possibility[i]};

			i += 1;

		return self.checkUniqueLetter(); # check if there isn't conflict with other letters


	def intersect(self, newDict):
		# if a a letter have 2 arrays of possibility, intersect those 2 can reduce the number of possibility
		# exemple old['a'] : ['a', 'b', 'c'] and newDict['a'] : ['b', 'c', 'd']
		# the so a can only code b or c
		for cypherCharNew, charPossibilitiesNew in newDict.items():
			if charPossibilitiesNew == set():
				continue; #if all letter possible, pass to next iter

			if self.alpha[cypherCharNew] == set():
				self.alpha[cypherCharNew] = set(self.alphabet); #if empty set and new isn t empty, set all the alphabet possibilities to intersect

			tmp = self.alpha[cypherCharNew].intersection(charPossibilitiesNew);

			if tmp == set():
				raise ValueError("intersection null, letter code nothing : " + cypherCharNew);
			else:
				self.alpha[cypherCharNew] = tmp;

	def update(self, word):
		tmp = self.getBlankCipherletterMapping();
		for index, cypherChar in enumerate(word.encrypted):
			for possibility in word.possibilities:
				tmp[cypherChar].add(possibility[index]);

		self.intersect(tmp);

	def checkCrack(self):
		#if only 1 element per key, we have cracked the alphabet
		if len([x for x in [value for cypherChar, value in self.alpha.items() ] if len(x) != 1]) == 0:
			self.cracked = True;
		else :
			self.cracked = False;

		return self.cracked;

	def checkUniqueLetter(self):
		# check if a letter have only one possibility, so keep this possibility and remove from the other letters
		modified = False
		for cypherChar, charPossibilities in self.alpha.items():
			if len(charPossibilities) == 1:
				char = list(charPossibilities)[0];
				for otherCypherChar, otherCharPossibilities in self.alpha.items():
					if otherCypherChar != cypherChar:
						if otherCharPossibilities == set():
							self.alpha[otherCypherChar] = set(self.alphabet);

						if char in otherCharPossibilities:
							otherCharPossibilities.discard(char);
							if otherCharPossibilities == set(): # it mean that a letter have 2 code, it was unique in 2 crypted
								return False;

							modified = True;

		if modified:
			return self.checkUniqueLetter(); # rerun to check if we haven't unlock new unique letter (by removing 1 un 2 possi for ex)

		return True;






if __name__ == "__main__":
	print("Run tests");
	# create some tests here...