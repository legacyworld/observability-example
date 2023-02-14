# Overview

This repo contains a small python service using flask. The service is available in 4 stages. 

1 - without any instrumentation

2 - with basic Elastic APM instrumentation

3 - with a more advanced Elastic APM instrumentation

4 - with custom spans

5 - with custom context

6 - with ECS logging

7 - calling second service, showing distributed tracing

8 - calling third service, showing distributed tracing

11 - instrumented with OTEL instead of Elastic APM

This repo also includes "selenium" to simulate RUM.
# Requirements
docker-compose or kubernetes is required.

## docker-compose
### Build your own image
At `services` directory,

`docker build -t observability-example_flask .`

### Configure APM server credentials
Before running the services, make sure you provide the following endpoints and credentials:
```
.env: 

SECRET_TOKEN
SERVER_URL
OTEL_EXPORTER_OTLP_ENDPOINT
OTEL_EXPORTER_OTLP_HEADERS
```

### Run docker-compose
`docker-compose up -d`

If you run on M1 Mac, change the image of selenium-svc to "seleniarm/standalone-chromium"

APM-Server, Elasticsearch and Kibana also need to be running. You can find more information about the Elastic Stack [here](https://www.elastic.co/elastic-stack/)

## Kubernetes
`kubectl apply -f selenium.yml`

# Access to Selenium
## docker-compose
VNC to `localhost:5900`

## Kubernetes
`selenium-svc` is conigured to use NodePort. Check the node address and port number by `kubectl get svc selenium-svc` and `kubectl get node -o wide`

### Screenshots of Kibana

![screencapture-community-conference-kb-us-central1-gcp-cloud-es-io-9243-app-apm-services-04-app-ecs-logging-overview-2022-01-20-10_43_46](https://user-images.githubusercontent.com/11661400/150313736-05bf3ddf-1b82-40e8-94d0-948f04a75ecb.png)
![screencapture-community-conference-kb-us-central1-gcp-cloud-es-io-9243-app-apm-services-04-app-ecs-logging-transactions-view-2022-01-20-10_44_23](https://user-images.githubusercontent.com/11661400/150313846-bff9ae02-4d6c-4ef9-844e-ff1aa265a727.png)
