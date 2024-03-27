# swagger_client.V1Api

All URIs are relative to *https://api.imperva.com/user-management*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_role**](V1Api.md#create_role) | **POST** /v1/roles | Create New Role
[**create_user**](V1Api.md#create_user) | **POST** /v1/users | Create New User
[**delete_role_by_role_id**](V1Api.md#delete_role_by_role_id) | **DELETE** /v1/roles/{roleId} | Delete Role By Role ID
[**delete_user_by_user_email**](V1Api.md#delete_user_by_user_email) | **DELETE** /v1/users | Delete User Details By User Email
[**get_all_available_account_abilities_by_account_id**](V1Api.md#get_all_available_account_abilities_by_account_id) | **GET** /v1/abilities/accounts/{accountId} | Get Account Abilities By Account ID
[**get_role_details_by_role_id**](V1Api.md#get_role_details_by_role_id) | **GET** /v1/roles/{roleId} | Get Role Details By Role ID
[**get_roles_details**](V1Api.md#get_roles_details) | **GET** /v1/roles | Get Role Details By Account ID, User Email, or Role Name
[**get_user_assignment_by_user_email**](V1Api.md#get_user_assignment_by_user_email) | **GET** /v1/assignments | Get role assignments By User Email And Account ID
[**get_user_by_user_email**](V1Api.md#get_user_by_user_email) | **GET** /v1/users | Get User Details By User Email and Account ID
[**update_assignments**](V1Api.md#update_assignments) | **POST** /v1/assignments | Assign Users To Roles or Delete Existing Assignment
[**update_role**](V1Api.md#update_role) | **POST** /v1/roles/{roleId} | Update Role Details By Role ID

# **create_role**
> RoleDetails create_role(body)

Create New Role

Role management APIs for role management

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
body = swagger_client.CreateRole() # CreateRole | The details required for creating the role.

try:
    # Create New Role
    api_response = api_instance.create_role(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->create_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateRole**](CreateRole.md)| The details required for creating the role. | 

### Return type

[**RoleDetails**](RoleDetails.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user**
> User create_user(body)

Create New User

User management APIs for user management

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
body = swagger_client.CreateUser() # CreateUser | The details required to create new user.

try:
    # Create New User
    api_response = api_instance.create_user(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->create_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateUser**](CreateUser.md)| The details required to create new user. | 

### Return type

[**User**](User.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_role_by_role_id**
> ApiSuccessResponse delete_role_by_role_id(role_id)

Delete Role By Role ID

Role management APIs for role management

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
role_id = 789 # int | The role ID of the required role.

try:
    # Delete Role By Role ID
    api_response = api_instance.delete_role_by_role_id(role_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->delete_role_by_role_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **int**| The role ID of the required role. | 

### Return type

[**ApiSuccessResponse**](ApiSuccessResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_by_user_email**
> ApiSuccessResponse delete_user_by_user_email(user_email, account_id)

Delete User Details By User Email

User management APIs for user management

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
user_email = 'user_email_example' # str | The email of the required user
account_id = 789 # int | Unique ID of the required account

try:
    # Delete User Details By User Email
    api_response = api_instance.delete_user_by_user_email(user_email, account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->delete_user_by_user_email: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_email** | **str**| The email of the required user | 
 **account_id** | **int**| Unique ID of the required account | 

### Return type

[**ApiSuccessResponse**](ApiSuccessResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_available_account_abilities_by_account_id**
> list[Ability] get_all_available_account_abilities_by_account_id(account_id)

Get Account Abilities By Account ID

Role management APIs for abilities management

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
account_id = 789 # int | Unique ID of the required account.

try:
    # Get Account Abilities By Account ID
    api_response = api_instance.get_all_available_account_abilities_by_account_id(account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->get_all_available_account_abilities_by_account_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **int**| Unique ID of the required account. | 

### Return type

[**list[Ability]**](Ability.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_role_details_by_role_id**
> RoleDetails get_role_details_by_role_id(role_id)

Get Role Details By Role ID

Role management APIs for role management

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
role_id = 789 # int | The role ID of the required role.

try:
    # Get Role Details By Role ID
    api_response = api_instance.get_role_details_by_role_id(role_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->get_role_details_by_role_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **int**| The role ID of the required role. | 

### Return type

[**RoleDetails**](RoleDetails.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_roles_details**
> list[RoleDetails] get_roles_details(account_id, user_email=user_email, role_name=role_name)

Get Role Details By Account ID, User Email, or Role Name

Role management APIs for role management

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
account_id = 789 # int | Unique ID of the required account
user_email = 'user_email_example' # str | The email of the required user (optional)
role_name = 'role_name_example' # str | The name of the required role (optional)

try:
    # Get Role Details By Account ID, User Email, or Role Name
    api_response = api_instance.get_roles_details(account_id, user_email=user_email, role_name=role_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->get_roles_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **int**| Unique ID of the required account | 
 **user_email** | **str**| The email of the required user | [optional] 
 **role_name** | **str**| The name of the required role | [optional] 

### Return type

[**list[RoleDetails]**](RoleDetails.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_assignment_by_user_email**
> User get_user_assignment_by_user_email(user_email, account_id)

Get role assignments By User Email And Account ID

Role management APIs for roles assignment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
user_email = 'user_email_example' # str | The email of the required user
account_id = 789 # int | Unique ID of the required account

try:
    # Get role assignments By User Email And Account ID
    api_response = api_instance.get_user_assignment_by_user_email(user_email, account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->get_user_assignment_by_user_email: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_email** | **str**| The email of the required user | 
 **account_id** | **int**| Unique ID of the required account | 

### Return type

[**User**](User.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_by_user_email**
> User get_user_by_user_email(user_email, account_id)

Get User Details By User Email and Account ID

User management APIs for user management

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
user_email = 'user_email_example' # str | The email of the required user
account_id = 789 # int | Unique ID of the required account

try:
    # Get User Details By User Email and Account ID
    api_response = api_instance.get_user_by_user_email(user_email, account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->get_user_by_user_email: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_email** | **str**| The email of the required user | 
 **account_id** | **int**| Unique ID of the required account | 

### Return type

[**User**](User.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_assignments**
> list[User] update_assignments(body)

Assign Users To Roles or Delete Existing Assignment

Role management APIs for roles assignment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
body = [swagger_client.RequestedAssignment()] # list[RequestedAssignment] | The details required for the new assignments.

try:
    # Assign Users To Roles or Delete Existing Assignment
    api_response = api_instance.update_assignments(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->update_assignments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[RequestedAssignment]**](RequestedAssignment.md)| The details required for the new assignments. | 

### Return type

[**list[User]**](User.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_role**
> RoleDetails update_role(body, role_id)

Update Role Details By Role ID

Role management APIs for role management

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
body = swagger_client.UpdateRole() # UpdateRole | The details required for updating the role.
role_id = 789 # int | The role ID of the required role.

try:
    # Update Role Details By Role ID
    api_response = api_instance.update_role(body, role_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->update_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateRole**](UpdateRole.md)| The details required for updating the role. | 
 **role_id** | **int**| The role ID of the required role. | 

### Return type

[**RoleDetails**](RoleDetails.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

