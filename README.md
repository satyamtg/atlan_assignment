# Atlan Challenge

Implementation of task scheduling on Celery with Redis and RabbitMQ as broker for performing the following -
- Creating tasks
- Pausing tasks
- Resuming tasks
- Terminating tasks

Tasks are considered here to be iterative in nature and have lots of iterations. The task done in each iteration here is just to wait for given number of seconds (just to replicate long iterative tasks), and APIs are created to enable all the four operations.

You can also go to flower to view all tasks at port `5555`
The API can be tested via the swagger UI at `:8000/docs` where `8000` is the port

The project uses docker compose to create the containers and expose these ports. This can eaisly be deployed on Kubernetes using `kompose` or `kubectl` (after convertion of the resources though)

A pre-made docker image can be found [here](https://hub.docker.com/repository/docker/satyamtg/atlan_assignment) and the kubernetes resource file to apply that using kubectl can be found [here]()
