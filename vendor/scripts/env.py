#!/usr/bin/env python
"""
Import API gateway definition

Usage:
  env init from <environment> <new-env>
  env render project <environment> [--tfstate=<file>] [<workdir>]
  env write project <environment> [--tfstate=<file>] [<workdir>]
  env link --environment=<string> [<workdir>]
  env render template [--tfstate=<file>] [--tfvars=<file>...] <template>...
  env write template --file=<file> [--tfstate=<file>] [--tfvars=<file>...] <template>...
  env import api [--tfstate=<file>] [--tfvars=<file>...] <template>...
  env render api [--tfstate=<file>] [--tfvars=<file>...] <template>...
  env add permissions <function> [<service>]
"""
import os, sys

script_dir = os.path.dirname( os.path.realpath(__file__) )
sys.path.insert(0, script_dir + os.sep + "lib")

import common as c
from docopt import docopt

import boto3, getpass, uuid

def read_first_existing(*files):
	for f in files:
		if os.path.exists(f):
			try:
				return c.read_json(f)
			except ValueError:
				pass
	raise IOError("Cannot find any of " + files)

def link(environment, target):
	dest = os.path.join(os.getcwd(), 'infrastructure', target)
	if not os.path.isdir(dest):
		source = os.path.join(os.getcwd(), 'infrastructure', environment)
		if os.path.islink(source):
			source = os.path.realpath(source)
		print "Creating symlink: " + dest
		os.symlink(source, dest)

def render_project_json(project, tfstate):
	if len( tfstate ):
		role = tfstate['apex_function_role']
		if role:
			project['role'] = role
		project = c.deep_merge(project, {"environment": tfstate})
	return c.to_json(project, False)

def read_tfvars(files, tfvars={}):
	for file in files:
		t = c.read_shlex(file)
		tfvars = c.deep_merge(tfvars, t)
	return tfvars
	
args = docopt(__doc__)
workdir = args.get('<workdir>') or os.getcwd()
environment = args.get('<environment>')
templates = args.get('<template>')

tfstate = {}
tfvars = read_tfvars( args.get('--tfvars') or [] )
if args.get('--tfstate'):
	tfstate = c.get_tfstate_f_outputs( args.get('--tfstate') )
params = c.deep_merge(tfstate, tfvars)

profile = os.getenv('AWS_PROFILE', 'default')
session = boto3.Session(profile_name=profile)

if args.get('init') and args.get('from'):
	target = args['<new-env>']
	link(environment, target)
	json =  read_first_existing(
		os.path.join(workdir, "project." + environment + ".json"),
		os.path.join(workdir, "project.json")
	)
	text = render_project_json(json, tfstate)
	c.write_file("project." + target + ".json", text)

if args.get('link'):
	link(environment, workdir)
	json = render_project_json(tfstate)

if args.get('project'):
	json =  read_first_existing(
		os.path.join(workdir, "project." + environment + ".json"),
		os.path.join(workdir, "project.json")
	)
	text = render_project_json(json, tfstate)
	if args.get('render'):
		print text
	if args.get('write'):
		c.write_file("project." + environment + ".json", text)

if args.get('template'):
	merge  = len(templates) > 1
	output = 'json' if len(templates) > 1 else 'text'
	text   = c.render_templates(templates, 
								params=params,
								merge=merge,
								output=outt)
	if args.get('render'):
		print text
	if args.get('write'):
		c.write_file( args["--file"], text)


if args.get('api'):
	payload = c.render_templates(templates, 
								 params=params,
								 merge=True,
								 output='json',
								 minify=False)
	if args.get('render'):
		print payload

	if args.get('import'):
		client  = session.client('apigateway')
		client.put_rest_api(
			failOnWarnings=False,
			restApiId=params['api_gateway_id'],
			mode='merge',
			body=str.encode(payload)
		)
		client.create_deployment(
			restApiId=params['api_gateway_id'],
			stageName=params['api_gateway_stage']
		)
		print 'done'

if args.get('add') and args.get('permissions'):
	function_name = 'serverless_{}_{}'.format(os.environ['ENV'], args['<function>'])
	service = args.get('<service>') or 'apigateway'
	lambda_client = session.client('lambda')
	print lambda_client.add_permission(
		FunctionName=function_name,
		StatementId=uuid.uuid4().hex,
		Action='lambda:InvokeFunction',
		Principal="{}.amazonaws.com".format(service)
			# SourceArn='string'
	)

if args.get('invalidate') and args.get('cache'):

  path = args['<path>'] if len(args['<path>']) else ['/*']

  client  = session.client('cloudfront')

  ref     = "evict " + str(path) + " by " + getpass.getuser()
  cloudfront = tfstate.get('cloudfront_id')
  print "Invalidate cache " + cloudfront + " with: " + ref
  
  print client.create_invalidation(
    DistributionId=cloudfront,
    InvalidationBatch={
        'Paths': {
            'Quantity': len(path),
            'Items': path
        },
        'CallerReference': ref
    }
)




