import subprocess
import sys, os
import pathlib as path

from Instrumentation import Instrumentation


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
###
#
#   "$(CC)" /Fo${dst} $(DEPS_FLAGS) $(CC_FLAGS) $(INC) ${src}
#   "$(CC)" /P /Fi${dst} $(DEPS_FLAGS) $(CC_FLAGS) $(INC) ${src}
#
###
if __name__ == '__main__':
    print_hi('PyCharm')

    cc_arg = sys.argv[1]
    dst_arg = sys.argv[2]
    deps_flags_arg = sys.argv[3]
    cc_flags_arg = sys.argv[4]
    inc_arg = sys.argv[5]
    src_arg = sys.argv[6]
    add_arg = sys.argv[7]
    #print(cc_arg, dst_arg, deps_flags_arg, cc_flags_arg, inc_arg, src_arg)

    #preproc
    cc_flags = cc_flags_arg
    cc_flags = cc_flags.replace(" /c ", " ")
    dst = dst_arg[3:]
    if dst.endswith(".obj"):
        dst = str(path.PureWindowsPath(dst).parent)
    p = dst #+ "\\.\\"
    if p[-1] != '\\':
        p += '\\'
    print(" pp ",p)
    runcmd = " ".join(["\"{0}\"".format(cc_arg), "/P", "/Fi"+p, deps_flags_arg, cc_flags, inc_arg, src_arg, add_arg])
    print(runcmd)
    subprocess.call("chcp 65001", shell=True)
    subprocess.call(runcmd, shell=True)

    #compile
    if src_arg.endswith(".txt"):
        with open(src_arg[1:]) as src_file:
            src_content = src_file.read().lstrip().split(" ")
         #   print(src_file.read())
            for i, filename in enumerate(src_content):
                p = path.Path(filename).name
                new_path = path.WindowsPath(dst_arg[3:]).joinpath(p)
                print(new_path)
                #new_filename = "{1}c".format(filename[:-1])
                src_content[i] = str(new_path)
                if path.Path(new_path).exists():
                    os.remove(new_path)
                # instrumentation .i files
                i = Instrumentation()
                i.instr(new_path.with_suffix('.i'))

                os.rename(new_path.with_suffix('.i'), new_path)
    else:
        new_path = path.WindowsPath(p).joinpath(path.PureWindowsPath(src_arg).name)
        os.rename(new_path.with_suffix('.i'), new_path)
        src_content = [str(new_path)]
    cc_flags = cc_flags_arg.replace("/FIAutoGen.h", "")
    runcmd = " ".join(["\"{0}\"".format(cc_arg), dst_arg, deps_flags_arg, cc_flags, " ".join(src_content)])
    print(runcmd)
    subprocess.call(runcmd, shell=True)



