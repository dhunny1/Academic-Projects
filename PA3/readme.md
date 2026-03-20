# Word Sense Disambiguation Classifier

This project implements a **Decision List classifier** for **word sense disambiguation (WSD)** on the word **line**.  
The program learns from tagged training examples, predicts the correct sense for unseen sentences, and evaluates performance against a gold-standard key.

## Project Overview

This project includes two Python programs:

- `wsd.py` — trains a model from `line-train.txt`, predicts senses for `line-test.txt`, writes the learned model to a file, and prints answer tags to standard output.
- `scorer.py` — compares predicted answers with `line-key.txt`, reports overall accuracy, and prints a confusion matrix.

The classifier uses a **bag-of-words feature representation** and learns a **decision list** from the training data only.

## What the Model Does

The model is trained to distinguish between two senses of the word **line**:

- **phone line**
- **product line**

During training, the program:
1. Reads the tagged training examples from `line-train.txt`
2. Extracts bag-of-words features from the surrounding words
3. Computes a score for each feature based on how strongly it predicts one sense over the other
4. Stores the ranked features as a decision list

During testing, the program:
1. Reads each sentence in `line-test.txt`
2. Checks whether any learned features appear in the sentence
3. Uses the highest-ranked matching feature to predict the sense
4. Prints the predicted answer tags to **STDOUT**

## Files

Expected project files:

- `wsd.py`
- `scorer.py`
- `line-train.txt`
- `line-test.txt`
- `line-key.txt`

Optional output files:

- `my-model.txt`
- `my-line-answers.txt`

## How to Run

### 1. Train the model and generate predictions

Run:

```bash
python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt
````

What this does:

* trains the decision list model using `line-train.txt`
* applies the model to the sentences in `line-test.txt`
* writes the learned model to `my-model.txt` or any .txt file you want to save the model to
* sends predicted answer tags to standard output, which are redirected into `my-line-answers.txt`

### 2. Score the predictions

Run:

```bash
python3 scorer.py my-line-answers.txt line-key.txt
```

What this does:

* compares your predicted tags with the gold-standard answers in `line-key.txt`
* prints the overall accuracy
* prints a confusion matrix showing correct and incorrect predictions by sense

## Output Format

### `wsd.py`

* **Model output:** saved to the file you provide as the third command-line argument
* **Predictions:** printed to standard output in the same format as `line-key.txt`

### `scorer.py`

* prints evaluation results directly to standard output

## Example Workflow

```bash
python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt
python3 scorer.py my-line-answers.txt line-key.txt
```

## Notes on the Approach

* The classifier only learns features from the **training data**
* The **test data is never used for training**
* The feature representation is **bag-of-words**
* The model file should list:

  * each feature
  * its log-likelihood score
  * the sense it predicts

## Results

This implementation achieved:

* **93.7% accuracy**
* above the assignment requirement of **80% accuracy**

The project also includes:

* a confusion matrix
* comparison against a **most frequent sense baseline**
* detailed comments in the source code explaining the decision list and feature design

## Why This Project Matters

This project demonstrates:

* breaking down an ambiguous problem into clear stages
* building a rule-based NLP classifier from scratch
* evaluating model quality with measurable metrics
* using debugging and iteration to improve performance

## Troubleshooting

* Make sure all required `.txt` files are in the same directory as `wsd.py` and `scorer.py`, or provide the correct file paths.
* If `my-line-answers.txt` is empty, check that you used the output redirect (`>`).
* If scoring fails, confirm that your prediction output format matches the format used in `line-key.txt`.

## Author
By: Hunny Biguvu
Created as part of a Python/NLP programming assignment on word sense disambiguation.

