# coding: utf-8

"""
    Groupe PSA Connected Car - WEB API B2C

    *PSA B2C Connected Car API*  # Introduction This is the description of the *Groupe PSA Connected Car V2 API*. The speccification is  is based on **OpenAPI Specification version 3** and can be displayed via [ReDoc](https://github.com/Rebilly/ReDoc)a or [Swagger](http://swagger.io).   This API allows applications to fetch data from the connected Vehicles data platform. # Authentication PSA Connected Car APIs uses the [OAuth 2.0](https://tools.ietf.org/html/rfc6749) protocol for authentication and Authorization. any application require a valid [Access Token](https://tools.ietf.org/html/rfc6749#section-1.4) to access to user data. # Errors   Error codes returned by all REST APIs comply with the standard. Nevertheless, PSA Services (callers) need to have more complete data structures (even when the answer is not Http-OK) to better detail the type of error by providing application code, message and a debugging code(for investigation purposes). The http code of the response is managed by the protocol itself (in the header).      **Errors are  returned as a generic error response:**    * ```xError``` object model.       # noqa: E501

    OpenAPI spec version: 4.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class TabLinks(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'first': 'Link',
        'last': 'Link',
        'next': 'Link',
        'prev': 'Link',
        '_self': 'Link'
    }

    attribute_map = {
        'first': 'first',
        'last': 'last',
        'next': 'next',
        'prev': 'prev',
        '_self': 'self'
    }

    def __init__(self, first=None, last=None, next=None, prev=None, _self=None):  # noqa: E501
        """TabLinks - a model defined in Swagger"""  # noqa: E501

        self._first = None
        self._last = None
        self._next = None
        self._prev = None
        self.__self = None
        self.discriminator = None

        if first is not None:
            self.first = first
        if last is not None:
            self.last = last
        if next is not None:
            self.next = next
        if prev is not None:
            self.prev = prev
        if _self is not None:
            self._self = _self

    @property
    def first(self):
        """Gets the first of this TabLinks.  # noqa: E501


        :return: The first of this TabLinks.  # noqa: E501
        :rtype: Link
        """
        return self._first

    @first.setter
    def first(self, first):
        """Sets the first of this TabLinks.


        :param first: The first of this TabLinks.  # noqa: E501
        :type: Link
        """

        self._first = first

    @property
    def last(self):
        """Gets the last of this TabLinks.  # noqa: E501


        :return: The last of this TabLinks.  # noqa: E501
        :rtype: Link
        """
        return self._last

    @last.setter
    def last(self, last):
        """Sets the last of this TabLinks.


        :param last: The last of this TabLinks.  # noqa: E501
        :type: Link
        """

        self._last = last

    @property
    def next(self):
        """Gets the next of this TabLinks.  # noqa: E501


        :return: The next of this TabLinks.  # noqa: E501
        :rtype: Link
        """
        return self._next

    @next.setter
    def next(self, next):
        """Sets the next of this TabLinks.


        :param next: The next of this TabLinks.  # noqa: E501
        :type: Link
        """

        self._next = next

    @property
    def prev(self):
        """Gets the prev of this TabLinks.  # noqa: E501


        :return: The prev of this TabLinks.  # noqa: E501
        :rtype: Link
        """
        return self._prev

    @prev.setter
    def prev(self, prev):
        """Sets the prev of this TabLinks.


        :param prev: The prev of this TabLinks.  # noqa: E501
        :type: Link
        """

        self._prev = prev

    @property
    def _self(self):
        """Gets the _self of this TabLinks.  # noqa: E501


        :return: The _self of this TabLinks.  # noqa: E501
        :rtype: Link
        """
        return self.__self

    @_self.setter
    def _self(self, _self):
        """Sets the _self of this TabLinks.


        :param _self: The _self of this TabLinks.  # noqa: E501
        :type: Link
        """

        self.__self = _self

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(TabLinks, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TabLinks):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
