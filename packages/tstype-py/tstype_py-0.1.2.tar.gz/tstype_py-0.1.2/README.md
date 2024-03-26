use `parse_type_definition` to parse a type definition string into a JSON object.

```
Python 3.11.7 (main, Dec  4 2023, 18:10:11) [Clang 15.0.0 (clang-1500.1.0.2.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import tstype_py as ts
>>> import json
>>> text = "string|Map<string,Map<number, Array<string | number>>>[][]"
>>> json.loads(ts.parse_type_definition(text))
{'Union': [{'Basic': 'string'}, {'Array': {'Array': {'Map': [{'Basic': 'string'}, {'Map': [{'Basic': 'number'}, {'Array': {'Union': [{'Basic': 'string'}, {'Basic': 'number'}]}}]}]}}}]}
>>>
```
