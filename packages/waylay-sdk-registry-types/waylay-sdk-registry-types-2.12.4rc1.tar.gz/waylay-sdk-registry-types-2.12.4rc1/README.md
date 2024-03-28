# Waylay Registry Service
V2 API to build and deploy Waylay functions (plugs, webscripts, BYOML models).

This Python package is automatically generated based on the 
Waylay Registry OpenAPI specification (API version: 2.12.4)

It is considered an extension of the waylay-sdk-registry package, and it consists of the typed model classes for all path params, query params, body params and responses for each of the api methods in `waylay-sdk-registry`.

## Requirements.
This package requires Python 3.9+.

## Installation
Typically this package is installed when installing the [waylay-sdk](https://github.com/waylayio/waylay-sdk-py) package to enable the service's functionality.
When the service api methods are required, waylay-sdk-registry is included in:
- ```pip install waylay-sdk[registry]``` to install `waylay-sdk` along with only this service, or
- ```pip install waylay-sdk[services]``` to install `waylay-sdk` along with all services.
When the typed models are required, both waylay-sdk-registry and waylay-sdk-registry-types are included in:
- ```pip install waylay-sdk[registry,registry-types]``` to install `waylay-sdk` along with only this service including the typed models, or
- ```pip install waylay-sdk[services,services-types]``` to install `waylay-sdk` along with all services along with the typed models.

## Usage


```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-registry-types` is installed
from ..models.function_type import FunctionType
from ..models.job_state_result import JobStateResult
from ..models.job_type_schema import JobTypeSchema
from ..models.jobs_response import JobsResponse
try:
    # List Jobs
    # calls `GET /registry/v2/jobs/`
    api_response = await waylay_client.registry.jobs.list(
        # query parameters:
        query = {
        },
    )
    print("The response of registry.jobs.list:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling registry.jobs.list: %s\n" % e)
```


