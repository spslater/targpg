# Tar GnuPG
Manage a secure archive containing sensative docs.

![Run Tests](https://github.com/spslater/targpg/actions/workflows/tests.yml/badge.svg)
![Build Standalone Apps](https://github.com/spslater/targpg/actions/workflows/execs.yml/badge.svg)
![Publish to Repositories](https://github.com/spslater/targpg/actions/workflows/repos.yml/badge.svg)

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
usage: targpg [-h] [-V] [-v] [-q] [-c] [-p PASSFILE] [-o] [-d DIR] [-a [ADD ...]] [-u [UPDATE ...]] [-r [REMOVE ...]] [-e [EXTR ...]] [-l]
              archive

manage secure archive containing sensative docs

positional arguments:
  archive               tar file secured by gpg symetric password

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -v, --verbose         more verbose output
  -q, --quite           supress output
  -c, --create          create the file without confirmation if it does not exist
  -p PASSFILE, --passfile PASSFILE
                        file with archive password stored in it
  -o, --output          directory to extract files to
  -d DIR, --directory DIR
                        when adding files, do it relative to this directory
  -a [ADD ...], --add [ADD ...]
                        add files to the archive
  -u [UPDATE ...], --update [UPDATE ...]
                        overwrite existing files if any being passed in match
  -r [REMOVE ...], --remove [REMOVE ...]
                        add files to the archive
  -e [EXTR ...], --extract [EXTR ...]
                        extract the files from the archive, if no files given a prompt will ask
  -l, --list            list the contents of the archive
```

### create
Auto create the archive if it does not already exist.

### passfile
Load the password of the archive from a file instead of stdin.

### add
Add new files to the archive. `--directory` sets the working directory so files are
added relative to that directory.

### update
Update existing files in the archive. If they don't exist then an error will
be raised. `--directory` sets the working directory so files are
added relative to that directory.

### remove
Remove existing files in the archive. If they don't exist then an error will
be raised. `--directory` sets the working directory so files are
added relative to that directory.

### extract
Extract files from the archive. If the flag is used with no arguments, you will
be asked which files you want to extract. The `--output` flag will set the
directory to extract the files to.

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
