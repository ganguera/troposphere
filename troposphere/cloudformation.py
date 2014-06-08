# Copyright (c) 2013, Mark Peek <mark@peek.org>
# Copyright (c) 2014, Guillem Anguera <ganguera@gmail.com>
# All rights reserved.
#
# See LICENSE file for full license.

from . import BaseAWSObject, AWSObject, AWSHelperFn, Ref
from .validators import integer
import types


class AWSCFAuthenticationObject(BaseAWSObject):
    dictname = None

    def validate(self):
        pass

    def JSONrepr(self):
        for name, value in self.resource.iteritems():
            if isinstance(value, list):
                for k, (prop_type, required) in self.props.items():
                    if required and k not in value:
                        type = getattr(self, 'type', "<unknown type>")
                        raise ValueError("Resource %s required in type %s"
                                         % (k, type))
            self.validate()
        return self.resource

    def __init__(self, *args, **kwargs):
        self.blocks = kwargs.pop('blocks', None)
        super(AWSCFAuthenticationObject, self).__init__(*args, **kwargs)

        blocknames = self.blocks.keys()

        for blockname in blocknames:
            self.resource.update({blockname: {}})

        for blockname in blocknames:
            for name, value in self.blocks[blockname].iteritems():
                if name in self.propnames:
                    # Check the type of the object and compare against what we
                    # were expecting.
                    expected_type = self.props[name][0]

                    # If the value is a AWSHelperFn we can't do much validation
                    # we'll have to leave that to Amazon.  Maybe there's
                    # another way to deal with this that we'll come up with
                    # eventually
                    if isinstance(value, AWSHelperFn):
                        pass

                    # If it's a list of types, check against those types...
                    elif isinstance(expected_type, list):
                        # If we're expecting a list, then make sure it is a
                        # list
                        if not isinstance(value, list):
                            self._raise_type(name, value, expected_type)

                        # Iterate over the list and make sure it matches our
                        # type checks
                        for v in value:
                            if not isinstance(v, tuple(expected_type)):
                                self._raise_type(name, v, expected_type)

                    # Single type so check the type of the object and compare
                    # against what we were expecting. Special case AWS helper
                    # functions.
                    elif isinstance(value, expected_type):
                        pass
                    else:
                        self._raise_type(name, value, expected_type)
                else:
                    raise AttributeError("%s object does not support attribute"
                                         " %s in user block %s" %
                                         (self.type, name, blockname))

            self.resource[blockname] = self.blocks[blockname]


class Authentication(AWSCFAuthenticationObject):
    type = "AWS::CloudFormation::Authentication"

    props = {
        'accessKeyId': (basestring, False),
        'buckets': ([basestring], False),
        'password': (basestring, False),
        'secretKey': (basestring, False),
        'type': (basestring, True),
        'uris': ([basestring], False),
        'username': (basestring, False),
        'roleName': (basestring, False),
    }


class Stack(AWSObject):
    type = "AWS::CloudFormation::Stack"

    props = {
        'TemplateURL': (basestring, True),
        'TimeoutInMinutes': (integer, False),
        'Parameters': (dict, False),
    }


class WaitCondition(AWSObject):
    type = "AWS::CloudFormation::WaitCondition"

    props = {
        'Count': (integer, False),
        'Handle': (Ref, True),
        'Timeout': (integer, True),
    }


class WaitConditionHandle(AWSObject):
    type = "AWS::CloudFormation::WaitConditionHandle"

    props = {}
