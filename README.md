Android Repo Manifest Management
================================

Tool which helps to create, edit and explore the Android repo manifest file.


Installation
------------

```
$ python setup.py install
```

or

```
$ pip install armm
```


Usage
-----

```
$ armm --help
Android Repo Manifest Management tool.

Usage:
  armm init [options]
  armm set [options] notice <value>
  armm set [options] default (<key> <value>)...
  armm set [options] extend-project (<key> <value>)...
  armm set [options] include (<key> <value>)...
  armm set [options] manifest-server (<key> <value>)...
  armm set [options] project (<key> <value>)...
  armm set [options] remote (<key> <value>)...
  armm set [options] remove-project (<key> <value>)...
  armm set [options] repo-hoops (<key> <value>)...
  armm pset [options] <project> annotation (<key> <value>)...
  armm pset [options] <project> copyfile (<key> <value>)...
  armm pset [options] <project> linkfile (<key> <value>)...
  armm pset [options] <project> project (<key> <value>)...
  armm remove [options] manifest-server
  armm remove [options] notice
  armm remove [options] repo-hoops
  armm remove [options] default [<key>]...
  armm remove [options] include <name>
  armm remove [options] remove-project <name>
  armm remove [options] extend-project <name> [<key>]...
  armm remove [options] project <name> [<key>]...
  armm remove [options] remote <name> [<key>]...
  armm premove [options] <project> copyfile <dest>
  armm premove [options] <project> linkfile <dest>
  armm premove [options] <project> annotation <name> [<key>]...
  armm premove [options] <project> project <name> [<key>]...
  armm list [options] default
  armm list [options] manifest-server
  armm list [options] notice
  armm list [options] repo-hoops
  armm list [options] extend-project [<key> <value>]...
  armm list [options] include [<key> <value>]...
  armm list [options] project [<key> <value>]...
  armm list [options] remote [<key> <value>]...
  armm list [options] remove-project [<key> <value>]...
  armm plist [options] <project> annotation [<key> <value>]...
  armm plist [options] <project> copyfile [<key> <value>]...
  armm plist [options] <project> linkfile [<key> <value>]...
  armm plist [options] <project> project [<key> <value>]...
  armm -h | --help
  armm --version

Init options:
  -F --force             Initiate new file even if the file already exists.

List options:
  -o TYPE --output=TYPE  Output type (plain|json|yaml) [default: plain].
  -n --not-pretty        Disable pretty formatting for JSON and YAML output.
  -a ATTR --attr=ATTR    Print only content of the specified attribute.

Common options:
  -f FILE --file=FILE    Manifest filename [default: default.xml].
  -v --verbose           Show verbose output.
  -h --help              Show this screen.
  --version              Show version.
```


Examples
--------

```
# Create empty XML document
armm init

# Create one remote element
armm set remote \
  name aosp \
  fetch .. \
  review https://android-review.googlesource.com/

# Create the default element
armm set default \
  revision master \
  remote aosp \
  sync-j 4

# Create three project elements
armm set project \
  name platform/build \
  path build/make \
  groups pdk
armm set project \
  name platform/build/blueprint \
  path build/blueprint \
  groups pdk,trade
armm set project \
  name platform/build/kati \
  path build/kati \
  groups pdk,tradefed

# Add revision into the first project
armm set project \
  name platform/build \
  revision master

# Change the value of the groups attribute in the second project
armm set project \
  name platform/build/blueprint \
  groups pdk,tradefed

# Remove the revision attribute from the first project
armm remove project platform/build revision

# Remove the second project
armm remove project platform/build/blueprint

# Add copyfile element into the first project
armm pset platform/build copyfile \
  src core/root.mk \
  dest Makefile

# Add project element into the first project
armm pset platform/build project \
  name test1

# Add linkfile element into the sub-project test1
armm pset test1 linkfile \
  src CleanSpec.mk \
  dest build/CleanSpec.mk

# Remove the copyfile element from the first project
armm premove platform/build copyfile Makefile

# List all remote elements
armm list remote

# List all top-level project elements
armm list project

# List all copyfile elements from the sub-project of the test1 project
armm plist test1 linkfile

# List all projects with groups=pdk
armm list project groups pdk

# List all projects containing pdk in their groups
# (the "~" at the beginning of the value indicates using regexp)
armm list project groups '~pdk'

# List all projects containing pdk in the groups and word kati in the path
# (using negative regex in the second value)
armm list project groups '~pdk' path '~!kati'

# Print only the path of the first project
armm -a path list project name platform/build
```


Dependencies
------------

- [`docopt`](http://docopt.org)
- [`lxml`](http://lxml.de)
- [`PyYAML`](http://pyyaml.org) (optional)


Resources
---------

- [Android repo script](https://code.google.com/p/git-repo/)
- [Manifest format](https://gerrit.googlesource.com/git-repo/+/master/docs/manifest-format.txt)
- [AOSP manifest file](https://android.googlesource.com/platform/manifest/+/master/default.xml)


License
-------

MIT


Author
------

Jiri Tyr
