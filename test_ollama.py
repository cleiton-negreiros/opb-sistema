import requests
import json

payload = {
    "model": "tinyllama",
    "prompt": "Teste: responda apenas com 'OK' se estiver funcionando.",
    "stream": False
}
try:
    response = requests.post('http://localhost:11434/api/generate', json=payload, timeout=10)
    print('Status code:', response.status_code)
    print('Response:', response.text)
    if response.status_code == 200:
        result = response.json()
        print('Generated text:', repr(result.get('response', '')))
except Exception as e:
    print('Error:', str(e))