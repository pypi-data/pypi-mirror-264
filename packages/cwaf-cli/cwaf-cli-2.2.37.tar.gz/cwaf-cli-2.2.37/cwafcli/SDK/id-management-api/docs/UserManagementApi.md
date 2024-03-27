# swagger_client.UserManagementApi

All URIs are relative to *https://api.imperva.com/identity-management*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_current_account_users**](UserManagementApi.md#get_current_account_users) | **GET** /v3/users/list | Retrieve the list of users for a given account

# **get_current_account_users**
> UsersExternalResponse get_current_account_users()

Retrieve the list of users for a given account

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.UserManagementApi()

try:
    # Retrieve the list of users for a given account
    api_response = api_instance.get_current_account_users()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserManagementApi->get_current_account_users: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**UsersExternalResponse**](UsersExternalResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

