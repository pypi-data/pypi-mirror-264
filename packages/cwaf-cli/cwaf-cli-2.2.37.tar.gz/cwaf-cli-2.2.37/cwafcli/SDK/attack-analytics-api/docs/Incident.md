# Incident

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique incident identifier | [optional] 
**main_sentence** | **str** | Short description of the attack | [optional] 
**secondary_sentence** | **str** | Secondary sentence with more details | [optional] 
**false_positive** | **bool** | Is incident false positive or not | [optional] 
**events_count** | **int** | The number of HTTP events that participated in the attack | [optional] 
**events_blocked_percent** | **int** | Percentage of http events that were blocked by Imperva | [optional] 
**first_event_time** | **int** | Timestamp (in milliseconds) of first event in the attack, specified as number of milliseconds since midnight 1970 (UNIX time * 1000) | [optional] 
**last_event_time** | **int** | Timestamp (in milliseconds) of last event in the attack, specified as number of milliseconds since midnight 1970 (UNIX time * 1000) | [optional] 
**severity** | **str** | Attack severity as set by the system. Possible values: CRITICAL, MAJOR, MINOR, CUSTOM | [optional] 
**severity_explanation** | **str** | Explanation on why attack receive its severity | [optional] 
**dominant_attack_country** | [**CountryDominance**](CountryDominance.md) |  | [optional] 
**dominant_attack_ip** | [**IpDominance**](IpDominance.md) |  | [optional] 
**dominant_attacked_host** | [**ShinyObject**](ShinyObject.md) |  | [optional] 
**dominant_attack_tool** | [**ToolDominance**](ToolDominance.md) |  | [optional] 
**dominant_attack_violation** | **str** | Violation in more than 50% of attacks | [optional] 
**only_custom_rule_based** | **bool** | True if all events of the incident were created due to user defined rules | [optional] 
**how_common** | **str** | Describes if this incident was spotted on other Imperva customers | [optional] 
**incident_type** | **str** | The type of the incident - regular or DDoS | [optional] 
**ddos_data** | [**DdosData**](DdosData.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

