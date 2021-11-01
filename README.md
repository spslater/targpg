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
usage: targpg [-h] [-V] [-v] [-q] [-c] [-p PASSFILE] [-a [ADD ...]] [-x] [-u] [-d DIR]
              [-e [EXTR ...]] [-o] [-l] archive

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
  -a [ADD ...], --add [ADD ...]
                        add files to the archive
  -x, --unique          only add unique files, if the file exists an error is thrown
  -u, --update          overwrite existing files if any being passed in match
  -d DIR, --directory DIR
                        when adding files, do it relative to this directory
  -e [EXTR ...], --extract [EXTR ...]
                        extract the files from the archive, if no files given a prompt will ask
  -o, --output          directory to extract files to
  -l, --list            list the contents of the archive
```

### create
Auto create the archive if it does not already exist.

### passfile
Load the password of the archive from a file instead of stdin.

### add
Add new files to the archive. If the `--unique` flag is used, then existing
files will cause an error. The `--update` flag will replace existing files
with ones passed in. `--directory` sets the working directory so files are
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
