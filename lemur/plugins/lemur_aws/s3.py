"""
.. module: lemur.plugins.lemur_aws.s3
    :platform: Unix
    :synopsis: Contains helper functions for interactive with AWS S3 Apis.
    :copyright: (c) 2018 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
"""
from botocore.exceptions import ClientError
from flask import current_app
from sentry_sdk import capture_exception

from .sts import sts_client
from typing import Any
from typing import Optional


@sts_client("s3", service_type="resource")
def put(bucket_name: str, region_name: str, prefix: str, data: str, encrypt: bool, **kwargs: Any) -> bool:
    """
    Use STS to write to an S3 bucket
    """
    bucket = kwargs["resource"].Bucket(bucket_name)
    current_app.logger.debug(
        "Persisting data to S3. Bucket: {0} Prefix: {1}".format(bucket_name, prefix)
    )

    # get data ready for writing
    if isinstance(data, str):
        data = data.encode("utf-8")

    if encrypt:
        bucket.put_object(
            Key=prefix,
            Body=data,
            ACL="bucket-owner-full-control",
            ServerSideEncryption="AES256",
        )
    else:
        try:
            bucket.put_object(Key=prefix, Body=data, ACL="bucket-owner-full-control")
            return True
        except ClientError:
            capture_exception()
            return False


@sts_client("s3", service_type="client")
def delete(bucket_name: str, prefixed_object_name: str, **kwargs: Any) -> bool:
    """
    Use STS to delete an object
    """
    try:
        response = kwargs["client"].delete_object(Bucket=bucket_name, Key=prefixed_object_name)
        current_app.logger.debug(f"Delete data from S3."
                                 f"Bucket: {bucket_name},"
                                 f"Prefix: {prefixed_object_name},"
                                 f"Status_code: {response}")
        return response['ResponseMetadata']['HTTPStatusCode'] < 300
    except ClientError:
        capture_exception()
        return False


@sts_client("s3", service_type="client")
def get(bucket_name: str, prefixed_object_name: str, **kwargs: Any) -> Optional[str]:
    """
    Use STS to get an object
    """
    try:
        response = kwargs["client"].get_object(Bucket=bucket_name, Key=prefixed_object_name)
        current_app.logger.debug(f"Get data from S3. Bucket: {bucket_name},"
                                 f"object_name: {prefixed_object_name}")
        return response['Body'].read().decode("utf-8")
    except ClientError:
        capture_exception()
        return None
