import sys
import glob
from shutil import copy

def copy_util(source, destination):
    for file in glob.iglob('%s/**/*.jpg' % source, recursive=True):
        print(file)
        copy(file, destination)
        
def main():
    copy_util(sys.argv[1], sys.argv[2])
    
if __name__ == "__main__":
    main()