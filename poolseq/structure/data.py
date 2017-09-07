import os


class Data():

    def __init__(self, directories):
        self.directories = directories

    def genome(self):
        temp = [f for f in os.listdir(self.directories.genomes) if f.endswith('.fasta')]
        if len(temp) == 0:
            print(' Error: genome file not found')
        elif len(temp) > 1:
            print(' Error: found ' + str(len(temp)) + ' genome files. There should be only 1.')
        file = temp[0]
        return os.path.join(self.directories.genomes, file)

    def reads(self):
        files = [f for f in os.listdir(self.directories.reads) if f.endswith('.fastq.gz')]
        if len(files) < 2:
            print('- Error: reads files not found')
        return [os.path.join(self.directories.reads, f) for
                f in os.listdir(self.directories.reads) if
                f.endswith('.fastq.gz')]
