# ConnectivityTest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connectivity_test_id** | **str** | Numeric identifier of the connectivity test that was performed against the origin server. | [optional] 
**site_id** | **int** | Numeric identifier of the site the test was performed on. | [optional] 
**account_id** | **int** | Numeric identifier of the account the site belongs to. | [optional] 
**origin_ip** | **str** | The IP of the origin server (that was resolved when the test was performed). | [optional] 
**origin_cname** | **str** | The CNAME of the origin server. | [optional] 
**time_stamp** | **int** | The timestamp in which the connectivity test was performed. | [optional] 
**pop** | [**Pop**](Pop.md) |  | [optional] 
**error_code** | **str** | The error code that triggered the connectivity test. | [optional] 
**tcp_port** | **int** | The port the MTR over TCP test is performed against. | [optional] 
**connectivity_tests_list** | [**list[Check]**](Check.md) | Output of connectivity test performed against origin server | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

