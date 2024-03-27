# UpdateDomainV1

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**site_id** | [**SiteId**](SiteId.md) |  | 
**challenge_ip_lookup_mode** | [**IpLookupModeV1**](IpLookupModeV1.md) |  | 
**analysis_ip_lookup_mode** | [**IpLookupModeV1**](IpLookupModeV1.md) |  | 
**cookiescope** | [**Cookiescope**](Cookiescope.md) |  | 
**captcha_settings** | [**CaptchaSettingsV1**](CaptchaSettingsV1.md) |  | 
**log_region** | [**LogRegionV1**](LogRegionV1.md) |  | 
**no_js_injection_paths** | [**list[NoJsInjectionPathV1]**](NoJsInjectionPathV1.md) |  | 
**obfuscate_path** | **str** | If &#x60;obfuscate_path&#x60; already has a value for this Domain, omitting the field or setting it to &#x60;null&#x60; will result in a 400 Bad Request. | [optional] 
**cookie_mode** | [**CookieModeV1**](CookieModeV1.md) |  | 
**unmasked_headers** | [**UnmaskedHeadersV1**](UnmaskedHeadersV1.md) |  | 
**proxy_flags** | [**ProxyFlagsV1**](ProxyFlagsV1.md) |  | 
**filter_out_static_assets** | **bool** | CWAF Only: Prevents certain static asset paths from being analyzed by ABP. Currently, this filters paths matching the following regular expression:  \&quot;\\.(js|gif|jpe?g|ico|png|css|svg?z|woff2?|ttf)$\&quot; | [optional] 
**enable_mitigation** | **bool** | If set to false, all Conditions in all related Policies will behave as if they were passive. If set to true, all Conditions will behave according to their state (active or passive). | [optional] [default to True]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

