# chuck-lambda

Chuck Norris microservice demonstrates how to use lambda. It will show few tools that nas been used to successfully do Serverless in Amazon Web Services

## Overview of Workshop Labs

Current workshop introduces the basecs of how to build Serverless Microservices using Java stacks. It provides set of labs and setp-by-step instructions and tool chain that is suitable for Java as of today (2016, October)

## Installation

#### Prerequisites

We cannot run on Windows, sorry. We use tool called `apex` which is does not supports Windows.

Our toolchain (see below) relies on the environment variables and aliases.

Before we start we want to assume that: 
- You have Python 2.7 
- Open (or Oracle) Java Development Kit v8 (JDK8)
- Node.js 6+

Everything else we will setup automatically

## Tool Chain

For this workshop we will use set of tools. Each will serve certain purpose in AWS Lambda deployment process

#### Apex 

[apex](https://apex.io) is the command line tool to deploy AWS Lambda and give to the developer convinient routines to operate with AWS Lambda deployment lifecycle. 

Due to [PR](http://github.com/apex/apex/issues/566) we want to use custom built apex. Once it will be merged to the origin we can switch to the vendor apex distribution.

#### Terraform

[Terraform](http://terraform.io/docs) developed by Hashicorp it gives deveoper a DSL to specify his own Cloud native stacks. See more details [here](http://terraform.io/docs/providers/aws/index.html).

#### CMake

AWS Lambda is polyglotic by it's nature. So, we need to pick a build up a tool that will be technology agnostic (as far as it can be) and simple to use. This tool pupose is to give to the user a simple `Makefile` so he or she could operate with Apex and Terraform and other tools.

#### Python

If you look to the file `vendor/scripts/env.py` you will see a python script that closes integration gaps between Apex (AWS Lambda functions) and Terraform (Cloud Stacks). For slightluy better user experience, this `env.py` scritp has been wrapped wiht `Makfile` tasks. However you can use it without `Makefile` because it provides generic enough CLI. run `bin/env --help` for more information. The python script uses boto3 (AWS client) and Pistacche (mustage templating engine).

#### JDK8

Yes we are using `Gradle` to build our AWS Lambda. So it relies to the JDK8 (Java Development Kit) for compilation process.

#### Nodejs

As every good app we need a UI. It has been built with the Angular + Material. Nodejs is needed to compile Angular application and prepare for deployment

#### AWS CLI

Yes, almost forgot we also use AWS ClI :)

## LAB 0: Prepping

1\. Clone follwoing repositories
```
$ git clone http://github.com/akranga/chuck-lambda.git
# optionally
$ git clone http://github.com/akranga/terraform-modules.git
```

2\. Checking apex. We do have apex binary for `macos` and `linux`. To validate apex installation please run
```
$ bin/apex version
Apex version 0.10.3
```
You can switch apex from linux to macos by changing alias in file `bin/apex`:

```
$ vi bin/apex
# change apex=$DIR/apex_linux
# to apex=$DIR/apex_darwin
:wq
# to exit vi :)
```

2\. Now we need to choose a good name to tag our environment. Name should be unique. This will help to avoid naming collisions between participants.

To help you to choose good name we have a small script:
```
$ bin/new-name
Like this name?
 smoggy-pointer

Then enter command
 $ export ENV=smoggy-pointer
 ```

3\. Set environment variable ENV if you like naming. 
```
$ export ENV=smoggy_pointer
```

Validate environmet variablr
```
$ echo $ENV
smoggy_pointer
```

4\. Run command `make init` . Result of the command you will see a new file `project.smoggy-poiner.json`. This file defines an `apex` project forenvironment tagget as `smoggy-pointer`. All AWS Lambda function defaults willgo there. Please feel free to customize it if needed. You might want to check apex [docs](http://apex.io) for more details and configuration options.

You will also notice a symlink in under `infrastructure` directory. This is needed to support apex convention. Every apex environment must have directory (or symlink) that corresponds to the convention: `infrastructure/environment-name`

5\. Now we need to run terraform script that will build our environment in the cloud. To do so please run following command
```
$ make infra
``` 

What just happened? You will see apex can run as a wrapper for terraform. Terraform provisioning (typially executed just once) happens with following lifecycle (see `Makefile` for implementation details):

a\. **Get**: `terraform get` or in our case `apex infra get`: this will download terraform stack definition dependencies known as modules.

b\. **Plan**: `terraform plan` or `apex infra plan`: this will inpect terraform definitions and interdependencies inside of the cloud resources and create an execution plan that will be storred inside: `infrastructure/terraform.environment-name.tfplan` file.

c\. **Apply**: `terraform apply` or `apex infra apply`: this command will create resources in the cloud based on execution plan and store result in `terraform state` file called `infrastructure/terraform.enviroinment-name.tfstate`. Don't lose this file!

3\. Now we need to update apex configuration with the information received from terraform. We have macros forthat... just run:
```
$ make projectfile
```

## LAB 1: Deploy Lambda Function

1\. Deploy lambda function
```
$ bin/apex deploy lab1
...
function created env=smoggy-pointer function=lab1 name=serverless_smoggy-pointer_lab1 version=1
```


Where `lab1` is the name of the directory inside `functions` directory. If you look closely into `function.json` you will see something like this:
```json
{
  "runtime": "java",
  "handler": "Main::handleRequest",
  "memory": 512,
  "timeout": 32,
  "hooks" : {
    "build" : "./gradlew jar",
    "clean" : "./gradlew clean"
  }
}
```
You can point that `function.json` can override defaults listed in `project.json`. It also specifies `hooks` to the build system which is `gradle` in our case.

Now open the `functions/lab1/build.gradle` file. You will see that AWS Lambda Function is actually an uberjar (also know fatjar) with the name `apex.jar`. This is filename apex seeks for deployment

2\. Validate AWS Lambda function
```
$ bin/apex list 
```

and finally let's execute the function:
```
$ bin/apex invoke lab1
"Chuck Norris went out of an infinite loop."

$ bin/apex logs
...
Duration: 222.98 ms Billed Duration: 300 ms    Memory Size: 512 MB Max Memory Used: 81 MB
```

3\. Expose AWS Lambda Function to API gateway. We will use swagger configuration for this. If we speak about API Gateway then Swagger configurations are little bit more elegant than terraform definition.

Look at the file in directory `templates/lab1.yaml`

Run `make api-lab1` it will import lambda function

## LAB2: Lambda function with parameters

