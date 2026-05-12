import http.server
import socketserver
import os

PORT = 8088

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_PUT(self):
        path = self.translate_path(self.path)
        if path.startswith(os.getcwd()):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            content = self.rfile.read(int(self.headers['Content-Length']))
            with open(path, 'wb') as f:
                f.write(content)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_error(403)
    
    def translate_path(self, path):
        path = path.split('?')[0]
        path = path.lstrip('/')
        if not path.startswith('context-brain'):
            path = os.path.join('context-brain', path)
        return os.path.join(os.getcwd(), path)

os.chdir(r'C:\Users\cleit\Desktop\opb-sistema')
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"  ╔══════════════════════════════════════╗")
    print(f"  ║     OPB - Sistema de Produtividade   ║")
    print(f"  ╠══════════════════════════════════════╣")
    print(f"  ║                                      ║")
    print(f"  ║  🌐 Hub:     http://localhost:{PORT}      ║")
    print(f"  ║  📝 Perfil:  http://localhost:{PORT}/index.html ║")
    print(f"  ║                                      ║")
    print(f"  ║  Ctrl+C para parar                   ║")
    print(f"  ╚══════════════════════════════════════╝")
    httpd.serve_forever()
