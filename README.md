# Kubernetes semaphore Validating Webhook

This repo contains a simple Kubernetes `ValidatingWebhook` app that can be used to deny API operations on objects with a specific label.

The validating webhook is deployed as a pod in the cluster, the webhook supports the following environment variables:

- `DEBUG`: if `yes` the debug is enabled, pod logs are more verbose
- `SEMAPHORE_ANNOTATION`: the annotation name to be used as a semaphore (default: `bertera.it/k8s-semaphore`)
- `SEMAPHORE_RED`: the annotation value to be used as a "red light" (default" `red`)

## Usage example

- The app is deployed with default `SEMAPHORE_ANNOTATION` and `SEMAPHORE_RED` env. variables into the namespace **k8s-semaphore**
- A service with name **k8s-semaphore** into the same namespace exposes the app on the port **8080**
- An `ValidatingWebhookConfiguration` is deployed to watch all the `DELETE` actions on `pods`, using the previously defined service as Webhook

Now if a pod has an annotation `bertera.it/k8s-semaphore: red` the web hook will forbid the DELETE action:

## Deployment

A deployment manifest is provided in `manifest.yaml`, the manifest contains a `Deployment`, a `Service` and the `ValidatingWebhookConfiguration`.

```
$ cat << EOF | oc apply -f -
apiVersion: v1
kind: Pod
metadata:
  annotations:
    bertera.it/k8s-semaphore: red
  name: k8s-semaphore-test
spec:
  containers:
  - name: test
    image: alpine
    # Just spin & wait forever
    command: [ "/bin/bash", "-c", "--" ]
    args: [ "while true; do sleep 30; done;" ]
EOF

$ oc get pod test
NAME     READY   STATUS    RESTARTS   AGE
test     1/1     Running   0          29m

$ oc delete test
Error from server: admission webhook "k8s-semaphore.k8s-semaphore.svc" denied the request: Resource test (kind: Pod, version: v1, group: ) is annotated with bertera.it/k8s-semaphore, cannot be removed

$ oc annotate pod test bertera.it/k8s-semaphore-
pod/test annotated

$ oc delete pod test
pod "test" deleted
```
