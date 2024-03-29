# alchemite_apiclient.JobsApi

All URIs are relative to *https://alchemiteapi.intellegens.ai/v0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**suggest_additional_metadata_put**](JobsApi.md#suggest_additional_metadata_put) | **PUT** /suggest-additional/metadata | List sorted and filtered suggest-additional metadata


# **suggest_additional_metadata_put**
> InlineResponse2003 suggest_additional_metadata_put()

List sorted and filtered suggest-additional metadata

Returns all suggest-additional jobs matching the query passed. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import jobs_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.suggest_additional_query import SuggestAdditionalQuery
from alchemite_apiclient.model.inline_response2003 import InlineResponse2003
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = jobs_api.JobsApi(api_client)
    offset = 0 # int | The number of items to skip before starting to collect the result set. (optional) if omitted the server will use the default value of 0
    limit = 20 # int | The number of items to return. (optional) if omitted the server will use the default value of 20
    suggest_additional_query = SuggestAdditionalQuery(
        sort=[
            SuggestAdditionalMetadataSort(
                name="name",
                direction="asc",
            ),
        ],
        filters=SuggestAdditionalMetadataFilters(
            name="name_example",
            status="pending",
            tags=[
                "tags_example",
            ],
            num_optimization_samples=NumericalFilter(None),
            num_suggestions=NumericalFilter(None),
            exploration_exploitation=NumericalFilter(None),
            project_id="00112233-4455-6677-8899-aabbccddeeff",
            transitive_model_id="00112233-4455-6677-8899-aabbccddeeff",
            exclude_model_id="00112233-4455-6677-8899-aabbccddeeff",
            model_id="00112233-4455-6677-8899-aabbccddeeff",
            search="search_example",
        ),
    ) # SuggestAdditionalQuery |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List sorted and filtered suggest-additional metadata
        api_response = api_instance.suggest_additional_metadata_put(offset=offset, limit=limit, suggest_additional_query=suggest_additional_query)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling JobsApi->suggest_additional_metadata_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| The number of items to skip before starting to collect the result set. | [optional] if omitted the server will use the default value of 0
 **limit** | **int**| The number of items to return. | [optional] if omitted the server will use the default value of 20
 **suggest_additional_query** | [**SuggestAdditionalQuery**](SuggestAdditionalQuery.md)|  | [optional]

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of suggest-additional jobs matching given query |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

