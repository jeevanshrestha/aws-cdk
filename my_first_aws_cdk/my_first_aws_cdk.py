from aws_cdk import Stack, RemovalPolicy
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_kms as kms
from constructs import Construct
import random

class MyPythonCdkAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # Create KMS key for bucket encryption
        key = kms.Key(self, "MyKMSKey",
            enable_key_rotation=True,
            description="KMS key for S3 bucket encryption"
        )
        
        # Create S3 bucket with KMS encryption
        bucket = s3.Bucket(self, "MyBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
        #    encryption_key=key,  # type: ignore
            removal_policy=RemovalPolicy.DESTROY,  # Allow deletion for testing
            auto_delete_objects=True,  # Delete objects when bucket is deleted 
            bucket_name=f"jeeves-bucket-1",
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )
        
        print(f"Bucket created: {bucket.bucket_name}")