import streamlit as st
from streamlit_chat import message
from typing import Dict
import json
from io import StringIO
from random import randint
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

import boto3
from langchain.llms.bedrock import Bedrock

# Index to be processed
# bank-doc-poc-indx
#kendra_index_id = "9ca6bcc2-47e7-47c4-a89b-2f443bb74ed7"

# csv sub set index
kendra_index_id ="5e68ed90-2f97-476e-945e-632361b63026"

model_id = "anthropic.claude-instant-v1"
language = "en"


prompt_template_string = dict()
prompt_template_string["en"] = "{history}\n\nHuman: {input}\n\nAI-Assistant:"

if language not in prompt_template_string:
    raise KeyError(f"No prompt template string for {language}")
    
input_template = "{}\nContext:\n{}"

st.set_page_config(page_title="Document Analysis (Model: Bedrock-Anthropic Claude-Instant)", page_icon=":ninja:", layout="centered")
st.header("Chat with your Financial Documents:ledger:")

boto3_bedrock = boto3.client("bedrock-runtime", "ap-northeast-1")
kendra = boto3.client("kendra", "ap-south-1")

inference_modifier = {"max_tokens_to_sample":4096, 
                      "temperature":0.1,
                      "top_k":250,
                      "top_p":1,
                      "stop_sequences": ["\n\nHuman"]
                     }

@st.cache_resource
def load_chain():
    llm = Bedrock(model_id = model_id,
                    client = boto3_bedrock, 
                    model_kwargs = inference_modifier 
                    )
    memory = ConversationBufferMemory(human_prefix="Human",
                                        ai_prefix="Assistant")
    prompt_template = PromptTemplate(input_variables=["history", "input"], output_parser=None, partial_variables={}, template=prompt_template_string[language], template_format="f-string", validate_template=True)
    chain = ConversationChain(llm=llm, memory=memory, prompt=prompt_template, verbose=False)
    return chain

def search_kendra(index_id, query):
    client = boto3.client("kendra", "ap-south-1")
    response = client.query(
        IndexId=index_id,
        QueryText=query
    )
    return response

# this is the object we will work with in the ap - it contains the LLM info as well as the memory
chatchain = load_chain()

# initialise session variables
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
    chatchain.memory.clear()
if "widget_key" not in st.session_state:
    st.session_state["widget_key"] = str(randint(1000, 100000000))

# Sidebar - the clear button is will flush the memory of the conversation
# st.sidebar.title("Options:")
# clear_button = st.sidebar.button("Clear Conversation", key="clear")

clear_button = st.button("Clear Chat", key="clear")

if clear_button:
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["widget_key"] = str(randint(1000, 100000000))
    chatchain.memory.clear()


# this is the container that displays the past conversation
response_container = st.container()
# this is the container with the input text box
container = st.container()

#create lambda function KendraRetrievalLambda
#lambda_client = boto3.client("lambda", "us-east-1")

with container:
    # define the input text box
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area("You:", key="input", height=100)
        submit_button = st.form_submit_button(label="Send")

    # when the submit button is pressed we send the user query to Kendra to retrieve the relevant passages for user"s query
    #  and later save the chat history
    if submit_button and user_input:
        print(f"user_input: {user_input}")
        
        result = search_kendra(kendra_index_id, user_input)

        print("context:    Found {} snippets in Kendra".format(len(result["ResultItems"])))
        theexcerpt = ""
        for item in result["ResultItems"]:
            theexcerpt += theexcerpt + "\n" + item['DocumentExcerpt']['Text']
    #    context = "Context:" + thenewline + theexcerpt + thenewline 
        context = theexcerpt
        
#        print("response is: " + str(kendra_rag))

        #Prompt to LLM= context (based on user_input) and relevant passages from Kendra+ "Question"- user_input+ "Answer:"
#        user_input_rag=kendra_rag + """Question: """+str(user_input) + """Answer: """
#        user_input_rag= "\n\nHuman:\n" + str(kendra_rag) + "\n" + str(user_input) + "\n\nAssistant: "
        user_input_with_context = input_template.format(user_input, context)
                
        try:
            output = chatchain(user_input_with_context)["response"]
        except Exception as e:
            print(e)
            output = "Bedrock returned an error: " + str(e)
            
        #st.text("output is: " + str(output)
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)

        print("ouput:     " + str(output[:80]) + "...")
        
# this loop is responsible for displaying the chat history
if st.session_state["generated"]:
    with response_container:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][i], key=str(i))
