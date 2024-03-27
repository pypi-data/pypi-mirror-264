# Certificate

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Imperva ID of the certificate. | [optional] 
**name** | **str** | For an Imperva-generated certificate, indicates the certificate name and the ID of the Imperva request to the CA. | [optional] 
**status** | **str** | Certificate status | [optional] 
**type** | **str** | Certificate type | [optional] 
**expiration_date** | **int** | Certificate expiration date | [optional] 
**in_renewal** | **bool** | Is certificate under renewal process | [optional] 
**renewal_cert_order_id** | **str** | The order ID of the Imperva request to the CA for a new certificate that will replace an expiring certificate. This certificate will replace the certificate specified by originCertOrderId. | [optional] 
**origin_cert_order_id** | **str** | The order ID of the Imperva request to the CA for a certificate that is set to expire in the near future and must be renewed. This certificate will be replaced by the certificate specified by renewalCertOrderId. | [optional] 
**sans** | [**list[CertificateSanDetails]**](CertificateSanDetails.md) | List of Subject Alternative Names found on the certificate | [optional] 
**ext_site_id** | **int** | The Imperva ID of the onboarded website covered by the certificate | [optional] 
**site_name** | **str** | The name of the onboarded website covered by the certificate | [optional] 
**auth_type** | **str** | The authentication type of the certificate | [optional] 
**level** | **str** | The level of the certificate (SITE or ACCOUNT) | [optional] 
**custom_certificate_details** | [**CustomCertificateDetails**](CustomCertificateDetails.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

