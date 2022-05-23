import streamlit as st
from io import stringio 

#INPUT CARD: TEXT FILE
# Open a file to read
uploaded_file = st.file_uploader("Choose a .txt file")
if uploaded_file is not None:
     # To read file as string:
     string_data = stringio.read()
     st.write(string_data)

#INPUT CARD: TEXT INPUT
# ask the user the language in which the text is written
if uploaded_file is not None:
     language_option = st.radio(
     "In which language is your text written?",
     ('American English', 'German', 'French', 'Spanish', 'Italian'))
     st.write('You selected:', language_option)
if uploaded_file is not None:
   lang = ' '
   if language_option.lower() == 'american english':
     lang = 'en-US'
   elif language_option.lower() == 'german':
     lang = 'de'
   elif language_option.lower() == 'french':
     lang = 'fr'
   elif language_option.lower() == 'spanish':
     lang = 'es'
   elif language_option.lower() == 'italian':
     lang = 'it'
   else:
     pass

#spelling and grammar check
#PROCESS CARD: FIX SPELLING AND GRAMMAR WITH LANGUAGE TOOL
#check API documentation 
#https://dev.languagetool.org/public-http-api
#https://languagetool.org/http-api/swagger-ui/#!/default/post_check
#https://pypi.org/project/language-tool-python/
#https://predictivehacks.com/languagetool-grammar-and-spell-checker-in-python/#:~:text=LanguageTool%20is%20an%20open%2Dsource,through%20a%20command%2Dline%20interface.
import language_tool_python
tool = language_tool_python.LanguageTool(lang)
matches = tool.check(text)
correct_text = tool.correct(text)

#adjectives analysis
#PROCESS CARD: TOKENIZE
#https://pypi.org/project/textblob/
import textblob            #to import
from textblob import TextBlob
import nltk
nltk.download('all')
blob = TextBlob(correct_text)
adjectives = [token[0] for token in blob.tags if token[1].startswith('JJ')]

#PROCESS CARD: SYNONIMS
## See API at http://www.datamuse.com/api/
import json,requests
repl = [ ]
for element in adjectives:
  url= 'https://api.datamuse.com/words?ml=' + element + '&max=1'
  response = requests.get(url)  
  dataFromDatamuse = json.loads(response.text) 
  for eachentry in dataFromDatamuse:
    repl.append(eachentry['word'])

import re 
replacements = {k:v for k,v in zip(adjectives, repl)}
for key, value in replacements.items(): 
    correct_text = correct_text.replace(key, value) 
    
#new text with changes + downloadable text file with the changes
#OUTPUT CARD: text to be displayed
st.write(correct_text)
#OUTPUT CARD: downloadable new text
st.download_button('Download your corrected text', correct_text, file_name='corrected_text.txt')
