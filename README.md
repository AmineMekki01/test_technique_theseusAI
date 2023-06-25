# test_technique_theseusAI


This test is given by TheseuseAI company for an apprenticeship position.

The task is to create a FastAPI. That takes a question and search for the answer in a text file.

To find the answer within the file, first we have to devide the text file into chunks of 500 tokens as maximum. 

Then a vector research should be done among the top 3 nearest chunks to the answer and then use our model on theses chunks and get the answer. 


To do this task i thought about the following code architecture.
- text_processor :
It will contain the code that will devide our text file into chunks of 500 tokens at most and stops at the point "." before the maximum number 500.

- utils :
In this module i will some functions that will be responsible of  getting the openAI API from the system environment.

- chatbot.py :
In this module, i'll be creating all the functions for the chatbot that will be answering the questions for our text file. 

- main.py
This module will contain the codes for our FastAPI
