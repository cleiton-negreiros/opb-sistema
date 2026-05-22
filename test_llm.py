import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))
from llm_provider import generate_text

result = generate_text('Teste: responda apenas com "OK" se estiver funcionando.')
print('Result:', repr(result))