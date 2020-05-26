import boto3


def get_regions():
    """Returns a list of all AWS regions."""
    c = boto3.client('ec2')
    regions = [region['RegionName']
               for region in c.describe_regions()['Regions']]
    return regions


def delete_cw_events():
    print("****CW EVENTS****")
    for region in get_regions():
        print(region)
        events_client = boto3.client('events', region_name=region)
        rules_to_delete = events_client.list_rules(NamePrefix='custodian')
        for rule in rules_to_delete['Rules']:
            rule_name = rule['Name']
            print("Delete Event Rule:", rule_name)
            for target in events_client.list_targets_by_rule(
                    Rule=rule_name)['Targets']:
                events_client.remove_targets(
                    Rule=rule_name, Ids=[target['Id']])
            events_client.delete_rule(Name=rule_name)
        rules_to_delete = events_client.list_rules(NamePrefix='cloud')
        for rule in rules_to_delete['Rules']:
            rule_name = rule['Name']
            print("Delete Event Rule:", rule_name)
            for target in events_client.list_targets_by_rule(
                    Rule=rule_name)['Targets']:
                events_client.remove_targets(
                    Rule=rule_name, Ids=[target['Id']])
            events_client.delete_rule(Name=rule_name)


def delete_cloudwatch_log():
    print("****CW LOGS*****")

    for region in get_regions():
        print("Region " + region)
        logs = boto3.client('logs', region_name=region)
        # log_groups = logs.describe_log_groups(
        #     logGroupNamePrefix='/aws/')
        log_groups = logs.describe_log_groups(
            logGroupNamePrefix='cloudcustodian')
        for log_group in log_groups['logGroups']:
            log_group_name = log_group['logGroupName']
            print("Delete log group:", log_group_name)
            logs.delete_log_group(logGroupName=log_group_name)
        log_groups = logs.describe_log_groups(
            logGroupNamePrefix='/aws/lambda/custodian')
        for log_group in log_groups['logGroups']:
            log_group_name = log_group['logGroupName']
            print("Delete log group:", log_group_name)
            logs.delete_log_group(logGroupName=log_group_name)


def delete_lambda_custodian():
    print("****LAMBDA*****")
    for region in get_regions():
        lambda_client = boto3.client('lambda', region_name=region)
        print("Region " + region)
        # print(lambda_client.list_functions()['Functions'])
        for lambda_function in lambda_client.list_functions()['Functions']:
            function_name = lambda_function['FunctionName']
            function_arn = lambda_function['FunctionArn']
            if "custodian-info" in lambda_client.list_tags(
                    Resource=function_arn)['Tags'] or ("custodian"
                                                       in function_name):
                print("*****List of Functions to be deleted******")
                print(function_name + ";" + function_arn)
                lambda_client.delete_function(FunctionName=function_name)
                print("****DELETED****")


if __name__ == "__main__":
    delete_cw_events()
    delete_cloudwatch_log()
    delete_lambda_custodian()
