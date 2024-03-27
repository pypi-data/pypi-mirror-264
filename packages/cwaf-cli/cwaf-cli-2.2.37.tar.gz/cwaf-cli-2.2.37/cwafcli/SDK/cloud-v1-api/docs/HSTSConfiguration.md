# HSTSConfiguration

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_enabled** | **bool** | Enable/disable HSTS support for this website | [optional] [default to False]
**max_age** | **int** | (TTL) The amount of time in seconds to apply HSTS in the browser before attempting to load the page using http://. | [optional] [default to 31536000]
**sub_domains_included** | **bool** | Enforce HSTS on sub-domains. For example, a page listed on xxx.ddd.com uses resources from images.ddd.com. If HSTS for sub-domains is enabled, the images are also covered. Make sure that the site and all sub-domains support HTTPS so that HSTS does not break an internal resource when rendering the page. | [optional] [default to False]
**pre_loaded** | **bool** | The most secure way to enforce HSTS. Ensures the first request goes out in a secure tunnel, since the browser already has that URL in the pre-load list. The domain needs to be listed at https://hstspreload.appspot.com/. | [optional] [default to False]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

