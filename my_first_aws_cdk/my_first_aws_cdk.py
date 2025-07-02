from aws_cdk import Stack, RemovalPolicy
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_kms as kms
from constructs import Construct
from aws_cdk import CfnOutput 
from aws_cdk import aws_iam

class MyPythonCdkAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # Create KMS key for bucket encryption
        key = kms.Key(self, "MyKMSKey",
            enable_key_rotation=True,
            description="KMS key for S3 bucket encryption"
        )
        
        # Create S3 bucket with KMS encryption
        my_bucket_1 = s3.Bucket(self, "MyBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
        #    encryption_key=key,
            removal_policy=RemovalPolicy.DESTROY,  # Allow deletion for testing
            auto_delete_objects=True,  # Delete objects when bucket is deleted 
            bucket_name=f"jeeves-bucket-1",
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )
        output_1 = CfnOutput(self,
                             id="MyBucket1NameOutput", 
                             value=my_bucket_1.bucket_name, 
                             description="The name of MyBucket 2")
        
        my_bucket_2 = s3.Bucket(self, "MyBucket2",
            encryption=s3.BucketEncryption.S3_MANAGED,
        #    encryption_key=key,
            removal_policy=RemovalPolicy.DESTROY,  # Allow deletion for testing
            auto_delete_objects=True,  # Delete objects when bucket is deleted 
            bucket_name=f"jeeves-bucket-2",
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )
        
 
        output_2 = CfnOutput(self,
                             id="MyBucket2NameOutput", 
                             value=my_bucket_2.bucket_name, 
                             description="The name of MyBucket 2")
        
        print(output_2) 
        group = aws_iam.Group(self,
                              "Jeeves-Local"
        )
        output_3 = CfnOutput(self,
                             id="MyGroupNameOutput",
                             value=group.group_name,
                             description="This is the group created by aws cdk")
        
        print(output_3)
        
        user = aws_iam.User(self,
                            "JeevesUser",
                            user_name="jeeves-user"
        )

        group.add_user(user)
        