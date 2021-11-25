# Neo milestone

This is our first milestone. We want to release just an operator that runs OpenWhisk standalone (no Kafka, Couchdb and other components yet).

We start building:

- an image with the standalone OpenWhisk  controller #5
- a operator that launches such a controller #3
- a set of runtimes to be used by such an image #4
- a test suite to test it at least in Docker Desktop and in one Kubernetes cluster built with Microk8s #2

