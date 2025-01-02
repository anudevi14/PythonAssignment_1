Python/Go/Java Project Requirements

Project 1
Read a pdf file from a folder. Refer to the PDF file Chemistry Questions.pdf

Requirements
Store a PDF file in a folder called “/content”
Read PDF file from the folder
Write the content to a text file called “output.txt”
Store this file under the “/content” folder

Error Handling
Take care of case where folder is not available
Take care of case where PDF file is not present in the content folder
Take care of case where the output.txt file is not available
/*****************************************************************/

Project 2
Traverse through folder tree and filter pdf files

Requirements
Add sub-folders called “One”, “Two”, “Three” under the folder called “/content”
Add PDF files under each of the sub-folders
Load all PDF files under the sub-folders and load the PDF content
Write the content to a text file called “output.txt” under each sub-folder respectively

Error Handling
Take care of case where folder is not available
Take care of case where PDF file is not present in a sub-folder
Take care of case where the output.txt file is not available in a sub-folder

/*****************************************************************/

Project 3
Read content from a particular page

Requirements
Update project 1 and update the reading of content
Take a page number as an input from command prompt
Read content of the page number provided and write to the output file

Error Handling
Take care of case where folder is not available
Take care of case where PDF file is not present in a sub-folder
Take care of case where the output.txt file is not available in a sub-folder

/*****************************************************************/

Project 4
Read regular expression from a config file and extract content

Requirements
Update project 3
Add support for a configuration file
In the configuration file set a config with key “regex” and value some regular expression that will match a part of the content in the PDF
Update code to extract only the content matching the regular expression
Write to the output file

Error Handling
Take care of case where folder is not available
Take care of case where PDF file is not present in a sub-folder
Take care of case where the output.txt file is not available in a sub-folder
Take care of case where no configuration file is available
Take care of the case where configuration file does not have the regular expression

/*****************************************************************/

Project 5
Store extracted questions in mysql

Requirements
Update project 4 and add support for database
Create a database to store the following
Subject Name
Question Text
Answer options
Chapter name
Load a PDF containing questions
Extract each question as per a regular expression
Store each question in the database

Error Handling
Take care of case where database is not available
Take care of case where table is not available
Take care of any error handling in DB operations

/*****************************************************************/

Project 6
Load all questions from a chapter

Requirements
Update project 5 and add support for taking a chapter name as input in the command line
Load all questions from the input chapter
Print all questions on the console

Error Handling
Take care of case where empty string is provided as input from command line
Take care of case where there are no questions corresponding to the provided chapter name

/*****************************************************************/

Project 7
Load RSS content and then extract content from each link. Do this in multiple threads

Requirements
Load an RSS xml file (Format: https://www.w3schools.com/xml/xml_rss.asp)
Loop through each link
Extract content from each link and write to “output.txt”
Execute reading from multiple links in parallel

Error Handling
Take care of case where no RSS xml file is available
Take care of case where xml file is empty

/*****************************************************************/

Project 8
Update project 5 to support different types of questions. Questions can be 1) Subjective type with long answers, Objective type with a True/False or Objective type with multiple answer choices.
Support an interface that takes a Question and stores it.

Use inheritance to support different types of questions being stored by the implementation of the interface

Example:

Q1 - Earth is round
True
False
Q2 - What are is the color of a leaf typically
Red
Blue
Green
White
Q3 - Describe the properties of steel
Requirements
Implement using the OOPs concepts
Error Handling
As per project 5

