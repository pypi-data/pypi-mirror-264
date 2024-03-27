import argparse
import os
import shutil
import site
from . import module_path

parser = argparse.ArgumentParser(
                    prog='Find JCMWAVE CLI',
                    description='Link JCMWAVE and your python environment',
                    epilog="That's all. Have fun.")

parser.add_argument('-l', '--lib',
                    action='store_true', 
                    help='link the third party support library into your ' 
                        'current python environment')
parser.add_argument('-i', '--interpreter',
                    action='store_true',
                    help='replace the jcm built in python interpreter '
                        'with the one from your environment')

def cli():
    args = parser.parse_args()
    if args.lib:
        link_lib()
    if args.interpreter:
        link_interpreter()
    if not (args.lib or args.interpreter):
        parser.print_help()

def link_lib():
    target = f"{site.getsitepackages()[0]}/jcmwave"
    if os.path.islink(target):
        os.remove(target)
    os.symlink(f"{module_path}/jcmwave", target)
    print("linked jcmwave module")

def link_interpreter():
    from glob import glob
    site_packages = glob(f"{module_path}/lib/python*/site-packages")[0]
    env_site_packages = site.getsitepackages()[0]

    for old_lib in ["numpy", "scipy", "matplotlib", "importlib"]:
        for old_lib_file in glob(f"{site_packages}/{old_lib}*"):
            if os.path.islink(old_lib_file):
                os.remove(old_lib_file)
            else:
                shutil.rmtree(old_lib_file)

    with open(f"{site_packages}/from_env.pth", "w") as f:
        f.write(env_site_packages)

    for new_lib in ["numpy", "scipy", "matplotlib", "importlib"]:
        for new_lib_file in glob(f"{env_site_packages}/{new_lib}*"):
            file_or_dirname = os.path.basename(os.path.normpath(new_lib_file))
            os.symlink(new_lib_file, f"{site_packages}/{file_or_dirname}")
    print("linked packages from your env to JCM")
    