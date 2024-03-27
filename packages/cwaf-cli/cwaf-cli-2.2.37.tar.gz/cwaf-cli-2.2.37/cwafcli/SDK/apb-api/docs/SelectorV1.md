# SelectorV1

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**SelectorId**](SelectorId.md) |  | 
**policy_id** | **OneOfSelectorV1PolicyId** | The ID of the Policy to be applied if this Selector is the first Selector in the list of Selectors for a Site that matches a request. If the ID is &#x60;null&#x60; then no Policy will be applied to matching requests. This is, for example, useful to prevent protection on static assets. | [optional] 
**criteria** | [**SelectorCriteriaV1**](SelectorCriteriaV1.md) |  | 
**analysis_settings** | [**AnalysisSettingsV1**](AnalysisSettingsV1.md) |  | 
**derived_id** | **OneOfSelectorV1DerivedId** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

