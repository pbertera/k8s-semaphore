from cheroot.server import HTTPServer
from cheroot.ssl.builtin import BuiltinSSLAdapter

import json
import web
import os

urls = (
    '/validate', 'validate'
)

if 'DEBUG' in os.environ.keys():
    debug = True
else:
    debug = False

class validate:
    def POST(self):
        request = json.loads(web.data())
        uid = request['request']['uid']
        if debug:
            print("/validate REQ: %s" % request)
        response = {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "uid": uid,
                "allowed": True
                }
            }
        if debug:
            print("/validate RES: %s" % response)
        return json.dumps(response)

if __name__ == "__main__":

    if 'TLS_CERT_PATH' in os.environ.keys():
        certificate_path = os.environ['TLS_CERT_PATH']
    else:
        certificate_path = "/etc/certs/cert.pem"

    if 'TLS_KEY_PATH' in os.environ:
        key_path = os.environ['TLS_KEY_PATH']
    else:
        key_path = "/etc/certs/key.pem"

    HTTPServer.ssl_adapter = BuiltinSSLAdapter(
        certificate=certificate_path,
        private_key=key_path)
    app = web.application(urls, globals())
    app.run()
