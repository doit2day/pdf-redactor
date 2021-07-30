import os

directory = '/var/lib/libvirt/images.2/filebu/FOIA2/'
 
for entry in os.scandir(directory):
    if entry.is_file() and entry.name.endswith('.pdf'):
        print(entry.path)
	python3 excombo1.py(entry.path)
else
continue
