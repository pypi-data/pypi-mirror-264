# IncidentStats

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique incident identifier | [optional] 
**events_count** | **int** | Number of http events participated in the attack | [optional] 
**blocked_events_timeseries** | [**list[KeyValueLongInteger]**](KeyValueLongInteger.md) | Timeseries of blocked event counts | [optional] 
**alerted_events_timeseries** | [**list[KeyValueLongInteger]**](KeyValueLongInteger.md) | Timeseries of alerted event counts | [optional] 
**attack_ips** | [**list[KeyValueIpObjectLong]**](KeyValueIpObjectLong.md) | List of IP addresses that participated in the attack | [optional] 
**attack_agents** | [**list[KeyValueStringLong]**](KeyValueStringLong.md) | List of user-agents that participated in the attack | [optional] 
**attack_tools** | [**list[KeyValueStringLong]**](KeyValueStringLong.md) | List of tools that were used in the attack | [optional] 
**attack_tool_types** | [**list[KeyValueStringLong]**](KeyValueStringLong.md) | List of tool types that were used in the attack | [optional] 
**violations_blocked** | [**list[KeyValueStringLong]**](KeyValueStringLong.md) | A list of blocked violations that were identified in the incident | [optional] 
**violations_alerted** | [**list[KeyValueStringLong]**](KeyValueStringLong.md) | A list of alerted violations that were identified in the incident | [optional] 
**attack_urls** | [**list[KeyValueStringLong]**](KeyValueStringLong.md) | List of URLs that were attacked during this incident | [optional] 
**attacked_hosts** | [**list[KeyValueStringLong]**](KeyValueStringLong.md) | List of hosts that were attacked during this incident | [optional] 
**attack_class_c** | [**list[KeyValueStringLong]**](KeyValueStringLong.md) | List of Class C subnets that participated in the attack | [optional] 
**attack_geolocations** | [**list[KeyValueStringLong]**](KeyValueStringLong.md) | List of geographical areas that events came from | [optional] 
**waf_origins_of_alerts** | [**list[SiteViolation]**](SiteViolation.md) | List of WAF servers that alerted events | [optional] 
**waf_origins_of_blocks** | [**list[SiteViolation]**](SiteViolation.md) | List of WAF servers that blocked events | [optional] 
**waf_origins_entities** | [**list[Site]**](Site.md) | List of WAF servers that events came through | [optional] 
**rules_list** | [**list[KeyValueStringLong]**](KeyValueStringLong.md) | List of rules that triggered this incident | [optional] 
**associated_cve** | **list[str]** | List of known CVEs associated with this incident | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

