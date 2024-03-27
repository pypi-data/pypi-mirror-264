# Event

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_id** | **int** | Id of the event | [optional] 
**method** | **str** | HTTP method that this request was sent with | [optional] 
**host** | **str** | The host that this request was sent to | [optional] 
**query_string** | **str** | Query string arguments that were sent with this request | [optional] 
**url_path** | **str** | Path that this request accessed | [optional] 
**response_code** | **str** | HTTP response code of this request | [optional] 
**session_id** | **str** | Id of request session | [optional] 
**main_client_ip** | **str** | IP address that was identified as request source | [optional] 
**country_code** | **list[str]** | Two digit country code that this request was sent from | [optional] 
**client_application** | **str** | Application that was identified by Imperva as the sender | [optional] 
**declared_client_application** | **str** | Application that was declared as the sender | [optional] 
**destination_ip** | **str** | IP address that event was sent to | [optional] 
**referrer** | **str** | The address of the webpage (i.e. the URI or IRI) that linked to the resource being requested | [optional] 
**is_event_blocked** | **bool** | Whether or not this event was blocked by Imperva WAF | [optional] 
**violations** | [**list[Violation]**](Violation.md) | The violations that this request was associated with | [optional] 
**headers** | [**list[KeyValueStringString]**](KeyValueStringString.md) | List of http headers in this request | [optional] 
**cookies** | [**list[Cookie]**](Cookie.md) | Cookies passed in the request | [optional] 
**reporter** | **str** | Imperva WAF system that reported this request. Can be either &#x27;Cloud WAF&#x27; or &#x27;On-Premise WAF&#x27; | [optional] 
**creation_time** | **str** | Time when this event occurred, specified as number of milliseconds since midnight 1970 (UNIX time * 1000) | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

