from aws_cdk import Stack, RemovalPolicy, Tags
from aws_cdk import aws_ec2 as ec2 , aws_s3 as s3
from constructs import Construct
from aws_cdk import CfnOutput 
from aws_cdk import aws_iam
from datetime import datetime

class MyCustomVPC(Stack):
    
    def __init__(self, scope: Construct, id: str, env_config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(
            self, "CustomVpc",
            ip_addresses=ec2.IpAddresses.cidr(env_config["vpcConfig"]["cidr"]),
            max_azs=env_config["vpcConfig"]["maxAzs"],
            nat_gateways=env_config["vpcConfig"]["natGateways"],
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=subnet["name"],
                    subnet_type=getattr(ec2.SubnetType, subnet["subnetType"]),
                    cidr_mask=subnet["cidrMask"]
                ) for subnet in env_config["vpcConfig"]["subnetConfiguration"]
            ],
             
        )

        # Tags
        # Apply tags from JSON config
        for tag_key, tag_value in env_config.get("tags", {}).items():
            Tags.of(self).add(tag_key, tag_value)
 
        Tags.of(self).add("CreatedDate", datetime.now().strftime("%Y-%m-%d"))

        # Add specific tags to the VPC
        Tags.of(vpc).add("Name", f"{id}-VPC")
        Tags.of(vpc).add("Description", "Core networking infrastructure")

        # Tag all subnets with their type
        for subnet in vpc.public_subnets:
            Tags.of(subnet).add("Name", f"{id}-PublicSubnet-{subnet.availability_zone}")
            Tags.of(subnet).add("Network", "Public")
            
        for subnet in vpc.private_subnets:
            Tags.of(subnet).add("Name", f"{id}-PrivateSubnet-{subnet.availability_zone}")
            Tags.of(subnet).add("Network", "Private")

        for subnet in vpc.isolated_subnets:
            Tags.of(subnet).add("Name", f"{id}-IsolatedSubnet-{subnet.availability_zone}")
            Tags.of(subnet).add("Network", "Isolated")

        # Tag route tables
        # Proper way to tag route tables
        for i, subnet in enumerate(vpc.public_subnets):
            # Tag the underlying L1 route table resource
            for child in subnet.node.children:
                if isinstance(child, ec2.CfnRouteTable):
                    Tags.of(child).add("Name", f"{id}-PublicRouteTable-{i}")

        for i, subnet in enumerate(vpc.private_subnets):
            for child in subnet.node.children:
                if isinstance(child, ec2.CfnRouteTable):
                    Tags.of(child).add("Name", f"{id}-PrivateRouteTable-{i}")
                    
        # Output all relevant VPC information
        CfnOutput(self, "VpcId", value=vpc.vpc_id)
        CfnOutput(self, "VpcCidr", value=env_config["vpcConfig"]["cidr"])
        
        # Output availability zones
        for i, az in enumerate(vpc.availability_zones):
            CfnOutput(self, f"AvailabilityZone{i}", value=az)
        
        # Output public subnet IDs
        for i, subnet in enumerate(vpc.public_subnets):
            CfnOutput(self, f"PublicSubnet{i}", 
                     value=subnet.subnet_id,
                     description=f"Public subnet in {subnet.availability_zone}")
        
        # Output private subnet IDs
        for i, subnet in enumerate(vpc.private_subnets):
            CfnOutput(self, f"PrivateSubnet{i}", 
                     value=subnet.subnet_id,
                     description=f"Private subnet in {subnet.availability_zone}")
        
        # Output isolated subnet IDs (if any)
        for i, subnet in enumerate(vpc.isolated_subnets):
            CfnOutput(self, f"IsolatedSubnet{i}", 
                     value=subnet.subnet_id,
                     description=f"Isolated subnet in {subnet.availability_zone}")
        
        # Output NAT gateway IDs (if NAT gateways exist)
        if env_config["vpcConfig"]["natGateways"] > 0:
            nat_gateway_ids = []
            for subnet in vpc.public_subnets:
                for resource in subnet.node.children:
                    if isinstance(resource, ec2.CfnNatGateway):
                        nat_gateway_ids.append(resource.ref)
            for i, nat_gw_id in enumerate(nat_gateway_ids):
                CfnOutput(self, f"NatGatewayId{i}",
                          value=nat_gw_id,
                          description=f"NAT Gateway ID {i} in VPC")
         
         
        # Resources in same account
        # my_existing_bucket = s3.Bucket.from_bucket_name(self,
        #                                                "JeevesK8SBucket",
        #                                                "jeeves-k8s-sydney")
        # CfnOutput(self, 
        #           f"Imported Bucket{my_existing_bucket.bucket_name}",
        #           value=my_existing_bucket.bucket_name,
        #           description="Imported Bucket"
        #           )
         
