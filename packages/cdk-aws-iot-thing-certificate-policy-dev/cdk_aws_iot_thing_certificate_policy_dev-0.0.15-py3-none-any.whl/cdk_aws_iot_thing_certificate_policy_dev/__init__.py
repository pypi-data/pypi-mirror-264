'''
# cdk-aws-iot-thing-certificate-policy

An [L3 CDK construct](https://docs.aws.amazon.com/cdk/v2/guide/constructs.html#constructs_lib) to create and associate a singular AWS IoT Thing, Certificate, and IoT Policy. The construct also retrieves and returns AWS IoT account specific details such as the AWS IoT data endpoint and the AWS IoT Credential provider endpoint.

The certificate and its private key are stored as AWS Systems Manager Parameter Store parameters that can be retrieved via the AWS Console or programmatically via construct members.

## Installation

### TypeScript

```shell
npm install cdk-aws-iot-thing-certificate-policy
```

[API Reference](doc/api-typescript.md)

### TypeScript

```shell
pip install cdk-aws-iot-thing-certificate-policy
```

[API Reference](doc/api-python.md)

## Examples

#### TypeScript

```python
import * as cdk from "aws-cdk-lib";
import { IotThingCertificatePolicy } from "cdk-aws-iot-thing-certificate-policy-dev";
/**
 * A minimum IoT Policy template using substitution variables for actual
 * policy to be deployed for "region", "account", and "thingname". Allows
 * the thing to publish and subscribe on any topics under "thing/*" topic
 * namespace. Normal IoT Policy conventions such as "*", apply.
 */
export const minimalIoTPolicy = `{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["iot:Connect"],
      "Resource": "arn:aws:iot:{{region}}:{{account}}:client/{{thingname}}"
    },
    {
      "Effect": "Allow",
      "Action": ["iot:Publish"],
      "Resource": [
        "arn:aws:iot:{{region}}:{{account}}:topic/{{thingname}}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["iot:Subscribe"],
      "Resource": [
        "arn:aws:iot:{{region}}:{{account}}:topicfilter/{{thingname}}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["iot:Receive"],
      "Resource": [
        "arn:aws:iot:{{region}}:{{account}}:topic/{{thingname}}/*"
      ]
    }
  ]
}`;

/**
 * Create the thing, certificate, and policy, then associate the
 * certificate to both the thing and the policy and fully activate.
 */
const fooThing = new IotThingCertificatePolicy(this, "MyFooThing", {
  thingName: "foo-thing", // Name to assign to AWS IoT thing, and value for {{thingname}} in policy template
  iotPolicyName: "foo-iot-policy", // Name to assign to AWS IoT policy
  iotPolicy: minimalIoTPolicy, // Policy with or without substitution parameters from above
  encryptionAlgorithm: "ECC", // Algorithm to use to private key (RSA or ECC)
  policyParameterMapping: [
    // substitution names and values for AWS IoT policy template, e.g., {{region}} and {{account}}
    {
      name: "region",
      value: cdk.Fn.ref("AWS::Region"),
    },
    {
      name: "account",
      value: cdk.Fn.ref("AWS::AccountId"),
    },
  ],
});

// The AWS IoT Thing Arn as a stack output
new cdk.CfnOutput(this, "ThingArn", {
  value: iotThing.thingArn,
});
// The AWS account unique endpoint for the MQTT data connection
// See API for other available public values that can be referenced
new cdk.CfnOutput(this, "IotEndpoint", {
  value: iotThing.dataAtsEndpointAddress,
});
```

#### Python

```python
import awsk_cdk
from cdk_aws_iot_thing_certificate_policy_dev import (
    IotThingCertificatePolicy,
)

minimal_iot_policy = """{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["iot:Connect"],
      "Resource": "arn:aws:iot:{{region}}:{{account}}:client/{{thingname}}"
    },
    {
      "Effect": "Allow",
      "Action": ["iot:Publish"],
      "Resource": [
        "arn:aws:iot:{{region}}:{{account}}:topic/{{thingname}}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["iot:Subscribe"],
      "Resource": [
        "arn:aws:iot:{{region}}:{{account}}:topicfilter/{{thingname}}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["iot:Receive"],
      "Resource": [
        "arn:aws:iot:{{region}}:{{account}}:topic/{{thingname}}/*"
      ]
    }
  ]
}"""
foo_thing = IotThingCertificatePolicy(
    self,
    "MyFooThing",
    thing_name="foo-thin",
    iot_policy_name="foo-iot-policy",
    iot_policy=minimal_iot_policy,
    encryption_algorithm="ECC",
    policy_parameter_mapping=[
        {
            "name": "region",
            "value":aws_cdk.Fn.ref("AWS::Region")
        },
        {
            "name": "account",
            "value":aws_cdk.Fn.ref("AWS::AccountId")
        }
    ],
)
aws_cdk.CfnOutput(self, "ThingArn", value=foo.thing_arn)
aws_cdk.CfnOutput(self, "IotEndpoint", value=foo.data_ats_endpoint_address)
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import constructs as _constructs_77d1e7e8


class IotThingCertificatePolicy(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iot-thing-certificate-policy-dev.IotThingCertificatePolicy",
):
    '''(experimental) Creates and associates an AWS IoT thing, AWS IoT certificate, and AWS IoT policy.

    It attaches the certificate to the thing and policy, and then stores the certificate
    and private key in AWS Systems Manager Parameter Store parameters for reference
    outside of the CloudFormation stack or by other constructs.

    Use this construct to create and delete a thing, certificate (principal), and IoT policy for
    testing or other singular uses. **Note:** Destroying this stack will fully detach and delete
    all created IoT resources.

    :stability: experimental
    :summary: Creates and associates an AWS IoT thing, certificate and policy.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        iot_policy: builtins.str,
        iot_policy_name: builtins.str,
        thing_name: builtins.str,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        policy_parameter_mapping: typing.Optional[typing.Sequence[typing.Union["PolicyMapping", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: Represents the scope for all the resources.
        :param id: This is a scope-unique id.
        :param iot_policy: (experimental) The AWS IoT policy in JSON format to be created and attached to the certificate. This is a JSON string that uses `mustache-compatible <https://handlebarsjs.com/guide/>`_ template substitution to create the AWS IoT policy. Default: - None
        :param iot_policy_name: (experimental) Name of the AWS IoT Core policy to create. Default: - None
        :param thing_name: (experimental) Name of AWS IoT thing to create. Default: - None
        :param encryption_algorithm: (experimental) Selects RSA or ECC private key and certificate generation. If not provided, ``RSA`` will be used. Default: - RSA
        :param policy_parameter_mapping: (experimental) Optional: A ``PolicyMapping`` object of parameters and values to be replaced if a `mustache-compatible <https://handlebarsjs.com/guide/>`_ template is provided as the ``iotPolicy`` (see example). For each matching parameter in the policy template, the value will be used. If not provided, only the ``{{thingname}}`` mapping will be available for the ``iotPolicy`` template. Default: - None

        :stability: experimental
        :since: 2.132.0
        :summary: Constructs a new instance of the ``IotThingCertificatePolicy`` class.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b25a5ec66e5d9c59bbcc5ef88d9deddda593ee06e2e64b7b9e8de48b690a600)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IotThingCertificatePolicyProps(
            iot_policy=iot_policy,
            iot_policy_name=iot_policy_name,
            thing_name=thing_name,
            encryption_algorithm=encryption_algorithm,
            policy_parameter_mapping=policy_parameter_mapping,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        '''(experimental) Arn of created AWS IoT Certificate.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @builtins.property
    @jsii.member(jsii_name="certificatePemParameter")
    def certificate_pem_parameter(self) -> builtins.str:
        '''(experimental) Fully qualified name in AWS Systems Manager Parameter Store of the certificate in ``PEM`` format.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificatePemParameter"))

    @builtins.property
    @jsii.member(jsii_name="credentialProviderEndpointAddress")
    def credential_provider_endpoint_address(self) -> builtins.str:
        '''(experimental) Fully qualified domain name of the AWS IoT Credential provider endpoint specific to this AWS account and AWS region.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "credentialProviderEndpointAddress"))

    @builtins.property
    @jsii.member(jsii_name="dataAtsEndpointAddress")
    def data_ats_endpoint_address(self) -> builtins.str:
        '''(experimental) Fully qualified domain name of the AWS IoT Core data plane endpoint specific to this AWS account and AWS region.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataAtsEndpointAddress"))

    @builtins.property
    @jsii.member(jsii_name="iotPolicyArn")
    def iot_policy_arn(self) -> builtins.str:
        '''(experimental) Arn of created AWS IoT Policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "iotPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="privateKeySecretParameter")
    def private_key_secret_parameter(self) -> builtins.str:
        '''(experimental) Fully qualified name in AWS Systems Manager Parameter Store of the certificate's private key in ``PEM`` format.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "privateKeySecretParameter"))

    @builtins.property
    @jsii.member(jsii_name="thingArn")
    def thing_arn(self) -> builtins.str:
        '''(experimental) Arn of created AWS IoT Thing.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "thingArn"))


@jsii.data_type(
    jsii_type="cdk-aws-iot-thing-certificate-policy-dev.IotThingCertificatePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "iot_policy": "iotPolicy",
        "iot_policy_name": "iotPolicyName",
        "thing_name": "thingName",
        "encryption_algorithm": "encryptionAlgorithm",
        "policy_parameter_mapping": "policyParameterMapping",
    },
)
class IotThingCertificatePolicyProps:
    def __init__(
        self,
        *,
        iot_policy: builtins.str,
        iot_policy_name: builtins.str,
        thing_name: builtins.str,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        policy_parameter_mapping: typing.Optional[typing.Sequence[typing.Union["PolicyMapping", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param iot_policy: (experimental) The AWS IoT policy in JSON format to be created and attached to the certificate. This is a JSON string that uses `mustache-compatible <https://handlebarsjs.com/guide/>`_ template substitution to create the AWS IoT policy. Default: - None
        :param iot_policy_name: (experimental) Name of the AWS IoT Core policy to create. Default: - None
        :param thing_name: (experimental) Name of AWS IoT thing to create. Default: - None
        :param encryption_algorithm: (experimental) Selects RSA or ECC private key and certificate generation. If not provided, ``RSA`` will be used. Default: - RSA
        :param policy_parameter_mapping: (experimental) Optional: A ``PolicyMapping`` object of parameters and values to be replaced if a `mustache-compatible <https://handlebarsjs.com/guide/>`_ template is provided as the ``iotPolicy`` (see example). For each matching parameter in the policy template, the value will be used. If not provided, only the ``{{thingname}}`` mapping will be available for the ``iotPolicy`` template. Default: - None

        :stability: experimental
        :summary:

        The properties for the IotThingCertificatePolicy class.

        Properties for defining an AWS IoT thing, AWS IoT certificate, and AWS IoT
        policy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0be38e2a9971125086bd1c703f7f38ac53a8d8e658569b4f88f8005e1846240)
            check_type(argname="argument iot_policy", value=iot_policy, expected_type=type_hints["iot_policy"])
            check_type(argname="argument iot_policy_name", value=iot_policy_name, expected_type=type_hints["iot_policy_name"])
            check_type(argname="argument thing_name", value=thing_name, expected_type=type_hints["thing_name"])
            check_type(argname="argument encryption_algorithm", value=encryption_algorithm, expected_type=type_hints["encryption_algorithm"])
            check_type(argname="argument policy_parameter_mapping", value=policy_parameter_mapping, expected_type=type_hints["policy_parameter_mapping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "iot_policy": iot_policy,
            "iot_policy_name": iot_policy_name,
            "thing_name": thing_name,
        }
        if encryption_algorithm is not None:
            self._values["encryption_algorithm"] = encryption_algorithm
        if policy_parameter_mapping is not None:
            self._values["policy_parameter_mapping"] = policy_parameter_mapping

    @builtins.property
    def iot_policy(self) -> builtins.str:
        '''(experimental) The AWS IoT policy in JSON format to be created and attached to the certificate.

        This is a JSON string that uses `mustache-compatible <https://handlebarsjs.com/guide/>`_
        template substitution to create the AWS IoT policy.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("iot_policy")
        assert result is not None, "Required property 'iot_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def iot_policy_name(self) -> builtins.str:
        '''(experimental) Name of the AWS IoT Core policy to create.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("iot_policy_name")
        assert result is not None, "Required property 'iot_policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def thing_name(self) -> builtins.str:
        '''(experimental) Name of AWS IoT thing to create.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("thing_name")
        assert result is not None, "Required property 'thing_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_algorithm(self) -> typing.Optional[builtins.str]:
        '''(experimental) Selects RSA or ECC private key and certificate generation.

        If not provided, ``RSA`` will be used.

        :default: - RSA

        :stability: experimental
        '''
        result = self._values.get("encryption_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_parameter_mapping(self) -> typing.Optional[typing.List["PolicyMapping"]]:
        '''(experimental) Optional: A ``PolicyMapping`` object of parameters and values to be replaced if a `mustache-compatible <https://handlebarsjs.com/guide/>`_ template is provided as the ``iotPolicy`` (see example). For each matching parameter in the policy template, the value will be used. If not provided, only the ``{{thingname}}`` mapping will be available for the ``iotPolicy`` template.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("policy_parameter_mapping")
        return typing.cast(typing.Optional[typing.List["PolicyMapping"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotThingCertificatePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-aws-iot-thing-certificate-policy-dev.PolicyMapping",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class PolicyMapping:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) Policy substitutions provided as key-value pairs.

        :param name: (experimental) Name of substitution variable, e.g., ``region`` or ``account``.
        :param value: (experimental) Value of substitution variable, e.g., ``us-east-1`` or ``12345689012``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96cf2593e03956b8ff2c387c9e0db2b00697ac06be3fd56d10366d39926bd64)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of substitution variable, e.g., ``region`` or ``account``.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) Value of substitution variable, e.g., ``us-east-1`` or ``12345689012``.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IotThingCertificatePolicy",
    "IotThingCertificatePolicyProps",
    "PolicyMapping",
]

publication.publish()

def _typecheckingstub__0b25a5ec66e5d9c59bbcc5ef88d9deddda593ee06e2e64b7b9e8de48b690a600(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    iot_policy: builtins.str,
    iot_policy_name: builtins.str,
    thing_name: builtins.str,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    policy_parameter_mapping: typing.Optional[typing.Sequence[typing.Union[PolicyMapping, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0be38e2a9971125086bd1c703f7f38ac53a8d8e658569b4f88f8005e1846240(
    *,
    iot_policy: builtins.str,
    iot_policy_name: builtins.str,
    thing_name: builtins.str,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    policy_parameter_mapping: typing.Optional[typing.Sequence[typing.Union[PolicyMapping, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96cf2593e03956b8ff2c387c9e0db2b00697ac06be3fd56d10366d39926bd64(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
