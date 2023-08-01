from aws_cdk import (
    core,
    aws_ec2 as ec2
)

class MyEC2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(
            self, "MyVpc",
            cidr="10.66.0.0/27"
        )

        # Create a public subnet
        public_subnet = ec2.Subnet(
            self, "PublicSubnet",
            vpc=vpc,
            cidr_block="10.66.0.0/28"
        )

        # Create an internet gateway
        internet_gateway = ec2.CfnInternetGateway(self, "InternetGateway")

        # Attach the internet gateway to the VPC
        ec2.CfnVPCGatewayAttachment(
            self, "VPCGatewayAttachment",
            vpc_id=vpc.vpc_id,
            internet_gateway_id=internet_gateway.ref
        )

        # Create a route table
        route_table = ec2.CfnRouteTable(
            self, "RouteTable",
            vpc_id=vpc.vpc_id
        )

        # Create a route to the internet gateway
        ec2.CfnRoute(
            self, "DefaultRoute",
            route_table_id=route_table.ref,
            destination_cidr_block="0.0.0.0/0",
            gateway_id=internet_gateway.ref
        )

        # Associate the route table with the public subnet
        ec2.CfnSubnetRouteTableAssociation(
            self, "PublicSubnetRouteTableAssociation",
            subnet_id=public_subnet.subnet_id,
            route_table_id=route_table.ref
        )

        # Create an EC2 instance
        instance = ec2.Instance(
            self, "MyEC2Instance",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=[public_subnet]),
        )

        # Add a Security Group rule to allow SSH access
        instance.connections.allow_from_any_ipv4(
            ec2.Port.tcp(22), description="SSH access"
        )

app = core.App()
MyEC2Stack(app, "MyEC2Stack")
app.synth()
# pip install aws-cdk-lib
# cdk init app --language python # If you haven't already initialized a CDK project
# cdk deploy