# CUSTODIAN RULES FOR RESOURCES IN AWS ACCOUNT

This repo contains custodian rules and scaffolding to check tags and execute action on non-compliant resources.

The execution of this repo is automated through AWS CodePipeline & AWS CodeBuild tools

## Repo structure

This repo has two main folders:

- mailer: has custodian rules regarding notifications, this is currently in test.
- policies: The main custodian policies, grouped by service and purpose;
  - RDS, S3, EC2
  - Report, notification, deletion, etc.

In the root of the repo, you can find:

- buildspec.yml, the file which controls the CodeBuild execution of this project, in the corresponding pipeline
- delete_custodian_lambdas.py, a Python script that automates the deletion of CloudCustodian Lambda Functions, CloudWatch Logs/Events and Rules related to them; review carefully before executing
- reqs.txt, file that contains the Python required dependencies

## Requirements to use

For using this repository you'll need to use Python 3.7+ (preferrably all runing in a virtualenv), and the following libraries, present in the reqs.txt file:

    argcomplete==1.11.1
    attrs==19.3.0
    boto3==1.12.47
    botocore==1.15.47
    c7n==0.9.1
    c7n-mailer==0.6.0
    certifi==2020.4.5.1
    chardet==3.0.4
    datadog==0.34.1
    decorator==4.4.2
    docutils==0.15.2
    idna==2.9
    importlib-metadata==1.6.0
    Jinja2==2.11.2
    jmespath==0.9.5
    jsonpatch==1.25
    jsonpointer==2.0
    jsonschema==3.2.0
    ldap3==2.7
    MarkupSafe==1.1.1
    pyasn1==0.4.8
    pyrsistent==0.16.0
    python-dateutil==2.8.1
    python-http-client==3.2.7
    PyYAML==5.3.1
    redis==3.4.1
    requests==2.23.0
    s3transfer==0.3.3
    sendgrid==6.2.2
    six==1.14.0
    tabulate==0.8.7
    urllib3==1.25.9
    zipp==3.1.0

## Rules included and validated

The following rules are already coded and implemented in production AWS Account:

- Validation of mandatory tags for EC2 Instances
- Validation of mandatory tags for RDS Instances


## Actions taken

The previous rules have implemented automatic deletion policies:

- Deletion of non-compliant resource
- Notification (in test)

## Next top-priority rules to implement

- Unused Elastic IP addresses deletion (and/or without tags)
- Automatic deletion of RDS/EC2 backups/snapshots, time constraints could apply
- Automatic and periodic resource report generation
