from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# Set OpenAI API key

openai.api_key = os.environ['OPENAI_API_KEY']

llm_model = "gpt-3.5-turbo"

# Create a chat instance

chat = ChatOpenAI(temperature=0.0, model=llm_model)

# Parser for the output

language_schema = ResponseSchema(name="language",
                                 description="Programming language\
                                  used on command generated.")

tables = ResponseSchema(name="tables",
                        description="Tables used on command generated.")

command = ResponseSchema(name="command",
                          description="Command generated.")

response_schemas = [language_schema, tables, command]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# Create a template for the chat

template_string = """Translate the text \
that is delimited by triple backticks \
into a valid sql command. \
text: ```{text}```

{format_instructions}
"""

prompt_template = ChatPromptTemplate.from_template(template_string)

text = """
Update the table `users` by setting the `name` column to `John` if the total rows is greater than 10.
"""

sql_messages = prompt_template.format_messages(text=text, format_instructions=format_instructions)

response = chat(sql_messages)

print(response.content)

output_dict = output_parser.parse(response.content)

print("Language: ", output_dict["language"])
print("Tables: ", output_dict["tables"])
print("Command: ", output_dict["command"])
