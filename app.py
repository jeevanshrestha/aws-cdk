#!/usr/bin/env python3
import os
from aws_cdk import App, Environment 

app = App()

dev_context = app.node.try_get_context('dev') or {}
prod_context = app.node.try_get_context('prod') or {}
# Load context
env_context = app.node.try_get_context("environments")

dev_account = dev_context.get('account')
dev_region = dev_context.get('region')
prod_account = prod_context.get('account')
prod_region = prod_context.get('region')

env_USA = Environment(account=dev_account, region=dev_region)
env_AUS = Environment(account=prod_account, region=prod_region)

from resource_stacks.custom_vpc_stack import MyCustomVPC

MyCustomVPC(app, "DevVPCStack", env_config=env_context['dev'], env=env_USA)


MyCustomVPC(app, "ProdVCPStack", env_config=env_context['prod'], env=env_AUS)



app.synth()


# Completed Chapters
# from my_first_aws_cdk.my_first_aws_cdk import MyPythonCdkAppStack
# MyPythonCdkAppStack(app, "my-first-cdk-stack",
#     env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
#     )

# from my_first_aws_cdk.my_second_aws_cdk import MyArtifactBucketStack
# MyArtifactBucketStack(app, "my-dev-cdk-stack",
#     env=env_USA
#     )
# MyArtifactBucketStack(app, "my-prod-cdk-stack",
#     env=env_AUS, is_prod=True
#     )