from DirectorySizeVisitor import DirectorySizeVisitor
from DirectorySizeVisitor import bcolors
from pathlib import PurePath

class DirectorySizeAndFileVisitor(object):
    def visit(self, directory_node, indent_level):

        # show existing directory iteration information
        dsv = DirectorySizeVisitor()
        dsv.visit(directory_node, indent_level)

        indent_string = dsv.get_indent_string(indent_level + 1)
        color_start = bcolors.OKBLUE
        color_end = bcolors.ENDC

        for file_info in directory_node.file_infos:
            file_name = PurePath(file_info).name
            file_size = dsv.format_bytes(file_info.stat().st_size)
            print("{0}{1}{2}: {3}{4}".format(color_start, indent_string, file_name, file_size, color_end))

