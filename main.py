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

from word import Word;
from cypherAlpha import CypherAlpha;
from dictionary import Dict
import string;
import pprint;
import copy;


"""
###############################################################################
									USER SECTION
###############################################################################
"""


message = "ABCCDEFAG HEGDCFCB IJK FJL MNOC GKPPCGGQKHHI KFHJPRCS JKB PJSC DMNFR IJK";

dictionaryPath = "./common_dictionary_eng.txt";
outputPath = "./out.txt";

alpha = list(string.ascii_lowercase); #a to z 26 chars in lower case, if need a bigger alphabet change this


"""
###############################################################################
			CODE : DO NOT TOUCH IF YOU DON'T KNOW WHAT YOU ARE DOING
###############################################################################
"""


def keepOnly(tree, level, possibilities):
	# keep only the possibilities given in a certain level of the tree of possibillities
	# tree is the tree of possibilities
	# level is an int indicating where to the change, start with 0
	# possibilities is a list of possibility to keep
	if level != 0: # if not at the good level, keep doing down in the tree
		for key, subTree in tree.items():
			tree[key] = keepOnly(subTree, level - 1, possibilities);
	else :
		keyToDel = set(); # cannot remove in the loop, due to err change size, so construct a set of TODO
		for key, value in tree.items():
			if key not in possibilities:
				keyToDel.add(key);

		for key in keyToDel:
			del tree[key];

	return tree; # return the tree update

def checkDepth(tree, depth):
	# check if each branches avec the good depth, else remove it
	# tree is the tree of possibilities
	# depth is an int indicated the normal depth of branches, start with 1
	if depth == 1 and tree != {}:
		return tree, True; # if we reach a leaf at good depth, all is ok

	keyToDel = set(); # can't remove in the loop, create a TODO list
	for key, subTree in tree.items():
		if subTree == {}: # if finished too early, we are not ok
			return tree, False;
		tree[key], ok = checkDepth(subTree, depth - 1);
		if not ok:
			keyToDel.add(key); #if not ok, add to TODO list

	for key in keyToDel:
		del tree[key];

	return tree, tree != {}; # if we deleted all key then false, keep del branch


def matchOutside(word, wordList):
	# construct the tree of possibilities with the pattern between words
	# word is ojbect word curently processed
	# wordList is the list of objects words after the word (1st parameter)
	if len(wordList[word.index:]) == 1:
		leaf = {}; # if we are at the end, no pattern with the next one (because there isn't)
		for possibility in word.possibilities:
			leaf[possibility] = {}; # leaf of tree of possibilities

		return wordList, leaf;

	tree = {};
	for possibility in word.possibilities:
		wordList, branch = matchOutside(wordList[word.index + 1], wordList); # construc the sub tree (branches)

		if branch == {}: # if no valid next word skip
			continue;

		tmpPossibilities = {};
		noPattern = True;
		patternWithNextWord = False;
		for pattern in word.outside: # check if possibilities match with the pattern shared with the next words
			if pattern != {}:
				if pattern['wordIndex'] == (word.index + 1):
					patternWithNextWord = True;

				if pattern["wordIndex"] not in tmpPossibilities: # if not there create it
					tmpPossibilities[pattern["wordIndex"]] = [];

				tmpPossibilities[pattern["wordIndex"]].append(
						set([x for x in wordList[pattern["wordIndex"]].possibilities
								   if possibility[pattern["insidePos"]] == x[pattern["outsidePos"]] ])
					);
				noPattern = False;

		# if no outside pattern add all possibilities
		if noPattern:
			tree[possibility] = {};
			for key, value in branch.items():
				tree[possibility][key] = value;

		elif tmpPossibilities != {}:
			# check if we have multiple pattern between 2 words and intersect those 2
			# for example "abbc" and "cabd" have a and b in common, only the intersect of the match from a and match from b is correct
			for key, value in tmpPossibilities.items():
				intersect = value[0];
				for i in range(len(value) - 1):
					intersect = intersect.intersection(value[i + 1]);

				tmpPossibilities[key] = {}; # reset
				tmpPossibilities[key] = intersect

			 # if at least 1 match in the next word (except if there isn't pattern with bnext word)
			if (word.index + 1) in tmpPossibilities or not patternWithNextWord:
				tree[possibility] = {} ;
				atLeastOneAdded = False;
				for key, possibilities in tmpPossibilities.items():
					branch = keepOnly(branch, (key - word.index - 1), possibilities); # remove the possibilities in subtree that didn't match with this word

				for key, item in branch.items():
					tree[possibility][key] = item;
					atLeastOneAdded = True;

				if not atLeastOneAdded:
					del tree[possibility];

	return wordList, tree;


def checkUniqueAttribution(tree, wordList, alpha, level):
	# check if in the tree of possibilities there isn't inconsistency with letter of alphabet
	# tree is the tree of possibilities
	# wordList is the full list of word objects
	# alpha is the dictionary of substitution
	# level, is the start level to check (recursively)
	if tree == {}:
		return tree, wordList, False; # no possibility at false because it's a leaf

	backupAlpha = copy.deepcopy(alpha);
	keyToDel = set(); # del list TODO
	for key, value in tree.items():
		valid = alpha.select(wordList[level].encrypted, key); # check if that this word is correct, will there be conflict ?
		if not valid:
			alpha = copy.deepcopy(backupAlpha);
			keyToDel.add(key);
			continue; # skip this tree

		tree[key], wordList, noNextPossibility = checkUniqueAttribution(value, wordList, alpha, level + 1);

		if noNextPossibility:
			keyToDel.add(key);

		alpha = copy.deepcopy(backupAlpha);

	for key in keyToDel:
		del tree[key];

	noPossibility = ( tree == {} ); # if se haven't possibility for next word it's a dead end

	return tree, wordList, noPossibility;

def translate(alpha, cryptedText):
	# translate a text with a dictionnary of substitution
	# alpha is a dictionary {'a' : {'b'}, 'b':{'c'}, ...}
	# cryptedText is a string
	decryptedText = "";
	for char in cryptedText:
		if char not in alpha:
			decryptedText += char; # for the space, ! etc
		else :
			decryptedText += list(alpha[char])[0];

	return decryptedText;

def main():
	cypherAlpha = CypherAlpha(alpha);

	dico = Dict(dictionaryPath, alpha);
	dico.preCalculate();
	print("Precalculs done");

	words = [];
	texts = message.lower().split();
	i = 0;
	for text in texts:
		words.append(Word(len(text)));
		words[-1].index = i; # -1 is for the last element of the list
		words[-1].encrypted = text;
		if not cypherAlpha.checkCrack():
			pattern = dico.getPattern(words[-1].encrypted);
			words[-1].possibilities = set(dico.patternDict[pattern]); # get all the words corresponding to the pattern
			cypherAlpha.update(words[-1]); # update the alphabet with the corresponding possibilities
			cypherAlpha.checkUniqueLetter(); # if 1 letter code for only 1 other, remove the letter from the other possibilities

		i += 1;

	print("Inside pattern done");
	if not cypherAlpha.checkCrack(): # if we haven't the alphabet, calcul the tree of possibilities
		for word in words:
			word.updatePossibilitiesWithAlphabet(cypherAlpha.alpha); # keep only the words that the cryped char correspond to a possibility in the alphabet

		i = 0;
		for word in words: # get the pattern between words
			word.outsidePattern(words[i:]);
			i += 1;

		words, tree = matchOutside(words[0], words); # reduce the possibilities with outside pattern and construct the tree of dependencies
		tree, words, rien = checkUniqueAttribution(tree, words, cypherAlpha, 0); # reduce possibilities by checking the alphabet
		tree, ok = checkDepth(tree, len(words)); # remove the branches where there is less words than in the crypted text

	if cypherAlpha.checkCrack():
		pprint.pprint(cypherAlpha.alpha);
		decrypt = translate(cypherAlpha.alpha, message.lower());
		print(decrypt);
	else :
		print("All possibilities : ");
		pprint.pprint(tree, width=1);


	# save the tree of possibilities
	f = open(outputPath, 'w');
	f.write(pprint.pformat(tree, width=1) );
	f.close();





if __name__ == "__main__":
	main();