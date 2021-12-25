## Spell_Checker
## Homework 2
### Preet Khowaja and Surabhi Trivedi

import re
import nltk.corpus
import numpy as np
import random

text = nltk.corpus.gutenberg.raw("austen-sense.txt")

corrupted = ""

p_edit = 0.04

for char in text:
    if re.fullmatch("[a-zA-Z]", char) is not None and np.random.rand() < p_edit:
        edit = np.random.randint(3)
        if edit == 0:
            # insert
            if 97 <= ord(char) < 123:
                corrupted += chr(97 + np.random.randint(26))
            elif 65 <= ord(char) < 91:
                corrupted += chr(65 + np.random.randint(26))
            corrupted += char
        elif edit == 1:
            # delete
            pass
        else:
            # substitute
            if 97 <= ord(char) < 123:
                corrupted += chr(97 + np.random.randint(26))
            elif 65 <= ord(char) < 91:
                corrupted += chr(65 + np.random.randint(26))
    else:
        corrupted += char

with open("austen-sense-corrupted.txt", "w") as stream:
    stream.write(corrupted)

## Homework Assignment
# Min Edit Distance function 
def min_ed_dist(target, source):
  target = '#' + target
  source = '#' + source
  target = [k for k in target]
  source = [k for k in source]
  sol = np.zeros((len(source), len(target)))

  sol[0] = [j for j in range(len(target))]
  sol[:,0] = [j for j in range(len(source))]

  if target[1] != source[1]:
    sol[1,1] = 1

  for c in range(1, len(target)):
    for r in range(1, len(source)):
      if target[c] != source[r]:
        sol[r,c] = min(sol[r-1, c], sol[r, c-1], sol[r-1,c-1]) + 1
      else:
        sol[r,c] = sol[r-1, c-1]
  return int(sol[r,c])


# converting dict.txt to a dictionary list 
with open('dict.txt') as d:
    dict_list = []
    for line in d:
        nw = line.strip() 
        dict_list.append(nw)
        dict_list.append(nw.capitalize())
        

# Finding typos and corrects 
pattern = r"\w+[-]?\w+|\w+|\d+"

def spell_check(input_str):
    word_list = input_str.split()
    for x in word_list:
        ed_dist = []
        L = []
        matcher = re.findall(pattern, x)[0]
        if matcher.lower() not in dict_list and not matcher.isdigit():
            for dict_words in dict_list:
                distance = min_ed_dist(dict_words, re.findall(pattern, x)[0])
                ed_dist.append(distance)
                L.append(dict_words)
                pass
            i = ed_dist.index(min(ed_dist))
            replace_word = L[i]
            if x[-1] in [',', '.', '?', '!', ':', ';', ')']:
                word_list[word_list.index(x)] = replace_word + x[-1]
            elif x[0] in ['(']:
                word_list[word_list.index(x)] = x[0] + replace_word
            else:
                word_list[word_list.index(x)] = replace_word
    final_str = ''
    for j in word_list: 
        final_str = final_str + j + ' '
    return(final_str)

# Testing on a sub-string of Sense and Sensibility
print(spell_check(corrupted[:900]))
       
