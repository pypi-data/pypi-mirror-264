from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool
from langchain_core.tools import ToolException
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.messages import AIMessage, HumanMessage
import os

import requests
import json
import aiohttp
import asyncio

from langchain_openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI

from langchain.agents.agent import RunnableAgent

#from langchain.callbacks import get_openai_callback
from langchain_community.callbacks import get_openai_callback

# Local imports
from miksi_ai_sdk.sqltool import (execute_mysql_query, get_mysql_database_schema,get_pgdb_schema,execute_pgdb_query,
                                  get_mssql_db_schema,execute_mssql_query)
from miksi_ai_sdk.pythontool import *
from miksi_ai_sdk.api import MiksiAPIHandler



from dotenv import load_dotenv
load_dotenv()

#db_info = get_database_schema()

class CustomRunnableAgent(RunnableAgent):
    def plan(
        self,
        intermediate_steps,
        callbacks,
        **kwargs
    ):
        inputs = {**kwargs, **{"intermediate_steps": intermediate_steps}}
        output = self.runnable.invoke(inputs, config={"callbacks": callbacks})
        return output
    

def create_chat_openai_instance(miksi_api_key):
    api_handler = MiksiAPIHandler(miksi_api_key=miksi_api_key)
    status = api_handler.validate_miksi_api_key()
    if not status:
        print("API key validation failed.")
        return None
    data = api_handler.get_openai_data()
    # Fetch the data or use default values
    model_name = data.get('model_name')  
    temperature = data.get('temperature', 1)  
    api_key = data.get('api_key') 
    
    # Create the ChatOpenAI instance
    llm = ChatOpenAI(openai_api_key=api_key, model=model_name, temperature=temperature)
    print(f"LLM is Ready!")
    return llm



def create_agent(miksi_api_key,media_path,engine,instructions=None):
    
    # Custom input validation models for the execute_sql_query tool
    class SQLQueryInput(BaseModel):
        sql_query: str = Field(description="SQL query string to be executed")

    # Custom input validation models for the python interpreter tool
    class PythonCodeInput(BaseModel):
        code: str = Field(description="Python code to be executed")

    
    # GET DB_SCHEMA TOOLS

    # This tool gets mySQL db schema
    get_mysql_database_schema_tool = StructuredTool.from_function(
        func=get_mysql_database_schema,
        name="GetDatabaseSchema",
        description="Used to get mySQL database schema. Use this tool to get MySQL db schema ",
    )
    
    # This tool gets Postgres DB schema
    get_pgdb_schema_tool = StructuredTool.from_function(
        func=get_pgdb_schema,
        name="GetPostgresDatabaseSchema",
        description="Used to get postgres database schema. Use this tool when you want to know/get postgres database schema "
    )
    
    # This tool connects gets Ms SQL db Schema
    get_mssql_database_schema_tool = StructuredTool.from_function(
        func=get_mssql_db_schema,
        name="GetMsSQLDatabaseSchema",
        description="Used to get MsSQL database schema. Use this tool to get MsSQL db schema ",
    )


    # ESTABLISH CONNECTION TO DB TOOLS
    
    # Tool to connect to mySQL and execute SQL code
    execute_mysql_query_tool = StructuredTool.from_function(
        func=execute_mysql_query,
        name="ExecuteSQLQuery",
        description="Takes in a correct mySQL query and executes it to give results.",
        args_schema=SQLQueryInput,
    )

    # Tool to connect to Postgres and execute SQL code
    execute_postgresdb_query_tool = StructuredTool.from_function(
        func=execute_pgdb_query,
        name="ExecutePostgresSQLQuery",
        description="Takes in a correct PostgreSQL query and executes it to give results.",
        args_schema=SQLQueryInput,
    )

    # Tool to connect to Postgres and execute SQL code
    execute_mssqldb_query_tool = StructuredTool.from_function(
        func=execute_mssql_query,
        name="ExecutePostgresSQLQuery",
        description="Takes in a correct PostgreSQL query and executes it to give results.",
        args_schema=SQLQueryInput,
    )
    

    # OTHER NON SQL TOOLS
    # Tool to execute python code
    execute_python_code_tool = StructuredTool.from_function(
        func=execute_code,  # imported from python tool
        name="ExecutePythonCode",
        description="Takes in  correct python code and executes it to give results.",
        args_schema=PythonCodeInput,
    )


    tools = [get_mysql_database_schema_tool,get_pgdb_schema_tool, get_mssql_database_schema_tool,
             execute_mysql_query_tool,execute_python_code_tool,execute_mssqldb_query_tool
             ,execute_postgresdb_query_tool ]


    

    # Load the language model
    #llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=1.0)
    llm = create_chat_openai_instance(miksi_api_key)

    '''
    AZURE_OPENAI_ENDPOINT= os.getenv("azure_endpoint")
    AZURE_OPENAI_API_KEY= os.getenv("AZURE_OPENAI_KEY")
    OPENAI_API_VERSION = os.getenv("api_version")

    llm = AzureChatOpenAI(deployment_name="miksi-gpt-35",
                      azure_endpoint="https://miksi.openai.azure.com/",# AZURE_OPENAI_ENDPOINT,
                      api_key= AZURE_OPENAI_API_KEY,
                      api_version="2024-02-15-preview",#OPENAI_API_VERSION,
                      model_name="gpt-35-turbo-16k", temperature=1)
    '''
    

    # Define prompt template with memory placeholders
    MEMORY_KEY = "chat_history"
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", f"""You are a very powerful and honest assistant with specific tools.You work with SQL databases
             . You are currently working with this engine {engine}. You have  specific get_database_schema_tool for this 
             specific engine, that 
            helps you see the db schema,execute_sql_query_tool that will execute correct sql code provided to it
            to give results,execute_python_code_tool that you can use to generate graphs/charts/tables by providing 
            correct python code to it.If an SQL query returns data store it in data structures like arrays and list 
            and pass the variable name do not directly pass the raw data to avoid violating context limit
            To use the pythoncode tool just provide the correct code that will be ecexuted
            to it.Dont directly provide raw data to it but use data structures like arrays and list to store results
            then use them to execute python code. Strictly use the tools dont do your own things
            ALWAYS return the SQL query that you executed and your reasoning 
            you used to answer the question as part of your final. Sometimes when the questions are not direct
            you need to make decisions on how to utilize these tools to provide the best answer to the questions asked
            answer.Dont suggest to the user the actions they should take instead take these actions yourself
            and just provide the answer to the question. For the questions that require your creativity be as 
            creative but STRICTLY explain your reasoning and what you did. When using matplotlib dont show the
            graph instead save it in {media_path} - matplotlib code should
             create this directory if doesnt exist-  in the current base directory. When you generate
            a graph label it well, and metion you generate a graph and return the path to saved graph in your final
            response.

            The only allowed file types you can generate are images(so if you generate a table e.g it has to be in image
            format). The following modules are already installed and you can utilise them for questions that require
            your creativity: # The agents default modules are :["matplotlib", "scikit-learn", "numpy", "statsmodels", "pandas",
              "scipy"]. The questions asking for trends/forecasting will need you to reason highly, deal with 
              errors such as incorrect date formatting since you are an intelligent agent.
              Try and explain the graphs from what you observe from the plotting data
            "IF THE QUESTION IS VAGUE JUST LOOK AT THE DATA,DECIDE YOURSELF AND COME UP WITH AN ANSWER!
            Strictly Give your final response in json format with the followings keys 1. answer- which is your
            final anwer from your observation, sql_queries.
            which is a list all the sql queries you executed to get to the answer, python-code which is python codes you 
            executed to get to the answer, and image_url which is the path to graph(s)/chart(s) you may have 
            generated.Strictly adhere to that format for all responses. 
            Below is the template for all your responses
            
            
            answer: 
                "Your final answer from your observations here.
            ,
            sql_queries:  "all SQL queries executed here
            ,
            python-code: python code that may have been used to plot graphs/charts/tables or other activity otherwise leave this blank,
            "image_url": 
                image paths here for all images generated, otherwise if no image generated also leave it blank
            
            Dont format your answer as a string it should be standard JSON, so dont enclose it in  ```json  ```

            If you ecounter a module not found error just run pip install <module_name> in the python tool
            If you dont find the answer or if an error occurs just simply give the answer as an error occurred
            try again dont given irrevant answer in respect to the question. 
            Below are the instructions you MUST follow! The below instructions can overide the ones provided above :
             {instructions}
            It is very important you follow all those instructions. I insist, It is very important you follow all those instructions"""),

            MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Bind the tools to the language model
    llm_with_tools = llm.bind_tools(tools)

    try:
        api_handler = MiksiAPIHandler(miksi_api_key=miksi_api_key)
        response = api_handler.validate_miksi_api_key()
        validation=response['status']
    except Exception as e:
        print(f"An error occured while attempting to valid your Miksi API key: {e}")
    if validation==True:
        try:
            # Create the agent
            agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
                    "chat_history": lambda x: x.get(MEMORY_KEY, []),
                }
                | prompt_template
                | llm_with_tools
                | OpenAIToolsAgentOutputParser()
            )

            # Initialize the AgentExecutor with the agent and tools
            agent_executor = AgentExecutor(agent=CustomRunnableAgent(runnable = agent), tools=tools, verbose=True,
                                           handle_parsing_errors=True,stream_runnable=False)
            print("Agent is Ready!")
            return agent_executor
        except Exception as e:
            print(f"An error occurred while creating the agent: {e}")
            return None
    else:
        print("Problem creating the agent!Please check your API key")
        

from miksi_ai_sdk.api import send_user_question


def run_agent(agent, miksi_api_key, query):
    chat_history = []
    input1 = query
    tokens = None
    total_cost = None

    if agent is not None:
        with get_openai_callback() as cb:
            try:
                result1 = agent.invoke({"input": input1, "chat_history": chat_history})
                chat_history.extend([HumanMessage(content=input1), AIMessage(content=result1["output"])])
                tokens = cb.total_tokens
                total_cost = cb.total_cost 
            except Exception as e:
                print(f"An error occurred when running the agent: {e}")

    if tokens is not None and total_cost is not None:
        send_user_question(miksi_api_key, query, tokens, total_cost)
    return result1["output"]
