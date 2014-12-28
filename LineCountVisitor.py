from pathlib import PurePath

class LineCountInfo(object):
    def __init__(self, total_lines, code_lines=0, comment_lines=0, blank_lines=0):
        self.code_lines = code_lines
        self.comment_lines = comment_lines
        self.blank_lines = blank_lines
        self.total_lines = total_lines

    def get_code_lines(self):
        return self.code_lines

    def get_comment_lines(self):
        return self.comment_lines

    def get_blank_lines(self):
        return self.blank_lines

    def get_total_lines(self):
        return self.total_lines

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        if isinstance(other, type(None)):
            return None

        self.code_lines += other.code_lines
        self.comment_lines += other.comment_lines
        self.blank_lines += other.blank_lines
        self.total_lines += other.total_lines
        return self


class LineCountDescriptor(object):
    def __init__(self, extensions):
        self.extensions = extensions

    def get_extensions(self):
        return self.extensions

    def count_lines(self, file_path):
        return LineCountInfo(0)


class PythonLineCountDescriptor(LineCountDescriptor):
    def __init__(self):
        super().__init__([".py", ".cs", ".js"])

    def count_lines(self, file_path):
        return LineCountInfo(20, 5, 10, 15)


class ObjectiveCLineCountDescriptor(LineCountDescriptor):
    def __init__(self):
        super().__init__([".m", ".h"])

    def count_lines(self, file_path):
        return LineCountInfo(12, 2, 4, 6)


class LineCountFileTypes:
    PYTHON = PythonLineCountDescriptor()
    OBJECTIVEC = ObjectiveCLineCountDescriptor()


class LineCountVisitor(object):
    def __init__(self, file_types=[LineCountFileTypes.PYTHON, LineCountFileTypes.OBJECTIVEC]):
        self.file_types = file_types

        self.extensions_descriptors = {}
        self.extensions_counts = {}
        for ft in file_types:
            for ext in ft.get_extensions():
                self.extensions_counts[ext] = LineCountInfo(0)
                self.extensions_descriptors[ext] = ft

    def visit(self, directory_node, indent_level):
        for file_info in directory_node.file_infos:
            suffix = PurePath(file_info).suffix
            if suffix in self.extensions_counts:
                self.extensions_counts[suffix] += self.extensions_descriptors[suffix].count_lines(file_info)

    def print_results(self):
        # print(self.extensions_counts)
        for ext, cnt_info in self.extensions_counts.items():
            if cnt_info is not None:
                print("{0}: {1} lines".format(ext, cnt_info.get_total_lines()))


