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
dev_context = app.node.try_get_context('dev') or {}
prod_context = app.node.try_get_context('prod') or {}

dev_account = dev_context.get('account')
dev_region = dev_context.get('region')
prod_account = prod_context.get('account')
prod_region = prod_context.get('region')

env_USA = Environment(account=dev_account, region=dev_region)
env_AUS = Environment(account=prod_account, region=prod_region)
from my_first_aws_cdk.my_second_aws_cdk import MyArtifactBucketStack
MyArtifactBucketStack(app, "my-dev-cdk-stack",
    env=env_USA
    )
MyArtifactBucketStack(app, "my-prod-cdk-stack",
    env=env_AUS, is_prod=True
    )

app.synth()
