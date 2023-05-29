# Overview

This repo contains a small python service using flask. The service is available in 4 stage.

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
## Modify Elastic Agent Processors
In order to use ECS format for container logs, you need to add the following processors to Elastic Agent Integrations.
```
- decode_json_fields:
    fields: ["message"]
    target: ""
    overwrite_keys: true
```
#### docker integration
Collect Docker container logs -> Advanced Options -> Processors
#### kubernetes integration
Collect Kubernetes container logs -> Advanced Options -> Processors
## docker-compose
This `docker-compose.yml` automatically creates Elastic Agent and enroll in Fleet.

#### Build your own image
At `services` directory,

`docker build -t observability-example_flask .`

If you build image on M1/M2 mac and run them on Intel processor, don't forget to add "--platform linux/amd64 "

#### Configure APM server Fleet server information

To get the value of `<Token>` and `<APM URL>`, refer to this link

https://www.elastic.co/guide/en/apm/guide/current/apm-quick-start.html#add-apm-integration

To get the value of `<Enrollemnt Token>` and `<Fleet URL>`, refer to this link

https://www.elastic.co/guide/en/fleet/current/elastic-agent-container.html#_step_3_run_the_elastic_agent_image
```
.env: 

SECRET_TOKEN="<Token>"
SERVER_URL="<APM URL>"
OTEL_METRICS_EXPORTER="otlp"
OTEL_EXPORTER_OTLP_ENDPOINT=${SERVER_URL}
OTEL_RESOURCE_ATTRIBUTES="service.name=11-app-otel,service.version=1.0.0,deployment.environment=dev"
OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer%${SECRET_TOKEN}"
OTEL_LOGS_EXPORTER="otlp"
FLEET_ENROLLMENT_TOKEN="<Enrollment Token>"
FLEET_ENROLL=1
FLEET_URL="<Fleet URL>"
```

#### Run docker-compose
`docker-compose up -d`

If you run on M1 Mac, change the image of selenium-svc to "seleniarm/standalone-chromium"

APM-Server, Elasticsearch and Kibana also need to be running. You can find more information about the Elastic Stack [here](https://www.elastic.co/elastic-stack/)

## Kubernetes
#### Deploy Elastic Agent
Refer to this document.

https://www.elastic.co/guide/en/fleet/current/running-on-kubernetes-managed-by-fleet.html
#### Configure APM server credentials
Change ConfigMap of "selenium.yml".
```
selenium.yml

apiVersion: v1
kind: ConfigMap
metadata:
  name: elastic
data:
  .env: |-
    SERVER_URL="<APM URL>"
    SECRET_TOKEN="<Token>"
    OTEL_EXPORTER_OTLP_ENDPOINT=${SERVER_URL}
    OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer%${SECRET_TOKEN}"
    OTEL_LOGS_EXPORTER="otlp"
    OTEL_METRICS_EXPORTER="otlp"
    OTEL_RESOURCE_ATTRIBUTES="service.name=11-app-otel,service.version=1.0.0,deployment.environment=dev"
```
`kubectl apply -f selenium.yml`

# Access to Selenium
## docker-compose
VNC to `localhost:5900`

## Kubernetes
`selenium-svc` is conigured to use NodePort. Check the node address and port number by `kubectl get svc selenium-svc` and `kubectl get node -o wide`

You can get these values by the following commands:
#### node addres
`kubectl get node -o json|jq -c '.items[0].status.addresses[]|select (.type=="ExternalIP")'|jq .address`

#### port number
`kubectl get svc selenium-svc -o json|jq -c '.spec.ports[]|select (.targetPort==5900)'|jq .nodePort`

# Screenshots of Selenium
<img width="934" alt="スクリーンショット 2023-02-15 13 26 09" src="https://user-images.githubusercontent.com/65324192/218933405-b54f0532-d840-4f95-8b95-bc26779818f9.png">

# Screenshots of Kibana
<img width="1593" alt="スクリーンショット 2023-02-15 13 27 16" src="https://user-images.githubusercontent.com/65324192/218933642-f06ff16d-66b6-417d-8bdb-002067ba399c.png">

![screencapture-community-conference-kb-us-central1-gcp-cloud-es-io-9243-app-apm-services-04-app-ecs-logging-overview-2022-01-20-10_43_46](https://user-images.githubusercontent.com/11661400/150313736-05bf3ddf-1b82-40e8-94d0-948f04a75ecb.png)
![screencapture-community-conference-kb-us-central1-gcp-cloud-es-io-9243-app-apm-services-04-app-ecs-logging-transactions-view-2022-01-20-10_44_23](https://user-images.githubusercontent.com/11661400/150313846-bff9ae02-4d6c-4ef9-844e-ff1aa265a727.png)
