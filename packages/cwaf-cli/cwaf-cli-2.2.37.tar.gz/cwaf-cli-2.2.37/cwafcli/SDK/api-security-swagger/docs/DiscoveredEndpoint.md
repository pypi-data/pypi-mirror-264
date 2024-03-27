# DiscoveredEndpoint

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The endpoint ID | [optional] 
**labels** | [**list[Label]**](Label.md) |  | 
**method** | **str** | The endpoint HTTP method | [optional] 
**risks** | **list[str]** | The discovered API risks | [optional] 
**risks_info** | [**list[RiskInfo]**](RiskInfo.md) | The discovered API risks&#x27; information | [optional] 
**authentication_info** | [**AuthenticationInfo**](AuthenticationInfo.md) |  | [optional] 
**data_exposure_info** | [**DataExposureInfo**](DataExposureInfo.md) |  | [optional] 
**host_id** | **int** | The ID of the host to which endpoint belongs | [optional] 
**site_id** | **int** | The ID of the site to which host belongs | [optional] 
**host_name** | **str** | The name of the host to which endpoint belongs | [optional] 
**resource** | **str** | The resource (url) to which endpoint belongs | [optional] 
**status** | **str** | The discovery status for the endpoint | [optional] 
**discovery_date** | **int** | The time when endpoint discovery started | [optional] 
**risk_types** | **list[str]** |  | 
**counter** | **int** | Counter for endpoint in case of duplicate/multiple endpoints with same path | [optional] 
**baselined_date** | **int** | The time when endpoint got baselined | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

