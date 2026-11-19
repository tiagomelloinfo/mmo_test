# Receptor local temporário: recebe arquivos em base64 (POST /caminho) e grava em assets/<caminho>.
# Fica de pé até receber POST /fim. Uso: python3 tools/receber_png.py [pasta_destino]
import base64,http.server,os,sys,threading
BASE=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
DEST=os.path.abspath(os.path.join(BASE,sys.argv[1] if len(sys.argv)>1 else 'assets'))
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a):pass
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin','*');self.send_header('Access-Control-Allow-Headers','*')
    def do_OPTIONS(self):
        self.send_response(204);self._cors();self.end_headers()
    def do_POST(self):
        n=int(self.headers.get('Content-Length',0));data=self.rfile.read(n).decode()
        rel=os.path.normpath(self.path.strip('/'))
        if rel=='fim':
            self.send_response(200);self._cors();self.end_headers();self.wfile.write(b'ok');threading.Thread(target=self.server.shutdown).start();return
        out=os.path.abspath(os.path.join(DEST,rel))
        if not out.startswith(DEST+os.sep):
            self.send_response(400);self._cors();self.end_headers();return
        os.makedirs(os.path.dirname(out),exist_ok=True)
        open(out,'wb').write(base64.b64decode(data.split(',',1)[-1]))
        self.send_response(200);self._cors();self.end_headers();self.wfile.write(b'ok')
http.server.HTTPServer(('127.0.0.1',8795),H).serve_forever()
