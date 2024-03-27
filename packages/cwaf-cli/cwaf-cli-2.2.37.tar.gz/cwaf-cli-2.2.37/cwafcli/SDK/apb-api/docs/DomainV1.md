# DomainV1

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**DomainId**](DomainId.md) |  | 
**account_id** | [**AccountId**](AccountId.md) |  | 
**site_id** | [**SiteId**](SiteId.md) |  | 
**challenge_ip_lookup_mode** | [**IpLookupModeV1**](IpLookupModeV1.md) |  | 
**analysis_ip_lookup_mode** | [**IpLookupModeV1**](IpLookupModeV1.md) |  | 
**criteria** | [**DomainCriteriaV1**](DomainCriteriaV1.md) |  | 
**cookiescope** | [**Cookiescope**](Cookiescope.md) |  | 
**captcha_settings** | [**CaptchaSettingsV1**](CaptchaSettingsV1.md) |  | 
**log_region** | [**LogRegionV1**](LogRegionV1.md) |  | 
**no_js_injection_paths** | [**list[NoJsInjectionPathV1]**](NoJsInjectionPathV1.md) | Prevents JavaScript injection on the specified paths. | 
**obfuscate_path** | **OneOfDomainV1ObfuscatePath** | The recommended path to use to load the ABP JavaScript. | [optional] 
**mobile_api_obfuscate_path** | [**Path**](Path.md) |  | 
**cookie_mode** | [**CookieModeV1**](CookieModeV1.md) |  | 
**unmasked_headers** | [**UnmaskedHeadersV1**](UnmaskedHeadersV1.md) |  | 
**proxy_flags** | [**ProxyFlagsV1**](ProxyFlagsV1.md) |  | 
**filter_out_static_assets** | **bool** | CWAF Only: Prevents certain static asset paths from being analyzed by ABP. Currently, this filters paths matching the following regular expression:  \&quot;\\.(js|gif|jpe?g|ico|png|css|svg?z|woff2?|ttf)$\&quot; | [optional] 
**created_at** | **OneOfDomainV1CreatedAt** |  | [optional] 
**modified_at** | **OneOfDomainV1ModifiedAt** |  | [optional] 
**enable_mitigation** | **bool** | If set to false, all active Conditions in all related Policies will behave as if they were in monitor state. If set to true, all active Conditions will behave according to their state (active or monitor). | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

