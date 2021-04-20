# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.2876
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from lusid.api_client import ApiClient
from lusid.exceptions import (
    ApiTypeError,
    ApiValueError
)


class PersonsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_person_relations(self, id_type_scope, id_type_code, code, **kwargs):  # noqa: E501
        """[DEPRECATED] Get Relations for Person  # noqa: E501

        Get relations for the specified person.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_person_relations(id_type_scope, id_type_code, code, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_type_scope: Scope of the person identifier type. (required)
        :param str id_type_code: Code of the person identifier type. (required)
        :param str code: Code of the person under specified identifier type's scope and code. This together with stated identifier type uniquely              identifies the person. (required)
        :param str effective_at: The effective datetime or cut label at which to get relations. Defaults to the current LUSID system datetime if not specified.
        :param datetime as_at: The asAt datetime at which to retrieve the person's relations. Defaults to return the latest LUSID AsAt time if not specified.
        :param str filter: Expression to filter the relations. Users should provide null or empty string for this field until further notice.
        :param list[str] identifier_types: Identifiers types (as property keys) used for referencing Persons or Legal Entities. These take the format              {domain}/{scope}/{code} e.g. \"Person/CompanyDetails/Role\". They must be from the \"Person\" or \"LegalEntity\" domain.              Only identifier types stated will be used to look up relevant entities in relations. If not applicable, provide an empty array.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ResourceListOfRelation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_person_relations_with_http_info(id_type_scope, id_type_code, code, **kwargs)  # noqa: E501

    def get_person_relations_with_http_info(self, id_type_scope, id_type_code, code, **kwargs):  # noqa: E501
        """[DEPRECATED] Get Relations for Person  # noqa: E501

        Get relations for the specified person.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_person_relations_with_http_info(id_type_scope, id_type_code, code, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_type_scope: Scope of the person identifier type. (required)
        :param str id_type_code: Code of the person identifier type. (required)
        :param str code: Code of the person under specified identifier type's scope and code. This together with stated identifier type uniquely              identifies the person. (required)
        :param str effective_at: The effective datetime or cut label at which to get relations. Defaults to the current LUSID system datetime if not specified.
        :param datetime as_at: The asAt datetime at which to retrieve the person's relations. Defaults to return the latest LUSID AsAt time if not specified.
        :param str filter: Expression to filter the relations. Users should provide null or empty string for this field until further notice.
        :param list[str] identifier_types: Identifiers types (as property keys) used for referencing Persons or Legal Entities. These take the format              {domain}/{scope}/{code} e.g. \"Person/CompanyDetails/Role\". They must be from the \"Person\" or \"LegalEntity\" domain.              Only identifier types stated will be used to look up relevant entities in relations. If not applicable, provide an empty array.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ResourceListOfRelation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_type_scope', 'id_type_code', 'code', 'effective_at', 'as_at', 'filter', 'identifier_types']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_person_relations" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if ('code' in local_var_params and
                len(local_var_params['code']) > 64):
            raise ApiValueError("Invalid value for parameter `code` when calling `get_person_relations`, length must be less than or equal to `64`")  # noqa: E501
        if ('code' in local_var_params and
                len(local_var_params['code']) < 1):
            raise ApiValueError("Invalid value for parameter `code` when calling `get_person_relations`, length must be greater than or equal to `1`")  # noqa: E501
        if 'code' in local_var_params and not re.search(r'^[a-zA-Z0-9\-_]+$', local_var_params['code']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `code` when calling `get_person_relations`, must conform to the pattern `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'id_type_scope' in local_var_params:
            path_params['idTypeScope'] = local_var_params['id_type_scope']  # noqa: E501
        if 'id_type_code' in local_var_params:
            path_params['idTypeCode'] = local_var_params['id_type_code']  # noqa: E501
        if 'code' in local_var_params:
            path_params['code'] = local_var_params['code']  # noqa: E501

        query_params = []
        if 'effective_at' in local_var_params:
            query_params.append(('effectiveAt', local_var_params['effective_at']))  # noqa: E501
        if 'as_at' in local_var_params:
            query_params.append(('asAt', local_var_params['as_at']))  # noqa: E501
        if 'filter' in local_var_params:
            query_params.append(('filter', local_var_params['filter']))  # noqa: E501
        if 'identifier_types' in local_var_params:
            query_params.append(('identifierTypes', local_var_params['identifier_types']))  # noqa: E501
            collection_formats['identifierTypes'] = 'multi'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501


        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        # set the LUSID header
        header_params['X-LUSID-SDK-Language'] = 'Python'
        header_params['X-LUSID-SDK-Version'] = '0.11.2876'

        return self.api_client.call_api(
            '/api/persons/{idTypeScope}/{idTypeCode}/{code}/relations', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ResourceListOfRelation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
