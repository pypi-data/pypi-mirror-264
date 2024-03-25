import os
from yaml import safe_load

class PromptManagerV2():
  """ PromptManager
  Class to contain a collection of prompts. The prompts are loaded from a YAML file
  and saved in self.versions.

  Utility methods are provided, such as latest(), to retrieve the last version.
  """
  current_script_dir = os.path.dirname(os.path.abspath(__file__))
  prompt_yaml_file_path = os.path.join(current_script_dir, "prompts")

  def __init__(self, prompts_dir = prompt_yaml_file_path):
    self.prompts_dir = prompts_dir
    self.prompts_dict = self.__get_yaml_files_dict()
    
  def get_prompt_attributes(self, task_name, version = "latest"):
    with open(self.prompts_dict[task_name], 'r') as f:
      prompts = safe_load(f)

    if version == "latest":
      version = max([k for k in list(prompts.keys()) if isinstance(k) == float])

    return PromptAttributes(
      text = prompts[version]['text'],
      version = version,
      required_input_variables = prompts[version]['input_variables'],
      required_partial_variables = prompts[version]['required_partial_variables'],
      task_name=task_name
      )
      
  def __get_yaml_files_dict(self):
    yaml_files_dict = {}
    for filename in os.listdir(self.prompts_dir):
        if filename.endswith(".yaml"):
            key = filename.split('.yaml')[0]
            absolute_path = os.path.abspath(os.path.join(self.prompts_dir, filename))
            yaml_files_dict[key] = absolute_path
    return yaml_files_dict

  def display_versions(self, markdown=False):
    string = ''
    if markdown:
      for version,prompt in self.versions.items():
        string += f'## Version {version}\n'
        string += prompt.replace('\n','\n\n') + '\n'
        string += 100*'-' + '\n'
    else:
      for version,prompt in self.versions.items():
        string += f'  Version {version}\n'
        string += 20*'-' + '\n'
        string += prompt + '\n'
        string += 100*'-' + '\n'
      print(string)


class PromptAttributes():
  def __init__(self, text, version, required_input_variables, required_partial_variables, task_name=None):
    self.version = version
    self.text = text
    self.required_input_variables = required_input_variables
    self.required_partial_variables = required_partial_variables
    self.task_name = task_name

