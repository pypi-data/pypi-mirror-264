# renaming
[CHANGELOG](CHANGELOG.md)

[renaming](https://github.com/kyan001/PyRenaming) is a CLI tool to rename files in a directory according to a configuration file.

## Get Started

```sh
pip install renaming  # Install renaming

renaming  # Rename files in the current directory according to `renaming.toml`.
renaming -c/--config $config_file  # Rename files in the current directory according to "$config_file".
renaming -f/--folder $folder  # Rename files in "$folder" according to `renaming.toml`.
renaming -d/--dry-run  # Dry run. Show what would have been done, but do not actually rename anything.
renaming -y/--yes  # Do not ask for confirmation before renaming files.

renaming -h/--help  # Command-line help message.
renaming -v/--version  # Show version information.
```

## Installation

```sh
# pip
pip install --user renaming  # install renaming
pip install --upgrade renaming # upgrade renaming
pip uninstall renaming  # uninstall renaming

# pipx
pipx install renaming  # install renaming through pipx
pipx upgrade renaming  # upgrade renaming through pipx
pipx uninstall renaming  # uninstall renaming through pipx
```

## Config File
* Config file example: [renaming.toml](renaming.toml)
