# coding: utf-8

"""
    FINBOURNE Luminesce Web API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import re  # noqa: F401
import io
import warnings

from pydantic import validate_arguments, ValidationError
from typing import overload, Optional, Union, Awaitable

from typing_extensions import Annotated
from pydantic import Field, StrictBool, StrictStr

from typing import Optional


from luminesce.api_client import ApiClient
from luminesce.api_response import ApiResponse
from luminesce.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class CurrentTableFieldCatalogApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @overload
    async def get_catalog(self, free_text_search : Annotated[Optional[StrictStr], Field(description="Limit the catalog to only things in some way dealing with the passed in text string")] = None, json_proper : Annotated[Optional[StrictBool], Field(description="Should this be text/json (not json-encoded-as-a-string)")] = None, **kwargs) -> str:  # noqa: E501
        ...

    @overload
    def get_catalog(self, free_text_search : Annotated[Optional[StrictStr], Field(description="Limit the catalog to only things in some way dealing with the passed in text string")] = None, json_proper : Annotated[Optional[StrictBool], Field(description="Should this be text/json (not json-encoded-as-a-string)")] = None, async_req: Optional[bool]=True, **kwargs) -> str:  # noqa: E501
        ...

    @validate_arguments
    def get_catalog(self, free_text_search : Annotated[Optional[StrictStr], Field(description="Limit the catalog to only things in some way dealing with the passed in text string")] = None, json_proper : Annotated[Optional[StrictBool], Field(description="Should this be text/json (not json-encoded-as-a-string)")] = None, async_req: Optional[bool]=None, **kwargs) -> Union[str, Awaitable[str]]:  # noqa: E501
        """GetCatalog: Shows Table and Field level information on Providers that are currently running that you have access to (in Json format)  # noqa: E501

         The following LuminesceSql is executed to return this information:  ```sql @reg = select     Name,     min(Description) as Description,     min(DocumentationLink) as DocumentationLink,     iif(Category = 'View' and Client is not null, true, false) as IsView from     Sys.Registration where     Type in ('DirectProvider', 'DataProvider')     and      ShowAll = false group by     1     ;  @fld = select     TableName,     FieldName,     DataType,     FieldType,     IsPrimaryKey,     IsMain,     Description,     ParamDefaultValue,     TableParamColumns from     Sys.Field     ;  @x = select     coalesce(f.TableName, r.Name) as TableName,     coalesce(f.FieldName, 'N/A') as FieldName,     f.DataType,     f.FieldType,     f.IsPrimaryKey,     f.IsMain,     case          when f.TableName is not null then             f.Description         else             r.Name || ' returns a different set of columns depending on use.'         end as Description,     f.ParamDefaultValue,     f.TableParamColumns,     r.Description as ProviderDescription,     r.DocumentationLink,     r.IsView from     @reg r     left outer join @fld f         on r.Name = f.TableName order by     1, 5 desc, 6 desc, 2     ;     ```  The following error codes are to be anticipated with standard Problem Detail reports: - 401 Unauthorized   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_catalog(free_text_search, json_proper, async_req=True)
        >>> result = thread.get()

        :param free_text_search: Limit the catalog to only things in some way dealing with the passed in text string
        :type free_text_search: str
        :param json_proper: Should this be text/json (not json-encoded-as-a-string)
        :type json_proper: bool
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: str
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the get_catalog_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        if async_req is not None:
            kwargs['async_req'] = async_req
        return self.get_catalog_with_http_info(free_text_search, json_proper, **kwargs)  # noqa: E501

    @validate_arguments
    def get_catalog_with_http_info(self, free_text_search : Annotated[Optional[StrictStr], Field(description="Limit the catalog to only things in some way dealing with the passed in text string")] = None, json_proper : Annotated[Optional[StrictBool], Field(description="Should this be text/json (not json-encoded-as-a-string)")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """GetCatalog: Shows Table and Field level information on Providers that are currently running that you have access to (in Json format)  # noqa: E501

         The following LuminesceSql is executed to return this information:  ```sql @reg = select     Name,     min(Description) as Description,     min(DocumentationLink) as DocumentationLink,     iif(Category = 'View' and Client is not null, true, false) as IsView from     Sys.Registration where     Type in ('DirectProvider', 'DataProvider')     and      ShowAll = false group by     1     ;  @fld = select     TableName,     FieldName,     DataType,     FieldType,     IsPrimaryKey,     IsMain,     Description,     ParamDefaultValue,     TableParamColumns from     Sys.Field     ;  @x = select     coalesce(f.TableName, r.Name) as TableName,     coalesce(f.FieldName, 'N/A') as FieldName,     f.DataType,     f.FieldType,     f.IsPrimaryKey,     f.IsMain,     case          when f.TableName is not null then             f.Description         else             r.Name || ' returns a different set of columns depending on use.'         end as Description,     f.ParamDefaultValue,     f.TableParamColumns,     r.Description as ProviderDescription,     r.DocumentationLink,     r.IsView from     @reg r     left outer join @fld f         on r.Name = f.TableName order by     1, 5 desc, 6 desc, 2     ;     ```  The following error codes are to be anticipated with standard Problem Detail reports: - 401 Unauthorized   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_catalog_with_http_info(free_text_search, json_proper, async_req=True)
        >>> result = thread.get()

        :param free_text_search: Limit the catalog to only things in some way dealing with the passed in text string
        :type free_text_search: str
        :param json_proper: Should this be text/json (not json-encoded-as-a-string)
        :type json_proper: bool
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(str, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'free_text_search',
            'json_proper'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_catalog" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('free_text_search') is not None:  # noqa: E501
            _query_params.append(('freeTextSearch', _params['free_text_search']))

        if _params.get('json_proper') is not None:  # noqa: E501
            _query_params.append(('jsonProper', _params['json_proper']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['oauth2']  # noqa: E501

        _response_types_map = {
            '200': "str",
        }

        return self.api_client.call_api(
            '/api/Catalog', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
