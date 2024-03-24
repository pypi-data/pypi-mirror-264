import importlib.util
import sys
import subprocess
import sys

def install(packages):
    packages.insert(0, "install")
    packages.insert(0, "pip")
    packages.insert(0, "-m")
    packages.insert(0, sys.executable)
    subprocess.check_call(packages)

# For illustrative purposes.
required_packges = ['flask_restful', 'flask', 'psutil', 'toml', 'numpy', 'chromadb', 'yaspin', 'rich', 'platformdirs', 'tiktoken', 'matplotlib', 'html2image', 'jupyter_client', 'litellm', 'tokentrim']
# print(required_packges)

not_installed = []

for name in required_packges:
    if name in sys.modules:
        # print(f"{name!r} already in sys.modules")
        pass
    elif (spec := importlib.util.find_spec(name)) is not None:
        pass
    else:
        print(f"can't find the {name!r} module")
        not_installed.append(name)
if(not_installed):
    install(not_installed)

from .interpreter.core.computer.terminal.base_language import BaseLanguage
from .interpreter.core.core import OpenInterpreter

interpreter = OpenInterpreter()


interpreter.offline = False
interpreter.llm.model = "/home/ubuntu/garage/RLAIF/outputs/chat_8475_code_execution_v2_1_with_file_based_examples/merged_weights-480"
interpreter.llm.context_window = 3000
interpreter.llm.max_tokens = 1000
interpreter.llm.api_key = "no_key"
interpreter.llm.api_base = "https://interpreter4.useblackbox.ai/v1"
interpreter.llm.temperature = 0
interpreter.system_message = "Below is an instruction that describes a task. Write a response that appropriately completes the request. You have access to code execution to execute python programs. Wrap your python code inside <execute></execute> block to trigger code execution.\n\n"

def runChat():
    interpreter.chat()