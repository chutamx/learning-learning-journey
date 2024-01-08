from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from settings import LLM_MODEL

# Create a chat instance
chat = ChatOpenAI(temperature=0.0, model=LLM_MODEL)

# Parser for the output
language_schema = ResponseSchema(name="language",
                 description="Programming language used on command generated.")
tables = ResponseSchema(name="tables",
            description="Tables used on command generated.")
command = ResponseSchema(name="command",
             description="Command generated.")

enhanced_image_prompt = ResponseSchema(name="enhanced_image_prompt",
              description="Enhanced image prompt generated.")

def prompt(text: str, context: str):
  if context == "sql_script":
    return generate_sql_script(text)
  elif context == "enhanced_image_prompt":
    return generate_enhanced_image_prompt(text)
  else:
    raise Exception("Invalid context.")


def generate_sql_script(text: str):
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

  sql_messages = prompt_template.format_messages(text=text, format_instructions=format_instructions)

  response = chat(sql_messages)

  output_dict = output_parser.parse(response.content)

  return output_dict

def generate_enhanced_image_prompt(text: str):
  output_parser = StructuredOutputParser.from_response_schemas([enhanced_image_prompt])
  format_instructions = output_parser.get_format_instructions()

  template_string = """* Translate the text \
  that is delimited by triple backticks \
  into one better.  \
  * Add very descriptive adjectives into translated text \
  * Add key words for gettings best results on Diffusion Mode into translated text  \
  * Invent a style for the image and add it into translated text \
  
  text: ```{text}```

  {format_instructions}
  """

  prompt_template = ChatPromptTemplate.from_template(template_string)

  chat_message = prompt_template.format_messages(text=text, format_instructions=format_instructions)

  print(chat_message)

  response = chat(chat_message)

  output = output_parser.parse(response.content)

  return output