# Programming Assignment: ELIZA-Style Chatbot
# Author: Hunny Biguvu
# Date: 01/29/2026
# Class: CMSC 437-001 Intro To NLP

# Description: This program implements a simple ELIZA-style chatbot that enages with the user in a conversational manner.

# Example Input/Output:
    # [ELIZA] Hello my name is Eliza. I am a psychotherapist. What is your name?
    # [User] my name is Bridget. 
    # [ELIZA] Nice to meet you, Bridget. How can I help you today?
    # [Bridget] I want to rule the world
    # [ELIZA] How long have you felt that you want to rule the world?
    # [Bridget] i think i crave power
    # [ELIZA] What makes you think you crave power?
    # [Bridget] because my sister feels sad
    # [ELIZA] How does it affect you when she feels that way?
    # [Bridget] idk bye
    # [ELIZA] Thank you for talking with me today.


# Algotithm:
# 1. Greet the user and ask for their name.
# 2. Continuously prompt the user for input until an exit command is given.
# 3. Analyze the user's input to identify if the input contains specific verbs or family mentions.
# 4. Generate appropriate responses based on the identified verbs or family mentions.
# 5. If no specific verbs or family mentions are found, ask the user to elaborate.
# 6. End the conversation when the user inputs an exit command.
# 7. This program also uses trigger words to handle inappropriate language.

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////---------- Code Starts here ----------/////////////////////////////////////////////////////////////////
import re

# mapping for converting pronouns
def replace_pronouns(word):
    pronoun_mapping = {
        "i": "you",
        "me": "you",
        "my": "your",
        "am": "are",
        "you": "I",
        "your": "my",
        "yours": "mine",
        "mine": "yours",
        "we": "you'll",

      }
    # returns the mapped pronoun
    return pronoun_mapping.get(word.lower(), word)
    
# words that indicate user wants to exit
exitTerms = ["quit", "exit", "bye", "goodbye", "stop"]

# sentences to choose from when user wants to exit
exitSentences= [
    "{BotName} Thank you for talking with me today.", 
    "{BotName} Goodbye! Take care of yourself.", 
    "{BotName} It was nice talking to you. Farewell!", 
    "{BotName} I hope our conversation was helpful. Goodbye!", 
    "{BotName} Take care! Remember, I'm here if you need to talk again."
    ]

# familly realted words and their pronoun mappings
familyMentions = {
    "mother": {"pronoun": "she"},
    "father": { "pronoun": "he"},
    "sister": {"pronoun": "she"},
    "brother": {"pronoun": "he"},
    "wife": {"pronoun": "she"},
    "husband": {"pronoun": "he"},
    "child": {"pronoun": "they"},
    "children": {"pronoun": "they"},
    "parent": {"pronoun": "they"},
    "parents": {"pronoun": "they "}
}

# Template sentences for family-related statements
famSentences = {
    "feels": [
        "What do you think might be causing {familyPossessive} to feel that way?",
        "How does it affect you when {familyPronoun} feels that way?",
        "What led you to believe that {familyPossessive} feels that way?"
    ],

    "thinks": [
        "What makes you think that {familyPossessive} thinks that?",
        "How do you feel about {familyPossessive} having that thought?",
        "Why do you believe that {familyPossessive} thinks that?"
    ],

    "wants": [
        "Why do you think {familyPossessive} wants that?",
        "How does it affect you knowing that {familyPronoun} wants that?",
        "What makes you say that {familyPossessive} wants that?"
    ],

    "needs": [
        "What makes you believe that {familyPossessive} needs that?",
        "How does it affect you that {familyPronoun} needs that?",
        "Why do you think {familyPossessive} needs that?"
    ],

    "is": [
        "What makes you describe {familyPossessive} that way?",
        "How do you feel about {familyPossessive} being that way?",
        "Why do you believe that applies to {familyPossessive}?"
    ],

    "believes": [
        "What makes you think {familyPossessive} believes that?",
        "How do you feel about {familyPossessive} holding that belief?",
        "Why do you believe {familyPossessive} believes that?"
    ],

    "desires": [
        "Why do you think {familyPossessive} desires that?",
        "How does it affect you that {familyPronoun} desires that?",
        "What makes you think {familyPossessive} desires that?"
    ],

    "loves": [
        "Why do you think {familyPossessive} loves that?",
        "How does it affect you that {familyPronoun} loves that?",
        "What makes you believe {familyPossessive} loves that?"
    ],

    "hates": [
        "Why do you think {familyPossessive} hates that?",
        "How does it affect you that {familyPronoun} feels that way?",
        "What makes you think {familyPossessive} hates that?"
    ],

    "likes": [
        "Why do you think {familyPossessive} likes that?",
        "How does it affect you that {familyPronoun} likes that?",
        "What makes you believe {familyPossessive} likes that?"
    ],

    "dislikes": [
        "Why do you think {familyPossessive} dislikes that?",
        "How does it affect you that {familyPronoun} dislikes that?",
        "What makes you think {familyPossessive} dislikes that?"
    ],

    "fears": [
        "Why do you think {familyPossessive} fears that?",
        "How does it affect you that {familyPronoun} fears that?",
        "What makes you believe {familyPossessive} fears that?"
    ],

    "worries": [
        "What makes you think {familyPossessive} worries about that?",
        "How does it affect you that {familyPronoun} worries about that?",
        "Why do you believe {familyPossessive} worries about that?"
    ],

    "hopes": [
        "Why do you think {familyPossessive} hopes for that?",
        "How does it affect you that {familyPronoun} hopes for that?",
        "What makes you believe {familyPossessive} hopes for that?"
    ],

    "wishes": [
        "Why do you think {familyPossessive} wishes for that?",
        "How does it affect you that {familyPronoun} wishes for that?",
        "What makes you think {familyPossessive} wishes for that?"
    ],

    "are": [
        "What makes you say that about {familyPossessive}?",
        "How do you feel about that in relation to {familyPossessive}?",
        "Why do you believe that is true of {familyPossessive}?"
    ],
    "default": [ 
        "Tell me more about your {familyPronoun} {familyPossessive}.", 
        "How long has this been happening with your {familyPronoun}?", 
        "What makes you say that about your {familyPronoun}?" ]
}

# Family-related verbs in regex format
famSVerbs = "feels|thinks|wants|needs|is|believes|desires|loves|hates|likes|dislikes|fears|worries|hopes|wishes|are"


# general verbs
verbs = ["feel", "think", "believe", "want", "need", "desire", "love", "hate", "like", "dislike","fear", "worry", "hope", "wish","crave", "despise", "adore", "detest", "dread", "long for", "envy"]

# Template sentences for general statements
genSentences = [
    "What makes {pronoun} {verb} {action}?",
    "Tell me more about why {pronoun} {verb} {action}.",
    "How long have you felt that {pronoun} {verb} {action}?",
    "What do you think leads {pronoun} to {verb} {action}?",
    "How does it affect you when {pronoun} {verb} {action}?"

]

# trigger words for inappropriate language
triggerWords = ["damn", "Shut up", "crap"]

# bot name and username placeholders
BotName = "[ELIZA]"
username = None

# inital greeting
print(f"{BotName} Hello my name is Eliza. I am a psychotherapist. What is your name?")

# Ask for user's name by checking for common name introduction phrases "is,am,I'm,name's" and store it in userName variable
userInput = input("[User] ")
if re.search(r"\b(is|am|i'm|name's)\b\s+(\w+)", userInput, re.IGNORECASE):
    match = re.search(r"\b(is|am|i'm|name's)\b\s+(\w+)", userInput, re.IGNORECASE)
    userName = match.group(2)
    print(f"{BotName} Nice to meet you, {userName}. How can I help you today?")

# saves the username in [username] format for future prompts
UserName = f"[{userName}]"

# import random module for random response selection
import random

# main conversation loop
while True:
    # prompt user for input and check for exit terms
    userInput = input(f"{UserName} ")
    if any(term in userInput.lower() for term in exitTerms):        
        print(random.choice(exitSentences).format(BotName=BotName))
        break

    # check for trigger words
    elif any(term in userInput.lower() for term in triggerWords):
        print(f"{BotName} Please refrane from using foul language.")
        
    
    # check for family-related mentions
    elif any(terms in userInput.lower() for terms in familyMentions.keys()):
        pattern = rf"\b(my|his|her|their)\s+(?:(\w+'s)\s+)?(mother|father|son|daughter|child|children|sister|brother|grandma|grandpa)\b(?:\s+({famSVerbs}))?\s+(.*)"
        match = re.search(pattern, userInput, re.IGNORECASE)

        # checks if the user input contains family-related verbs
        if any(terms in userInput.lower() for terms in famSVerbs):
            if match:
                # extract relevant parts from user input
                famProNoun = match.group(1).lower()
                subject = match.group(2)

                famMember = match.group(3).lower()
                famVerb = (match.group(4) or "").lower()

                action = match.group(5).strip()                
                
                subject = subject.strip() if subject else ""
                proNoun = replace_pronouns(famProNoun)

                if famVerb == "":
                    famVerb = "default"


                # construct family possessive phrase depending on presence of subject
                if subject:
                    family_possessive = f"{proNoun} {subject} {famMember}"
                else:
                    family_possessive = f"{proNoun} {famMember}"

                family_pronoun_subject = familyMentions[famMember]["pronoun"]
                
                # select a random template and format the response with extracted values and prints it
                template = random.choice(famSentences[famVerb])
                response = template.format(
                    familyPronoun=family_pronoun_subject,
                    familyPossessive=family_possessive,
                    action=action
                )
                print(f"{BotName} {response}")  

        # if no family-related verbs are found, ask user to elaborate   
        else:
            print(f"{BotName} Please tell me more about your family.")

    # check for general verbs
    elif any(verb in userInput.lower() for verb in verbs):
        verbGroup = r"(feel|think|believe|want|need|desire|love|hate|like|dislike|fear|worry|hope|wish|crave|despise|adore|detest|dread|envy)"  
         
        pattern = rf"(?:.*?,\s*)?\b(i|you|he|she|we|they)\s+{verbGroup}\b(?:\s+(i|you|he|she|we|they))?\s*(?:{verbGroup})?\s+(.*)"


        match = re.search(pattern, userInput, re.IGNORECASE)
        if match:
            proNoun = match.group(1).lower()
            verb = match.group(2).lower()
            optionPronoun = match.group(3)
            optionalverb = match.group(4)
            action = match.group(5).strip()

            # optional verb and pronoun formatting for special cases like "i think i crave ..""
            optionalverb = optionalverb.strip()+" " if optionalverb else ""
            optionPronoun = replace_pronouns(optionPronoun)+" " if optionPronoun else ""
            
            # replace pronouns if necessary
            if proNoun.lower() in ("i", "you","we"):
                proNounReplaced = replace_pronouns(proNoun)
           
            # select a random template and format the response with extracted values and prints it
            if verb in verbs:
                template = random.choice(genSentences)
                response = template.format(
                    pronoun=proNounReplaced,
                    verb=verb,
                    action= optionPronoun + optionalverb + action
                )
                print(f"{BotName} {response}")

    # if no matches found, ask user to elaborate
    else:
        print(f"{BotName} Can you tell me more about it?")
        
        

    




