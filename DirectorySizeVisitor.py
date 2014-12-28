from DirectoryNode import DirectoryNode
from pathlib import PurePath


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = "\033[1m"


class DirectorySizeVisitor(object):

    KILOBYTE = 1024
    MEGABYTE = 1048576
    GIGABYTE = 1073741824
    TERABYTE = 1099511627776

    def __init__(self):
        self.tab_size = 2

    def visit(self, directory_node, indent_level):
        assert isinstance(directory_node, DirectoryNode)

        dir_name = directory_node.full_path
        if indent_level > 0:
            dir_name = PurePath(dir_name).stem

        indent_string = self.get_indent_string(indent_level)
        total_bytes = self.format_bytes(directory_node.total_size)
        local_bytes = self.format_bytes(directory_node.local_size)
        num_files = "{0}".format(len(directory_node.file_infos))

        color_start = bcolors.OKGREEN
        color_end = bcolors.ENDC

        if directory_node.total_size >= self.MEGABYTE:
            color_start = bcolors.WARNING

        if directory_node.total_size >= self.GIGABYTE:
            color_start = bcolors.BOLD + bcolors.FAIL

        print("{0}{1}{2}: {3} ({4} local in {5} files){6}".format(color_start, indent_string, dir_name, total_bytes, local_bytes, num_files, color_end))

    def get_indent_string(self, indent_level):
        return " " * (indent_level * self.tab_size)

    def format_bytes(self, num_bytes):
        if num_bytes < self.KILOBYTE:
            return "{0}".format(num_bytes)
        elif num_bytes < self.MEGABYTE:
            return "{0:.2f}KB".format(num_bytes / self.KILOBYTE)
        elif num_bytes < self.GIGABYTE:
            return "{0:.2f}MB".format(num_bytes / self.MEGABYTE)
        elif num_bytes < self.TERABYTE:
            return "{0:.2f}GB".format(num_bytes / self.GIGABYTE)
        else:
            return "{0:.2F}TB".format(num_bytes / self.TERABYTE)


