# IPDataApi

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ip** | **str** | The IP address for which reputation intelligence data is presented. | [optional] 
**origin** | [**IPGeoData**](IPGeoData.md) |  | [optional] 
**asn** | [**AsnData**](AsnData.md) |  | [optional] 
**known_to_use** | **str** | The tools or mechanisms used to carry out the attacks, such as Tor, automated browser, or anonymous proxy. | [optional] 
**known_for** | **str** | The attack type, such as DDoS or account takeover. | [optional] 
**risk_score** | [**RiskData**](RiskData.md) |  | [optional] 
**requests** | **str** | The number of requests sent from this IP to Imperva customers during the 2 week time frame covered in this report. | [optional] 
**violations_over_time** | **dict(str, dict(str, str))** | Hits per attack type at the specified time stamp. | [optional] 
**violations** | **dict(str, str)** | Attack type distribution. | [optional] 
**client_application** | **dict(str, str)** | Client application distribution. | [optional] 
**client_application_details** | **dict(str, dict(str, str))** | Details of the client applications used to attack. | [optional] 
**attacks_by_industries** | **dict(str, str)** | Distribution of the industries associated with the attacked sites. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

