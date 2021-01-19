# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.2492
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class Quote(object):
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
        'quote_id': 'QuoteId',
        'metric_value': 'MetricValue',
        'lineage': 'str',
        'cut_label': 'str',
        'uploaded_by': 'str',
        'as_at': 'datetime'
    }

    attribute_map = {
        'quote_id': 'quoteId',
        'metric_value': 'metricValue',
        'lineage': 'lineage',
        'cut_label': 'cutLabel',
        'uploaded_by': 'uploadedBy',
        'as_at': 'asAt'
    }

    required_map = {
        'quote_id': 'required',
        'metric_value': 'optional',
        'lineage': 'optional',
        'cut_label': 'optional',
        'uploaded_by': 'required',
        'as_at': 'required'
    }

    def __init__(self, quote_id=None, metric_value=None, lineage=None, cut_label=None, uploaded_by=None, as_at=None):  # noqa: E501
        """
        Quote - a model defined in OpenAPI

        :param quote_id:  (required)
        :type quote_id: lusid.QuoteId
        :param metric_value: 
        :type metric_value: lusid.MetricValue
        :param lineage:  Description of the quote's lineage e.g. 'FundAccountant_GreenQuality'.
        :type lineage: str
        :param cut_label:  The cut label that this quote was updated or inserted with.
        :type cut_label: str
        :param uploaded_by:  The unique id of the user that updated or inserted the quote. (required)
        :type uploaded_by: str
        :param as_at:  The asAt datetime at which the quote was committed to LUSID. (required)
        :type as_at: datetime

        """  # noqa: E501

        self._quote_id = None
        self._metric_value = None
        self._lineage = None
        self._cut_label = None
        self._uploaded_by = None
        self._as_at = None
        self.discriminator = None

        self.quote_id = quote_id
        if metric_value is not None:
            self.metric_value = metric_value
        self.lineage = lineage
        self.cut_label = cut_label
        self.uploaded_by = uploaded_by
        self.as_at = as_at

    @property
    def quote_id(self):
        """Gets the quote_id of this Quote.  # noqa: E501


        :return: The quote_id of this Quote.  # noqa: E501
        :rtype: QuoteId
        """
        return self._quote_id

    @quote_id.setter
    def quote_id(self, quote_id):
        """Sets the quote_id of this Quote.


        :param quote_id: The quote_id of this Quote.  # noqa: E501
        :type: QuoteId
        """
        if quote_id is None:
            raise ValueError("Invalid value for `quote_id`, must not be `None`")  # noqa: E501

        self._quote_id = quote_id

    @property
    def metric_value(self):
        """Gets the metric_value of this Quote.  # noqa: E501


        :return: The metric_value of this Quote.  # noqa: E501
        :rtype: MetricValue
        """
        return self._metric_value

    @metric_value.setter
    def metric_value(self, metric_value):
        """Sets the metric_value of this Quote.


        :param metric_value: The metric_value of this Quote.  # noqa: E501
        :type: MetricValue
        """

        self._metric_value = metric_value

    @property
    def lineage(self):
        """Gets the lineage of this Quote.  # noqa: E501

        Description of the quote's lineage e.g. 'FundAccountant_GreenQuality'.  # noqa: E501

        :return: The lineage of this Quote.  # noqa: E501
        :rtype: str
        """
        return self._lineage

    @lineage.setter
    def lineage(self, lineage):
        """Sets the lineage of this Quote.

        Description of the quote's lineage e.g. 'FundAccountant_GreenQuality'.  # noqa: E501

        :param lineage: The lineage of this Quote.  # noqa: E501
        :type: str
        """

        self._lineage = lineage

    @property
    def cut_label(self):
        """Gets the cut_label of this Quote.  # noqa: E501

        The cut label that this quote was updated or inserted with.  # noqa: E501

        :return: The cut_label of this Quote.  # noqa: E501
        :rtype: str
        """
        return self._cut_label

    @cut_label.setter
    def cut_label(self, cut_label):
        """Sets the cut_label of this Quote.

        The cut label that this quote was updated or inserted with.  # noqa: E501

        :param cut_label: The cut_label of this Quote.  # noqa: E501
        :type: str
        """

        self._cut_label = cut_label

    @property
    def uploaded_by(self):
        """Gets the uploaded_by of this Quote.  # noqa: E501

        The unique id of the user that updated or inserted the quote.  # noqa: E501

        :return: The uploaded_by of this Quote.  # noqa: E501
        :rtype: str
        """
        return self._uploaded_by

    @uploaded_by.setter
    def uploaded_by(self, uploaded_by):
        """Sets the uploaded_by of this Quote.

        The unique id of the user that updated or inserted the quote.  # noqa: E501

        :param uploaded_by: The uploaded_by of this Quote.  # noqa: E501
        :type: str
        """
        if uploaded_by is None:
            raise ValueError("Invalid value for `uploaded_by`, must not be `None`")  # noqa: E501

        self._uploaded_by = uploaded_by

    @property
    def as_at(self):
        """Gets the as_at of this Quote.  # noqa: E501

        The asAt datetime at which the quote was committed to LUSID.  # noqa: E501

        :return: The as_at of this Quote.  # noqa: E501
        :rtype: datetime
        """
        return self._as_at

    @as_at.setter
    def as_at(self, as_at):
        """Sets the as_at of this Quote.

        The asAt datetime at which the quote was committed to LUSID.  # noqa: E501

        :param as_at: The as_at of this Quote.  # noqa: E501
        :type: datetime
        """
        if as_at is None:
            raise ValueError("Invalid value for `as_at`, must not be `None`")  # noqa: E501

        self._as_at = as_at

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
        if not isinstance(other, Quote):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
