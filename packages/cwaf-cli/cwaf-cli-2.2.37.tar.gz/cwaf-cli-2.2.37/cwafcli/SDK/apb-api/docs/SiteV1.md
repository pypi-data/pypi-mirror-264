# SiteV1

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**SiteId**](SiteId.md) |  | 
**account_id** | [**AccountId**](AccountId.md) |  | 
**mx_hostname_id** | **OneOfSiteV1MxHostnameId** |  | [optional] 
**name** | [**Name**](Name.md) |  | 
**selectors** | [**list[SelectorV1]**](SelectorV1.md) | A list of Selectors in priority order, such that the first Selector that matches the incoming request will decide the Policy that will be applied. | 
**created_at** | **OneOfSiteV1CreatedAt** |  | [optional] 
**modified_at** | **OneOfSiteV1ModifiedAt** |  | [optional] 
**default_max_requests_per_minute** | [**MaxRequestsPerMinute**](MaxRequestsPerMinute.md) |  | [optional] 
**default_max_requests_per_session** | [**MaxRequestsPerSession**](MaxRequestsPerSession.md) |  | [optional] 
**default_max_session_length** | [**MaxSessionLength**](MaxSessionLength.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

