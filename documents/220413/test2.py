from prance import BaseParser
import yaml
import json
import requests

namefile = "220413_car"
with open(f"{namefile}.yaml", 'r') as yaml_in, open(f"{namefile}.json", "w") as json_out:
    yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
    json.dump(yaml_object, json_out)

parser = BaseParser(f"{namefile}.json")
spec = parser.specification

class PathParam:
    def __init__(self, name, required: bool, type_par):
        self.name = name
        self.required = required
        self.type_par = type_par

class BodyParam:
    def __init__(self, op_id, required: bool, type_par, schema):
        self.name = op_id
        self.required = required
        self.type_par = type_par
        self.schema = schema

class Operation:
    def __init__(self, op_id, method, path_params, body_params, responses):
        self.name = op_id
        self.method = method
        self.path_params = path_params
        self.body_params = body_params
        self.responses = responses


class SchemaProp:
    def __init__(self, name, type_prop, min_prop = int | None, max_prop = int | None, enum_prop = [] | None):
        self.name = name
        self.type_prop = type_prop
        self.min_prop = min_prop
        self.max_prop = max_prop
        self.enum_prop = enum_prop

    def validate(self, value):
        if self.type_prop == 'string':
            if type(value) is not str:
                raise ValueError(value)
            if self.min_prop and len(value) < self.min_prop:
                raise ValueError(value)
            if self.max_prop and len(value) > self.max_prop:
                raise ValueError(value)
            if self.enum_prop and value not in self.enum_prop:
                raise ValueError(value)
        elif self.type_prop == 'number':
            # TODO: Aggiungere formato
            if type(value) is not int or type(value) is not float:
                raise ValueError(value)
            if self.min_prop and value < self.min_prop:
                raise ValueError(value)
            if self.max_prop and value > self.max_prop:
                raise ValueError(value)
        elif self.type_prop == 'array':
            if type(value) is not type([]):
                raise ValueError(value)

            

def get_min_type_prop(type_prop: str):
    if type_prop == 'string':
        return 'minLength'
    elif type_prop == 'number':
        return 'minimum'
    return None
def get_max_type_prop(type_prop: str):
    if type_prop == 'string':
        return 'maxLength'
    elif type_prop == 'number':
        return 'maximum'
    return None

def parse_schema(schema):
    out = {}
    if schema['type'] != 'object':
        raise Exception('not object schemas not implemented')
    for prop in schema['properties']:
        cont_prop = schema['properties'][prop]
        type_prop = cont_prop['type']
        out[prop] = SchemaProp(
            prop, type_prop, 
            min_prop=cont_prop.get(get_min_type_prop(type_prop)),
            max_prop=cont_prop.get(get_max_type_prop(type_prop)),
            enum_prop=cont_prop.get('enum')
        )
    return out

def handle_path_params(spec: dict, path: str):
    components = path.split('/')
    path_params = []
    real_path_params = []
    for c in components:
        if c[0] == '{' and c[-1] == '}':
            path_params.append(c[1, -2])
    for param in spec['paths'][path]['parameters']:
        if param['name'] in path_params:
            path_params.remove(param['name'])
        else:
            raise Exception('Path parameter not found')
        req = param.get('required') or False
        ty = param['type']
        # TODO: Handle format
        real_path_params.append(PathParam(param['name'], req, ty))
    return real_path_params

def get_responses(responses: dict):
    return [key for key in responses]

def handle_get_method(spec):
    body_get = spec['paths'][path].get('post')
    if body_get is not None:
        responses = []
        for res in body_get['responses']:
            ref_schema_res = body_get['responses'][res].get('schema')
            if ref_schema_res is not None:
                if not ref_schema_res.startsWith('#/definitions'):
                    raise Exception('invalid definition, must begin with "#/definitions"')
                schema = spec['definitions'][ref_schema_res.split('/')[2]]
                real_schema = parse_schema(schema)
            
        responses = get_responses(body_get['responses'])
        list_ops.append(Operation(
            path, 'get', path_params=path_params, 
            body_params=body_params, responses=responses
        ))

base_url = spec['schemes'] + spec['host'] + spec['basePath']
list_ops = []
for path in spec['paths']:
    components = path.split('/')
    path_params = handle_path_params(spec, path)
    body_params = []
    body_post = spec['paths'][path].get('post')
    if body_post is not None:
        # req = body_post.get('required') or False
        if body_post['in'] != 'body':
            raise Exception('not body')
        ref_schema = body_post['schema']['$ref']
        if not ref_schema.startsWith('#/definitions'):
            raise Exception('invalid definition, must begin with "#/definitions"')
        schema = spec['definitions'][ref_schema.split('/')[2]]
        real_schema = parse_schema(schema)
        body_params.append(real_schema)
        responses = get_responses(body_post['responses'])
        list_ops.append(Operation(
            path, 'post', path_params=path_params, 
            body_params=body_params, responses=responses
        ))


r = requests.post(base_url+'/slot/2', json=None)
print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))