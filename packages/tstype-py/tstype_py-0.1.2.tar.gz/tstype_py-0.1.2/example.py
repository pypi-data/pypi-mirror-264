import tstype_py as ts
import json

text = "Map<string,Map<number| string|Something, Array<string[][][] | Map<string|number, User[]>>>[][]>[] | number[] | string"
d = json.loads(ts.parse_type_definition(text))
print(d)