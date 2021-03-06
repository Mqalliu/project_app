import streamlit as st
from io import StringIO

st.title("CheckMe: make your texts better")
st.subheader("Use this app to check the grammar and the spelling of your text and to improve some vocabulary!")
#INPUT CARD: TEXT FILE
#Theory in streamlit docs: https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader
# Open a file to read
uploaded_file = st.file_uploader("Choose a .txt file")
if uploaded_file is not None:
     # To read file as string:
     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
     string_data = stringio.read()
     text = string_data
     st.subheader("This is your original text:")
     st.write(text)

#INPUT CARD: TEXT INPUT
# ask the user the language in which the text is written
#Theory in streamlit docs: https://docs.streamlit.io/library/api-reference/widgets/st.radio
if uploaded_file is not None:
     st.subheader("In which language is your text written?")
     language_option = st.radio(
     "Choose from the following:",
     ('English', 'German', 'French', 'Spanish', 'Italian'))
     st.write('You selected:', language_option)
if uploaded_file is not None:
   lang = ' '
   if language_option.lower() == 'english':
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
if uploaded_file is not None:
     with st.spinner('In progress...'):
          import language_tool_python
          tool = language_tool_python.LanguageTool(lang)
          correct_text = tool.correct(text)

#adjectives analysis
#PROCESS CARD: TOKENIZE
#https://pypi.org/project/textblob/
if uploaded_file is not None:
     with st.spinner('In progress...'):
          import textblob            #to import
          from textblob import TextBlob
          import nltk
          nltk.download('all')
          blob = TextBlob(correct_text)
          adjectives = []
          for token in blob.tags:
               if token[1].startswith('JJ'):
                    adjectives.append(token[0])

#PROCESS CARD: SYNONIMS
## See API at http://www.datamuse.com/api/
#theory from Class4 Module2
if uploaded_file is not None:
     with st.spinner('In progress...'):
          import json,requests
          repl = [ ]
          for element in adjectives:
               url= 'https://api.datamuse.com/words?ml=' + element + '&max=1' #ml = means like --> to get synonyms 
               response = requests.get(url)  
               dataFromDatamuse = json.loads(response.text) 
               for eachentry in dataFromDatamuse:
                    repl.append(eachentry['word'])

#inspiration from exercise "quizzes_dictionaries_iteration_comprehension.ipynb" from Class16 Module1                    
if uploaded_file is not None:
     with st.spinner('In progress...'):
          import re 
          replacements = {k:v for k,v in zip(adjectives, repl)}
          for key, value in replacements.items(): 
               correct_text = correct_text.replace(key, value) 
    
#new text with changes + downloadable text file with the changes
#OUTPUT CARD: text to be displayed
if uploaded_file is not None:
     st.success('Done!')
     st.subheader("This is your text with some corrections and some more interesting adjectives:")
     st.write(correct_text)
#OUTPUT CARD: downloadable new text
#Theory in streamlit docs: https://docs.streamlit.io/library/api-reference/widgets/st.download_button
if uploaded_file is not None:
     st.subheader("If you like this version, you can download it!")
     st.download_button('Download your corrected text', correct_text, file_name='corrected_text.txt')
