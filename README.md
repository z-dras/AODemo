# AODemo

This lays out the base functionality for an interactive audio book platform

### Setup

`pip install requirements.txt` 

### Content Creation

To add you own content, create a new directory at the root dir thats name is the audio book name. Inside the audio book name directory you can create as many content nodes, prompt nodes and mapping nodes as you want. 

Id Nums: Make sure assoiciated nodes share and id number and there is only one node of each type per id number. The set of nodes with id 0 will be the start of the book. Be sure that id numbers are sequential, we will stop reading them in after one sequential id doesn't exist (ie if your ids are 0, 1,2,3,5 node 5 will not be included and should have id 4 instead)

Content nodes: .txt files named `content-<id_num>.txt` They should contain the content for this part of the story. If there is no matching prompt node for this content, it will be assumed to be a terminal (leaf) node in the book "tree" and nothing will play after.

Mapping nodes: .txt files named `map-<id_num>.txt` These should be a json encoded dictionary where each key is a user response (we recomned using string forms of numbers "1", "2", "3"... but these can be any English word or phrase) and each value is the id number of the next content node to play if that response is given. If the mapping file is empty or doesn't exist we will assume the book is over. You can also use next id number -1 to indicate an ending state for a particular response. Please make this file ONLY ONE LINE.

Prompt nodes: .txt files named `prompt-<id_num>.txt` These should contain the content for the prompt itself and the options should correspond with the keys in the mapping node. If the prompt file is empty or doesn't exist we will assume the book is over.

See the example in test directory

### Running the Demo

to run the demo `python3 buildbooks.py <audio book name>`

email `audioodyssey@umich.edu` with any questions, comments or concerns. If you liked our demo, we would love to hear from you! Feel free to submit a PR as well with your content or code improvements!

Note that the voice recognition is a little touchy, wait a second before responding and make sure you're in a quiet environment for best results.
