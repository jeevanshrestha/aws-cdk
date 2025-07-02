from aws_cdk import Stack, RemovalPolicy
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_kms as kms
from constructs import Construct
from aws_cdk import CfnOutput 
from aws_cdk import aws_iam

class MyArtifactBucketStack(Stack):
    
    def __init__(self, scope: Construct, id: str, is_prod=False, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create KMS key for bucket encryption
        key = kms.Key(self, "MyKMSKey",
            enable_key_rotation=True,
            description="KMS key for S3 bucket encryption"
        )
        
        if is_prod:
            artifactBucket = s3.Bucket(self, "MyProductionBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
        #    encryption_key=key,
            removal_policy=RemovalPolicy.RETAIN,  # Allow deletion for testing
            auto_delete_objects=False,  # Delete objects when bucket is deleted 
            bucket_name=f"jeeves-bucket-prod",
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
            
        else:
            artifactBucket = s3.Bucket(self, "MyDevelopmentBucket", 
        #    encryption_key=key,
            removal_policy=RemovalPolicy.DESTROY,  # Allow deletion for testing
            auto_delete_objects=True,  # Delete objects when bucket is deleted 
            bucket_name=f"jeeves-bucket-dev",
            versioned=False)
            
        output= CfnOutput(self,
                             id="MyBucket1NameOutput", 
                             value=artifactBucket.bucket_name, 
                             description="The name of Bucket")
        