import sys
from poolseq import Pipeline

if len(sys.argv) != 2:
    print('\n** Error: no input directory specified\n\n   Usage: python3 poolseq.py path_to_directory\n')
    exit(0)

root_dir = sys.argv[1]

p = Pipeline(root_dir)
p.run()
