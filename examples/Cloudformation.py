# This is an example of a CloudFormation

from troposphere import (
    Template, Parameter, Ref, Condition, Equals, And, Or, Not, If
)
import troposphere.cloudformation as cloudformation

t = Template()

t.add_version("2010-09-09")

auth = t.add_resource(cloudformation.Authentication(
    "TestCFAuth",
    blocks={
        'testS3': {
            'type': 'S3',
            'accessKeyId': Ref('AccessKeyID'),
            'secretKey': Ref('SecretAccessKeyID'),
            'buckets': ['myawsbucket'],
        },
        'testBasic': {
            'type': 'basic',
            'username': Ref('UserName'),
            'password': Ref('Password'),
            'uris': ['http://www.example.com/test'],
        },
        'rolebased': {
            'type': 's3',
            'buckets': ['myBucket'],
            'roleName': Ref('myRole'),
        }
    }
))

print(t.to_json())
