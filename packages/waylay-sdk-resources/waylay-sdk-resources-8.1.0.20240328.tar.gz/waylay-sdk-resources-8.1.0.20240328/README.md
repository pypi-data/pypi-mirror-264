# Waylay Resources Service
This service manages 
[Waylay Resources](/#/features/resources/?id=resource) and related entities.

A _Waylay Resource_ models a real-world device or abstract entity of your IoT solution,
and provides a context when processing data in the Rule Engine.

You'll interact with the _Waylay Resources_ API to create this _Digital Twin_ model, 
a process that's also called _resource provisioning_.

This Python package is automatically generated based on the 
Waylay Resources OpenAPI specification (API version: 8.1.0)

It consists of a plugin for the waylay-sdk package, and contains the Resources api methods.
Note that the typed model classes for all path params, query params, body params and responses for each of the api methods are contained in a separate package called waylay-sdk-resources-types.

## Requirements.
This package requires Python 3.9+.

## Installation
Typically this package is installed when installing the [waylay-sdk](https://github.com/waylayio/waylay-sdk-py) package to enable the service's functionality.
When the service api methods are required, waylay-sdk-resources is included in:
- ```pip install waylay-sdk[resources]``` to install `waylay-sdk` along with only this service, or
- ```pip install waylay-sdk[services]``` to install `waylay-sdk` along with all services.
When the typed models are required, both waylay-sdk-resources and waylay-sdk-resources-types are included in:
- ```pip install waylay-sdk[resources,resources-types]``` to install `waylay-sdk` along with only this service including the typed models, or
- ```pip install waylay-sdk[services,services-types]``` to install `waylay-sdk` along with all services along with the typed models.

## Usage


```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-resources-types` is installed
from resources.models.batch_operation_enqueued import BatchOperationEnqueued
from resources.models.batch_resource_operation import BatchResourceOperation
try:
    # Bulk Delete
    # calls `POST /resources/v1/batch`
    api_response = await waylay_client.resources.batch_operations.start(
        # json data: use a generated model or a json-serializable python data structure (dict, list)
        json = resources.BatchResourceOperation() # BatchResourceOperation | Resource Batch Operation
    )
    print("The response of resources.batch_operations.start:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling resources.batch_operations.start: %s\n" % e)
```


