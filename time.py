from tim_py import *
import sys
def main():
    argc = len(sys.argv)
    argv = sys.argv
    if (argc < 2):
        raise RuntimeError("Usage: %s <file_name.tim-py>\n", argv[0])
    file_name = argv[1]
    machine = read_program_from_file(argv[1])
    machine.run()
    machine.print_stack()
main()