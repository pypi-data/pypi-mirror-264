# ClassificationStatistics

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**labels_identified** | [**ResourceStatTrend**](ResourceStatTrend.md) |  | [optional] 
**labeled_hosts** | [**ResourceStatTrend**](ResourceStatTrend.md) |  | [optional] 
**labeled_resources** | [**ResourceStatTrend**](ResourceStatTrend.md) |  | [optional] 
**labeled_endpoints** | [**ResourceStatTrend**](ResourceStatTrend.md) |  | [optional] 
**risky_endpoints** | [**ResourceStatTrend**](ResourceStatTrend.md) |  | [optional] 
**endpoints_owasp_top10_risks** | [**ResourceStatTrend**](ResourceStatTrend.md) |  | [optional] 
**endpoints_other_risks** | [**ResourceStatTrend**](ResourceStatTrend.md) |  | [optional] 
**hosts_classification_statistics** | [**list[HostClassificationStatistics]**](HostClassificationStatistics.md) | The collection of hosts which had any label in the time window | [optional] 
**resources_classification_statistics** | [**list[ResourceClassificationStatistics]**](ResourceClassificationStatistics.md) | The collection of resources which had any label in the time window | [optional] 
**endpoints_classification_statistics** | [**list[EndpointClassificationStatistics]**](EndpointClassificationStatistics.md) | The collection of endpoints which had a label in the time window | [optional] 
**sensitive_classification_volume_statistics** | [**list[ClassificationVolumeStatistics]**](ClassificationVolumeStatistics.md) | The collection of endpoints which had sensitive label in the time window | [optional] 
**non_sensitive_classification_volume_statistics** | [**list[ClassificationVolumeStatistics]**](ClassificationVolumeStatistics.md) | The collection of endpoints which had non sensitive label in the time window | [optional] 
**all_classification_volume_statistics** | [**list[ClassificationVolumeStatistics]**](ClassificationVolumeStatistics.md) | The collection of endpoints which had both sensitive and non sensitive label in the time window | [optional] 
**top_risks_volume_statistics** | [**list[ClassificationRiskVolumeStatistics]**](ClassificationRiskVolumeStatistics.md) | The collection of endpoints that had top risks in the time window | [optional] 
**risks_identified** | [**ResourceStatTrend**](ResourceStatTrend.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

