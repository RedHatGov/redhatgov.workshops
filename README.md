### Install

#### GNU/Linux, or macOS

```sh
#!/bin/bash

git clone https://github.com/RedHatGov/redhatgov.workshops
cd redhatgov.workshops
```

##### No `git`? No problem!

```sh
#!/bin/bash

DIRPATH="${HOME}/Downloads/redhatgov.workshops"; GITUSER="RedHatGov"
GITREPO="https://github.com/${GITUSER}/redhatgov.workshops/archive/master.zip"
ARCHIVE="$(printf "%s" "${GITREPO##*/}")"

# Download and extract
wget $GITREPO \
&& temp="$(mktemp -d)" \
&& unzip -d $temp $ARCHIVE \
&& mkdir -p $DIRPATH \
&& mv $temp/*/* $DIRPATH \
&& rm -rf $temp $ARCHIVE \
&& cd $DIRPATH \
&& unset DIRPATH GITUSER GITREPO ARCHIVE temp
```
