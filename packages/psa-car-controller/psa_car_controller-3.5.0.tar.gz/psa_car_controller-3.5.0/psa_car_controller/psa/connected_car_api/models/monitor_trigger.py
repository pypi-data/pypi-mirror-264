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


class MonitorTrigger(object):
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
        'data': 'DataTrigger',
        'name': 'str',
        'time': 'TimeTrigger',
        'zone': 'ZoneTrigger'
    }

    attribute_map = {
        'data': 'data',
        'name': 'name',
        'time': 'time',
        'zone': 'zone'
    }

    def __init__(self, data=None, name=None, time=None, zone=None):  # noqa: E501
        """MonitorTrigger - a model defined in Swagger"""  # noqa: E501

        self._data = None
        self._name = None
        self._time = None
        self._zone = None
        self.discriminator = None

        if data is not None:
            self.data = data
        self.name = name
        if time is not None:
            self.time = time
        if zone is not None:
            self.zone = zone

    @property
    def data(self):
        """Gets the data of this MonitorTrigger.  # noqa: E501


        :return: The data of this MonitorTrigger.  # noqa: E501
        :rtype: DataTrigger
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this MonitorTrigger.


        :param data: The data of this MonitorTrigger.  # noqa: E501
        :type: DataTrigger
        """

        self._data = data

    @property
    def name(self):
        """Gets the name of this MonitorTrigger.  # noqa: E501

        The trigger name(should be uniq)  # noqa: E501

        :return: The name of this MonitorTrigger.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MonitorTrigger.

        The trigger name(should be uniq)  # noqa: E501

        :param name: The name of this MonitorTrigger.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def time(self):
        """Gets the time of this MonitorTrigger.  # noqa: E501


        :return: The time of this MonitorTrigger.  # noqa: E501
        :rtype: TimeTrigger
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this MonitorTrigger.


        :param time: The time of this MonitorTrigger.  # noqa: E501
        :type: TimeTrigger
        """

        self._time = time

    @property
    def zone(self):
        """Gets the zone of this MonitorTrigger.  # noqa: E501


        :return: The zone of this MonitorTrigger.  # noqa: E501
        :rtype: ZoneTrigger
        """
        return self._zone

    @zone.setter
    def zone(self, zone):
        """Sets the zone of this MonitorTrigger.


        :param zone: The zone of this MonitorTrigger.  # noqa: E501
        :type: ZoneTrigger
        """

        self._zone = zone

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
        if issubclass(MonitorTrigger, dict):
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
        if not isinstance(other, MonitorTrigger):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
