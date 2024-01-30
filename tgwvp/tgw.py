##vpcA is alias for vpc_prod,vpcC alias for vpc_nonprod,vpcB is alias for vpc_shared_service

import boto3

# Create VPCs
ec2 = boto3.resource('ec2')

# Create VPC 1
vpcA = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpcA_id = vpcA.id

# Create VPC 2
vpcC = ec2.create_vpc(CidrBlock='10.2.0.0/16')
vpcC_id = vpcC.id

# Create VPC 3
vpcB = ec2.create_vpc(CidrBlock='10.1.0.0/16')
vpcB_id = vpcB.id

# Enable DNS Support and Hostname for VPCs
vpcA.modify_attribute(EnableDnsSupport={'Value': True})
vpcA.modify_attribute(EnableDnsHostnames={'Value': True})

vpcC.modify_attribute(EnableDnsSupport={'Value': True})
vpcC.modify_attribute(EnableDnsHostnames={'Value': True})

vpcB.modify_attribute(EnableDnsSupport={'Value': True})
vpcB.modify_attribute(EnableDnsHostnames={'Value': True})

# Create Subnets
subnet1_public = ec2.create_subnet(VpcId=vpcA_id, CidrBlock='10.0.1.0/24', AvailabilityZone='us-east-1a')
subnet2_private = ec2.create_subnet(VpcId=vpcA_id, CidrBlock='10.0.2.0/24', AvailabilityZone='us-east-1a')

subnet3_private = ec2.create_subnet(VpcId=vpcC_id, CidrBlock='10.2.1.0/24', AvailabilityZone='us-east-1a')

subnet4_private = ec2.create_subnet(VpcId=vpcB_id, CidrBlock='10.1.1.0/24', AvailabilityZone='us-east-1a')

# Create Transit Gateway
tgw = ec2.create_transit_gateway(Description='TransitGateway')
tgw_id = tgw.id

 #create route table
vpcA_route_table=ec2.create_route_table()
vpcA_route_table.associate_with_subnet(subnetId=subnet1_public.id)
vpcA_route_table.create_route(
    DestCidrBlock = '10.1.0.0/16',
    GatewayId=tgw_id.id
)



#create route table
vpcC_route_table=ec2.create_route_table()
vpcC_route_table.associate_with_subnet(subnetId=subnet3_private.id)
vpcC_route_table.create_route(
    DestCidrBlock = '10.1.0.0/16',
    GatewayId=tgw_id.id
)

 #create route table
vpcB_route_table=ec2.create_route_table()
vpcB_route_table.associate_with_subnet(subnetId=subnet4_private.id)
vpcB_route_table.create_route(
    DestCidrBlock='10.0.0.0/16',
    #GatewayId='string'
)
vpcB_route_table.create_route(
    DestCidrBlock='10.2.0.0/16',
    #GatewayId='string'
)
 
#create tgw attachment
vpc_transit_gateway_attachment1 = ec2.create_transit_gateway_vpc_attachment(
    TransitGatewayId='tgw.id',
    VpcId='vpcA.id',
    SubnetIds=[
        'subnet1_public.id',
        'subnet2_private.id'
],
    TagSpecifications=[
    {
        'ResourceType': 'transit-gateway-attachment',
        'Tags': [
            {
                'Key': 'anything',
                'Value': 'anything'
            },
        ]
    },
],  
)


 #create tgw route table for vpcA
vpcA_transit_gateway_RT = ec2.create_transit_gateway_route_table(
TransitGatewayId='tgw.id',
TagSpecifications=[
    {
        'ResourceType': 'transit_gateway_route_table',
        'Tags': [
            {
                'Key': 'string',
                'Value': 'string'
            },
        ]
    },
],
)

#associating route table
associate_RT_with_attachment1 = vpcA_transit_gateway_RT.associate_transit_gateway_route_table(
TransitGatewayRouteTableId='vpcA_transit_gateway_RT.id',
TransitGatewayAttachmentId='vpc_transit_gateway_attachment1.id',
)

#create tgw attachment    
vpc_transit_gateway_attachment2 = ec2.create_transit_gateway_vpc_attachment(
    TransitGatewayId='tgw.id',
    VpcId='vpcC.id',
    SubnetIds=[
        'subnet3_private.id',
],
    TagSpecifications=[
    {
        'ResourceType': 'transit-gateway-attachment',
        'Tags': [
            {
                'Key': 'anything',
                'Value': 'anything'
            },
        ]
    },
],  
)

# #create tgw route table for  vpc B
vpc3_transit_gateway_RT = ec2.create_transit_gateway_route_table(
TransitGatewayId='tgw.id',
TagSpecifications=[
    {
        'ResourceType': 'transit_gateway_route_table',
        'Tags': [
            {
                'Key': 'string',
                'Value': 'string'
            },
        ]
    },
],
)

#associating route table
associate_RT_with_attachment2 = vpcC_transit_gateway_RT.associate_transit_gateway_route_table(
TransitGatewayRouteTableId='vpcC_transit_gateway_RT.id',
TransitGatewayAttachmentId='vpc_transit_gateway_attachment2.id',
)

#-----------    
#create tgw attachment
vpc_transit_gateway_attachment3 = ec2.create_transit_gateway_vpc_attachment(
    TransitGatewayId='tgw.id',
    VpcId='vpcB.id',
    SubnetIds=[
        'subnet4_private.id',
],
    TagSpecifications=[
    {
        'ResourceType': 'transit-gateway-attachment',
        'Tags': [
            {
                'Key': 'anything',
                'Value': 'anything'
            },
        ]
    },
],  
)

# #create tgw route table for junction vpc
vpcB_transit_gateway_RT = ec2.create_transit_gateway_route_table(
TransitGatewayId='tgw.id',
TagSpecifications=[
    {
        'ResourceType': 'transit_gateway_route_table',
        'Tags': [
            {
                'Key': 'string',
                'Value': 'string'
            },
        ]
    },
],
)

#associating route table
associate_RT_with_attachment3 = vpcB_transit_gateway_RT.associate_transit_gateway_route_table(
TransitGatewayRouteTableId='vpcB_transit_gateway_RT.id',
TransitGatewayAttachmentId='vpc_transit_gateway_attachment3.id',
)

#-----------    

#dynamically propagating the route tables of VPC to tgw
ec2.enable_transit_gateway_route_table_propagation(
TransitGatewayRouteTableId='transit_gateway_route_table.id',
TransitGatewayAttachmentId='vpc_transit_gateway_attachment1.id',
)

ec2.enable_transit_gateway_route_table_propagation(
TransitGatewayRouteTableId='transit_gateway_route_table.id',
TransitGatewayAttachmentId='vpc_transit_gateway_attachment2.id',
)

ec2.enable_transit_gateway_route_table_propagation(
TransitGatewayRouteTableId='transit_gateway_route_table.id',
TransitGatewayAttachmentId='vpc_transit_gateway_attachment3.id',
)

#create internet gateway
internet_gateway=ec2.create_internet_gateway()
vpcA.attach_internet_gateway(InternetGatewayId=internet_gateway.id)
















































