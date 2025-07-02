#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import App, Environment
from dotenv import load_dotenv

load_dotenv()
 

def main():
    
    print("Hello from aws-cdk!")
    print(f"Account: {os.getenv('CDK_DEFAULT_ACCOUNT')}")
    print(f"Region: {os.getenv('CDK_DEFAULT_REGION')}")


if __name__ == "__main__":
    main()
