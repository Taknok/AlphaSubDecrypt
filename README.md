# AlphaSubDecrypt
Simple script to decrypt alpha substitution cypher. Try to break the subs, if can't display all the possibilities.

## Install dependencies
Run `pip install -r dependency.txt` in the project folder.

## Users
The script with display the decrypted string if it successfully decrypted the substitution dictionary, **else** it will display the tree of possibilities. For exemple `ABCCDEFAG HEGDCFCB IJK FJL MNOC GKPPCGGQKHHI KFHJPRCS JKB PJSC DMNFR IJK` gives 
```
{'greetings': {'listener': {'you': {'now': {'have': {'successfully': {'unlocked': {'our': {'code': {'thank': {'you': {}}}}}}},
                                            'haze': {'successfully': {'unlocked': {'our': {'code': {'thank': {'you': {}}}}}}}}}}}}
```
The `common_dictionary_eng.txt` include all the most used words. Use this one for a fast result. `full_dictionary_eng.txt` contain all the english words, even the less used, it increase the compute time a lot.
You can select your own dictionnary by editing the `dictionaryPath`. Same for the output file with `outputPath`. By default the alphabet is **a to z**, you can edit it in `alpha`.

If there is any bugs, please report it in [issues](https://github.com/Taknok/AlphaSubDecrypt/issues) by explaining what is wrong and giving information on the situation (inputs, what is expected etc). You can also correct it and [PR](https://github.com/Taknok/AlphaSubDecrypt/pulls) your fix :)

Compliments (or questions) are allowed to [pg.developper.fr@gmail.com](mailto:pg.developper.fr@gmail.com) :smiley:

## TODO
* pass tree into an object
* create more units tests
* probably a lot more...
