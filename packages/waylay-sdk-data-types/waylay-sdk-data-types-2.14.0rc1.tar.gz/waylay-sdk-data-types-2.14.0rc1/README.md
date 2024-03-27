# Waylay Data Service
Data is ingested into the platform by the Waylay Broker.

This Python package is automatically generated based on the 
Waylay Data OpenAPI specification (API version: 2.14.0)

It is considered an extension of the waylay-sdk-data package, and it consists of the typed model classes for all path params, query params, body params and responses for each of the api methods in `waylay-sdk-data`.

## Requirements.
This package requires Python 3.9+.

## Installation
Typically this package is installed when installing the [waylay-sdk](https://github.com/waylayio/waylay-sdk-py) package to enable the service's functionality.
When the service api methods are required, waylay-sdk-data is included in:
- ```pip install waylay-sdk[data]``` to install `waylay-sdk` along with only this service, or
- ```pip install waylay-sdk[services]``` to install `waylay-sdk` along with all services.
When the typed models are required, both waylay-sdk-data and waylay-sdk-data-types are included in:
- ```pip install waylay-sdk[data,data-types]``` to install `waylay-sdk` along with only this service including the typed models, or
- ```pip install waylay-sdk[services,services-types]``` to install `waylay-sdk` along with all services along with the typed models.

## Usage


```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-data-types` is installed
from ..models.timestamped_resource_event import TimestampedResourceEvent
try:
    # Stream Events For Resource
    # calls `GET /data/v1/events/{resourceId}`
    api_response = await waylay_client.data.events.stream_events(
        'resource_id_example', # resource_id | path param "resourceId"
    )
    print("The response of data.events.stream_events:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling data.events.stream_events: %s\n" % e)
```


