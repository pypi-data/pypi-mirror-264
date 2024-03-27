# UpdateSiteV1

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | [**Name**](Name.md) |  | 
**selectors** | [**list[UpdateSelectorV1]**](UpdateSelectorV1.md) | A list of Selectors in priority order, such that the first Selector that matches the incoming request will decide the Policy that will be applied. In addition to the provided Selectors, a default Selector will be created with the lowest priority. It will match any path and apply the default policy. | 
**default_max_requests_per_minute** | [**MaxRequestsPerMinute**](MaxRequestsPerMinute.md) |  | [optional] 
**default_max_requests_per_session** | [**MaxRequestsPerSession**](MaxRequestsPerSession.md) |  | [optional] 
**default_max_session_length** | [**MaxSessionLength**](MaxSessionLength.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

