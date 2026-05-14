#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script for OPB API Server"""
import subprocess
import sys
import time
import urllib.request
import json
import os

os.chdir("C:/Users/cleit/Desktop/opb-sistema")
sys.stdout.reconfigure(encoding='utf-8')

# Start server
proc = subprocess.Popen(
    [sys.executable, "api_server.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print("Servidor iniciando...", flush=True)
time.sleep(2)

# Check if process is running
if proc.poll() is not None:
    stdout, stderr = proc.communicate()
    print("Servidor morreu! stdout=" + stdout.decode('utf-8', errors='replace'))
    print("stderr=" + stderr.decode('utf-8', errors='replace'))
    sys.exit(1)

try:
    # Test health endpoint
    resp = urllib.request.urlopen("http://localhost:5000/api/health", timeout=5)
    data = json.loads(resp.read())
    print("Health check: " + str(data))

    # Test stats endpoint
    resp = urllib.request.urlopen("http://localhost:5000/api/stats", timeout=5)
    data = json.loads(resp.read())
    print("Stats: agentes_ativos=" + str(data.get('agentes_ativos')) + " ideias=" + str(data.get('ideias_salvas')))

    # Test start-bot endpoint
    req = urllib.request.Request(
        "http://localhost:5000/api/bot/start",
        data=json.dumps({}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    resp = urllib.request.urlopen(req, timeout=5)
    data = json.loads(resp.read())
    print("Start bot: " + str(data))

    # Test ideias endpoint
    resp = urllib.request.urlopen("http://localhost:5000/api/ideias", timeout=5)
    data = json.loads(resp.read())
    print("Ideias: total=" + str(data.get('total')))

    # Test frontend serve
    resp = urllib.request.urlopen("http://localhost:5000/", timeout=5)
    html = resp.read().decode('utf-8', errors='replace')
    if "OPB Studio" in html:
        print("Frontend carregado corretamente")
    else:
        print("Frontend pode ter problema")

    # Test favicon
    resp = urllib.request.urlopen("http://localhost:5000/favicon.ico", timeout=5)
    print("Favicon: " + str(len(resp.read())) + " bytes")

    # Test manifest
    resp = urllib.request.urlopen("http://localhost:5000/manifest.json", timeout=5)
    print("Manifest: OK")

    print("")
    print("Todos os testes passaram!")

except urllib.error.HTTPError as e:
    print("HTTP Error " + str(e.code) + ": " + str(e.reason))
except urllib.error.URLError as e:
    print("URL Error: " + str(e.reason))
except Exception as e:
    print("Erro: " + str(e))
finally:
    print("")
    print("Parando servidor...")
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except:
        proc.kill()
    print("Concluido.")