import sys
sys.path.append('../')
from dpu_utils.utils import RichPath
from src.utils import my_ast
from src.utils.codegen import *
import subprocess

from parent_node_parse_helpers import dfs_traversal_with_parents
import pandas as pd
import os



count = 0
def convert_code_to_tokens(code):
    global count
    tree =''
    # tree = my_ast.parse(code)

    try:
        tree = my_ast.parse(code)
    except:
        try:
            f = open('temp.py', 'w+')
            f.write(code)
            f.close()
            subprocess.run(['2to3', '-w', 'temp.py'])
            f = open('temp.py', 'r')
            code = f.read()
            # print(code)
            tree = my_ast.parse(code)
            # os.rmdir('temp.py')
        except:
            pass
    if tree!='' and tree != None:
        return dfs_traversal_with_parents(tree)
    else:
        return [], []
#


from pprint import pprint
if __name__=='__main__':
    print('something')



    root_path = '../resources/data/python/final/jsonl/'
    for subdir, dirs, files in os.walk(root_path, topdown=True):
        current_path = os.getcwd()

        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(".gz"):
                print(file, 'is being converted.')
                s_path = root_path + 'dfs_informed/' + subdir[len(root_path):]
                if not os.path.exists(s_path):
                    os.makedirs(s_path)

                a = RichPath.create(filepath)
                s = RichPath.create(s_path + os.sep + file)

                b = list(a.read_as_jsonl())

                b = sorted(b, key=lambda v: len(v['code_tokens']))
                templist = []

                c = []


                for idx, sample in enumerate(b):
                    #print("sample {} in progress".format(idx))
                    # print(sample['code'])

                    #if idx == 19 or sample['sha']=='618d6bff71073c8c93501ab7392c3cc579730f0b':
                    #    print(sample['code'])

                    dfs, parent_dfs = convert_code_to_tokens(sample['code'])
                    if dfs == [] or parent_dfs==[]:
                        templist.append(idx)
                    else:
                        b[idx]['code_tokens'] = dfs
                        b[idx]['parent_dfs'] = parent_dfs
                        c.append(b[idx])
                print("Saving ", file)
                s.save_as_compressed_file(c)

