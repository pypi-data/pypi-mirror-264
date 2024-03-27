# ResourceUsageRecord

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Resource Usage Record ID. | [optional] 
**resource_id** | **str** | The ID of the resource. | [optional] 
**resource_name** | **str** | The display name of the resource. | [optional] 
**record_status** | **str** | The status of this resource usage record. | [optional] 
**purchased** | **float** | The purchased amount of the resource. | [optional] 
**trial** | **float** | The trial portion of the resource. | [optional] 
**used** | **float** | The amount of the resource that was used, out of the purchased amount. | [optional] 
**overages** | **float** | The amount of monthly usage in excess of the amount included with your plan. | [optional] 
**data_unit** | **str** | The measurement unit of the data. Possible values: Mbps, Gb, M Requests. | [optional] 
**cycle_start_date** | **date** | The start date of this resource usage record. | [optional] 
**cycle_end_date** | **date** | The end date of this resource usage record. | [optional] 
**close_term_reason** | **str** | The reason for term closure. Possible values: End of cycle, Quantity changed, Usage cycle day changed, Resource cancelled, Subscription cancelled, SubAccount deleted, Change in services included in calculation. | [optional] 
**calculated_for_resources** | **list[str]** | Additional resources included in this usage calculation. | [optional] 
**unlimited_purchase** | **bool** | Indicates if the plan includes unlimited usage of the resource. | [optional] 
**unlimited_trial** | **bool** | Indicates if the trial plan includes unlimited usage of the resource. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

