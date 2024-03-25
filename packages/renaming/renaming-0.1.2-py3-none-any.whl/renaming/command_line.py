import argparse

import renaming


README_URL = "https://github.com/kyan001/PyRenaming/blob/main/README.md"


def main(assigned_args: list | None = None):
    parser = argparse.ArgumentParser(prog="renaming", description="Rename files according to config file.", epilog=f"Checkout README for more details: {README_URL}")
    parser.add_argument("-v", "--version", action="version", version=renaming.__version__)
    parser.add_argument("-c", "--config", dest="config", help="The path or the file name of the config file.")
    parser.add_argument("-f", "--folder", dest="folder", help="The folder path of the files to be renamed. Default is the current folder.")
    parser.add_argument("-d", "--dry-run", dest="dry_run", action="store_true", help="Dry run. Do not actully rename the files.")
    parser.add_argument("-y", "--yes", dest="yes", action="store_true", help="No confirmation. Rename all files without asking.")
    args = parser.parse_args(assigned_args)
    renaming.run_renaming(args.config, folder=args.folder, dry_run=args.dry_run, confirm=(False if args.yes else None))


if __name__ == "__main__":
    main()
