from aws_cdk import Stack, RemovalPolicy
from aws_cdk import aws_ec2 as ec2 
from constructs import Construct
from aws_cdk import CfnOutput 
from aws_cdk import aws_iam

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
            ]
        )
        
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