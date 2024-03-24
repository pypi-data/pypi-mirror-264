# MythosMaker

This is a python library to generate fake data for testing purposes. This uses the faker, sqlalchemy, multiprocessing and other libraries to generate fake data objects in multiple processes to speed up performance and generate large amounts of data.

# How to Use

```python
from MythosMaker import run_generator

'''
Arguments (with = as default)

sql_models_path -> The path to your sqlalchemy models to be used in format of "directory.file"...

database_uri='sqlite:///database.db' -> The name of your database to be persisted...

number_of_processes=5 -> The number of processes...Keep in mind the more you add the more overhead on the system...

number_of_records=1000 -> The number of records to be persisted...
'''

run_generator('directory.file', 'sqlite:///database.db', 5, 1000)
```

# Additional Notes

This framework will only pickup tables defined by classes in the sqlalchemy models files...

The more records the more time it will take to run through...

Default values will be filled in depending on your data type...

It is best to overestimate the size of your columns...

Do not add too many processes...