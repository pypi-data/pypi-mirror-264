import os
import yaml

def configure(model_name='gpt-35-turbo'):
  current_script_dir = os.path.dirname(os.path.abspath(__file__))
  yaml_file_path = os.path.join(current_script_dir, "catalog", "openai_config.yaml")
  with open(yaml_file_path, "r") as file:
      openai_api_config = yaml.safe_load(file)

  os.environ["OPENAI_API_KEY"] = get_openai_key(model_name)
  os.environ["OPENAI_API_VERSION"] = openai_api_config[model_name]["OPENAI_API_VERSION"]
  os.environ["AZURE_OPENAI_ENDPOINT"] = openai_api_config[model_name]["AZURE_OPENAI_ENDPOINT"]
  
def get_openai_key(model_name):
  if 'DATABRICKS_RUNTIME_VERSION' in os.environ:
    from databricks.sdk.runtime import dbutils
    if model_name == 'gpt-35-turbo':
      return dbutils.secrets.get(scope="gen_ai", key="openai_key")
    elif model_name == 'gpt-4-1106-preview':
      return dbutils.secrets.get(scope="gen_ai", key="openai_key_gpt4")
    else:
      print(f'Model "{model_name}" not found. Please use one of: gpt-35-turbo, gpt-4-1106-preview')
      return

  else:
    import catalog.key as key
    return key.OPEN_AI_KEY(model_name)
  