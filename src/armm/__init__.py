from lxml import etree as ET
import re
import os
import sys


# List of required attributes for each of the elements
REQUIRED = {
    'default': [],
    'extend-project': ['name'],
    'include': ['name'],
    'manifest-server': ['url'],
    'notice': [],
    'project': ['name'],
    'remote': ['name', 'fetch'],
    'remove-project': ['name'],
    'repo-hoops': ['in-project', 'enabled-list'],
    'annotation': ['name', 'value'],
    'copyfile': ['src', 'dest'],
    'linkfile': ['src', 'dest'],
}

# Elements which can be defined multiple times
MULTI = [
    'extend-project',
    'include',
    'project',
    'remote',
    'remove-project',
    'annotation',
    'copyfile',
    'linkfile'
]

# Key attributes for elements which can be defined multiple times
MULTI_KEY = {
    'extend-project': 'name',
    'include': 'name',
    'project': 'name',
    'remote': 'name',
    'remove-project': 'name',
    'annotation': 'name',
    'copyfile': 'dest',
    'linkfile': 'dest',
    'project': 'name'
}

# List of elements without attributes
TEXT_ONLY = [
    'notice'
]


class AndroidRepoManifest():
    filename = 'default.xml'
    log = None
    xml = None

    def __init__(self, filename=None, log=None):
        self.log = log

        if filename is not None:
            self.filename = filename

        parser = ET.XMLParser(
            remove_blank_text=True)

        ET.set_default_parser(parser)

    def init(self, force=False):
        self._log_debug('Action: init')

        # Check if file exists or if the forced write is defined
        if os.path.isfile(self.filename) and not force:
            self._log_error("Manifest file %s already exists." % self.filename)

        self.xml = ET.Element('manifest')

        return self

    def load(self):
        self._log_debug('Action: load')

        try:
            self.xml = ET.parse(self.filename).getroot()
        except IOError as e:
            self._log_error(
                "Cannot load manifest file %s. %s" % (self.filename, str(e)))

        return self

    def save(self):
        self._log_debug('Action: save')

        try:
            # Format the XML
            xml = ET.tostring(
                self.xml,
                pretty_print=True,
                xml_declaration=True,
                encoding='utf-8')

            # Write the XML into the file
            fd = open(self.filename, 'wb')
            fd.write(xml)
            fd.close()
        except Exception as e:
            self._log_error(
                "Cannot write manifest file %s. %s" % (self.filename, str(e)))

    def set(self, element, attrs=[], root=None):
        self._log_debug('Action: set')

        if root is None:
            root = self.xml

        if element in MULTI:
            for el in root.findall(element):
                el_key = MULTI_KEY[element]

                # Check if element with the same key already exists
                if el_key in attrs and el.get(el_key) == attrs[el_key]:
                    for key, value in attrs.items():
                        el.set(key, value)

                    break
            else:
                diff = set(REQUIRED[element]).difference(attrs.keys())

                # Check if required attrs are provided
                if diff != set():
                    self._log_error(
                        'The following required attributes not provided: %s' %
                        ', '.join(diff))

                # Add new element
                el = ET.Element(element)

                if element in TEXT_ONLY:
                    el.text = attrs['text']
                else:
                    # Add attributes into the element
                    for key, value in attrs.items():
                        el.set(key, value)

                # Append the new element
                root.append(el)
        else:
            el = root.find(element)

            if el is not None:
                if element in TEXT_ONLY:
                    el.text = attrs['text']
                else:
                    # Add attributes into the element
                    for key, value in attrs.items():
                        el.set(key, value)
            else:
                diff = set(REQUIRED[element]).difference(attrs.keys())

                # Check if required attrs are provided
                if diff != set():
                    self._log_error(
                        'The following required attributes not provided: %s' %
                        ', '.join(diff))

                # Add new element
                el = ET.Element(element)

                if element in TEXT_ONLY:
                    el.text = attrs['text']
                else:
                    # Add attributes into the element
                    for key, value in attrs.items():
                        el.set(key, value)

                # Append the new element
                root.append(el)

        return self

    def pset(self, project, element, attrs=[], root=None):
        self._log_debug('Action: pset')

        if root is None:
            root = self.xml

        # Find the right project element
        for el in root.findall('project'):
            if project == el.get('name'):
                self.set(
                    element=element,
                    attrs=attrs,
                    root=el)

                break
            else:
                # Search sub-projects recursively
                self.pset(
                    project=project,
                    element=element,
                    attrs=attrs,
                    root=el)

        return self

    def remove(self, element, name, attrs=[], root=None):
        self._log_debug('Action: remove')

        if root is None:
            root = self.xml

        if element in MULTI:
            for el in root.findall(element):
                if name == el.get(MULTI_KEY[element]):
                    if len(attrs):
                        intersect = set(REQUIRED[element]).intersection(attrs)

                        # Check if any of the attrs are required
                        if intersect != set():
                            self._log_error(
                                "Cannot remove the follwoing required "
                                "attributes: %s" % ', '.join(intersect))

                        # Remove matching attributes
                        for key in attrs:
                            if key in el.attrib:
                                del el.attrib[key]
                    else:
                        # Remove the whole element
                        root.remove(el)
        else:
            el = root.find(element)

            if el is not None:
                if len(attrs):
                    intersect = set(REQUIRED[element]).intersection(attrs)

                    # Check if any of the attrs are required
                    if intersect != set():
                        self._log_error(
                            "Cannot remove the follwoing required attributes: "
                            "%s" % ', '.join(intersect))

                    # Remove matching attributes
                    for key in attrs:
                        if key in el.attrib:
                            del el.attrib[key]
                else:
                    # Remove the whole element
                    root.remove(el)

        return self

    def premove(self, project, element, name, attrs=[], root=None):
        self._log_debug('Action: premove')

        if root is None:
            root = self.xml

        # Find the right project element
        for el in root.findall('project'):
            if project == el.get('name'):
                self.remove(
                    element=element,
                    name=name,
                    attrs=attrs,
                    root=el)

                break
            else:
                # Search sub-projects recursively
                self.premove(
                    project=project,
                    element=element,
                    name=name,
                    attrs=attrs,
                    root=el)

        return self

    def list(self, element, key=[], value=[], root=None, attr=None):
        self._log_debug('Action: list')

        if root is None:
            root = self.xml

        ret = []

        for el in root.findall(element):
            if len(key):
                all_match = True

                # Check if all key/value pairs match
                for k, v in zip(key, value):
                    if k not in el.attrib:
                        all_match = False
                        break

                    if v.startswith('~'):
                        v = v[1:]
                        neg = False

                        if v.startswith('!'):
                            v = v[1:]
                            neg = True

                        re_p = re.compile(v)
                        not_match = re_p.search(el.attrib[k]) is None

                        if neg:
                            not_match = not not_match

                        if not_match:
                            all_match = False
                            break
                    else:
                        if v != el.attrib[k]:
                            all_match = False
                            break

                # Get only elements with particular key/value combination
                if all_match:
                    record = {
                        'element': element,
                        'attrs': dict(el.attrib),
                        'text': el.text
                    }

                    if attr is not None:
                        if attr in record['attrs']:
                            ret.append(record['attrs'][attr])
                    else:
                        ret.append(record)
            else:
                # Get all elements
                record = {
                    'element': element,
                    'attrs': dict(el.attrib),
                    'text': el.text
                }

                if attr is not None:
                    if attr in record['attrs']:
                        ret.append(record['attrs'][attr])
                else:
                    ret.append(record)

        return ret

    def plist(self, project, element, key=[], value=[], root=None, attr=None):
        self._log_debug('Action: plist')

        if root is None:
            root = self.xml

        ret = []

        # Find the right project element
        for el in root.findall('project'):
            if project == el.get('name'):
                ret = self.list(
                    element=element,
                    key=key,
                    value=value,
                    root=el,
                    attr=attr)

                break
            else:
                # Search sub-projects recursively
                ret = self.plist(
                    project=project,
                    element=element,
                    key=key,
                    value=value,
                    root=el)

                if ret != []:
                    break

        return ret

    def _log_info(self, text):
        if self.log is not None:
            self.log.info(text)

    def _log_debug(self, text):
        if self.log is not None:
            self.log.debug(text)

    def _log_error(self, text):
        if self.log is not None:
            self.log.error(text)
            sys.exit(1)
        else:
            raise(text)
