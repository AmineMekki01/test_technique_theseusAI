# test_technique_theseusAI


This test is given by TheseuseAI company for an apprenticeship position.

## The general idea : 
The task involves creating a FastAPI that takes a question and searches for the answer in a text file.

## Test explanation :

To find the answer within the file, we need to divide the text file into chunks, with each chunk containing a maximum of 500 tokens. The division should stop at the closest full stop (".") before reaching the token limit. After dividing the text file into chunks, a vector research process is conducted among the top three nearest chunks to the answer. These chunks are selected based on their similarity to the query. Once the nearest chunks are identified, our model is applied to these chunks to retrieve the answer. This approach ensures that the answer is obtained from the most relevant and contextually similar portions of the text file.

## OpenAI API key :
- You will need to set the OpenAI API key as a system environment variable 
  - Windows :
    - setx OPENAI_API_KEY "YOUR_API_KEY"
    - If it doesn't work try to restart your vscode/ide or terminal.
  
  - MacOS/linux 
    - In your terminal open one of the following files "nano ~/.bashrc" or "nano ~/.bash_profile"
    - Add the following code at the end : export OPENAI_API_KEY="YOUR_API_KEY"
    - Save the file and run "source ~/.bashrc" or "source ~/.bash_profile"  to apply the changes.

## Install all the required libraries : 
pip install -r requirements 

## Try the app : 
Make sure you are in the correct directory where main.py is located.
run the following code : uvicorn main:app --reload (--reload to see directly the changes your adding to the code, if you don't want you can forget about it.)

## Code Architecure :

To do this task i thought about the following code architecture.
- src directory :
  - text_processor :
It will contain the code that will devide our text file into chunks of 500 tokens at most and stops at the point "." before the maximum number 500.

  - utils :
  In this module i will some functions that will be responsible of  getting the openAI API from the system environment.
  
  - chatbot.py :
  In this module, i'll be creating all the functions for the chatbot that will be answering the questions for our text file. 
  
  - main.py
  This module will contain the codes for our FastAPI

  - static directory
    - script.js : This file will contain JavaScript code for handling user interactions, such as submitting questions and uploading text files.
    - styles.css : This file will contain CSS code to style the web application.
      
  - templates directory
    - index.html : This template represents the home page of the web app, providing an overview of its content
    - about.html : This template presents a comprehensive explanation of the task and provides relevant information about the application.
    - query.html : This template represents the page where users can upload a text file and input their desired question. It generates the corresponding answer based on the provided question and the processed chunks from the text file.

