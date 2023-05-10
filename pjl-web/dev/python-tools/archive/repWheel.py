#!/usr/bin/python3

#import packages
import os as os #docs: https://docs.python.org/3.4/library/os.html
import argparse #docs: https://docs.python.org/3.4/library/argparse.html

#parameters

root = "/usr/local/master/pjl-web/"
db_storage = root + "data/"
new_xml = root+ "dev/labDB.xml"


def get_db_files():
    all_files = os.listdir(db_storage)
    db_files = []
    for f in all_files:
        if f.startswith("labDB") and f.split(".")[0][-1] in ['0','1','2','3','4','5','6','7']:
            db_files.append(f)
    return sorted(db_files)

def increment_files(files):
    for i,f in enumerate(files):
        name = f.split(".")[0]
        index = int(name[-1])
        index += 1
        f = name[:-1] + str(index) + ".xml"
        os.rename(db_storage + files[i], db_storage + f)
    os.rename(db_storage + "labDB.xml", db_storage + "labDB-0.xml")
    os.system("cp " + new_xml + " " + db_storage + "labDB.xml")
    os.system("chmod 644 " + db_storage + "labDB.xml")



    
#MAIN
        
if __name__ == "__main__":
    files = get_db_files()
    increment_files(list(reversed(files)))
