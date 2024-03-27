# ApiResultSiteStats

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**res** | **int** | res - contains specific error code | [optional] 
**res_message** | **str** |  | [optional] 
**debug_info** | **list[dict(str, object)]** |  | [optional] 
**visits_timeseries** | [**list[VisitsItem]**](VisitsItem.md) |  | [optional] 
**requests_geo_dist_summary** | [**RequestsGeo**](RequestsGeo.md) |  | [optional] 
**visits_dist_summary** | [**list[VisitsSummary]**](VisitsSummary.md) |  | [optional] 
**caching** | [**Caching**](Caching.md) |  | [optional] 
**caching_timeseries** | [**list[TimeSeriesItem]**](TimeSeriesItem.md) |  | [optional] 
**hits_timeseries** | [**list[TimeSeriesItem]**](TimeSeriesItem.md) |  | [optional] 
**bandwidth_timeseries** | [**list[TimeSeriesItem]**](TimeSeriesItem.md) |  | [optional] 
**threats** | [**list[Threat]**](Threat.md) |  | [optional] 
**incap_rules** | [**list[IncapRule]**](IncapRule.md) |  | [optional] 
**incap_rules_timeseries** | [**list[IncapRuleSeries]**](IncapRuleSeries.md) |  | [optional] 
**delivery_rules** | [**list[ADRule]**](ADRule.md) |  | [optional] 
**delivery_rules_timeseries** | [**list[ADRuleSeries]**](ADRuleSeries.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

