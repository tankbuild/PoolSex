from poolseq import Pipeline

p = Pipeline()
p.run()

test_results = open('./test_results.txt', 'w')

test_results.write('# Structure\n')

test_results.write('\n### Directories\n')
test_results.write('  - root    :  ' + p.structure.directories.root + '\n')
test_results.write('  - genomes :  ' + p.structure.directories.genomes + '\n')
test_results.write('  - qsub    :  ' + p.structure.directories.qsub + '\n')
test_results.write('  - reads   :  ' + p.structure.directories.reads + '\n')
test_results.write('  - results :  ' + p.structure.directories.results + '\n')
test_results.write('  - poolseq :  ' + p.structure.directories.poolseq + '\n')
test_results.write('  - shell   :  ' + p.structure.directories.shell + '\n')

test_results.write('\n### Data\n')
test_results.write('  - genome    :  ' + p.structure.data.genome() + '\n')
test_results.write('  - reads :  ' + '\n')
for read in p.structure.data.reads():
    test_results.write('      - ' + read + '\n')

test_results.write('\n### Shell\n')
test_results.write('  - mapping :  ' + '\n')
for read in p.structure.output.mapping():
    test_results.write('      - ' + read + '\n')
