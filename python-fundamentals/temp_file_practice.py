import tempfile
import os

with tempfile.NamedTemporaryFile(mode="w",delete=False) as file:
    temp_file_name = file.name
    file.write("Hello Python")

with open(temp_file_name,"r") as file:
    content = file.read()

print(content)
os.remove(temp_file_name)