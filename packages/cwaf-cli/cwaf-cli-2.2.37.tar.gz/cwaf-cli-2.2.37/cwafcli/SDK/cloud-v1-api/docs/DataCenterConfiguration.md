# DataCenterConfiguration

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Data center name | 
**id** | **int** | Data center id | [optional] 
**ip_mode** | **str** | Load-balancing mode.&lt;br/&gt;Possible values:&lt;ul&gt;&lt;li&gt;&lt;b&gt;SINGLE_IP&lt;/b&gt; - Use it only when you need to support multiple ports. Allows a single active server listening on multiple ports, plus the option of a single standby server. Traffic is distributed across the server ports.&lt;br/&gt;&lt;b&gt;Note&lt;/b&gt;: The server address must be a valid IP address (i.e. not host/domain name).&lt;br/&gt;SINGLE_IP is applicable only for datacenters. It may not be used when dataCenterMode &#x3D; ‘SINGLE_SERVER’.&lt;/li&gt;&lt;li&gt;&lt;b&gt;MULTIPLE_IP&lt;/b&gt; – Allows one or more origin servers having a single webserver and listening port per server. Traffic is distributed across servers.&lt;/li&gt;&lt;/ul&gt; | [optional] [default to 'MULTIPLE_IP']
**web_servers_per_server** | **int** | When IP mode &#x3D; SINGLE_IP, number of webservers per server. Each webserver listens to different port. E.g. when webServersPerServer &#x3D; 5, HTTP traffic will use ports 80-84 while HTTPS traffic will use ports 443-447 | [optional] [default to 1]
**lb_algorithm** | **str** | Specifies how to load balance between the servers of this data center | [optional] [default to 'LB_LEAST_PENDING_REQUESTS']
**weight** | **int** | Weight in pecentage. Mandatory if lbAlgorithm &#x3D; WEIGHTED_LB. Then, total weights of all data centers must be equal to 100 | [optional] 
**is_enabled** | **bool** | For each site, at least one data center must be enabled | [optional] [default to True]
**is_active** | **bool** | Specify false to define a standby datacenter. No more than one data center can be defined as standby. Failover to standby data center is performed only when no other active data center is available | [optional] [default to True]
**is_content** | **bool** | When true, this data center will only handle requests that were routed to it using application delivery forward rules. If true, must be an active data center. | [optional] [default to False]
**is_rest_of_the_world** | **bool** | When global lbAlgorithm &#x3D; GEO_PREFERRED or GEO_REQUIRED, exactly one data center must have isRestOfTheWorld &#x3D; true. This data center will handle traffic from any region that is not assigned to a specific data center. | [optional] [default to False]
**geo_locations** | **list[str]** |  | [optional] 
**origin_pop** | **str** | The ID of the PoP that serves as an access point between Imperva and the customer’s origin server. For example: \&quot;lax\&quot;, for Los Angeles. When not specified, all Imperva PoPs can send traffic to this data center. The list of available PoPs is documented at: https://docs.imperva.com/bundle/cloud-application-security/page/more/pops.htm | [optional] 
**servers** | [**list[DataCenterServerConfiguration]**](DataCenterServerConfiguration.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

