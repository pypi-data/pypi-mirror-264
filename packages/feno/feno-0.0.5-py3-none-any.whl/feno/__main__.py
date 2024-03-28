from __future__ import annotations

import argparse
import sys


from .actions import Actions
from .__init__ import __version__
from .log import Log


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('targets', metavar='T', type=str, nargs='*', help='Readmes or folders')
    parser.add_argument("--check", "-c", action="store_true", help="Check if the file needs to be rebuilt")
    parser.add_argument("--preamble", "-p", action="store_true", help="disable qxcode preamble")
    parser.add_argument("--version", "-v", action="store_true", help="Prints the version")
    parser.add_argument("--debug", "-d", action="store_true", help="Verbose mode")
    parser.add_argument("--keep", "-k", action="store_true", help="Keep the cache files")
    parser.add_argument("--remote", "-r", type=str, help="remote config file")
    
    args = parser.parse_args()
    Log.verbose = args.debug
    
    if args.version:
        print(__version__)
        sys.exit(0)

    if len(args.targets) == 0:
        print("No targets specified")
        exit(1)

    for target in args.targets:
        actions = Actions(target, args.remote)
        
        if not actions.validate():
            continue
        actions.load_title()
        actions.create_cache()
        actions.update_markdown()

        if args.check and not actions.check_rebuild():
            return

        Log.write(actions.hook, ": Changes found [ ")
        actions.recreate_cache() # erase .cache
        actions.remote_md(args.preamble)         
        actions.html()
        actions.build_cases()
        actions.copy_drafts()
        actions.run_local_sh()
        actions.init_vpl()
        actions.create_mapi()
        Log.write("\n")
        if not args.keep:
            actions.clean()
        else:
            print("html: ", actions.target_html)
            print("cases: ", actions.cases)



if __name__ == "__main__":
    main()
