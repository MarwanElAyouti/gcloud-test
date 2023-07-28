# Devoteam Assessment 

## Live version of the app is currently hosted on:
Frontend: 
- https://friendlyeats-frontend-mxhq4nn7cq-ey.a.run.app/
Api:
- https://friendlyeats-server-mxhq4nn7cq-ey.a.run.app/

## Configure .env config
- Create a Service Account Key
- Each service directory has a .env.example fill in the required config

## Run the app locally
After settings up the config:

- Go the services directory
- `docker compose up`


## Deployment
- Run `./push.sh` to build and push image to container registry
- `gcloud run deploy "$GCR_SERVICE_NAME" --image "docker.io/$DOCKER_IMAGE_NAME" --platform managed --region "$GCR_REGION" --allow-unauthenticated --memory 512Mi`


## To access api documentation and download openapi.yaml

- Navigate to the api endpoint
- Go to `{{API_ENDPOINT}}/docs` or `{{API_ENDPOINT}}/redoc` to explore api documentation and test out requests



## Architecture Overview
First iteration just decouple server from frontend

- ![First Version](/Architectures/ArchitectureV1.svg)

Second iteration

- ![Second Version](/Architectures/ArchitectureV2.svg)


