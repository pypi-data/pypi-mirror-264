import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-aws-iot-thing-certificate-policy-dev",
    "version": "0.0.15",
    "description": "Creates an AWS IoT thing, certificate, policy, and associates the three together",
    "license": "Apache-2.0",
    "url": "https://github.com/gadams999/cdk-aws-iot-thing-certificate-policy.git",
    "long_description_content_type": "text/markdown",
    "author": "Gavin Adams<gavinaws@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/gadams999/cdk-aws-iot-thing-certificate-policy.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_aws_iot_thing_certificate_policy_dev",
        "cdk_aws_iot_thing_certificate_policy_dev._jsii"
    ],
    "package_data": {
        "cdk_aws_iot_thing_certificate_policy_dev._jsii": [
            "cdk-aws-iot-thing-certificate-policy-dev@0.0.15.jsii.tgz"
        ],
        "cdk_aws_iot_thing_certificate_policy_dev": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.133.0, <3.0.0",
        "cdk-nag>=2.28.63, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.95.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
