import sys
from poolseq import Pipeline

root_dir = sys.argv[1]

p = Pipeline(root_dir)
p.run()
