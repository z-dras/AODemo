# AODemo

This lays out the base functionality for an interactive media platform, including audio books and trivia games. We hope a platform of this nature can help tired drivers maintain focus for longer on the road. We hope to port this functionality into an iphone app.

### Setup

`pip install requirements.txt` 

### Usage

`python3 ao.py <mode> <name>`

mode should be `book` or `b` to run the demo in audiobook mode
mode should be `trivia` or `t` to run the demo in trivia mode

### Content Creation


#### Audio Book Mode

To add you own audio book content, create a new directory at the root dir thats name is the audio book name. Inside the audio book name directory you can create as many content nodes, prompt nodes and mapping nodes as you want. 

Id Nums: Make sure assoiciated nodes share and id number and there is only one node of each type per id number. The set of nodes with id 0 will be the start of the book. Be sure that id numbers are sequential, we will stop reading them in after one sequential id doesn't exist (ie if your ids are 0, 1,2,3,5 node 5 will not be included and should have id 4 instead)

Content nodes: .txt files named `content-<id_num>.txt` They should contain the content for this part of the story. If there is no matching prompt node for this content, it will be assumed to be a terminal (leaf) node in the book "tree" and nothing will play after.

Prompt nodes: .txt files named `prompt-<id_num>.txt` These should contain the content for the prompt itself and the options should correspond with the keys in the mapping node. If the prompt file is empty or doesn't exist we will assume the book is over.

Mapping nodes: .json files named `mapping-<id_num>.json` These should be a json encoded dictionary where each key is a user response (we recomned using string forms of numbers "1", "2", "3"... but these can be any English word or phrase) and each value is the id number of the next content node to play if that response is given. If the mapping file is empty or doesn't exist we will assume the book is over. You can also use next id number -1 to indicate an ending state for a particular response. 

See the example in test_book directory

#### Trivia Game Mode

To make your own trivia pack, add a new directory to the root directory and title it the name of the pack. 

For each question:

1) put the content of the question in a file named `question-<id>.txt`
2) put the multiple choice answers (if there are any) in a file named `answers-<id>.txt`
3) put the correct answer on a the first (and only) line of a file named `correct-<id>.txt`

ID Nums: Make sure your id numbers start at 0 and count up sequentially. If your ids skip a number, they will not be read after the skipped id (ie if your ids are 0, 1,2,3,5 node 5 will not be included and should have id 4 instead)

Final score is the number of questions that were answered correctly for that pack/

### Notes

email `audioodyssey@umich.edu` with any questions, comments or concerns. If you liked our demo, we would love to hear from you! Feel free to submit a PR as well with your content or code improvements!

Note that the voice recognition is a little touchy, wait a second before responding and make sure you're in a quiet environment for best results.
