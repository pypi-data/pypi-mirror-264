# ApiSiteIdBody

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_specification** | **str** | The API specification document. The supported format is OAS2 or OAS3 (JSON or YAML) | 
**base_path** | **str** | Override the spec basePath / server base path with this value | [optional] 
**description** | **str** | A description that will help recognize the API in the dashboard | [optional] 
**oas_file_name** | **str** | Uploaded OAS file name | [optional] 
**specification_violation_action** | **str** | The action taken when an API Specification Violation occurs | [optional] [default to 'ALERT_ONLY']
**validate_host** | **bool** | When set to true, verifies that the host name and site name match. Set to false in cases such as CNAME reuse or API management integrations where the host name and site name do not match. | [optional] [default to True]
**violation_actions** | **str** | Json payload described by ViolationActions Object. This object defines different actions taken when each violation occurs | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

