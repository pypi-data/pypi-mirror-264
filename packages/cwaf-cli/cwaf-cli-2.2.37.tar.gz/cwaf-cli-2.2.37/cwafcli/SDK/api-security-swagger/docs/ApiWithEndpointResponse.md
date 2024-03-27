# ApiWithEndpointResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**specification_violation_action** | **str** | The action taken when an API Specification Violation occurs | [optional] 
**violation_actions** | [**ApiViolationActions**](ApiViolationActions.md) |  | [optional] 
**id** | **int** | The API ID | [optional] 
**site_id** | **int** | The site ID | [optional] 
**site_name** | **str** | The site’s domain name | [optional] 
**host_name** | **str** | The  API&#x27;s host name | [optional] 
**base_path** | **str** | The API&#x27;s basePath | [optional] 
**description** | **str** | The API&#x27;s description in the dashboard | [optional] 
**last_modified** | **int** | The last modified timestamp | [optional] 
**creation_time** | **int** | The timestamp when this api was created | [optional] 
**api_source** | **str** | The source from which the API was created | [optional] 
**oas_file_name** | **str** | Uploaded oas file name | [optional] 
**endpoints** | [**list[EndpointResponse]**](EndpointResponse.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

