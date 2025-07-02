#!/usr/bin/env python3
import os
from aws_cdk import App, Environment
from dotenv import load_dotenv

load_dotenv()

# from aws_cdk.aws_cdk_stack import AwsCdkStack


app = App()

# from my_first_aws_cdk.my_first_aws_cdk import MyPythonCdkAppStack
# MyPythonCdkAppStack(app, "my-first-cdk-stack",
#     env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
#     )

env_USA = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='us-east-1')
env_AUS = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='ap-southeast-2')
from my_first_aws_cdk.my_second_aws_cdk import MyArtifactBucketStack
MyArtifactBucketStack(app, "my-dev-cdk-stack",
    env=env_USA
    )
MyArtifactBucketStack(app, "my-prod-cdk-stack",
    env=env_AUS, is_prod=True
    )

app.synth()
