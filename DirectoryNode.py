from pathlib import Path


class DirectoryNode(object):
    def __init__(self, full_path):
        self.full_path = full_path
        self.file_infos = []   # Path objects
        self.local_size = 0
        self.sub_dirs = []
        self.total_size = 0

    def accept(self, visitor, indent_level=0):
        visitor.visit(self, indent_level)
        for dn in self.sub_dirs:
            dn.accept(visitor, indent_level + 1)

    def scan(self, progress_callback):
        current_path = Path(self.full_path)

        progress_callback(self.full_path)

        # collect information about all of the files in this specific directory
        self.file_infos = [x for x in current_path.glob("*") if x.is_file()]
        for local_file in self.file_infos:
            self.local_size += local_file.stat().st_size

        # update total_size with local files sizes
        self.total_size += self.local_size

        # scan subdirectories
        sub_dirs = [x for x in current_path.iterdir() if x.is_dir()]
        for sub_dir in sub_dirs:
            dn = DirectoryNode(sub_dir)
            dn.scan(progress_callback)
            self.sub_dirs.append(dn)
            # for each sub directory node, update total size from here down
            self.total_size += dn.total_size





