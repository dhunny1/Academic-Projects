# Assignment PA2
# By Hunny Biguvu         Date:- 2/21/2026
# Description:- This program implements an N-gram language model that learns word sequences from one or more plain text files. It converts all text to lowercase, separates punctuation from words, detects sentence boundaries, and builds an n-gram model that does not cross those boundaries. Given values for n and m from the command line, the program generates m random sentences by probabilistically selecting words based on the learned model, continuing until a sentence-ending punctuation mark is reached.
# ---------------------------------------------------------

from sys import argv
from collections import Counter
import random, re

# ---------------------------------------------------------
# 1. Read command-line arguments
# ---------------------------------------------------------
# argv[1] → n value (size of n-gram)
# argv[2] → m value (number of sentences to generate)
# argv[3:6] → input text files
n_values = int(argv[1])
m_sentences = int(argv[2])
input_txt_files = [argv[3], argv[4], argv[5]]


raw_text = ""

# ---------------------------------------------------------
# 2. Read and normalize input text
# ---------------------------------------------------------
# All files are concatenated into a single corpus.
# Text is normalized to lowercase and cleaned so that
# sentence splitting and tokenization behave consistently.
for txt_file in input_txt_files:
    with open(txt_file, "r", encoding="utf-8") as f:
        raw_text += f.read()+" ".lower()

# replaces newline and tab with Whitespace
raw_text = raw_text.replace("\n", " ")
raw_text = raw_text.replace("\t", " ")

# Ensure commas are treated as separate tokens
raw_text = re.sub(r","," ,",raw_text)

# ---------------------------------------------------------
# 3. Sentence segmentation
# ---------------------------------------------------------
# We split on sentence-ending punctuation while preserving
# the delimiter using capturing groups in regex.
# This keeps punctuation as separate tokens (., !, ?, ;)

parts = re.split(r'([.!?;])', raw_text.lower())

sentences = []
for i in range(0, len(parts)-1, 2):
    sentence = parts[i].strip() + " " + parts[i+1]
    sentences.append(sentence.strip())


# ---------------------------------------------------------
# 4. Build the n-gram model (Markov mapping)
# ---------------------------------------------------------
# Data structure:
# - If n = 1:
#     mapping[word] = frequency count
#
# - If n > 1:
#     mapping[prefix_tuple] = list of possible next words
#
# This forms a probabilistic transition model where each
# prefix maps to possible continuations.

mapping ={}

if n_values <= 1:    
    # Unigram Model
    for sentence in sentences:
        words = sentence.split(" ")
        for wrd in words:
            mapping[wrd] = mapping.get(wrd,0)+1  
else:
    # N-gram Model
    for sentence in sentences:
        words = sentence.split(" ")
        
        for i in range(len(words)-n_values):

            prefix = tuple(words[i:i+n_values])
            next_word = words[i+n_values]         
            if prefix not in mapping: 
                mapping[prefix] = [] 
            mapping[prefix].append(next_word)

print("mapping", mapping)

# -------------Computing sentences ----------------------------------
# created an array to store the sentences

sentences  = []

count_sentence = 0

# loop to create m number of sentence
while count_sentence < m_sentences:
    combined_text = ""
    count_words = n_values
    
          
    if n_values <=1:
        # Unigram Model       
        while True: 
            word = random.choice(list(mapping.keys())) 
            combined_text += " " + word 
            if word in [".", "?", "!", ";"]:
                sentences.append(combined_text) 
                break
    else:         
        # N-gram  Model
        prefix = random.choice(list(mapping.keys()))
        combined_text = " ".join(prefix)
        
             
        while True:
            words = combined_text.split() 
            prefix = tuple(words[-n_values:]) 
            
            if prefix not in mapping or not mapping[prefix] or count_words > 100:
                sentences.append(combined_text.strip())
                break
            
            x = random.choice(mapping[prefix])
            combined_text += " " + x
            count_words += 1
            
            if x in [".", "?", "!",";"]:
                sentences.append(combined_text.strip())
                break
    count_sentence += 1
    print(f"sentence {count_sentence} finished") 

# ---------------------------------------------------------
# 6. Output Generated Sentences
# ---------------------------------------------------------

print("\nRandomly Generated Sentences:\n")
for i, sentence in enumerate(sentences, start=1):
    print(f"sentence {i}:\n")
    print(sentence + "\n")




