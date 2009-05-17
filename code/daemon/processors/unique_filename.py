__author__ = "Wim Leers (work@wimleers.com)"
__version__ = "$Rev$"
__date__ = "$Date$"
__license__ = "GPL"


from processor import *
import stat
import shutil
import hashlib


class Mtime(Processor):
    """gives the file a unique filename based on its mtime"""


    valid_extensions = () # Any extension is valid.


    def run(self):
        # Get the parts of the input file.
        (path, basename, name, extension) = Processor.get_path_parts(self, self.input_file)

        # Set the output file base name.
        mtime = os.stat(self.input_file)[stat.ST_MTIME]
        self.set_output_file_basename(name + "_" + str(mtime) + extension)

        # Copy the input file to the output file.
        shutil.copyfile(self.input_file, self.output_file)

        return self.output_file


class MD5(Processor):
    """gives the file a unique filename based on its MD5 hash"""


    valid_extensions = () # Any extension is valid.


    def run(self):
        # Get the parts of the input file.
        (path, basename, name, extension) = Processor.get_path_parts(self, self.input_file)

        # Calculate the output file path.
        md5 = self.md5(self.input_file)
        self.set_output_file_basename(name + "_" + md5 + extension)

        # Copy the input file to the output file.
        shutil.copyfile(self.input_file, self.output_file)

        return self.output_file


    def md5(self, filename):
        """compute the md5 hash of the specified file"""
        m = hashlib.md5()
        try:
            f = open(filename, "rb")
        except IOError:
            raise FileIOError("Unable to open the file in readmode: %s" % (filename))

        line = f.readline()
        while line:
            m.update(line)
            line = f.readline()
        f.close()
        return m.hexdigest()


if __name__ == "__main__":
    import time

    p = Mtime("logo.gif")
    print p.run()
    p = MD5("logo.gif")
    print p.run()
