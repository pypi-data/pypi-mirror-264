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


class PositionProperties(object):
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
        'heading': 'float',
        'signal_quality': 'float',
        'type': 'str',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'heading': 'heading',
        'signal_quality': 'signalQuality',
        'type': 'type',
        'updated_at': 'createdAt'
    }

    def __init__(self, heading=None, signal_quality=None, type=None, updated_at=None):  # noqa: E501
        """PositionProperties - a model defined in Swagger"""  # noqa: E501

        self._heading = None
        self._signal_quality = None
        self._type = None
        self._updated_at = None
        self.discriminator = None

        if heading is not None:
            self.heading = heading
        if signal_quality is not None:
            self.signal_quality = signal_quality
        if type is not None:
            self.type = type
        if updated_at is not None:
            self.updated_at = updated_at

    @property
    def heading(self):
        """Gets the heading of this PositionProperties.  # noqa: E501


        :return: The heading of this PositionProperties.  # noqa: E501
        :rtype: float
        """
        return self._heading

    @heading.setter
    def heading(self, heading):
        """Sets the heading of this PositionProperties.


        :param heading: The heading of this PositionProperties.  # noqa: E501
        :type: float
        """
        if heading is not None and heading > 360:  # noqa: E501
            raise ValueError("Invalid value for `heading`, must be a value less than or equal to `360`")  # noqa: E501
        if heading is not None and heading < 0:  # noqa: E501
            raise ValueError("Invalid value for `heading`, must be a value greater than or equal to `0`")  # noqa: E501

        self._heading = heading

    @property
    def signal_quality(self):
        """Gets the signal_quality of this PositionProperties.  # noqa: E501


        :return: The signal_quality of this PositionProperties.  # noqa: E501
        :rtype: float
        """
        return self._signal_quality

    @signal_quality.setter
    def signal_quality(self, signal_quality):
        """Sets the signal_quality of this PositionProperties.


        :param signal_quality: The signal_quality of this PositionProperties.  # noqa: E501
        :type: float
        """

        self._signal_quality = signal_quality

    @property
    def type(self):
        """Gets the type of this PositionProperties.  # noqa: E501


        :return: The type of this PositionProperties.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this PositionProperties.


        :param type: The type of this PositionProperties.  # noqa: E501
        :type: str
        """
        allowed_values = ["Estimated", "Acquired", "Estimate", "Acquire"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def updated_at(self):
        """Gets the updated_at of this PositionProperties.  # noqa: E501


        :return: The updated_at of this PositionProperties.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this PositionProperties.


        :param updated_at: The updated_at of this PositionProperties.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

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
        if issubclass(PositionProperties, dict):
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
        if not isinstance(other, PositionProperties):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
