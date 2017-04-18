def a(path):
...   field_names = []
...   fields = arcpy.ListFields(path,"")
...   for field in fields:
...     field_names.append(field.name)
...   return field_names
