import json
from subprocess import call
import os

f = open('out.txt', 'w')

json_data=open("tools.json").read()

data = json.loads(json_data)

for tool in data:
    id = tool['id']

    print("----------", file=f)
    print(id, file=f)
    print("----------", file=f)

    file_path = "logs/" + id + "/"
    directory = os.path.dirname(file_path)

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    result = call(['tooldog', '-g', id, '-l', '--log_level', 'INFO', '--log_file', file_path + "/" + id + ".xml.log", '-f', file_path + "/" + id + ".xml"])

    print(result, file=f)

    result = call(['tooldog', '-c', id, '-l', '--log_level', 'INFO', '--log_file', file_path + "/" + id + ".cwl.log", '-f', file_path + "/" + id + ".cwl"])

    print(result, file=f)


f.close()