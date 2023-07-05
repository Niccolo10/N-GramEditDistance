# Edit Distance Implementation with and without N-Gram

This project includes an implementation of the Edit Distance algorithm with and without N-Gram support. The repository also contains a comparison between the two approaches, a theoretical report on the algorithm and techniques used, and an analysis of the test results.

## Edit Distance Algorithm

The `edit_distance` function calculates the minimum number of operations (insertions, deletions, replacements, and twiddles) required to transform one string into another. It uses dynamic programming to efficiently compute the edit distance between two strings.

## N-Gram Support

The `nGramCreator` function creates N-grams (substrings of length N) for a given input string. N-Grams are used to enhance the edit distance algorithm by measuring the Jaccard similarity between two strings. The `Jaccard` function computes the Jaccard similarity between two sets of N-grams.

## Test Results

The `TestEditDistance` function tests the edit distance algorithm on a dictionary of 1000 Italian words. It finds the word with the minimum edit distance from the input word.

The `TestEditDistance_Gram` function tests the edit distance algorithm with N-gram support. It computes the Jaccard similarity between N-grams of the input word and words in the dictionary, and then calculates the edit distance for similar words.

## Test Cases

The project includes several test cases to evaluate the performance of the edit distance algorithm with and without N-gram support. The tests include the following scenarios:

1. Testing on a dictionary of 1000 words: The algorithm's performance is measured for a random word from the dictionary using both standard edit distance and N-gram supported edit distance (2-gram, 3-gram, and 4-gram).

2. Testing on a word with an added character: The edit distance algorithm's performance is measured on a word with one additional character.

3. Testing on a word with a removed character: The edit distance algorithm's performance is measured on a word with one character removed.

4. Testing on a word with two swapped characters: The edit distance algorithm's performance is measured on a word with two characters swapped.

## Graphs

The project generates graphs showing the time taken by the edit distance algorithm with and without N-gram support for various scenarios. The graphs provide insights into the efficiency of the algorithms in different scenarios.

## Usage

To use the edit distance implementation, follow these steps:

1. Clone the repository: `git clone https://github.com/yourusername/edit-distance-ngram.git`
2. Navigate to the project directory: `cd edit-distance-ngram`
3. Run the main script: `python main.py`

## Requirements

The project requires Python 3.x and the matplotlib library for generating graphs.

## Contributors

- Niccolò Parlanti
