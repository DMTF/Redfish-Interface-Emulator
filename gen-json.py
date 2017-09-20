import requests
from pprint import pprint as pp

url = 'http://redfish.dmtf.org/schemas/Processor.v1_1_0.json'
# url=raw_input('URL for Schema: ')

SCHEMA = requests.get(url).json()


def schema_get(root, path):
    try:
        ipath = path.split('/')[1:]
        schema = root
        for p in ipath:
            schema = schema[p]
        return schema, root
    except:
        schema = requests.get(path).json()
        if '#' in path:
            ref='#'+path.split('#')[-1]
        else: ref=schema.get('$ref','')
        if ref:
            return schema_get(schema, ref)
        return {}, root

def safe_input(prompt):
    inp=raw_input(prompt)
    try:
        return eval(inp)
    except:
        return inp


def read_property(schema, root):
    if '$ref' in schema:
        print 'got ref: %s'%schema['$ref']
        follow=(raw_input('follow?(y/n)')=='y')
        if follow:
            new_schema, new_root = schema_get(root, schema['$ref'])
            if new_schema:
                return read_property(new_schema, new_root)
        else:
            return safe_input('not following, enter your input:')
    if 'properties' in schema:
        if not schema['properties']:
            pp(schema)
            return safe_input('manual input: ')
        print schema.get('description', 'no description')
        print 'required: ', schema.get('required', [])
        props = {}
        for item in schema['properties'].items():
            print 'Input relates to :',schema.get('description', 'no description')
            if item[0]=='@odata.type':
                prop=root.get('title')
                print item[0], prop
            elif item[0]=='@odata.context':
                odatatype=root.get('title')
                prop='/redfish/v1/$metadata{0}.{2}'.format(*odatatype.split('.'))
                print item[0], prop
            else:
                print item[0]
                prop = read_property(item[1], root)
            if prop:
                props[item[0]] = prop
        return props
    if 'anyOf' in schema:
        pp(zip(schema['anyOf'],xrange(len(schema['anyOf']))))
        inp=safe_input('choose id of $ref or press enter for null: ')
        return read_property(*schema_get(root,schema['anyOf'][inp].values()[0])) \
            if inp!='' else safe_input('manual input:')
    if 'string' in str(schema['type']):
        pp(schema)
        return safe_input('your string input:')
    elif 'boolean' in str(schema['type']) or 'number' in str(schema['type']):
        pp(schema)
        return safe_input('your input:')
    elif 'object' in str(schema['type']):
        if 'properties' in schema:
            print schema.get('description', 'No description')
            print 'required: ', schema.get('required', [])
            return read_property(schema['properties'], root)
        else:
            pp(schema)
            return safe_input('manual input: ')
    elif 'array' in str(schema['type']):
        pp(schema)
        raw_input('cant read array yet, just press enter')
        return None
    else:
        print 'catch all:'
        print schema
        return safe_input('your input: ')


# def build_data(schema,):


pp(read_property(SCHEMA, SCHEMA))
