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
