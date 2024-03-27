# DataCentersConfiguration

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**lb_algorithm** | **str** | Specifies how to load balance between multiple data centers | [optional] [default to 'BEST_CONNECTION_TIME']
**fail_over_required_monitors** | **str** | How many Imperva PoPs should assess Data Center as down before failover is performed.MANY means more than one. MOST means more than 50%. | [optional] [default to 'MOST']
**data_center_mode** | **str** | SINGLE_SERVER does not allow load balancing. SINGLE_DC allows load balancing and/or failover between its servers. MULTIPLE_DC allows load balancing and/or failover between the data centers plus geo aware routing. | [optional] [default to 'SINGLE_DC']
**min_available_servers_for_data_center_up** | **int** | The minimal number of available data center&#x27;s servers to consider that data center as UP | [optional] [default to 1]
**kick_start_url** | **str** | The URL that will be sent to the standby server when Imperva performs failover based on our monitoring. Port must be specified, if protocol is https. | [optional] 
**kick_start_user** | **str** | The kickstart user, if kickstart URL is protected by user and password | [optional] 
**kick_start_pass** | **str** | The kickstart password, if kickstart URL is protected by user and password | [optional] 
**is_persistent** | **bool** | When true our proxy servers will maintain session stickiness to origin servers by a cookie | [optional] [default to True]
**data_centers** | [**list[DataCenterConfiguration]**](DataCenterConfiguration.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

