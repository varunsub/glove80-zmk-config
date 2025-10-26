import re
import json

# Read the keymap file
with open('/Users/varun/Documents/GitHub/glove80-zmk-config/config/glove80.keymap', 'r') as f:
    content = f.read()

# Extract layers
layer_pattern = r'layer_(\w+)\s*\{[^}]*bindings\s*=\s*<([^>]+)>;'
layers = re.findall(layer_pattern, content, re.DOTALL)

print("Found layers:", layers)

layer_dict = {}
for name, bindings_str in layers:
    # Clean the bindings string
    raw_bindings = re.split(r'\s+', bindings_str.strip())
    # Group into bindings
    bindings_list = []
    current = []
    for item in raw_bindings:
        item = item.strip()
        if item.startswith('&'):
            if current:
                bindings_list.append(current)
            current = [item]
        else:
            current.append(item)
    if current:
        bindings_list.append(current)
    layer_dict[name.lower()] = bindings_list

print("Layer dict keys:", list(layer_dict.keys()))
print("Base layer first 5:", layer_dict['base'][:5])

# Now, for each binding, parse into JSON format
def parse_binding(binding_list):
    if not binding_list or not binding_list[0].startswith('&'):
        return None
    value = binding_list[0]
    params = [{"value": p, "params": []} for p in binding_list[1:]]
    return {"value": value, "params": params}

# Map to the layer names in test.json
mapping = {
    'base': 'Base',
    'left': 'left',
    'right': 'right',
    'magic': 'magic'
}

json_layers = []
for key, display in mapping.items():
    if key in layer_dict:
        bindings_list = layer_dict[key]
        json_bindings = [parse_binding(b) for b in bindings_list if parse_binding(b)]
        json_layers.append(json_bindings)

print("JSON layers length:", [len(l) for l in json_layers])

# Now, read test.json
with open('/Users/varun/Documents/GitHub/glove80-zmk-config/config/test.json', 'r') as f:
    test_json = json.load(f)

# Update the layers
test_json['layers'] = json_layers

# Write back
with open('/Users/varun/Documents/GitHub/glove80-zmk-config/config/test.json', 'w') as f:
    json.dump(test_json, f, indent=2)

print("Updated test.json")