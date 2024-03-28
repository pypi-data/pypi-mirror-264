# Waylay Rules Service
The REST api to manage rule tasks and rule templates in the Waylay platform.

This Python package is automatically generated based on the 
Waylay Rules OpenAPI specification (API version: 6.5.0)

It is considered an extension of the waylay-sdk-rules package, and it consists of the typed model classes for all path params, query params, body params and responses for each of the api methods in `waylay-sdk-rules`.

## Requirements.
This package requires Python 3.9+.

## Installation
Typically this package is installed when installing the [waylay-sdk](https://github.com/waylayio/waylay-sdk-py) package to enable the service's functionality.
When the service api methods are required, waylay-sdk-rules is included in:
- ```pip install waylay-sdk[rules]``` to install `waylay-sdk` along with only this service, or
- ```pip install waylay-sdk[services]``` to install `waylay-sdk` along with all services.
When the typed models are required, both waylay-sdk-rules and waylay-sdk-rules-types are included in:
- ```pip install waylay-sdk[rules,rules-types]``` to install `waylay-sdk` along with only this service including the typed models, or
- ```pip install waylay-sdk[services,services-types]``` to install `waylay-sdk` along with all services along with the typed models.

## Usage


```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-rules-types` is installed
from ..models.execute_plugs_specification import ExecutePlugsSpecification
from ..models.transformer_execution_result import TransformerExecutionResult
try:
    # Execute Specified Transformer Version
    # calls `POST /rules/v1/transformers/{name}/versions/{version}`
    api_response = await waylay_client.rules.plugs_execution.execute_transformer_version(
        'name_example', # name | path param "name"
        'version_example', # version | path param "version"
    )
    print("The response of rules.plugs_execution.execute_transformer_version:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling rules.plugs_execution.execute_transformer_version: %s\n" % e)
```


