from pathlib import Path
from DirectoryNode import DirectoryNode
from DirectorySizeVisitor import DirectorySizeVisitor
from DirectorySizeAndFileVisitor import DirectorySizeAndFileVisitor
from LineCountVisitor import LineCountVisitor

class DiskUsage(object):
    def __init__(self):
        self.rootDirectory = "/Users/zube/Downloads"
        self.root_node = None
        self.lcv = LineCountVisitor()

    def scan_progress(self, current_path):
        print("Scanning: {0}".format(current_path))

    def build(self):
        self.root_node = DirectoryNode(self.rootDirectory)
        self.root_node.scan(self.scan_progress)

        dsv = DirectorySizeVisitor()
        dsv = DirectorySizeAndFileVisitor()
        self.root_node.accept(dsv)

        # todo: get scan_progress hooked up into this somehow...
        self.root_node.accept(self.lcv)
        self.lcv.print_results()

    def run(self):
        p = Path(self.rootDirectory)
        directories = [x for x in p.iterdir() if x.is_dir()]
        for directory in directories:
            print(directory)
            files = [x for x in directory.glob("*") if x.is_file()]
            for theFile in files:
                print(theFile)
                theFile.stat().st_size


diskUsage = DiskUsage()
diskUsage.build()
