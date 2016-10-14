import os, sys

sys.path.insert(0, "lib")
import pprint, yaml, json, ConfigParser, pystache
import StringIO as io

# http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python
class FakeSecHead(object):
	def __init__(self, fp):
		self.fp = fp
		self.sechead = '[dummy]\n'

	def readline(self):
		if self.sechead:
			try: 
				return self.sechead
			finally: 
				self.sechead = None
		else: 
			return self.fp.readline()

cp = ConfigParser.ConfigParser()

# see: http://stackoverflow.com/questions/1447575/symlinks-on-windows/4388195#4388195
if os.name == 'nt':
	__CSL = None
	def symlink(source, link_name):
		global __CSL
		if __CSL is None:
			import ctypes
			csl = ctypes.windll.kernel32.CreateSymbolicLinkW
			csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
			csl.restype = ctypes.c_ubyte
			__CSL = csl
		flags = 0
		if source is not None and os.path.isdir(source):
			flags = 1
		if __CSL(link_name, source, flags) == 0:
			raise ctypes.WinError()
	os.symlink = symlink

def deep_merge(doc1, doc2):
	if isinstance(doc1,dict) and isinstance(doc2,dict):
		for k,v in doc2.iteritems():
			if k not in doc1:
				doc1[k] = v
			elif isinstance(doc1[k],list) and isinstance(v,list):
				doc1[k] = doc1[k] + v
			else:
				doc1[k] = deep_merge(doc1[k],v)
	return doc1

def to_json(content, minify=False):
	if not minify:
		return json.dumps(content, separators=(',', ':'), indent=4, sort_keys=True)
	return json.dumps(content, separators=(',', ':'))

def read_yaml(file):
	with open( file, 'r') as stream:
		return yaml.load(stream)

def read_json(file):
	with open( file, 'r') as stream:
		return json.load(stream)

def strip_values(d, s):
	return dict(map(lambda (k,v): (k, v.strip(s)), d.iteritems()))

def read_shlex(file):
	cp.readfp(FakeSecHead(open(file, 'r')))
	result = cp._sections['dummy']
	result = strip_values(result, '"')
	result = strip_values(result, "'")
	return result

def read_text(file):
	with open (file, "r") as stream:
		return stream.read()

def read_file(file):
	_, ext = os.path.splitext( file )
	if ext == 'yml' or ext == 'yaml':
		return read_yaml( file )
	if ext == 'conf' or ext == 'tfvars':
		return read_shlex( file )
	if ext == 'json':
		return read_json( file )
	return read_text(file)

def write_file(file, text):
	print 'Saving to ' + file
	with open(file, 'w+') as text_file:
		text_file.write(text)

def parse_text(txt):
	stream = io.StringIO(txt)
	try:
		return json.load(stream)
	except ValueError, e:
		pass
	return yaml.load(txt)

def get_tfstate_outputs(tfstate):
	result = {}
	for m in tfstate['modules']:
		if m['path'] == ['root']: 
			for k in m['outputs'].keys():
				result[k] = m['outputs'][k]['value']
			break 
	return result

def get_tfstate_f_outputs(tfstate):
	j = read_json(tfstate)
	return get_tfstate_outputs(j)

def render_templates(templates, **kwargs):
	params = kwargs['params'] if 'params' in kwargs else []
	output = kwargs['output'] if 'output' in kwargs else 'json'
	merge  = kwargs['merge']  if 'merge'  in kwargs else True
	minify = kwargs['minify'] if 'minify' in kwargs else False

	result = {}
	for file in templates:
		text     = read_text(file)
		rendered = pystache.render(text, params)
		if merge:
			parsed = parse_text(rendered)
			result = deep_merge(result, parsed)
		else:
			result = str(result) + "\n" + rendered if len(result) > 0 else rendered
 	if output is 'json':
		return to_json(result, minify)
	else:
		return result
