# Tar GnuPG
Manage a secure archive containing sensative docs.

You might be thinking, "Hey there's already a
[gpgtar](https://www.gnupg.org/documentation/manuals/gnupg/gpgtar.html)
which seems to do exactly this, why don't I use that?", and you could be right,
depending on your needs. The biggest difference is this package allows you to
add files to an existing archive. (It technically creates a new one and
overwrites your old one, but does it without you needing to worry about that).
That's my biggest use case anyway. Also, I was bad at searching and didn't
realize that program existed before writing this one (I had even initally given
them the same name by coincidence).

## Usage
```
usage: targpg [-h] [-V] [--add [ADD ...]] [--create] [--extract [EXTR ...]]
              [--passfile PASSFILE] [--list] [--unique] [--update]
              [--output] [--directory DIRECTORY]
              archive

manage secure archive containing sensative docs

positional arguments:
  archive               tar archive secured by gpg symetric password

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  --add [ADD ...], -a [ADD ...]
                        add files to the archive
  --create, -c          create the file without confirmation if it does
                        not exist
  --extract [EXTR ...], -e [EXTR ...]
                        extract the files from the archive, if no files given
                        a prompt will ask
  --passfile PASSFILE, -p PASSFILE
                        file with archive password stored in it
  --list, -l            list the contents of the archive
  --unique, -x          only add unique files, if the file exists an error
                        is thrown
  --update, -u          overwrite existing files if any being passed in match
  --output, -o          directory to extract files to
  --directory DIRECTORY, -d DIRECTORY
                        when adding files, do it relative to this directory
```

### add
Add new files to the archive. If the `--unique` flag is used, then existing
files will cause an error. The `--update` flag will replace existing files
with ones passed in. `--directory` sets the working directory so files are
added relative to that directory.

### create
Auto create the archive if it does not already exist.

### extract
Extract files from the archive. If the flag is used with no arguments, you will
be asked which files you want to extract. The `--output` flag will set the
directory to extract the files to.

### passfile
Load the password of the archive from a file instead of stdin.

### list
List the contents of the archive.


## Links
* [PyPi Project](https://pypi.org/project/targpg)
* [Github](https://github.com/spslater/targpg)

## Contributing
Help is greatly appreciated. First check if there are any issues open that
relate to what you want to help with. Also feel free to make a pull request
with changes / fixes you make.

## License
[MIT License](https://opensource.org/licenses/MIT)
