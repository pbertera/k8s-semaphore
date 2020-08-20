from cheroot.server import HTTPServer
from cheroot.ssl.builtin import BuiltinSSLAdapter

import json
import web
import os

urls = (
    '/validate', 'validate'
)

if 'DEBUG' in os.environ.keys():
    web.config.debug = True
    debug = True
else:
    web.config.debug = False
    debug = False

if 'SEMAPHORE_ANNOTATION' in os.environ:
    semaphore_annotation = os.environ['SEMAPHORE_ANNOTATION']
else:
    semaphore_annotation = 'bertera.it/k8s-semaphore'

class validate:
    def POST(self):
        request = json.loads(web.data())
        if debug:
            print("/validate REQ: %s" % request)
        
        uid = request['request']['uid']
        annotations = request['request']['oldObject']['metadata']['annotations']
        resource_name = request['request']['name']
        resource_kind = request['request']['requestKind']['kind']
        resource_version = request['request']['requestKind']['version']
        resource_group = request['request']['requestKind']['group']
        
        if semaphore_annotation in annotations:
            if annotations[semaphore_annotation] == "red":
                response = {
                    "apiVersion": "admission.k8s.io/v1",
                    "kind": "AdmissionReview",
                    "response": {
                        "uid": uid,
                        "allowed": False,
                        "status": {
                            "code": 403,
                            "message": "Resource %s (kind: %s, version: %s, group: %s) is annotated with %s, cannot be removed" % (resource_name, resource_version, resource_group, red_light_annotation)
                            }
                        }
                    } 
                if debug:
                    print("/validate RES: %s" % response)
                return json.dumps(response)
        
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
