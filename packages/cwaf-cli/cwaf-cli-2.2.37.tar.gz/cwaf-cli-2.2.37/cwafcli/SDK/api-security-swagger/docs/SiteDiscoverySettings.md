# SiteDiscoverySettings

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**site_id** | **int** | The site ID | [optional] 
**account_id** | **int** | The account ID | [optional] 
**site_name** | **str** | The site name | [optional] 
**last_modified** | **int** | The last modified timestamp | [optional] 
**last_modified_user** | **str** | The last modified user | [optional] 
**related_hosts** | [**list[Host]**](Host.md) |  | [optional] 
**is_discovery_enabled** | **bool** |  | [optional] 
**discovery_exclude_paths** | **list[str]** | Exclude discovery from these specific base paths | [optional] 
**discovery_include_only_paths** | **list[str]** | Set discovery for these specific base paths only | [optional] 
**is_automatic_discovery_api_integration_enabled** | **bool** |  | [optional] 
**authentication_enabled** | **bool** |  | [optional] 
**auth_parameter_settings** | [**list[AuthParameterSettings]**](AuthParameterSettings.md) | Authentication location settings | [optional] 
**excessive_data_exposure_settings** | [**ExcessiveDataExposureSettings**](ExcessiveDataExposureSettings.md) |  | [optional] 
**deprecated_api_settings** | [**DeprecatedApiSettings**](DeprecatedApiSettings.md) |  | [optional] 
**endpoint_settings** | [**list[EndpointSettingsDto]**](EndpointSettingsDto.md) | Enable or disable endpoint exceptions | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

