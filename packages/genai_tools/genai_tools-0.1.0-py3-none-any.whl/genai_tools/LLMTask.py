from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from parser_classes import task_classes

class LLMTask:
    def __init__(self, llm, prompt_attr):
        self.llm = llm
        self.prompt_attr = prompt_attr
        self.prompt = None
        self.parser = None
        
    def build_prompt(self, given_partial_variables={}):
        partial_variables = {}
        format_instructions_str = 'format_instructions'
        if self.prompt_attr.task_name:
            self.parser = PydanticOutputParser(pydantic_object=task_classes[self.prompt_attr.task_name])

        for pv in self.prompt_attr.required_partial_variables:
            if pv == format_instructions_str:
                if not self.parser:
                    raise Exception
                else:
                    partial_variables[format_instructions_str] = self.parser.get_format_instructions()
            elif pv not in given_partial_variables.keys():
                raise Exception
            else:
                partial_variables[pv] = given_partial_variables[pv]

        self.prompt = PromptTemplate(
                template=self.prompt_attr.text,
                input_variables=self.prompt_attr.required_input_variables,
                partial_variables = partial_variables
            )
        
    def get_chain(self):
        if not self.prompt:
            self.build_prompt()
        return self.prompt | self.llm | self.parser
