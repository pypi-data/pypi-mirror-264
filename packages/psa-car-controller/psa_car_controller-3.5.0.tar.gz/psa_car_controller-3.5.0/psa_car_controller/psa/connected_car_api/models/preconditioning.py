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


class Preconditioning(object):
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
        'air_conditioning': 'PreconditioningAirConditioning'
    }

    attribute_map = {
        'air_conditioning': 'airConditioning'
    }

    def __init__(self, air_conditioning=None):  # noqa: E501
        """Preconditioning - a model defined in Swagger"""  # noqa: E501

        self._air_conditioning = None
        self.discriminator = None

        if air_conditioning is not None:
            self.air_conditioning = air_conditioning

    @property
    def air_conditioning(self):
        """Gets the air_conditioning of this Preconditioning.  # noqa: E501


        :return: The air_conditioning of this Preconditioning.  # noqa: E501
        :rtype: PreconditioningAirConditioning
        """
        return self._air_conditioning

    @air_conditioning.setter
    def air_conditioning(self, air_conditioning):
        """Sets the air_conditioning of this Preconditioning.


        :param air_conditioning: The air_conditioning of this Preconditioning.  # noqa: E501
        :type: PreconditioningAirConditioning
        """

        self._air_conditioning = air_conditioning

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
        if issubclass(Preconditioning, dict):
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
        if not isinstance(other, Preconditioning):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
