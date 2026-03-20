"""
Name: Hunny Biguvu
Date: March 13, 2026
Assignment: Word Sense Disambiguation using a Decision List

Problem Description:
This program performs word sense disambiguation for the word "line".
The program determines whether the word "line" refers to a "phone"
sense or a "product" sense based on surrounding context words.
It learns patterns from the training data and then predicts the
correct sense for instances in the test data.

Program Input:
The program takes three command line arguments:
1. A training file
2. A testing file
3. A model output file

then saves everything we print into the my-line-answers.txt

Example usage:
python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt

s
Example output:
line-test-nw.line-1 phone
line-test-nw.line-2 product

Algorithm Description:
1. Read the training and testing files.
2. Extract each instance and its context sentences from the training data.
3. Count the occurrences of words for each sense (phone or product).
4. Ignore common stopwords when counting features.
5. Compute log-likelihood scores for each feature word.
6. Build a decision list sorted by strongest features.
7. Save the decision list model to the specified model file.
8. For each test instance, check context words against the decision list.
9. Predict the sense based on the first matching feature.
"""

# Import required libraries for command line arguments, text processing,
# counting features, and mathematical calculations
from sys import argv
from collections import Counter
import re
import math

# Get file names from command line arguments
line_train = argv[1]
line_test = argv[2]
model_txt = argv[3]

# Variables used to store text data, instance information, and word counts
train_txt = ""
test_txt = ""

instances= {}
phone={}
product={}
decision_list =[]
predicted_list=[]



# List of common words to ignore during feature extraction
stoplist = ["the","in","to","and","of","are","a","it","for","this","is","his","her","on","those","these","that","into","like","what","which","<head>","lines","</head>","line","other","my", ""]

# changing the list to set for a faster lookup
stopwords = set(stoplist)



# Read training and test files and store the lowercase text in variables
with open(line_train,"r", encoding="utf-8") as f:
    train_txt += f.read().lower()

with open(line_test,"r", encoding="utf-8") as f:
    test_txt += f.read().lower()


# This function counts the words that appear in the context sentences.
# It ignores stopwords and updates the dictionary with the word counts
# for either the phone sense or the product sense.
def mapping(context,target_dict):
    words = []
    for sentence in context:       
        for w in sentence:    
            w = w.strip('",.!?:;()')
            if w not in stopwords:
                words.append(w)
    counts = Counter(words)
    for w, c in counts.items():
        target_dict[w] = target_dict.get(w, 0) + c

# This function calculates the log-likelihood value for a feature.
# It compares how often a word appears in the phone sense vs product sense.
# Laplace smoothing (+1) is used so there are no zero probabilities.
def compute_llh(phone_count,product_count):
    phone_count+=1
    product_count +=1
    total = phone_count + product_count

    prob_Phone = phone_count / total
    prob_Product = product_count / total

    return abs(math.log2(prob_Phone/prob_Product))



# This function builds the decision list model.
# It combines the word counts from phone and product dictionaries,
# calculates the log-likelihood score for each word,
# and sorts the features from strongest to weakest.
# The model is also saved to a file called "my-model.txt".
def build_model(phone,product):
    feature_counts = {}

    all_words = set(phone.keys()) | set(product.keys())

    for w in all_words:
        phone_count = phone.get(w,0)
        product_count = product.get(w,0)
        
        feature_counts[w]={
            "phone": phone_count,
            "product": product_count
        }
    

    decision_model = []
    for w, counts in feature_counts.items():
        # llh is log.likehood
        llh = compute_llh(counts["phone"],counts["product"])

        predict = "phone" if counts["phone"] > counts["product"] else "product"
        decision_model.append((w,llh,predict))

    # Sort the decision list by log-likelihood score (strongest features first)
    decision_model.sort(key=lambda x: x[1], reverse=True)

    with open(model_txt, "w") as f:
        for feature, llr, predicts in decision_model:
            f.write(f"FEATURE: {feature}\n")
            f.write(f"LOG-LIKELIHOOD: {llr}\n")
            f.write(f"PREDICTS: {predicts}\n\n")

    return decision_model


# This function predicts the sense of the word "line".
# It checks the words in the context against the decision list.
# The first matching feature determines whether the sense is phone or product.
def predict_sense(words):
    for feature, llh, predict in decision_list:
        if feature in words:
            return predict
    return "phone"


# This function trains the model using the training text.
# It extracts each instance, reads the sense label (phone or product),
# and collects the context sentences.
# The word counts are updated and then the decision list model is built.
def trainModel(text):
    txt_instances = re.findall(r"<instance.*?>.*?</instance>", text, flags=re.DOTALL)

    for instance in txt_instances:
        id = (re.search(r'id="(.*?)"',instance).group(1))
        senseId = (re.search(r'senseid="(.*?)"',instance).group(1))
        context = re.findall(r'<s>(.*?)</s>',instance, flags=re.DOTALL )
            
        instances[id]={
            "sense": senseId,
            "context":[sentence.strip().split() for sentence in context]
        }

    # Count word occurrences for each sense
    for id in instances:
        sense=(instances[id]["sense"])
        context = instances[id]["context"]
        if sense == "phone":
            mapping(context,phone)
        else:
            mapping(context,product)

    return build_model(phone,product)



# This function tests the trained model on the test data.
# It extracts the context words from each instance
# and uses the decision list to predict the correct sense.
# The predicted sense for each instance id is printed.
def testModel(text):
    txt_instances = re.findall(r"<instance.*?>.*?</instance>", text, flags=re.DOTALL)
    instances = {}

    for instance in txt_instances:
        id = (re.search(r'id="(.*?)"',instance).group(1))
        context = re.findall(r'<s>(.*?)</s>',instance, flags=re.DOTALL )
            
        instances[id]={
            "context":[sentence.strip().split() for sentence in context]
        }

    for id in instances:
        context = instances[id]["context"]
        words = [w for sentence in context for w in sentence]

        sense = predict_sense(words)

        print(id,sense)


# Run the training function to build the decision list model,
# then run the testing function to predict senses on the test data
decision_list = trainModel(train_txt)
testModel(test_txt)



    