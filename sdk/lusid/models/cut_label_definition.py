# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.3273
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class CutLabelDefinition(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'code': 'str',
        'display_name': 'str',
        'description': 'str',
        'cut_local_time': 'CutLocalTime',
        'time_zone': 'str',
        'href': 'str',
        'links': 'list[Link]'
    }

    attribute_map = {
        'code': 'code',
        'display_name': 'displayName',
        'description': 'description',
        'cut_local_time': 'cutLocalTime',
        'time_zone': 'timeZone',
        'href': 'href',
        'links': 'links'
    }

    required_map = {
        'code': 'optional',
        'display_name': 'optional',
        'description': 'optional',
        'cut_local_time': 'optional',
        'time_zone': 'optional',
        'href': 'optional',
        'links': 'optional'
    }

    def __init__(self, code=None, display_name=None, description=None, cut_local_time=None, time_zone=None, href=None, links=None):  # noqa: E501
        """
        CutLabelDefinition - a model defined in OpenAPI

        :param code: 
        :type code: str
        :param display_name: 
        :type display_name: str
        :param description: 
        :type description: str
        :param cut_local_time: 
        :type cut_local_time: lusid.CutLocalTime
        :param time_zone: 
        :type time_zone: str
        :param href: 
        :type href: str
        :param links:  Collection of links.
        :type links: list[lusid.Link]

        """  # noqa: E501

        self._code = None
        self._display_name = None
        self._description = None
        self._cut_local_time = None
        self._time_zone = None
        self._href = None
        self._links = None
        self.discriminator = None

        self.code = code
        self.display_name = display_name
        self.description = description
        if cut_local_time is not None:
            self.cut_local_time = cut_local_time
        self.time_zone = time_zone
        self.href = href
        self.links = links

    @property
    def code(self):
        """Gets the code of this CutLabelDefinition.  # noqa: E501


        :return: The code of this CutLabelDefinition.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this CutLabelDefinition.


        :param code: The code of this CutLabelDefinition.  # noqa: E501
        :type: str
        """

        self._code = code

    @property
    def display_name(self):
        """Gets the display_name of this CutLabelDefinition.  # noqa: E501


        :return: The display_name of this CutLabelDefinition.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this CutLabelDefinition.


        :param display_name: The display_name of this CutLabelDefinition.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def description(self):
        """Gets the description of this CutLabelDefinition.  # noqa: E501


        :return: The description of this CutLabelDefinition.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CutLabelDefinition.


        :param description: The description of this CutLabelDefinition.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def cut_local_time(self):
        """Gets the cut_local_time of this CutLabelDefinition.  # noqa: E501


        :return: The cut_local_time of this CutLabelDefinition.  # noqa: E501
        :rtype: CutLocalTime
        """
        return self._cut_local_time

    @cut_local_time.setter
    def cut_local_time(self, cut_local_time):
        """Sets the cut_local_time of this CutLabelDefinition.


        :param cut_local_time: The cut_local_time of this CutLabelDefinition.  # noqa: E501
        :type: CutLocalTime
        """

        self._cut_local_time = cut_local_time

    @property
    def time_zone(self):
        """Gets the time_zone of this CutLabelDefinition.  # noqa: E501


        :return: The time_zone of this CutLabelDefinition.  # noqa: E501
        :rtype: str
        """
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        """Sets the time_zone of this CutLabelDefinition.


        :param time_zone: The time_zone of this CutLabelDefinition.  # noqa: E501
        :type: str
        """

        self._time_zone = time_zone

    @property
    def href(self):
        """Gets the href of this CutLabelDefinition.  # noqa: E501


        :return: The href of this CutLabelDefinition.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this CutLabelDefinition.


        :param href: The href of this CutLabelDefinition.  # noqa: E501
        :type: str
        """

        self._href = href

    @property
    def links(self):
        """Gets the links of this CutLabelDefinition.  # noqa: E501

        Collection of links.  # noqa: E501

        :return: The links of this CutLabelDefinition.  # noqa: E501
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this CutLabelDefinition.

        Collection of links.  # noqa: E501

        :param links: The links of this CutLabelDefinition.  # noqa: E501
        :type: list[Link]
        """

        self._links = links

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CutLabelDefinition):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
