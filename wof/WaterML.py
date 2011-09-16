#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Generated Tue Feb 15 14:13:42 2011 by generateDS.py version 2.3b.
#

import sys
import getopt
import re as re_

etree_ = None
Verbose_import_ = False
(   XMLParser_import_none, XMLParser_import_lxml,
    XMLParser_import_elementtree
    ) = range(3)
XMLParser_import_library = None
try:
    # lxml
    from lxml import etree as etree_
    XMLParser_import_library = XMLParser_import_lxml
    if Verbose_import_:
        print("running with lxml.etree")
except ImportError:
    try:
        # cElementTree from Python 2.5+
        import xml.etree.cElementTree as etree_
        XMLParser_import_library = XMLParser_import_elementtree
        if Verbose_import_:
            print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # ElementTree from Python 2.5+
            import xml.etree.ElementTree as etree_
            XMLParser_import_library = XMLParser_import_elementtree
            if Verbose_import_:
                print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree_
                XMLParser_import_library = XMLParser_import_elementtree
                if Verbose_import_:
                    print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree_
                    XMLParser_import_library = XMLParser_import_elementtree
                    if Verbose_import_:
                        print("running with ElementTree")
                except ImportError:
                    raise ImportError("Failed to import ElementTree from any known place")


class GeneratedsSuper(object):
    def gds_format_string(self, input_data, input_name=''):
        return input_data
    def gds_format_integer(self, input_data, input_name=''):
        return '%d' % input_data
    def gds_format_float(self, input_data, input_name=''):
        return "{0}".format(input_data)
    def gds_format_double(self, input_data, input_name=''):
        return "{0}".format(input_data)
    def gds_format_boolean(self, input_data, input_name=''):
        return '%s' % input_data
    def gds_str_lower(self, instring):
        return instring.lower()

#
# Globals
#

ExternalEncoding = 'utf-8'
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
STRING_CLEANUP_PAT = re_.compile(r"[\n\r\s]+")

#
# Support/utility functions.
#

def showIndent(outfile, level):
    for idx in range(level):
        outfile.write(u'    ')

def quote_xml(inStr):
    if not inStr:
        return ''
    s1 = (isinstance(inStr, basestring) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1

def quote_attrib(inStr):
    s1 = (isinstance(inStr, basestring) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1

def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


class GDSParseError(Exception):
    pass

def raise_parse_error(node, msg):
    if XMLParser_import_library == XMLParser_import_lxml:
        msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline, )
    else:
        msg = '%s (element %s)' % (msg, node.tag, )
    raise GDSParseError(msg)


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name, namespace):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip(): 
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(outfile, level, namespace,name)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write(u'<%s>%s</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write(u'<%s>%d</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write(u'<%s>%f</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write(u'<%s>%g</%s>' % (self.name, self.value, self.name))
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write(u'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write(u'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write(u'model_.MixedContainer(%d, %d, "%s",\n' % \
                (self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(u')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0):
        self.name = name
        self.data_type = data_type
        self.container = container
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type_chain(self): return self.data_type
    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container

def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#

class siteCode(GeneratedsSuper):
    """A &lt;siteCode&gt; is an identifier that this site is referred to
    as. This Code used by organization that collects the data to
    identify the site. A siteCode has a reference to it's source or
    network as the @network. For waterWebServices, a site/location
    is the network plus the value of the sitecode, eg
    '@network:siteCode' siteCode identifiers often change, so
    multiple siteCode elements are allowed There may be multiple
    siteCode elements. Only one should be labeled as the default
    using @defaultID (set attribute defaultID=true) Multiple
    siteCode elements can utilize different observation networks may
    refer to the same site with different identifiers. True if this
    is the main identifier that this service uses to access this
    site. default value is false. The abbreviation for the
    datasource or observation network that this site code is
    associated with. A siteCode has a reference to it's source or
    network as the @network. For waterWebServices, a site/location
    is the network plus the value of the sitecode, eg
    '@network:siteCode'An internal numeric identifier of the site.
    Code used to differentiate sites in a datasource. Agency codes
    are specific to a data source, and are not required nor do they
    need to be understood by a web service client.optional name to
    provide more detail about an agency code"""
    subclass = None
    superclass = None
    def __init__(self, agencyCode=None, defaultId=None, siteID=None, network=None, agencyName=None, valueOf_=None):
        self.agencyCode = _cast(None, agencyCode)
        self.defaultId = _cast(bool, defaultId)
        self.siteID = _cast(None, siteID)
        self.network = _cast(None, network)
        self.agencyName = _cast(None, agencyName)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if siteCode.subclass:
            return siteCode.subclass(*args_, **kwargs_)
        else:
            return siteCode(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_agencyCode(self): return self.agencyCode
    def set_agencyCode(self, agencyCode): self.agencyCode = agencyCode
    def get_defaultId(self): return self.defaultId
    def set_defaultId(self, defaultId): self.defaultId = defaultId
    def get_siteID(self): return self.siteID
    def set_siteID(self, siteID): self.siteID = siteID
    def get_network(self): return self.network
    def set_network(self, network): self.network = network
    def get_agencyName(self): return self.agencyName
    def set_agencyName(self, agencyName): self.agencyName = agencyName
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='siteCode', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='siteCode')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='siteCode'):
        if self.agencyCode is not None and 'agencyCode' not in already_processed:
            already_processed.append('agencyCode')
            outfile.write(u' agencyCode=%s' % (self.gds_format_string(quote_attrib(self.agencyCode), input_name='agencyCode'), ))
        if self.defaultId is not None and 'defaultId' not in already_processed:
            already_processed.append('defaultId')
            outfile.write(u' defaultId="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.defaultId)), input_name='defaultId'))
        if self.siteID is not None and 'siteID' not in already_processed:
            already_processed.append('siteID')
            outfile.write(u' siteID=%s' % (self.gds_format_string(quote_attrib(self.siteID), input_name='siteID'), ))
        outfile.write(u' network=%s' % (self.gds_format_string(quote_attrib(self.network), input_name='network'), ))
        if self.agencyName is not None and 'agencyName' not in already_processed:
            already_processed.append('agencyName')
            outfile.write(u' agencyName=%s' % (self.gds_format_string(quote_attrib(self.agencyName), input_name='agencyName'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='siteCode'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='siteCode'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.agencyCode is not None and 'agencyCode' not in already_processed:
            already_processed.append('agencyCode')
            showIndent(outfile, level)
            outfile.write(u'agencyCode = "%s",\n' % (self.agencyCode,))
        if self.defaultId is not None and 'defaultId' not in already_processed:
            already_processed.append('defaultId')
            showIndent(outfile, level)
            outfile.write(u'defaultId = %s,\n' % (self.defaultId,))
        if self.siteID is not None and 'siteID' not in already_processed:
            already_processed.append('siteID')
            showIndent(outfile, level)
            outfile.write(u'siteID = "%s",\n' % (self.siteID,))
        if self.network is not None and 'network' not in already_processed:
            already_processed.append('network')
            showIndent(outfile, level)
            outfile.write(u'network = "%s",\n' % (self.network,))
        if self.agencyName is not None and 'agencyName' not in already_processed:
            already_processed.append('agencyName')
            showIndent(outfile, level)
            outfile.write(u'agencyName = "%s",\n' % (self.agencyName,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('agencyCode')
        if value is not None and 'agencyCode' not in already_processed:
            already_processed.append('agencyCode')
            self.agencyCode = value
        value = attrs.get('defaultId')
        if value is not None and 'defaultId' not in already_processed:
            already_processed.append('defaultId')
            if value in ('true', '1'):
                self.defaultId = True
            elif value in ('false', '0'):
                self.defaultId = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = attrs.get('siteID')
        if value is not None and 'siteID' not in already_processed:
            already_processed.append('siteID')
            self.siteID = value
        value = attrs.get('network')
        if value is not None and 'network' not in already_processed:
            already_processed.append('network')
            self.network = value
        value = attrs.get('agencyName')
        if value is not None and 'agencyName' not in already_processed:
            already_processed.append('agencyName')
            self.agencyName = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class siteCode


class geoLocation(GeneratedsSuper):
    """The geoLocation speficies the details of the geographic location. It
    contains two portions, a geographic locaiton
    &amp;lt;geogLocation&amp;gt;, and a local location
    &amp;lt;localSiteXY&amp;gt;. In order to be discovered
    spatially, geogLocation is required. The geogLocation can be of
    GeogLocationType, which at present is either a latLonPoint or a
    latLongBox. There may be multiple localSiteXY, which might be
    used by data sources to provide other coordinated system
    information, like UTM and State Plane coordinates."""
    subclass = None
    superclass = None
    def __init__(self, geogLocation=None, localSiteXY=None):
        self.geogLocation = geogLocation
        if localSiteXY is None:
            self.localSiteXY = []
        else:
            self.localSiteXY = localSiteXY
    def factory(*args_, **kwargs_):
        if geoLocation.subclass:
            return geoLocation.subclass(*args_, **kwargs_)
        else:
            return geoLocation(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_geogLocation(self): return self.geogLocation
    def set_geogLocation(self, geogLocation): self.geogLocation = geogLocation
    def get_localSiteXY(self): return self.localSiteXY
    def set_localSiteXY(self, localSiteXY): self.localSiteXY = localSiteXY
    def add_localSiteXY(self, value): self.localSiteXY.append(value)
    def insert_localSiteXY(self, index, value): self.localSiteXY[index] = value
    def export(self, outfile, level, namespace_='', name_='geoLocation', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='geoLocation')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='geoLocation'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='geoLocation'):
        if self.geogLocation:
            self.geogLocation.export(outfile, level, namespace_, name_='geogLocation', )
        for localSiteXY_ in self.localSiteXY:
            localSiteXY_.export(outfile, level, namespace_, name_='localSiteXY')
    def hasContent_(self):
        if (
            self.geogLocation is not None or
            self.localSiteXY
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='geoLocation'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.geogLocation is not None:
            showIndent(outfile, level)
            outfile.write(u'geogLocation=model_.GeogLocationType(\n')
            self.geogLocation.exportLiteral(outfile, level, name_='geogLocation')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        showIndent(outfile, level)
        outfile.write(u'localSiteXY=[\n')
        level += 1
        for localSiteXY_ in self.localSiteXY:
            showIndent(outfile, level)
            outfile.write(u'model_.localSiteXY(\n')
            localSiteXY_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'geogLocation': 
            obj_ = GeogLocationType.factory()
            obj_.build(child_)
            self.set_geogLocation(obj_)
        elif nodeName_ == 'localSiteXY': 
            obj_ = localSiteXY.factory()
            obj_.build(child_)
            self.localSiteXY.append(obj_)
# end class geoLocation


class localSiteXY(GeneratedsSuper):
    """Site information can contain one or more other locations using the
    localSiteXY element. The projection string should be stored in
    projectionInformation. Lat or Northing = Y Lon or Easting = X
    Spatial Reference System of the local coordinates. This should
    use the PROJ4 projection string standard"""
    subclass = None
    superclass = None
    def __init__(self, projectionInformation=None, X=None, Y=None, Z=None, note=None):
        self.projectionInformation = _cast(None, projectionInformation)
        self.X = X
        self.Y = Y
        self.Z = Z
        if note is None:
            self.note = []
        else:
            self.note = note
    def factory(*args_, **kwargs_):
        if localSiteXY.subclass:
            return localSiteXY.subclass(*args_, **kwargs_)
        else:
            return localSiteXY(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_X(self): return self.X
    def set_X(self, X): self.X = X
    def get_Y(self): return self.Y
    def set_Y(self, Y): self.Y = Y
    def get_Z(self): return self.Z
    def set_Z(self, Z): self.Z = Z
    def get_note(self): return self.note
    def set_note(self, note): self.note = note
    def add_note(self, value): self.note.append(value)
    def insert_note(self, index, value): self.note[index] = value
    def get_projectionInformation(self): return self.projectionInformation
    def set_projectionInformation(self, projectionInformation): self.projectionInformation = projectionInformation
    def export(self, outfile, level, namespace_='', name_='localSiteXY', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='localSiteXY')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='localSiteXY'):
        if self.projectionInformation is not None and 'projectionInformation' not in already_processed:
            already_processed.append('projectionInformation')
            outfile.write(u' projectionInformation=%s' % (self.gds_format_string(quote_attrib(self.projectionInformation), input_name='projectionInformation'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='localSiteXY'):
        if self.X is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sX>%s</%sX>\n' % (namespace_, self.gds_format_string(quote_xml(self.X), input_name='X'), namespace_))
        if self.Y is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sY>%s</%sY>\n' % (namespace_, self.gds_format_string(quote_xml(self.Y), input_name='Y'), namespace_))
        if self.Z is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sZ>%s</%sZ>\n' % (namespace_, self.gds_format_string(quote_xml(self.Z), input_name='Z'), namespace_))
        for note_ in self.note:
            note_.export(outfile, level, namespace_, name_='note')
    def hasContent_(self):
        if (
            self.X is not None or
            self.Y is not None or
            self.Z is not None or
            self.note
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='localSiteXY'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.projectionInformation is not None and 'projectionInformation' not in already_processed:
            already_processed.append('projectionInformation')
            showIndent(outfile, level)
            outfile.write(u'projectionInformation = "%s",\n' % (self.projectionInformation,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.X is not None:
            showIndent(outfile, level)
            outfile.write(u'X=%s,\n' % quote_python(self.X))
        if self.Y is not None:
            showIndent(outfile, level)
            outfile.write(u'Y=%s,\n' % quote_python(self.Y))
        if self.Z is not None:
            showIndent(outfile, level)
            outfile.write(u'Z=%s,\n' % quote_python(self.Z))
        showIndent(outfile, level)
        outfile.write(u'note=[\n')
        level += 1
        for note_ in self.note:
            showIndent(outfile, level)
            outfile.write(u'model_.NoteType(\n')
            note_.exportLiteral(outfile, level, name_='NoteType')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('projectionInformation')
        if value is not None and 'projectionInformation' not in already_processed:
            already_processed.append('projectionInformation')
            self.projectionInformation = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'X':
            X_ = child_.text
            self.X = X_
        elif nodeName_ == 'Y':
            Y_ = child_.text
            self.Y = Y_
        elif nodeName_ == 'Z':
            Z_ = child_.text
            self.Z = Z_
        elif nodeName_ == 'note': 
            obj_ = NoteType.factory()
            obj_.build(child_)
            self.note.append(obj_)
# end class localSiteXY


class TsValuesSingleVariableType(GeneratedsSuper):
    """TsValuesSingleVariableTypea aggregates the list of values and
    associated metadata. It is the values element in the
    timeSereisResponse Attributes are optional, but use @count is
    encouraged. The atrributes @unitsAreConverted,
    @untsCode,@unitsAbbreviation, and @unitsType were originally
    included to allow for translation from orignal variable units.
    Thier use is not encouraged. Get unit information from the
    Variable element.If a webservice has transformed the time zone
    from the original data.the measurment units of the value
    elements in this values element True if a webservice has
    transformed the data from the original units."""
    subclass = None
    superclass = None
    def __init__(self, count=None, unitsAbbreviation=None, unitsType=None, timeZoneShiftApplied=None, unitsAreConverted=False, unitsCode=None, value=None, qualifier=None, qualityControlLevel=None, method=None, source=None, offset=None):
        self.count = _cast(int, count)
        self.unitsAbbreviation = _cast(None, unitsAbbreviation)
        self.unitsType = _cast(None, unitsType)
        self.timeZoneShiftApplied = _cast(bool, timeZoneShiftApplied)
        self.unitsAreConverted = _cast(bool, unitsAreConverted)
        self.unitsCode = _cast(None, unitsCode)
        if value is None:
            self.value = []
        else:
            self.value = value
        if qualifier is None:
            self.qualifier = []
        else:
            self.qualifier = qualifier
        if qualityControlLevel is None:
            self.qualityControlLevel = []
        else:
            self.qualityControlLevel = qualityControlLevel
        if method is None:
            self.method = []
        else:
            self.method = method
        if source is None:
            self.source = []
        else:
            self.source = source
        if offset is None:
            self.offset = []
        else:
            self.offset = offset
    def factory(*args_, **kwargs_):
        if TsValuesSingleVariableType.subclass:
            return TsValuesSingleVariableType.subclass(*args_, **kwargs_)
        else:
            return TsValuesSingleVariableType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_value(self): return self.value
    def set_value(self, value): self.value = value
    def add_value(self, value): self.value.append(value)
    def insert_value(self, index, value): self.value[index] = value
    def get_qualifier(self): return self.qualifier
    def set_qualifier(self, qualifier): self.qualifier = qualifier
    def add_qualifier(self, value): self.qualifier.append(value)
    def insert_qualifier(self, index, value): self.qualifier[index] = value
    def get_qualityControlLevel(self): return self.qualityControlLevel
    def set_qualityControlLevel(self, qualityControlLevel): self.qualityControlLevel = qualityControlLevel
    def add_qualityControlLevel(self, value): self.qualityControlLevel.append(value)
    def insert_qualityControlLevel(self, index, value): self.qualityControlLevel[index] = value
    def get_method(self): return self.method
    def set_method(self, method): self.method = method
    def add_method(self, value): self.method.append(value)
    def insert_method(self, index, value): self.method[index] = value
    def get_source(self): return self.source
    def set_source(self, source): self.source = source
    def add_source(self, value): self.source.append(value)
    def insert_source(self, index, value): self.source[index] = value
    def get_offset(self): return self.offset
    def set_offset(self, offset): self.offset = offset
    def add_offset(self, value): self.offset.append(value)
    def insert_offset(self, index, value): self.offset[index] = value
    def get_count(self): return self.count
    def set_count(self, count): self.count = count
    def get_unitsAbbreviation(self): return self.unitsAbbreviation
    def set_unitsAbbreviation(self, unitsAbbreviation): self.unitsAbbreviation = unitsAbbreviation
    def get_unitsType(self): return self.unitsType
    def set_unitsType(self, unitsType): self.unitsType = unitsType
    def validate_UnitsTypeEnum(self, value):
        # Validate type UnitsTypeEnum, a restriction on xsi:string.
        pass
    def get_timeZoneShiftApplied(self): return self.timeZoneShiftApplied
    def set_timeZoneShiftApplied(self, timeZoneShiftApplied): self.timeZoneShiftApplied = timeZoneShiftApplied
    def get_unitsAreConverted(self): return self.unitsAreConverted
    def set_unitsAreConverted(self, unitsAreConverted): self.unitsAreConverted = unitsAreConverted
    def get_unitsCode(self): return self.unitsCode
    def set_unitsCode(self, unitsCode): self.unitsCode = unitsCode
    def export(self, outfile, level, namespace_='', name_='TsValuesSingleVariableType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='TsValuesSingleVariableType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='TsValuesSingleVariableType'):
        if self.count is not None and 'count' not in already_processed:
            already_processed.append('count')
            outfile.write(u' count="%s"' % self.gds_format_integer(self.count, input_name='count'))
        if self.unitsAbbreviation is not None and 'unitsAbbreviation' not in already_processed:
            already_processed.append('unitsAbbreviation')
            outfile.write(u' unitsAbbreviation=%s' % (self.gds_format_string(quote_attrib(self.unitsAbbreviation), input_name='unitsAbbreviation'), ))
        if self.unitsType is not None and 'unitsType' not in already_processed:
            already_processed.append('unitsType')
            outfile.write(u' unitsType=%s' % (quote_attrib(self.unitsType), ))
        if self.timeZoneShiftApplied is not None and 'timeZoneShiftApplied' not in already_processed:
            already_processed.append('timeZoneShiftApplied')
            outfile.write(u' timeZoneShiftApplied="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.timeZoneShiftApplied)), input_name='timeZoneShiftApplied'))
        if self.unitsAreConverted is not None and 'unitsAreConverted' not in already_processed:
            already_processed.append('unitsAreConverted')
            outfile.write(u' unitsAreConverted="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.unitsAreConverted)), input_name='unitsAreConverted'))
        if self.unitsCode is not None and 'unitsCode' not in already_processed:
            already_processed.append('unitsCode')
            outfile.write(u' unitsCode=%s' % (self.gds_format_string(quote_attrib(self.unitsCode), input_name='unitsCode'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='TsValuesSingleVariableType'):
        for value_ in self.value:
            value_.export(outfile, level, namespace_, name_='value')
        for qualifier_ in self.qualifier:
            qualifier_.export(outfile, level, namespace_, name_='qualifier')
        for qualityControlLevel_ in self.qualityControlLevel:
            qualityControlLevel_.export(outfile, level, namespace_, name_='qualityControlLevel')
        for method_ in self.method:
            method_.export(outfile, level, namespace_, name_='method')
        for source_ in self.source:
            source_.export(outfile, level, namespace_, name_='source')
        for offset_ in self.offset:
            offset_.export(outfile, level, namespace_, name_='offset')
    def hasContent_(self):
        if (
            self.value or
            self.qualifier or
            self.qualityControlLevel or
            self.method or
            self.source or
            self.offset
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='TsValuesSingleVariableType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.count is not None and 'count' not in already_processed:
            already_processed.append('count')
            showIndent(outfile, level)
            outfile.write(u'count = %d,\n' % (self.count,))
        if self.unitsAbbreviation is not None and 'unitsAbbreviation' not in already_processed:
            already_processed.append('unitsAbbreviation')
            showIndent(outfile, level)
            outfile.write(u'unitsAbbreviation = "%s",\n' % (self.unitsAbbreviation,))
        if self.unitsType is not None and 'unitsType' not in already_processed:
            already_processed.append('unitsType')
            showIndent(outfile, level)
            outfile.write(u'unitsType = "%s",\n' % (self.unitsType,))
        if self.timeZoneShiftApplied is not None and 'timeZoneShiftApplied' not in already_processed:
            already_processed.append('timeZoneShiftApplied')
            showIndent(outfile, level)
            outfile.write(u'timeZoneShiftApplied = %s,\n' % (self.timeZoneShiftApplied,))
        if self.unitsAreConverted is not None and 'unitsAreConverted' not in already_processed:
            already_processed.append('unitsAreConverted')
            showIndent(outfile, level)
            outfile.write(u'unitsAreConverted = %s,\n' % (self.unitsAreConverted,))
        if self.unitsCode is not None and 'unitsCode' not in already_processed:
            already_processed.append('unitsCode')
            showIndent(outfile, level)
            outfile.write(u'unitsCode = "%s",\n' % (self.unitsCode,))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write(u'value=[\n')
        level += 1
        for value_ in self.value:
            showIndent(outfile, level)
            outfile.write(u'model_.ValueSingleVariable(\n')
            value_.exportLiteral(outfile, level, name_='ValueSingleVariable')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        showIndent(outfile, level)
        outfile.write(u'qualifier=[\n')
        level += 1
        for qualifier_ in self.qualifier:
            showIndent(outfile, level)
            outfile.write(u'model_.qualifier(\n')
            qualifier_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        showIndent(outfile, level)
        outfile.write(u'qualityControlLevel=[\n')
        level += 1
        for qualityControlLevel_ in self.qualityControlLevel:
            showIndent(outfile, level)
            outfile.write(u'model_.qualityControlLevel(\n')
            qualityControlLevel_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        showIndent(outfile, level)
        outfile.write(u'method=[\n')
        level += 1
        for method_ in self.method:
            showIndent(outfile, level)
            outfile.write(u'model_.MethodType(\n')
            method_.exportLiteral(outfile, level, name_='MethodType')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        showIndent(outfile, level)
        outfile.write(u'source=[\n')
        level += 1
        for source_ in self.source:
            showIndent(outfile, level)
            outfile.write(u'model_.SourceType(\n')
            source_.exportLiteral(outfile, level, name_='SourceType')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        showIndent(outfile, level)
        outfile.write(u'offset=[\n')
        level += 1
        for offset_ in self.offset:
            showIndent(outfile, level)
            outfile.write(u'model_.OffsetType(\n')
            offset_.exportLiteral(outfile, level, name_='OffsetType')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('count')
        if value is not None and 'count' not in already_processed:
            already_processed.append('count')
            try:
                self.count = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
            if self.count < 0:
                raise_parse_error(node, 'Invalid NonNegativeInteger')
        value = attrs.get('unitsAbbreviation')
        if value is not None and 'unitsAbbreviation' not in already_processed:
            already_processed.append('unitsAbbreviation')
            self.unitsAbbreviation = value
        value = attrs.get('unitsType')
        if value is not None and 'unitsType' not in already_processed:
            already_processed.append('unitsType')
            self.unitsType = value
        value = attrs.get('timeZoneShiftApplied')
        if value is not None and 'timeZoneShiftApplied' not in already_processed:
            already_processed.append('timeZoneShiftApplied')
            if value in ('true', '1'):
                self.timeZoneShiftApplied = True
            elif value in ('false', '0'):
                self.timeZoneShiftApplied = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = attrs.get('unitsAreConverted')
        if value is not None and 'unitsAreConverted' not in already_processed:
            already_processed.append('unitsAreConverted')
            if value in ('true', '1'):
                self.unitsAreConverted = True
            elif value in ('false', '0'):
                self.unitsAreConverted = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = attrs.get('unitsCode')
        if value is not None and 'unitsCode' not in already_processed:
            already_processed.append('unitsCode')
            self.unitsCode = value
            self.unitsCode = ' '.join(self.unitsCode.split())
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'value': 
            obj_ = ValueSingleVariable.factory()
            obj_.build(child_)
            self.value.append(obj_)
        elif nodeName_ == 'qualifier': 
            obj_ = qualifier.factory()
            obj_.build(child_)
            self.qualifier.append(obj_)
        elif nodeName_ == 'qualityControlLevel': 
            obj_ = qualityControlLevel.factory()
            obj_.build(child_)
            self.qualityControlLevel.append(obj_)
        elif nodeName_ == 'method': 
            obj_ = MethodType.factory()
            obj_.build(child_)
            self.method.append(obj_)
        elif nodeName_ == 'source': 
            obj_ = SourceType.factory()
            obj_.build(child_)
            self.source.append(obj_)
        elif nodeName_ == 'offset': 
            obj_ = OffsetType.factory()
            obj_.build(child_)
            self.offset.append(obj_)
# end class TsValuesSingleVariableType


class VariableInfoType(GeneratedsSuper):
    """VariableInfoType is a complex type containting full descriptive
    information about a variable, as described by the ODM. This
    includes one or more variable codes, the short variable name, a
    detailed variable description, and suggest It also extends the
    ODM model, in several methods: - options contain extended
    reuqest information. - note(s) are for generic extension. -
    extension is an element where additional namespace information
    should be placed. - related allows for parent and child
    relationships between variables to be communicated."""
    subclass = None
    superclass = None
    def __init__(self, metadataDateTime=None, oid=None, variableCode=None, variableName=None, variableDescription=None, valueType=None, dataType=None, generalCategory=None, sampleMedium=None, units=None, options=None, note=None, related=None, extension=None, NoDataValue=None, timeSupport=None):
        self.metadataDateTime = _cast(None, metadataDateTime)
        self.oid = _cast(None, oid)
        if variableCode is None:
            self.variableCode = []
        else:
            self.variableCode = variableCode
        self.variableName = variableName
        self.variableDescription = variableDescription
        self.valueType = valueType
        self.dataType = dataType
        self.generalCategory = generalCategory
        self.sampleMedium = sampleMedium
        self.units = units
        self.options = options
        if note is None:
            self.note = []
        else:
            self.note = note
        self.related = related
        self.extension = extension
        self.NoDataValue = NoDataValue
        self.timeSupport = timeSupport
    def factory(*args_, **kwargs_):
        if VariableInfoType.subclass:
            return VariableInfoType.subclass(*args_, **kwargs_)
        else:
            return VariableInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_variableCode(self): return self.variableCode
    def set_variableCode(self, variableCode): self.variableCode = variableCode
    def add_variableCode(self, value): self.variableCode.append(value)
    def insert_variableCode(self, index, value): self.variableCode[index] = value
    def get_variableName(self): return self.variableName
    def set_variableName(self, variableName): self.variableName = variableName
    def get_variableDescription(self): return self.variableDescription
    def set_variableDescription(self, variableDescription): self.variableDescription = variableDescription
    def get_valueType(self): return self.valueType
    def set_valueType(self, valueType): self.valueType = valueType
    def validate_valueType(self, value):
        # validate type valueType
        pass
    def get_dataType(self): return self.dataType
    def set_dataType(self, dataType): self.dataType = dataType
    def validate_dataType(self, value):
        # validate type dataType
        pass
    def get_generalCategory(self): return self.generalCategory
    def set_generalCategory(self, generalCategory): self.generalCategory = generalCategory
    def validate_generalCategory(self, value):
        # validate type generalCategory
        pass
    def get_sampleMedium(self): return self.sampleMedium
    def set_sampleMedium(self, sampleMedium): self.sampleMedium = sampleMedium
    def validate_sampleMedium(self, value):
        # validate type sampleMedium
        pass
    def get_units(self): return self.units
    def set_units(self, units): self.units = units
    def get_options(self): return self.options
    def set_options(self, options): self.options = options
    def get_note(self): return self.note
    def set_note(self, note): self.note = note
    def add_note(self, value): self.note.append(value)
    def insert_note(self, index, value): self.note[index] = value
    def get_related(self): return self.related
    def set_related(self, related): self.related = related
    def get_extension(self): return self.extension
    def set_extension(self, extension): self.extension = extension
    def get_NoDataValue(self): return self.NoDataValue
    def set_NoDataValue(self, NoDataValue): self.NoDataValue = NoDataValue
    def get_timeSupport(self): return self.timeSupport
    def set_timeSupport(self, timeSupport): self.timeSupport = timeSupport
    def get_metadataDateTime(self): return self.metadataDateTime
    def set_metadataDateTime(self, metadataDateTime): self.metadataDateTime = metadataDateTime
    def get_oid(self): return self.oid
    def set_oid(self, oid): self.oid = oid
    def export(self, outfile, level, namespace_='', name_='VariableInfoType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='VariableInfoType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='VariableInfoType'):
        if self.metadataDateTime is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            outfile.write(u' metadataDateTime=%s' % (self.gds_format_string(quote_attrib(self.metadataDateTime), input_name='metadataDateTime'), ))
        if self.oid is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            outfile.write(u' oid=%s' % (self.gds_format_string(quote_attrib(self.oid), input_name='oid'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='VariableInfoType'):
        for variableCode_ in self.variableCode:
            variableCode_.export(outfile, level, namespace_, name_='variableCode')
        if self.variableName is not None:
            showIndent(outfile, level)
            outfile.write(u'<%svariableName>%s</%svariableName>\n' % (namespace_, self.gds_format_string(quote_xml(self.variableName), input_name='variableName'), namespace_))
        if self.variableDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'<%svariableDescription>%s</%svariableDescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.variableDescription), input_name='variableDescription'), namespace_))
        if self.valueType is not None:
            showIndent(outfile, level)
            outfile.write(u'<%svalueType>%s</%svalueType>\n' % (namespace_, self.gds_format_string(quote_xml(self.valueType), input_name='valueType'), namespace_))
        if self.dataType is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sdataType>%s</%sdataType>\n' % (namespace_, self.gds_format_string(quote_xml(self.dataType), input_name='dataType'), namespace_))
        if self.generalCategory is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sgeneralCategory>%s</%sgeneralCategory>\n' % (namespace_, self.gds_format_string(quote_xml(self.generalCategory), input_name='generalCategory'), namespace_))
        if self.sampleMedium is not None:
            showIndent(outfile, level)
            outfile.write(u'<%ssampleMedium>%s</%ssampleMedium>\n' % (namespace_, self.gds_format_string(quote_xml(self.sampleMedium), input_name='sampleMedium'), namespace_))
        if self.units:
            self.units.export(outfile, level, namespace_, name_='units')
        if self.options:
            self.options.export(outfile, level, namespace_, name_='options')
        for note_ in self.note:
            note_.export(outfile, level, namespace_, name_='note')
        if self.related:
            self.related.export(outfile, level, namespace_, name_='related')
        if self.extension is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sextension>%s</%sextension>\n' % (namespace_, self.gds_format_string(quote_xml(self.extension), input_name='extension'), namespace_))
        if self.NoDataValue is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sNoDataValue>%s</%sNoDataValue>\n' % (namespace_, self.gds_format_string(quote_xml(self.NoDataValue), input_name='NoDataValue'), namespace_))
        if self.timeSupport:
            self.timeSupport.export(outfile, level, namespace_, name_='timeSupport')
    def hasContent_(self):
        if (
            self.variableCode or
            self.variableName is not None or
            self.variableDescription is not None or
            self.valueType is not None or
            self.dataType is not None or
            self.generalCategory is not None or
            self.sampleMedium is not None or
            self.units is not None or
            self.options is not None or
            self.note or
            self.related is not None or
            self.extension is not None or
            self.NoDataValue is not None or
            self.timeSupport is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='VariableInfoType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.metadataDateTime is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            showIndent(outfile, level)
            outfile.write(u'metadataDateTime = "%s",\n' % (self.metadataDateTime,))
        if self.oid is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            showIndent(outfile, level)
            outfile.write(u'oid = "%s",\n' % (self.oid,))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write(u'variableCode=[\n')
        level += 1
        for variableCode_ in self.variableCode:
            showIndent(outfile, level)
            outfile.write(u'model_.variableCode(\n')
            variableCode_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        if self.variableName is not None:
            showIndent(outfile, level)
            outfile.write(u'variableName=%s,\n' % quote_python(self.variableName))
        if self.variableDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'variableDescription=%s,\n' % quote_python(self.variableDescription))
        if self.valueType is not None:
            showIndent(outfile, level)
            outfile.write(u'valueType=%s,\n' % quote_python(self.valueType))
        if self.dataType is not None:
            showIndent(outfile, level)
            outfile.write(u'dataType=%s,\n' % quote_python(self.dataType))
        if self.generalCategory is not None:
            showIndent(outfile, level)
            outfile.write(u'generalCategory=%s,\n' % quote_python(self.generalCategory))
        if self.sampleMedium is not None:
            showIndent(outfile, level)
            outfile.write(u'sampleMedium=%s,\n' % quote_python(self.sampleMedium))
        if self.units is not None:
            showIndent(outfile, level)
            outfile.write(u'units=model_.units(\n')
            self.units.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.options is not None:
            showIndent(outfile, level)
            outfile.write(u'options=model_.options(\n')
            self.options.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        showIndent(outfile, level)
        outfile.write(u'note=[\n')
        level += 1
        for note_ in self.note:
            showIndent(outfile, level)
            outfile.write(u'model_.NoteType(\n')
            note_.exportLiteral(outfile, level, name_='NoteType')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        if self.related is not None:
            showIndent(outfile, level)
            outfile.write(u'related=model_.related(\n')
            self.related.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.extension is not None:
            showIndent(outfile, level)
            outfile.write(u'extension=%s,\n' % quote_python(self.extension))
        if self.NoDataValue is not None:
            showIndent(outfile, level)
            outfile.write(u'NoDataValue=%s,\n' % quote_python(self.NoDataValue))
        if self.timeSupport is not None:
            showIndent(outfile, level)
            outfile.write(u'timeSupport=model_.timeSupport(\n')
            self.timeSupport.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('metadataDateTime')
        if value is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            self.metadataDateTime = value
        value = attrs.get('oid')
        if value is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            self.oid = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'variableCode': 
            obj_ = variableCode.factory()
            obj_.build(child_)
            self.variableCode.append(obj_)
        elif nodeName_ == 'variableName':
            variableName_ = child_.text
            self.variableName = variableName_
        elif nodeName_ == 'variableDescription':
            variableDescription_ = child_.text
            self.variableDescription = variableDescription_
        elif nodeName_ == 'valueType':
            valueType_ = child_.text
            self.valueType = valueType_
            self.validate_valueType(self.valueType)    # validate type valueType
        elif nodeName_ == 'dataType':
            dataType_ = child_.text
            self.dataType = dataType_
            self.validate_dataType(self.dataType)    # validate type dataType
        elif nodeName_ == 'generalCategory':
            generalCategory_ = child_.text
            self.generalCategory = generalCategory_
            self.validate_generalCategory(self.generalCategory)    # validate type generalCategory
        elif nodeName_ == 'sampleMedium':
            sampleMedium_ = child_.text
            self.sampleMedium = sampleMedium_
            self.validate_sampleMedium(self.sampleMedium)    # validate type sampleMedium
        elif nodeName_ == 'units': 
            obj_ = units.factory()
            obj_.build(child_)
            self.set_units(obj_)
        elif nodeName_ == 'options': 
            obj_ = options.factory()
            obj_.build(child_)
            self.set_options(obj_)
        elif nodeName_ == 'note': 
            obj_ = NoteType.factory()
            obj_.build(child_)
            self.note.append(obj_)
        elif nodeName_ == 'related': 
            obj_ = related.factory()
            obj_.build(child_)
            self.set_related(obj_)
        elif nodeName_ == 'extension':
            extension_ = child_.text
            self.extension = extension_
        elif nodeName_ == 'NoDataValue':
            NoDataValue_ = child_.text
            self.NoDataValue = NoDataValue_
        elif nodeName_ == 'timeSupport': 
            obj_ = timeSupport.factory()
            obj_.build(child_)
            self.set_timeSupport(obj_)
# end class VariableInfoType


class related(GeneratedsSuper):
    """This can be used to build up relationships between variables."""
    subclass = None
    superclass = None
    def __init__(self, parentID=None, relatedID=None):
        self.parentID = parentID
        self.relatedID = relatedID
    def factory(*args_, **kwargs_):
        if related.subclass:
            return related.subclass(*args_, **kwargs_)
        else:
            return related(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_parentID(self): return self.parentID
    def set_parentID(self, parentID): self.parentID = parentID
    def get_relatedID(self): return self.relatedID
    def set_relatedID(self, relatedID): self.relatedID = relatedID
    def export(self, outfile, level, namespace_='', name_='related', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='related')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='related'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='related'):
        if self.parentID is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sparentID>%s</%sparentID>\n' % (namespace_, self.gds_format_string(quote_xml(self.parentID), input_name='parentID'), namespace_))
        if self.relatedID is not None:
            showIndent(outfile, level)
            outfile.write(u'<%srelatedID>%s</%srelatedID>\n' % (namespace_, self.gds_format_string(quote_xml(self.relatedID), input_name='relatedID'), namespace_))
    def hasContent_(self):
        if (
            self.parentID is not None or
            self.relatedID is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='related'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.parentID is not None:
            showIndent(outfile, level)
            outfile.write(u'parentID=%s,\n' % quote_python(self.parentID))
        if self.relatedID is not None:
            showIndent(outfile, level)
            outfile.write(u'relatedID=%s,\n' % quote_python(self.relatedID))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'parentID': 
            obj_ = xsi_string.factory()
            obj_.build(child_)
            self.set_parentID(obj_)
        elif nodeName_ == 'relatedID': 
            obj_ = xsi_string.factory()
            obj_.build(child_)
            self.set_relatedID(obj_)
# end class related


class parentID(GeneratedsSuper):
    """variableCode for the parent"""
    subclass = None
    superclass = None
    def __init__(self, default=None, network=None, vocabulary=None, valueOf_=None):
        self.default = _cast(bool, default)
        self.network = _cast(None, network)
        self.vocabulary = _cast(None, vocabulary)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if parentID.subclass:
            return parentID.subclass(*args_, **kwargs_)
        else:
            return parentID(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_default(self): return self.default
    def set_default(self, default): self.default = default
    def get_network(self): return self.network
    def set_network(self, network): self.network = network
    def get_vocabulary(self): return self.vocabulary
    def set_vocabulary(self, vocabulary): self.vocabulary = vocabulary
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='parentID', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='parentID')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='parentID'):
        if self.default is not None and 'default' not in already_processed:
            already_processed.append('default')
            outfile.write(u' default="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.default)), input_name='default'))
        if self.network is not None and 'network' not in already_processed:
            already_processed.append('network')
            outfile.write(u' network=%s' % (self.gds_format_string(quote_attrib(self.network), input_name='network'), ))
        if self.vocabulary is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            outfile.write(u' vocabulary=%s' % (self.gds_format_string(quote_attrib(self.vocabulary), input_name='vocabulary'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='parentID'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='parentID'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.default is not None and 'default' not in already_processed:
            already_processed.append('default')
            showIndent(outfile, level)
            outfile.write(u'default = %s,\n' % (self.default,))
        if self.network is not None and 'network' not in already_processed:
            already_processed.append('network')
            showIndent(outfile, level)
            outfile.write(u'network = "%s",\n' % (self.network,))
        if self.vocabulary is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            showIndent(outfile, level)
            outfile.write(u'vocabulary = "%s",\n' % (self.vocabulary,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('default')
        if value is not None and 'default' not in already_processed:
            already_processed.append('default')
            if value in ('true', '1'):
                self.default = True
            elif value in ('false', '0'):
                self.default = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = attrs.get('network')
        if value is not None and 'network' not in already_processed:
            already_processed.append('network')
            self.network = value
        value = attrs.get('vocabulary')
        if value is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            self.vocabulary = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class parentID


class relatedID(GeneratedsSuper):
    """Child or other relationships can be encoded using the related
    element."""
    subclass = None
    superclass = None
    def __init__(self, default=None, network=None, vocabulary=None, valueOf_=None):
        self.default = _cast(bool, default)
        self.network = _cast(None, network)
        self.vocabulary = _cast(None, vocabulary)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if relatedID.subclass:
            return relatedID.subclass(*args_, **kwargs_)
        else:
            return relatedID(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_default(self): return self.default
    def set_default(self, default): self.default = default
    def get_network(self): return self.network
    def set_network(self, network): self.network = network
    def get_vocabulary(self): return self.vocabulary
    def set_vocabulary(self, vocabulary): self.vocabulary = vocabulary
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='relatedID', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='relatedID')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='relatedID'):
        if self.default is not None and 'default' not in already_processed:
            already_processed.append('default')
            outfile.write(u' default="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.default)), input_name='default'))
        if self.network is not None and 'network' not in already_processed:
            already_processed.append('network')
            outfile.write(u' network=%s' % (self.gds_format_string(quote_attrib(self.network), input_name='network'), ))
        if self.vocabulary is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            outfile.write(u' vocabulary=%s' % (self.gds_format_string(quote_attrib(self.vocabulary), input_name='vocabulary'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='relatedID'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='relatedID'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.default is not None and 'default' not in already_processed:
            already_processed.append('default')
            showIndent(outfile, level)
            outfile.write(u'default = %s,\n' % (self.default,))
        if self.network is not None and 'network' not in already_processed:
            already_processed.append('network')
            showIndent(outfile, level)
            outfile.write(u'network = "%s",\n' % (self.network,))
        if self.vocabulary is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            showIndent(outfile, level)
            outfile.write(u'vocabulary = "%s",\n' % (self.vocabulary,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('default')
        if value is not None and 'default' not in already_processed:
            already_processed.append('default')
            if value in ('true', '1'):
                self.default = True
            elif value in ('false', '0'):
                self.default = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = attrs.get('network')
        if value is not None and 'network' not in already_processed:
            already_processed.append('network')
            self.network = value
        value = attrs.get('vocabulary')
        if value is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            self.vocabulary = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class relatedID


class timeSupport(GeneratedsSuper):
    """Element containing the time support (or temporal footprint) of the
    data values. @isRegular indicates if the spacing is regular. In
    waterML 1.0, there is a divergence of mean between ODM, and
    WaterML. WaterML only communcates the regularity, and the
    spacing of the observations (timeInterval). Whereas timesupport
    in the ODM is associated with the dataType, and time support.
    This will be addressed in 1.1 0 is used to indicate data values
    that are instantaneous. Other values indicate the time over
    which the data values are implicitly or explicitly averaged or
    aggregated. The default for the TimeSupport field is 0. This
    corresponds to instantaneous values. If the TimeSupport field is
    set to a value other than 0, an appropriate TimeUnitsID must be
    specified. The TimeUnitsID field can only reference valid
    UnitsID values from the Units controlled vocabulary table. If
    the TimeSupport field is set to 0, any time units can be used
    (i.e., seconds, minutes, hours, etc.), however a default value
    of 103 has been used, which corresponds with hours"""
    subclass = None
    superclass = None
    def __init__(self, isRegular=None, unit=None, timeInterval=None):
        self.isRegular = _cast(bool, isRegular)
        self.unit = unit
        self.timeInterval = timeInterval
    def factory(*args_, **kwargs_):
        if timeSupport.subclass:
            return timeSupport.subclass(*args_, **kwargs_)
        else:
            return timeSupport(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_unit(self): return self.unit
    def set_unit(self, unit): self.unit = unit
    def get_timeInterval(self): return self.timeInterval
    def set_timeInterval(self, timeInterval): self.timeInterval = timeInterval
    def get_isRegular(self): return self.isRegular
    def set_isRegular(self, isRegular): self.isRegular = isRegular
    def export(self, outfile, level, namespace_='', name_='timeSupport', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='timeSupport')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='timeSupport'):
        if self.isRegular is not None and 'isRegular' not in already_processed:
            already_processed.append('isRegular')
            outfile.write(u' isRegular="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.isRegular)), input_name='isRegular'))
    def exportChildren(self, outfile, level, namespace_='', name_='timeSupport'):
        if self.unit:
            self.unit.export(outfile, level, namespace_, name_='unit')
        #TODO: Why is an empty element being exported when in ODM the value for time support is 0?
        if self.timeInterval is not None:
            showIndent(outfile, level)
            outfile.write(u'<%stimeInterval>%s</%stimeInterval>\n' % (namespace_, self.gds_format_string(quote_xml(self.timeInterval), input_name='timeInterval'), namespace_))
    def hasContent_(self):
        if (
            self.unit is not None or
            self.timeInterval is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='timeSupport'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.isRegular is not None and 'isRegular' not in already_processed:
            already_processed.append('isRegular')
            showIndent(outfile, level)
            outfile.write(u'isRegular = %s,\n' % (self.isRegular,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.unit is not None:
            showIndent(outfile, level)
            outfile.write(u'unit=model_.UnitsType(\n')
            self.unit.exportLiteral(outfile, level, name_='unit')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.timeInterval is not None:
            showIndent(outfile, level)
            outfile.write(u'timeInterval=%s,\n' % quote_python(self.timeInterval))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('isRegular')
        if value is not None and 'isRegular' not in already_processed:
            already_processed.append('isRegular')
            if value in ('true', '1'):
                self.isRegular = True
            elif value in ('false', '0'):
                self.isRegular = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'unit': 
            obj_ = UnitsType.factory()
            obj_.build(child_)
            self.set_unit(obj_)
        elif nodeName_ == 'timeInterval':
            timeInterval_ = child_.text
            self.timeInterval = timeInterval_
# end class timeSupport


class QueryInfoType(GeneratedsSuper):
    """This contains information about the request, and is used to enable
    the XML responses (timeSeriesResponse,
    variablesResponse,siteResponse) to be stored on disk."""
    subclass = None
    superclass = None
    def __init__(self, creationTime=None, queryURL=None, querySQL=None, criteria=None, note=None, extension=None):
        self.creationTime = creationTime
        self.queryURL = queryURL
        self.querySQL = querySQL
        self.criteria = criteria
        if note is None:
            self.note = []
        else:
            self.note = note
        self.extension = extension
    def factory(*args_, **kwargs_):
        if QueryInfoType.subclass:
            return QueryInfoType.subclass(*args_, **kwargs_)
        else:
            return QueryInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_creationTime(self): return self.creationTime
    def set_creationTime(self, creationTime): self.creationTime = creationTime
    def get_queryURL(self): return self.queryURL
    def set_queryURL(self, queryURL): self.queryURL = queryURL
    def get_querySQL(self): return self.querySQL
    def set_querySQL(self, querySQL): self.querySQL = querySQL
    def get_criteria(self): return self.criteria
    def set_criteria(self, criteria): self.criteria = criteria
    def get_note(self): return self.note
    def set_note(self, note): self.note = note
    def add_note(self, value): self.note.append(value)
    def insert_note(self, index, value): self.note[index] = value
    def get_extension(self): return self.extension
    def set_extension(self, extension): self.extension = extension
    def export(self, outfile, level, namespace_='', name_='QueryInfoType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='QueryInfoType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='QueryInfoType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='QueryInfoType'):
        if self.creationTime is not None:
            showIndent(outfile, level)
            outfile.write(u'<%screationTime>%s</%screationTime>\n' % (namespace_, self.gds_format_string(quote_xml(self.creationTime), input_name='creationTime'), namespace_))
        if self.queryURL is not None:
            showIndent(outfile, level)
            outfile.write(u'<%squeryURL>%s</%squeryURL>\n' % (namespace_, self.gds_format_string(quote_xml(self.queryURL), input_name='queryURL'), namespace_))
        if self.querySQL is not None:
            showIndent(outfile, level)
            outfile.write(u'<%squerySQL>%s</%squerySQL>\n' % (namespace_, self.gds_format_string(quote_xml(self.querySQL), input_name='querySQL'), namespace_))
        if self.criteria:
            self.criteria.export(outfile, level, namespace_, name_='criteria')
        for note_ in self.note:
            note_.export(outfile, level, namespace_, name_='note')
        if self.extension is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sextension>%s</%sextension>\n' % (namespace_, self.gds_format_string(quote_xml(self.extension), input_name='extension'), namespace_))
    def hasContent_(self):
        if (
            self.creationTime is not None or
            self.queryURL is not None or
            self.querySQL is not None or
            self.criteria is not None or
            self.note or
            self.extension is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='QueryInfoType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.creationTime is not None:
            showIndent(outfile, level)
            outfile.write(u'creationTime=%s,\n' % quote_python(self.creationTime))
        if self.queryURL is not None:
            showIndent(outfile, level)
            outfile.write(u'queryURL=%s,\n' % quote_python(self.queryURL))
        if self.querySQL is not None:
            showIndent(outfile, level)
            outfile.write(u'querySQL=%s,\n' % quote_python(self.querySQL))
        if self.criteria is not None:
            showIndent(outfile, level)
            outfile.write(u'criteria=model_.criteria(\n')
            self.criteria.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        showIndent(outfile, level)
        outfile.write(u'note=[\n')
        level += 1
        for note_ in self.note:
            showIndent(outfile, level)
            outfile.write(u'model_.NoteType(\n')
            note_.exportLiteral(outfile, level, name_='NoteType')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        if self.extension is not None:
            showIndent(outfile, level)
            outfile.write(u'extension=%s,\n' % quote_python(self.extension))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'creationTime':
            creationTime_ = child_.text
            self.creationTime = creationTime_
        elif nodeName_ == 'queryURL':
            queryURL_ = child_.text
            self.queryURL = queryURL_
        elif nodeName_ == 'querySQL':
            querySQL_ = child_.text
            self.querySQL = querySQL_
        elif nodeName_ == 'criteria': 
            obj_ = criteria.factory()
            obj_.build(child_)
            self.set_criteria(obj_)
        elif nodeName_ == 'note': 
            obj_ = NoteType.factory()
            obj_.build(child_)
            self.note.append(obj_)
        elif nodeName_ == 'extension':
            extension_ = child_.text
            self.extension = extension_
# end class QueryInfoType


class criteria(GeneratedsSuper):
    """The criteria are the actual parameters that are passed into the
    method. If you are generate this without a XML helper class, be
    sure to properly encode these elements."""
    subclass = None
    superclass = None
    def __init__(self, locationParam=None, variableParam=None, timeParam=None):
        self.locationParam = locationParam
        self.variableParam = variableParam
        self.timeParam = timeParam
    def factory(*args_, **kwargs_):
        if criteria.subclass:
            return criteria.subclass(*args_, **kwargs_)
        else:
            return criteria(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_locationParam(self): return self.locationParam
    def set_locationParam(self, locationParam): self.locationParam = locationParam
    def get_variableParam(self): return self.variableParam
    def set_variableParam(self, variableParam): self.variableParam = variableParam
    def get_timeParam(self): return self.timeParam
    def set_timeParam(self, timeParam): self.timeParam = timeParam
    def export(self, outfile, level, namespace_='', name_='criteria', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='criteria')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='criteria'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='criteria'):
        if self.locationParam is not None:
            showIndent(outfile, level)
            outfile.write(u'<%slocationParam>%s</%slocationParam>\n' % (namespace_, self.gds_format_string(quote_xml(self.locationParam), input_name='locationParam'), namespace_))
        if self.variableParam is not None:
            showIndent(outfile, level)
            outfile.write(u'<%svariableParam>%s</%svariableParam>\n' % (namespace_, self.gds_format_string(quote_xml(self.variableParam), input_name='variableParam'), namespace_))
        if self.timeParam:
            self.timeParam.export(outfile, level, namespace_, name_='timeParam')
    def hasContent_(self):
        if (
            self.locationParam is not None or
            self.variableParam is not None or
            self.timeParam is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='criteria'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.locationParam is not None:
            showIndent(outfile, level)
            outfile.write(u'locationParam=%s,\n' % quote_python(self.locationParam))
        if self.variableParam is not None:
            showIndent(outfile, level)
            outfile.write(u'variableParam=%s,\n' % quote_python(self.variableParam))
        if self.timeParam is not None:
            showIndent(outfile, level)
            outfile.write(u'timeParam=model_.timeParam(\n')
            self.timeParam.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'locationParam':
            locationParam_ = child_.text
            self.locationParam = locationParam_
        elif nodeName_ == 'variableParam':
            variableParam_ = child_.text
            self.variableParam = variableParam_
        elif nodeName_ == 'timeParam': 
            obj_ = timeParam.factory()
            obj_.build(child_)
            self.set_timeParam(obj_)
# end class criteria


class timeParam(GeneratedsSuper):
    """the begin and end time of the GetValues request used to generate a
    timeSeriesResponse."""
    subclass = None
    superclass = None
    def __init__(self, beginDateTime=None, endDateTime=None):
        self.beginDateTime = beginDateTime
        self.endDateTime = endDateTime
    def factory(*args_, **kwargs_):
        if timeParam.subclass:
            return timeParam.subclass(*args_, **kwargs_)
        else:
            return timeParam(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_beginDateTime(self): return self.beginDateTime
    def set_beginDateTime(self, beginDateTime): self.beginDateTime = beginDateTime
    def get_endDateTime(self): return self.endDateTime
    def set_endDateTime(self, endDateTime): self.endDateTime = endDateTime
    def export(self, outfile, level, namespace_='', name_='timeParam', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='timeParam')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='timeParam'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='timeParam'):
        if self.beginDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sbeginDateTime>%s</%sbeginDateTime>\n' % (namespace_, self.gds_format_string(quote_xml(self.beginDateTime), input_name='beginDateTime'), namespace_))
        if self.endDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sendDateTime>%s</%sendDateTime>\n' % (namespace_, self.gds_format_string(quote_xml(self.endDateTime), input_name='endDateTime'), namespace_))
    def hasContent_(self):
        if (
            self.beginDateTime is not None or
            self.endDateTime is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='timeParam'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.beginDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'beginDateTime=%s,\n' % quote_python(self.beginDateTime))
        if self.endDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'endDateTime=%s,\n' % quote_python(self.endDateTime))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'beginDateTime':
            beginDateTime_ = child_.text
            self.beginDateTime = beginDateTime_
        elif nodeName_ == 'endDateTime':
            endDateTime_ = child_.text
            self.endDateTime = endDateTime_
# end class timeParam


class variables(GeneratedsSuper):
    """variables is a list of variable elements (VariableInfoType)."""
    subclass = None
    superclass = None
    def __init__(self, variable=None):
        if variable is None:
            self.variable = []
        else:
            self.variable = variable
    def factory(*args_, **kwargs_):
        if variables.subclass:
            return variables.subclass(*args_, **kwargs_)
        else:
            return variables(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_variable(self): return self.variable
    def set_variable(self, variable): self.variable = variable
    def add_variable(self, value): self.variable.append(value)
    def insert_variable(self, index, value): self.variable[index] = value
    def export(self, outfile, level, namespace_='', name_='variables', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='variables')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='variables'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='variables'):
        for variable_ in self.variable:
            variable_.export(outfile, level, namespace_, name_='variable')
    def hasContent_(self):
        if (
            self.variable
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='variables'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write(u'variable=[\n')
        level += 1
        for variable_ in self.variable:
            showIndent(outfile, level)
            outfile.write(u'model_.VariableInfoType(\n')
            variable_.exportLiteral(outfile, level, name_='VariableInfoType')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'variable': 
            obj_ = VariableInfoType.factory()
            obj_.build(child_)
            self.variable.append(obj_)
# end class variables


class timeZoneInfo(GeneratedsSuper):
    """The default time zone for this site (+00:00) and if this site shifts
    to daylight savings time (attribute: usesDaylightSavingsTime)If
    the location shifts it's data sources to Daylight Savings Time,
    this flag should be true."""
    subclass = None
    superclass = None
    def __init__(self, siteUsesDaylightSavingsTime=False, defaultTimeZone=None, daylightSavingsTimeZone=None):
        self.siteUsesDaylightSavingsTime = _cast(bool, siteUsesDaylightSavingsTime)
        self.defaultTimeZone = defaultTimeZone
        self.daylightSavingsTimeZone = daylightSavingsTimeZone
    def factory(*args_, **kwargs_):
        if timeZoneInfo.subclass:
            return timeZoneInfo.subclass(*args_, **kwargs_)
        else:
            return timeZoneInfo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_defaultTimeZone(self): return self.defaultTimeZone
    def set_defaultTimeZone(self, defaultTimeZone): self.defaultTimeZone = defaultTimeZone
    def get_daylightSavingsTimeZone(self): return self.daylightSavingsTimeZone
    def set_daylightSavingsTimeZone(self, daylightSavingsTimeZone): self.daylightSavingsTimeZone = daylightSavingsTimeZone
    def get_siteUsesDaylightSavingsTime(self): return self.siteUsesDaylightSavingsTime
    def set_siteUsesDaylightSavingsTime(self, siteUsesDaylightSavingsTime): self.siteUsesDaylightSavingsTime = siteUsesDaylightSavingsTime
    def export(self, outfile, level, namespace_='', name_='timeZoneInfo', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='timeZoneInfo')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='timeZoneInfo'):
        if self.siteUsesDaylightSavingsTime is not None and 'siteUsesDaylightSavingsTime' not in already_processed:
            already_processed.append('siteUsesDaylightSavingsTime')
            outfile.write(u' siteUsesDaylightSavingsTime="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.siteUsesDaylightSavingsTime)), input_name='siteUsesDaylightSavingsTime'))
    def exportChildren(self, outfile, level, namespace_='', name_='timeZoneInfo'):
        if self.defaultTimeZone is not None:
            self.defaultTimeZone.export(outfile, level, namespace_, 'defaultTimeZone')
        if self.daylightSavingsTimeZone is not None:
            self.daylightSavingsTimeZone.export(outfile, level, namespace_, 'daylightSavingsTimeZone')
    def hasContent_(self):
        if (
            self.defaultTimeZone is not None or
            self.daylightSavingsTimeZone is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='timeZoneInfo'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.siteUsesDaylightSavingsTime is not None and 'siteUsesDaylightSavingsTime' not in already_processed:
            already_processed.append('siteUsesDaylightSavingsTime')
            showIndent(outfile, level)
            outfile.write(u'siteUsesDaylightSavingsTime = %s,\n' % (self.siteUsesDaylightSavingsTime,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.defaultTimeZone is not None:
            showIndent(outfile, level)
            outfile.write(u'defaultTimeZone=%s,\n' % quote_python(self.defaultTimeZone))
        if self.daylightSavingsTimeZone is not None:
            showIndent(outfile, level)
            outfile.write(u'daylightSavingsTimeZone=%s,\n' % quote_python(self.daylightSavingsTimeZone))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('siteUsesDaylightSavingsTime')
        if value is not None and 'siteUsesDaylightSavingsTime' not in already_processed:
            already_processed.append('siteUsesDaylightSavingsTime')
            if value in ('true', '1'):
                self.siteUsesDaylightSavingsTime = True
            elif value in ('false', '0'):
                self.siteUsesDaylightSavingsTime = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'defaultTimeZone': 
            obj_ = xsi_string.factory()
            obj_.build(child_)
            self.set_defaultTimeZone(obj_)
        elif nodeName_ == 'daylightSavingsTimeZone': 
            obj_ = xsi_string.factory()
            obj_.build(child_)
            self.set_daylightSavingsTimeZone(obj_)
# end class timeZoneInfo


class defaultTimeZone(GeneratedsSuper):
    """The default time zone for a site, specified in hours and minutes: hh:mm"""
    subclass = None
    superclass = None
    def __init__(self, ZoneOffset=None, ZoneAbbreviation=None, valueOf_=None):
        self.ZoneOffset = _cast(None, ZoneOffset)
        self.ZoneAbbreviation = _cast(None, ZoneAbbreviation)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if defaultTimeZone.subclass:
            return defaultTimeZone.subclass(*args_, **kwargs_)
        else:
            return defaultTimeZone(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ZoneOffset(self): return self.ZoneOffset
    def set_ZoneOffset(self, ZoneOffset): self.ZoneOffset = ZoneOffset
    def get_ZoneAbbreviation(self): return self.ZoneAbbreviation
    def set_ZoneAbbreviation(self, ZoneAbbreviation): self.ZoneAbbreviation = ZoneAbbreviation
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='defaultTimeZone', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='defaultTimeZone')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='defaultTimeZone'):
        outfile.write(u' ZoneOffset=%s' % (self.gds_format_string(quote_attrib(self.ZoneOffset), input_name='ZoneOffset'), ))
        if self.ZoneAbbreviation is not None and 'ZoneAbbreviation' not in already_processed:
            already_processed.append('ZoneAbbreviation')
            outfile.write(u' ZoneAbbreviation=%s' % (self.gds_format_string(quote_attrib(self.ZoneAbbreviation), input_name='ZoneAbbreviation'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='defaultTimeZone'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='defaultTimeZone'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.ZoneOffset is not None and 'ZoneOffset' not in already_processed:
            already_processed.append('ZoneOffset')
            showIndent(outfile, level)
            outfile.write(u'ZoneOffset = "%s",\n' % (self.ZoneOffset,))
        if self.ZoneAbbreviation is not None and 'ZoneAbbreviation' not in already_processed:
            already_processed.append('ZoneAbbreviation')
            showIndent(outfile, level)
            outfile.write(u'ZoneAbbreviation = "%s",\n' % (self.ZoneAbbreviation,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('ZoneOffset')
        if value is not None and 'ZoneOffset' not in already_processed:
            already_processed.append('ZoneOffset')
            self.ZoneOffset = value
        value = attrs.get('ZoneAbbreviation')
        if value is not None and 'ZoneAbbreviation' not in already_processed:
            already_processed.append('ZoneAbbreviation')
            self.ZoneAbbreviation = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class defaultTimeZone


class daylightSavingsTimeZone(GeneratedsSuper):
    """The daylight savings time zone for a site, specified in hours and
    minutes: hh:mm"""
    subclass = None
    superclass = None
    def __init__(self, ZoneOffset=None, ZoneAbbreviation=None, valueOf_=None):
        self.ZoneOffset = _cast(None, ZoneOffset)
        self.ZoneAbbreviation = _cast(None, ZoneAbbreviation)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if daylightSavingsTimeZone.subclass:
            return daylightSavingsTimeZone.subclass(*args_, **kwargs_)
        else:
            return daylightSavingsTimeZone(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ZoneOffset(self): return self.ZoneOffset
    def set_ZoneOffset(self, ZoneOffset): self.ZoneOffset = ZoneOffset
    def get_ZoneAbbreviation(self): return self.ZoneAbbreviation
    def set_ZoneAbbreviation(self, ZoneAbbreviation): self.ZoneAbbreviation = ZoneAbbreviation
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='daylightSavingsTimeZone', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='daylightSavingsTimeZone')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='daylightSavingsTimeZone'):
        outfile.write(u' ZoneOffset=%s' % (self.gds_format_string(quote_attrib(self.ZoneOffset), input_name='ZoneOffset'), ))
        if self.ZoneAbbreviation is not None and 'ZoneAbbreviation' not in already_processed:
            already_processed.append('ZoneAbbreviation')
            outfile.write(u' ZoneAbbreviation=%s' % (self.gds_format_string(quote_attrib(self.ZoneAbbreviation), input_name='ZoneAbbreviation'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='daylightSavingsTimeZone'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='daylightSavingsTimeZone'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.ZoneOffset is not None and 'ZoneOffset' not in already_processed:
            already_processed.append('ZoneOffset')
            showIndent(outfile, level)
            outfile.write(u'ZoneOffset = "%s",\n' % (self.ZoneOffset,))
        if self.ZoneAbbreviation is not None and 'ZoneAbbreviation' not in already_processed:
            already_processed.append('ZoneAbbreviation')
            showIndent(outfile, level)
            outfile.write(u'ZoneAbbreviation = "%s",\n' % (self.ZoneAbbreviation,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('ZoneOffset')
        if value is not None and 'ZoneOffset' not in already_processed:
            already_processed.append('ZoneOffset')
            self.ZoneOffset = value
        value = attrs.get('ZoneAbbreviation')
        if value is not None and 'ZoneAbbreviation' not in already_processed:
            already_processed.append('ZoneAbbreviation')
            self.ZoneAbbreviation = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class daylightSavingsTimeZone


class optionGroup(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, option=None):
        if option is None:
            self.option = []
        else:
            self.option = option
    def factory(*args_, **kwargs_):
        if optionGroup.subclass:
            return optionGroup.subclass(*args_, **kwargs_)
        else:
            return optionGroup(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_option(self): return self.option
    def set_option(self, option): self.option = option
    def add_option(self, value): self.option.append(value)
    def insert_option(self, index, value): self.option[index] = value
    def export(self, outfile, level, namespace_='', name_='optionGroup', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='optionGroup')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='optionGroup'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='optionGroup'):
        for option_ in self.option:
            option_.export(outfile, level, namespace_, name_='option')
    def hasContent_(self):
        if (
            self.option
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='optionGroup'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write(u'option=[\n')
        level += 1
        for option_ in self.option:
            showIndent(outfile, level)
            outfile.write(u'model_.option(\n')
            option_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'option': 
            obj_ = option.factory()
            obj_.build(child_)
            self.option.append(obj_)
# end class optionGroup


class DocumentationType(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, title=None, href=None, type_=None, show=None, valueOf_=None, mixedclass_=None, content_=None):
        self.title = _cast(None, title)
        self.href = _cast(None, href)
        self.type_ = _cast(None, type_)
        self.show = _cast(None, show)
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if DocumentationType.subclass:
            return DocumentationType.subclass(*args_, **kwargs_)
        else:
            return DocumentationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_title(self): return self.title
    def set_title(self, title): self.title = title
    def get_href(self): return self.href
    def set_href(self, href): self.href = href
    def get_type(self): return self.type_
    def set_type(self, type_): self.type_ = type_
    def validate_DocumentationEnumTypes(self, value):
        # Validate type DocumentationEnumTypes, a restriction on xsi:token.
        pass
    def get_show(self): return self.show
    def set_show(self, show): self.show = show
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='DocumentationType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='DocumentationType')
        outfile.write(u'>')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        outfile.write(u'</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='DocumentationType'):
        if self.title is not None and 'title' not in already_processed:
            already_processed.append('title')
            outfile.write(u' title=%s' % (self.gds_format_string(quote_attrib(self.title), input_name='title'), ))
        if self.href is not None and 'href' not in already_processed:
            already_processed.append('href')
            outfile.write(u' href=%s' % (self.gds_format_string(quote_attrib(self.href), input_name='href'), ))
        if self.type_ is not None and 'type_' not in already_processed:
            already_processed.append('type_')
            outfile.write(u' type=%s' % (quote_attrib(self.type_), ))
        if self.show is not None and 'show' not in already_processed:
            already_processed.append('show')
            outfile.write(u' show=%s' % (self.gds_format_string(quote_attrib(self.show), input_name='show'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='DocumentationType'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='DocumentationType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.title is not None and 'title' not in already_processed:
            already_processed.append('title')
            showIndent(outfile, level)
            outfile.write(u'title = "%s",\n' % (self.title,))
        if self.href is not None and 'href' not in already_processed:
            already_processed.append('href')
            showIndent(outfile, level)
            outfile.write(u'href = "%s",\n' % (self.href,))
        if self.type_ is not None and 'type_' not in already_processed:
            already_processed.append('type_')
            showIndent(outfile, level)
            outfile.write(u'type_ = "%s",\n' % (self.type_,))
        if self.show is not None and 'show' not in already_processed:
            already_processed.append('show')
            showIndent(outfile, level)
            outfile.write(u'show = "%s",\n' % (self.show,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('title')
        if value is not None and 'title' not in already_processed:
            already_processed.append('title')
            self.title = value
        value = attrs.get('href')
        if value is not None and 'href' not in already_processed:
            already_processed.append('href')
            self.href = value
        value = attrs.get('type')
        if value is not None and 'type' not in already_processed:
            already_processed.append('type')
            self.type_ = value
            self.type_ = ' '.join(self.type_.split())
        value = attrs.get('show')
        if value is not None and 'show' not in already_processed:
            already_processed.append('show')
            self.show = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if not from_subclass and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
        pass
# end class DocumentationType


class options(GeneratedsSuper):
    """A list of options. Option elements are key-value pair elements that
    control how a variable maght be utilized in a service. Examples:
    MODIS web service. Information is aggreated over land or ocean
    or both. The plotarea option can include: plotarea=land,
    plotarea=land, plotarea=landocean USGS uses a statistic code,
    0003, to repesent a value type of 'Average'. The USGS statistic
    codes also several options that do not fit the ODM data model."""
    subclass = None
    superclass = None
    def __init__(self, option=None):
        if option is None:
            self.option = []
        else:
            self.option = option
    def factory(*args_, **kwargs_):
        if options.subclass:
            return options.subclass(*args_, **kwargs_)
        else:
            return options(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_option(self): return self.option
    def set_option(self, option): self.option = option
    def add_option(self, value): self.option.append(value)
    def insert_option(self, index, value): self.option[index] = value
    def export(self, outfile, level, namespace_='', name_='options', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='options')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='options'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='options'):
        for option_ in self.option:
            option_.export(outfile, level, namespace_, name_='option')
    def hasContent_(self):
        if (
            self.option
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='options'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write(u'option=[\n')
        level += 1
        for option_ in self.option:
            showIndent(outfile, level)
            outfile.write(u'model_.option(\n')
            option_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'option': 
            obj_ = option.factory()
            obj_.build(child_)
            self.option.append(obj_)
# end class options


class SourceInfoType(GeneratedsSuper):
    """SourceInfoType is used to describe the data source in the
    timeSeriesResponse. SourceInfoType is the base type for data
    source information. At present, two types are derived from
    SourceInfoType: SiteInfoType, and DataSetInfoType. SiteInfoType
    describes tlocation for a timeseries where that time series is
    located at a site or a DataSetInfoType describes time series
    derived from a dataset, such as a netCDF file, or a gridded
    model."""
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if SourceInfoType.subclass:
            return SourceInfoType.subclass(*args_, **kwargs_)
        else:
            return SourceInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='SourceInfoType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='SourceInfoType')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='SourceInfoType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='SourceInfoType'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='SourceInfoType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class SourceInfoType


class DataSetInfoType(SourceInfoType):
    """DataSetInfoType describes time series derived from a dataset, such
    as a netCDF file, or a gridded model."""
    subclass = None
    superclass = SourceInfoType
    def __init__(self, dataSetIdentifier=None, timeZoneInfo=None, dataSetDescription=None, note=None, dataSetLocation=None, extension=None):
        super(DataSetInfoType, self).__init__()
        self.dataSetIdentifier = dataSetIdentifier
        self.timeZoneInfo = timeZoneInfo
        self.dataSetDescription = dataSetDescription
        if note is None:
            self.note = []
        else:
            self.note = note
        self.dataSetLocation = dataSetLocation
        self.extension = extension
    def factory(*args_, **kwargs_):
        if DataSetInfoType.subclass:
            return DataSetInfoType.subclass(*args_, **kwargs_)
        else:
            return DataSetInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_dataSetIdentifier(self): return self.dataSetIdentifier
    def set_dataSetIdentifier(self, dataSetIdentifier): self.dataSetIdentifier = dataSetIdentifier
    def get_timeZoneInfo(self): return self.timeZoneInfo
    def set_timeZoneInfo(self, timeZoneInfo): self.timeZoneInfo = timeZoneInfo
    def get_dataSetDescription(self): return self.dataSetDescription
    def set_dataSetDescription(self, dataSetDescription): self.dataSetDescription = dataSetDescription
    def get_note(self): return self.note
    def set_note(self, note): self.note = note
    def add_note(self, value): self.note.append(value)
    def insert_note(self, index, value): self.note[index] = value
    def get_dataSetLocation(self): return self.dataSetLocation
    def set_dataSetLocation(self, dataSetLocation): self.dataSetLocation = dataSetLocation
    def get_extension(self): return self.extension
    def set_extension(self, extension): self.extension = extension
    def export(self, outfile, level, namespace_='', name_='DataSetInfoType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='DataSetInfoType')
        outfile.write(u' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(u' xsi:type="DataSetInfoType"')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='DataSetInfoType'):
        super(DataSetInfoType, self).exportAttributes(outfile, level, already_processed, namespace_, name_='DataSetInfoType')
    def exportChildren(self, outfile, level, namespace_='', name_='DataSetInfoType'):
        super(DataSetInfoType, self).exportChildren(outfile, level, namespace_, name_)
        if self.dataSetIdentifier is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sdataSetIdentifier>%s</%sdataSetIdentifier>\n' % (namespace_, self.gds_format_string(quote_xml(self.dataSetIdentifier), input_name='dataSetIdentifier'), namespace_))
        if self.timeZoneInfo:
            self.timeZoneInfo.export(outfile, level, namespace_, name_='timeZoneInfo')
        if self.dataSetDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sdataSetDescription>%s</%sdataSetDescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.dataSetDescription), input_name='dataSetDescription'), namespace_))
        for note_ in self.note:
            note_.export(outfile, level, namespace_, name_='note')
        if self.dataSetLocation:
            self.dataSetLocation.export(outfile, level, namespace_, name_='dataSetLocation')
        if self.extension is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sextension>%s</%sextension>\n' % (namespace_, self.gds_format_string(quote_xml(self.extension), input_name='extension'), namespace_))
    def hasContent_(self):
        if (
            self.dataSetIdentifier is not None or
            self.timeZoneInfo is not None or
            self.dataSetDescription is not None or
            self.note or
            self.dataSetLocation is not None or
            self.extension is not None or
            super(DataSetInfoType, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='DataSetInfoType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        super(DataSetInfoType, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(DataSetInfoType, self).exportLiteralChildren(outfile, level, name_)
        if self.dataSetIdentifier is not None:
            showIndent(outfile, level)
            outfile.write(u'dataSetIdentifier=%s,\n' % quote_python(self.dataSetIdentifier))
        if self.timeZoneInfo is not None:
            showIndent(outfile, level)
            outfile.write(u'timeZoneInfo=model_.timeZoneInfo(\n')
            self.timeZoneInfo.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.dataSetDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'dataSetDescription=%s,\n' % quote_python(self.dataSetDescription))
        showIndent(outfile, level)
        outfile.write(u'note=[\n')
        level += 1
        for note_ in self.note:
            showIndent(outfile, level)
            outfile.write(u'model_.NoteType(\n')
            note_.exportLiteral(outfile, level, name_='NoteType')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        if self.dataSetLocation is not None:
            showIndent(outfile, level)
            outfile.write(u'dataSetLocation=model_.GeogLocationType(\n')
            self.dataSetLocation.exportLiteral(outfile, level, name_='dataSetLocation')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.extension is not None:
            showIndent(outfile, level)
            outfile.write(u'extension=%s,\n' % quote_python(self.extension))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        super(DataSetInfoType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'dataSetIdentifier':
            dataSetIdentifier_ = child_.text
            self.dataSetIdentifier = dataSetIdentifier_
        elif nodeName_ == 'timeZoneInfo': 
            obj_ = timeZoneInfo.factory()
            obj_.build(child_)
            self.set_timeZoneInfo(obj_)
        elif nodeName_ == 'dataSetDescription':
            dataSetDescription_ = child_.text
            self.dataSetDescription = dataSetDescription_
        elif nodeName_ == 'note': 
            obj_ = NoteType.factory()
            obj_.build(child_)
            self.note.append(obj_)
        elif nodeName_ == 'dataSetLocation': 
            obj_ = GeogLocationType.factory()
            obj_.build(child_)
            self.set_dataSetLocation(obj_)
        elif nodeName_ == 'extension':
            extension_ = child_.text
            self.extension = extension_
        super(DataSetInfoType, self).buildChildren(child_, nodeName_, True)
# end class DataSetInfoType


class TimePeriodType(GeneratedsSuper):
    """time series (site-variable-observation) can have three types of time
    periods: 1) definite start and end time, or TimeIntervalType, 2)
    single observation, or TimeSingleType 3) Real Time station with
    moving window of data available, or TimeRealTimeType In order to
    simplify client development, all types now include
    beginDateTime, and endDateTime. A fourth type should be added:
    4) continuing site, where start is known, and site is still
    collecting data. This could be a realTimeType, or rename the
    real time type to TimeDefinedPeriodType."""
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if TimePeriodType.subclass:
            return TimePeriodType.subclass(*args_, **kwargs_)
        else:
            return TimePeriodType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='TimePeriodType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='TimePeriodType')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='TimePeriodType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='TimePeriodType'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='TimePeriodType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class TimePeriodType


class TimeIntervalType(TimePeriodType):
    """For where a series has multiple observations, and a define
    beingDateTime as dateTime of the first data value in the series,
    and endDateTime dateTime of the last data value in the series."""
    subclass = None
    superclass = TimePeriodType
    def __init__(self, beginDateTime=None, endDateTime=None):
        super(TimeIntervalType, self).__init__()
        self.beginDateTime = beginDateTime
        self.endDateTime = endDateTime
    def factory(*args_, **kwargs_):
        if TimeIntervalType.subclass:
            return TimeIntervalType.subclass(*args_, **kwargs_)
        else:
            return TimeIntervalType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_beginDateTime(self): return self.beginDateTime
    def set_beginDateTime(self, beginDateTime): self.beginDateTime = beginDateTime
    def get_endDateTime(self): return self.endDateTime
    def set_endDateTime(self, endDateTime): self.endDateTime = endDateTime
    def export(self, outfile, level, namespace_='', name_='TimeIntervalType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='TimeIntervalType')
        outfile.write(u' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(u' xsi:type="TimeIntervalType"')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='TimeIntervalType'):
        super(TimeIntervalType, self).exportAttributes(outfile, level, already_processed, namespace_, name_='TimeIntervalType')
    def exportChildren(self, outfile, level, namespace_='', name_='TimeIntervalType'):
        super(TimeIntervalType, self).exportChildren(outfile, level, namespace_, name_)
        if self.beginDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sbeginDateTime>%s</%sbeginDateTime>\n' % (namespace_, self.gds_format_string(quote_xml(self.beginDateTime), input_name='beginDateTime'), namespace_))
        if self.endDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sendDateTime>%s</%sendDateTime>\n' % (namespace_, self.gds_format_string(quote_xml(self.endDateTime), input_name='endDateTime'), namespace_))
    def hasContent_(self):
        if (
            self.beginDateTime is not None or
            self.endDateTime is not None or
            super(TimeIntervalType, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='TimeIntervalType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        super(TimeIntervalType, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(TimeIntervalType, self).exportLiteralChildren(outfile, level, name_)
        if self.beginDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'beginDateTime=%s,\n' % quote_python(self.beginDateTime))
        if self.endDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'endDateTime=%s,\n' % quote_python(self.endDateTime))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        super(TimeIntervalType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'beginDateTime':
            beginDateTime_ = child_.text
            self.beginDateTime = beginDateTime_
        elif nodeName_ == 'endDateTime':
            endDateTime_ = child_.text
            self.endDateTime = endDateTime_
        super(TimeIntervalType, self).buildChildren(child_, nodeName_, True)
# end class TimeIntervalType


class TimeSingleType(TimePeriodType):
    """For where a series is a single observation. timeSingle,
    beginDateTime, and endDateTime will have the same value. The
    beginDateTime and endDateTime are provided to simplify usage by
    clients.They should be be calculated based on the duration
    stored in realTimeDataPeriod"""
    subclass = None
    superclass = TimePeriodType
    def __init__(self, timeSingle=None, beginDateTime=None, endDateTime=None):
        super(TimeSingleType, self).__init__()
        self.timeSingle = timeSingle
        self.beginDateTime = beginDateTime
        self.endDateTime = endDateTime
    def factory(*args_, **kwargs_):
        if TimeSingleType.subclass:
            return TimeSingleType.subclass(*args_, **kwargs_)
        else:
            return TimeSingleType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_timeSingle(self): return self.timeSingle
    def set_timeSingle(self, timeSingle): self.timeSingle = timeSingle
    def get_beginDateTime(self): return self.beginDateTime
    def set_beginDateTime(self, beginDateTime): self.beginDateTime = beginDateTime
    def get_endDateTime(self): return self.endDateTime
    def set_endDateTime(self, endDateTime): self.endDateTime = endDateTime
    def export(self, outfile, level, namespace_='', name_='TimeSingleType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='TimeSingleType')
        outfile.write(u' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(u' xsi:type="TimeSingleType"')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='TimeSingleType'):
        super(TimeSingleType, self).exportAttributes(outfile, level, already_processed, namespace_, name_='TimeSingleType')
    def exportChildren(self, outfile, level, namespace_='', name_='TimeSingleType'):
        super(TimeSingleType, self).exportChildren(outfile, level, namespace_, name_)
        if self.timeSingle is not None:
            showIndent(outfile, level)
            outfile.write(u'<%stimeSingle>%s</%stimeSingle>\n' % (namespace_, self.gds_format_string(quote_xml(self.timeSingle), input_name='timeSingle'), namespace_))
        if self.beginDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sbeginDateTime>%s</%sbeginDateTime>\n' % (namespace_, self.gds_format_string(quote_xml(self.beginDateTime), input_name='beginDateTime'), namespace_))
        if self.endDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sendDateTime>%s</%sendDateTime>\n' % (namespace_, self.gds_format_string(quote_xml(self.endDateTime), input_name='endDateTime'), namespace_))
    def hasContent_(self):
        if (
            self.timeSingle is not None or
            self.beginDateTime is not None or
            self.endDateTime is not None or
            super(TimeSingleType, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='TimeSingleType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        super(TimeSingleType, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(TimeSingleType, self).exportLiteralChildren(outfile, level, name_)
        if self.timeSingle is not None:
            showIndent(outfile, level)
            outfile.write(u'timeSingle=%s,\n' % quote_python(self.timeSingle))
        if self.beginDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'beginDateTime=%s,\n' % quote_python(self.beginDateTime))
        if self.endDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'endDateTime=%s,\n' % quote_python(self.endDateTime))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        super(TimeSingleType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'timeSingle':
            timeSingle_ = child_.text
            self.timeSingle = timeSingle_
        elif nodeName_ == 'beginDateTime':
            beginDateTime_ = child_.text
            self.beginDateTime = beginDateTime_
        elif nodeName_ == 'endDateTime':
            endDateTime_ = child_.text
            self.endDateTime = endDateTime_
        super(TimeSingleType, self).buildChildren(child_, nodeName_, True)
# end class TimeSingleType


class TimePeriodRealTimeType(TimePeriodType):
    """Use where a site has an evolving period where data is available. The
    US Geological Survey real time data is available for 30 days,
    the realTimeDataPeriod element is an XML duration and woudl be
    "30d" The beginDateTime and endDateTime are provided to simplify
    usage by clients.They should be be calculated based on the
    duration stored in realTimeDataPeriod"""
    subclass = None
    superclass = TimePeriodType
    def __init__(self, realTimeDataPeriod=None, beginDateTime=None, endDateTime=None):
        super(TimePeriodRealTimeType, self).__init__()
        self.realTimeDataPeriod = realTimeDataPeriod
        self.beginDateTime = beginDateTime
        self.endDateTime = endDateTime
    def factory(*args_, **kwargs_):
        if TimePeriodRealTimeType.subclass:
            return TimePeriodRealTimeType.subclass(*args_, **kwargs_)
        else:
            return TimePeriodRealTimeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_realTimeDataPeriod(self): return self.realTimeDataPeriod
    def set_realTimeDataPeriod(self, realTimeDataPeriod): self.realTimeDataPeriod = realTimeDataPeriod
    def get_beginDateTime(self): return self.beginDateTime
    def set_beginDateTime(self, beginDateTime): self.beginDateTime = beginDateTime
    def get_endDateTime(self): return self.endDateTime
    def set_endDateTime(self, endDateTime): self.endDateTime = endDateTime
    def export(self, outfile, level, namespace_='', name_='TimePeriodRealTimeType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='TimePeriodRealTimeType')
        outfile.write(u' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(u' xsi:type="TimePeriodRealTimeType"')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='TimePeriodRealTimeType'):
        super(TimePeriodRealTimeType, self).exportAttributes(outfile, level, already_processed, namespace_, name_='TimePeriodRealTimeType')
    def exportChildren(self, outfile, level, namespace_='', name_='TimePeriodRealTimeType'):
        super(TimePeriodRealTimeType, self).exportChildren(outfile, level, namespace_, name_)
        if self.realTimeDataPeriod is not None:
            showIndent(outfile, level)
            outfile.write(u'<%srealTimeDataPeriod>%s</%srealTimeDataPeriod>\n' % (namespace_, self.gds_format_string(quote_xml(self.realTimeDataPeriod), input_name='realTimeDataPeriod'), namespace_))
        if self.beginDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sbeginDateTime>%s</%sbeginDateTime>\n' % (namespace_, self.gds_format_string(quote_xml(self.beginDateTime), input_name='beginDateTime'), namespace_))
        if self.endDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sendDateTime>%s</%sendDateTime>\n' % (namespace_, self.gds_format_string(quote_xml(self.endDateTime), input_name='endDateTime'), namespace_))
    def hasContent_(self):
        if (
            self.realTimeDataPeriod is not None or
            self.beginDateTime is not None or
            self.endDateTime is not None or
            super(TimePeriodRealTimeType, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='TimePeriodRealTimeType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        super(TimePeriodRealTimeType, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(TimePeriodRealTimeType, self).exportLiteralChildren(outfile, level, name_)
        if self.realTimeDataPeriod is not None:
            showIndent(outfile, level)
            outfile.write(u'realTimeDataPeriod=%s,\n' % quote_python(self.realTimeDataPeriod))
        if self.beginDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'beginDateTime=%s,\n' % quote_python(self.beginDateTime))
        if self.endDateTime is not None:
            showIndent(outfile, level)
            outfile.write(u'endDateTime=%s,\n' % quote_python(self.endDateTime))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        super(TimePeriodRealTimeType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'realTimeDataPeriod':
            realTimeDataPeriod_ = child_.text
            self.realTimeDataPeriod = realTimeDataPeriod_
        elif nodeName_ == 'beginDateTime':
            beginDateTime_ = child_.text
            self.beginDateTime = beginDateTime_
        elif nodeName_ == 'endDateTime':
            endDateTime_ = child_.text
            self.endDateTime = endDateTime_
        super(TimePeriodRealTimeType, self).buildChildren(child_, nodeName_, True)
# end class TimePeriodRealTimeType


class GeogLocationType(GeneratedsSuper):
    """GeogLocationType is the base class for the two geometry types:
    LatLonPointType, and LatLonBoxType. Any additional types should
    derive from this type. The default spatial reference system is
    @srs is EPSG:4326 or Geographic lat long."""
    subclass = None
    superclass = None
    def __init__(self, srs='EPSG:4326', valueOf_=None):
        self.srs = _cast(None, srs)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if GeogLocationType.subclass:
            return GeogLocationType.subclass(*args_, **kwargs_)
        else:
            return GeogLocationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_srs(self): return self.srs
    def set_srs(self, srs): self.srs = srs
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='GeogLocationType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='GeogLocationType')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='GeogLocationType'):
        if self.srs is not None and 'srs' not in already_processed:
            already_processed.append('srs')
            outfile.write(u' srs=%s' % (self.gds_format_string(quote_attrib(self.srs), input_name='srs'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='GeogLocationType'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='GeogLocationType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.srs is not None and 'srs' not in already_processed:
            already_processed.append('srs')
            showIndent(outfile, level)
            outfile.write(u'srs = "%s",\n' % (self.srs,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('srs')
        if value is not None and 'srs' not in already_processed:
            already_processed.append('srs')
            self.srs = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class GeogLocationType


class LatLonPointType(GeogLocationType):
    subclass = None
    superclass = GeogLocationType
    def __init__(self, srs='EPSG:4326', latitude=None, longitude=None):
        super(LatLonPointType, self).__init__(srs, )
        self.latitude = latitude
        self.longitude = longitude
    def factory(*args_, **kwargs_):
        if LatLonPointType.subclass:
            return LatLonPointType.subclass(*args_, **kwargs_)
        else:
            return LatLonPointType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_latitude(self): return self.latitude
    def set_latitude(self, latitude): self.latitude = latitude
    def validate_latitude(self, value):
        # validate type latitude
        pass
    def get_longitude(self): return self.longitude
    def set_longitude(self, longitude): self.longitude = longitude
    def validate_longitude(self, value):
        # validate type longitude
        pass
    def export(self, outfile, level, namespace_='', name_='LatLonPointType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='LatLonPointType')
        outfile.write(u' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(u' xsi:type="LatLonPointType"')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='LatLonPointType'):
        super(LatLonPointType, self).exportAttributes(outfile, level, already_processed, namespace_, name_='LatLonPointType')
    def exportChildren(self, outfile, level, namespace_='', name_='LatLonPointType'):
        super(LatLonPointType, self).exportChildren(outfile, level, namespace_, name_)
        if self.latitude is not None:
            showIndent(outfile, level)
            outfile.write(u'<%slatitude>%s</%slatitude>\n' % (namespace_, self.gds_format_double(self.latitude, input_name='latitude'), namespace_))
        if self.longitude is not None:
            showIndent(outfile, level)
            outfile.write(u'<%slongitude>%s</%slongitude>\n' % (namespace_, self.gds_format_double(self.longitude, input_name='longitude'), namespace_))
    def hasContent_(self):
        if (
            self.latitude is not None or
            self.longitude is not None or
            super(LatLonPointType, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='LatLonPointType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        super(LatLonPointType, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(LatLonPointType, self).exportLiteralChildren(outfile, level, name_)
        if self.latitude is not None:
            showIndent(outfile, level)
            outfile.write(u'latitude=%e,\n' % self.latitude)
        if self.longitude is not None:
            showIndent(outfile, level)
            outfile.write(u'longitude=%e,\n' % self.longitude)
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        super(LatLonPointType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'latitude':
            sval_ = child_.text
            try:
                fval_ = float(sval_)
            except (TypeError, ValueError), exp:
                raise_parse_error(child_, 'requires float or double: %s' % exp)
            self.latitude = fval_
            self.validate_latitude(self.latitude)    # validate type latitude
        elif nodeName_ == 'longitude':
            sval_ = child_.text
            try:
                fval_ = float(sval_)
            except (TypeError, ValueError), exp:
                raise_parse_error(child_, 'requires float or double: %s' % exp)
            self.longitude = fval_
            self.validate_longitude(self.longitude)    # validate type longitude
        super(LatLonPointType, self).buildChildren(child_, nodeName_, True)
# end class LatLonPointType


class LatLonBoxType(GeogLocationType):
    subclass = None
    superclass = GeogLocationType
    def __init__(self, srs='EPSG:4326', south=None, west=None, north=None, east=None):
        super(LatLonBoxType, self).__init__(srs, )
        self.south = south
        self.west = west
        self.north = north
        self.east = east
    def factory(*args_, **kwargs_):
        if LatLonBoxType.subclass:
            return LatLonBoxType.subclass(*args_, **kwargs_)
        else:
            return LatLonBoxType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_south(self): return self.south
    def set_south(self, south): self.south = south
    def validate_south(self, value):
        # validate type south
        pass
    def get_west(self): return self.west
    def set_west(self, west): self.west = west
    def validate_west(self, value):
        # validate type west
        pass
    def get_north(self): return self.north
    def set_north(self, north): self.north = north
    def validate_north(self, value):
        # validate type north
        pass
    def get_east(self): return self.east
    def set_east(self, east): self.east = east
    def validate_east(self, value):
        # validate type east
        pass
    def export(self, outfile, level, namespace_='', name_='LatLonBoxType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='LatLonBoxType')
        outfile.write(u' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(u' xsi:type="LatLonBoxType"')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='LatLonBoxType'):
        super(LatLonBoxType, self).exportAttributes(outfile, level, already_processed, namespace_, name_='LatLonBoxType')
    def exportChildren(self, outfile, level, namespace_='', name_='LatLonBoxType'):
        super(LatLonBoxType, self).exportChildren(outfile, level, namespace_, name_)
        if self.south is not None:
            showIndent(outfile, level)
            outfile.write(u'<%ssouth>%s</%ssouth>\n' % (namespace_, self.gds_format_double(self.south, input_name='south'), namespace_))
        if self.west is not None:
            showIndent(outfile, level)
            outfile.write(u'<%swest>%s</%swest>\n' % (namespace_, self.gds_format_double(self.west, input_name='west'), namespace_))
        if self.north is not None:
            showIndent(outfile, level)
            outfile.write(u'<%snorth>%s</%snorth>\n' % (namespace_, self.gds_format_double(self.north, input_name='north'), namespace_))
        if self.east is not None:
            showIndent(outfile, level)
            outfile.write(u'<%seast>%s</%seast>\n' % (namespace_, self.gds_format_double(self.east, input_name='east'), namespace_))
    def hasContent_(self):
        if (
            self.south is not None or
            self.west is not None or
            self.north is not None or
            self.east is not None or
            super(LatLonBoxType, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='LatLonBoxType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        super(LatLonBoxType, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(LatLonBoxType, self).exportLiteralChildren(outfile, level, name_)
        if self.south is not None:
            showIndent(outfile, level)
            outfile.write(u'south=%e,\n' % self.south)
        if self.west is not None:
            showIndent(outfile, level)
            outfile.write(u'west=%e,\n' % self.west)
        if self.north is not None:
            showIndent(outfile, level)
            outfile.write(u'north=%e,\n' % self.north)
        if self.east is not None:
            showIndent(outfile, level)
            outfile.write(u'east=%e,\n' % self.east)
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        super(LatLonBoxType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'south':
            sval_ = child_.text
            try:
                fval_ = float(sval_)
            except (TypeError, ValueError), exp:
                raise_parse_error(child_, 'requires float or double: %s' % exp)
            self.south = fval_
            self.validate_south(self.south)    # validate type south
        elif nodeName_ == 'west':
            sval_ = child_.text
            try:
                fval_ = float(sval_)
            except (TypeError, ValueError), exp:
                raise_parse_error(child_, 'requires float or double: %s' % exp)
            self.west = fval_
            self.validate_west(self.west)    # validate type west
        elif nodeName_ == 'north':
            sval_ = child_.text
            try:
                fval_ = float(sval_)
            except (TypeError, ValueError), exp:
                raise_parse_error(child_, 'requires float or double: %s' % exp)
            self.north = fval_
            self.validate_north(self.north)    # validate type north
        elif nodeName_ == 'east':
            sval_ = child_.text
            try:
                fval_ = float(sval_)
            except (TypeError, ValueError), exp:
                raise_parse_error(child_, 'requires float or double: %s' % exp)
            self.east = fval_
            self.validate_east(self.east)    # validate type east
        super(LatLonBoxType, self).buildChildren(child_, nodeName_, True)
# end class LatLonBoxType


class seriesCatalogType(GeneratedsSuper):
    """Series catalog represents a list of series, where each separate data
    series are for the purposes of identifying or displaying what
    data are available at each site. For clients, this is the list
    of the html select group element. This would allow for groups or
    seriesCatalogs to appear in an HTML select menu.(depreciated)
    location of the WaterOneFlow service that the client should
    execute GetValues call on. All services now proxy getValues
    methods from other sources."""
    subclass = None
    superclass = None
    def __init__(self, menuGroupName=None, serviceWsdl=None, note=None, series=None):
        self.menuGroupName = _cast(None, menuGroupName)
        self.serviceWsdl = _cast(None, serviceWsdl)
        if note is None:
            self.note = []
        else:
            self.note = note
        if series is None:
            self.series = []
        else:
            self.series = series
    def factory(*args_, **kwargs_):
        if seriesCatalogType.subclass:
            return seriesCatalogType.subclass(*args_, **kwargs_)
        else:
            return seriesCatalogType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_note(self): return self.note
    def set_note(self, note): self.note = note
    def add_note(self, value): self.note.append(value)
    def insert_note(self, index, value): self.note[index] = value
    def get_series(self): return self.series
    def set_series(self, series): self.series = series
    def add_series(self, value): self.series.append(value)
    def insert_series(self, index, value): self.series[index] = value
    def get_menuGroupName(self): return self.menuGroupName
    def set_menuGroupName(self, menuGroupName): self.menuGroupName = menuGroupName
    def get_serviceWsdl(self): return self.serviceWsdl
    def set_serviceWsdl(self, serviceWsdl): self.serviceWsdl = serviceWsdl
    def export(self, outfile, level, namespace_='', name_='seriesCatalogType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='seriesCatalogType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='seriesCatalogType'):
        if self.menuGroupName is not None and 'menuGroupName' not in already_processed:
            already_processed.append('menuGroupName')
            outfile.write(u' menuGroupName=%s' % (self.gds_format_string(quote_attrib(self.menuGroupName), input_name='menuGroupName'), ))
        if self.serviceWsdl is not None and 'serviceWsdl' not in already_processed:
            already_processed.append('serviceWsdl')
            outfile.write(u' serviceWsdl=%s' % (self.gds_format_string(quote_attrib(self.serviceWsdl), input_name='serviceWsdl'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='seriesCatalogType'):
        for note_ in self.note:
            note_.export(outfile, level, namespace_, name_='note')
        for series_ in self.series:
            series_.export(outfile, level, namespace_, name_='series')
    def hasContent_(self):
        if (
            self.note or
            self.series
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='seriesCatalogType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.menuGroupName is not None and 'menuGroupName' not in already_processed:
            already_processed.append('menuGroupName')
            showIndent(outfile, level)
            outfile.write(u'menuGroupName = "%s",\n' % (self.menuGroupName,))
        if self.serviceWsdl is not None and 'serviceWsdl' not in already_processed:
            already_processed.append('serviceWsdl')
            showIndent(outfile, level)
            outfile.write(u'serviceWsdl = "%s",\n' % (self.serviceWsdl,))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write(u'note=[\n')
        level += 1
        for note_ in self.note:
            showIndent(outfile, level)
            outfile.write(u'model_.NoteType(\n')
            note_.exportLiteral(outfile, level, name_='NoteType')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        showIndent(outfile, level)
        outfile.write(u'series=[\n')
        level += 1
        for series_ in self.series:
            showIndent(outfile, level)
            outfile.write(u'model_.series(\n')
            series_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('menuGroupName')
        if value is not None and 'menuGroupName' not in already_processed:
            already_processed.append('menuGroupName')
            self.menuGroupName = value
        value = attrs.get('serviceWsdl')
        if value is not None and 'serviceWsdl' not in already_processed:
            already_processed.append('serviceWsdl')
            self.serviceWsdl = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'note': 
            obj_ = NoteType.factory()
            obj_.build(child_)
            self.note.append(obj_)
        elif nodeName_ == 'series': 
            obj_ = series.factory()
            obj_.build(child_)
            self.series.append(obj_)
# end class seriesCatalogType


class series(GeneratedsSuper):
    """Separate data series are for the purposes of identifying or
    displaying what data are available at each site. Site
    information is a parent of the series so that it does not need
    to be repeated (difference from the ODM. ). A Site contains one
    or more seriesCatalogs which contain one or more series.
    Assotiated with site, a series is a unique combination of the
    textual repesentation of ODM series:
    Variable,Method,Source,QualityControlLevel. An ODM series is a
    unique site/variable combinations are defined by unique
    combinations of SiteID, VariableID, MethodID, SourceID, and
    QualityControlLevelID."""
    subclass = None
    superclass = None
    def __init__(self, dataType=None, variable=None, valueCount=None, variableTimeInterval=None, valueType=None, generalCategory=None, sampleMedium=None, Method=None, Source=None, QualityControlLevel=None):
        self.dataType = dataType
        self.variable = variable
        self.valueCount = valueCount
        self.variableTimeInterval = variableTimeInterval
        self.valueType = valueType
        self.generalCategory = generalCategory
        self.sampleMedium = sampleMedium
        self.Method = Method
        self.Source = Source
        self.QualityControlLevel = QualityControlLevel
    def factory(*args_, **kwargs_):
        if series.subclass:
            return series.subclass(*args_, **kwargs_)
        else:
            return series(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_dataType(self): return self.dataType
    def set_dataType(self, dataType): self.dataType = dataType
    def validate_dataType(self, value):
        # validate type dataType
        pass
    def get_variable(self): return self.variable
    def set_variable(self, variable): self.variable = variable
    def get_valueCount(self): return self.valueCount
    def set_valueCount(self, valueCount): self.valueCount = valueCount
    def get_variableTimeInterval(self): return self.variableTimeInterval
    def set_variableTimeInterval(self, variableTimeInterval): self.variableTimeInterval = variableTimeInterval
    def get_valueType(self): return self.valueType
    def set_valueType(self, valueType): self.valueType = valueType
    def validate_valueType(self, value):
        # validate type valueType
        pass
    def get_generalCategory(self): return self.generalCategory
    def set_generalCategory(self, generalCategory): self.generalCategory = generalCategory
    def validate_generalCategory(self, value):
        # validate type generalCategory
        pass
    def get_sampleMedium(self): return self.sampleMedium
    def set_sampleMedium(self, sampleMedium): self.sampleMedium = sampleMedium
    def validate_sampleMedium(self, value):
        # validate type sampleMedium
        pass
    def get_Method(self): return self.Method
    def set_Method(self, Method): self.Method = Method
    def get_Source(self): return self.Source
    def set_Source(self, Source): self.Source = Source
    def get_QualityControlLevel(self): return self.QualityControlLevel
    def set_QualityControlLevel(self, QualityControlLevel): self.QualityControlLevel = QualityControlLevel
    def export(self, outfile, level, namespace_='', name_='series', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='series')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='series'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='series'):
        if self.dataType is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sdataType>%s</%sdataType>\n' % (namespace_, self.gds_format_string(quote_xml(self.dataType), input_name='dataType'), namespace_))
        if self.variable:
            self.variable.export(outfile, level, namespace_, name_='variable', )
        if self.valueCount:
            self.valueCount.export(outfile, level, namespace_, name_='valueCount', )
        if self.variableTimeInterval:
            self.variableTimeInterval.export(outfile, level, namespace_, name_='variableTimeInterval', )
        if self.valueType is not None:
            showIndent(outfile, level)
            outfile.write(u'<%svalueType>%s</%svalueType>\n' % (namespace_, self.gds_format_string(quote_xml(self.valueType), input_name='valueType'), namespace_))
        if self.generalCategory is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sgeneralCategory>%s</%sgeneralCategory>\n' % (namespace_, self.gds_format_string(quote_xml(self.generalCategory), input_name='generalCategory'), namespace_))
        if self.sampleMedium is not None:
            showIndent(outfile, level)
            outfile.write(u'<%ssampleMedium>%s</%ssampleMedium>\n' % (namespace_, self.gds_format_string(quote_xml(self.sampleMedium), input_name='sampleMedium'), namespace_))
        if self.Method:
            self.Method.export(outfile, level, namespace_, name_='Method')
        if self.Source:
            self.Source.export(outfile, level, namespace_, name_='Source')
        if self.QualityControlLevel:
            self.QualityControlLevel.export(outfile, level, namespace_, name_='QualityControlLevel')
    def hasContent_(self):
        if (
            self.dataType is not None or
            self.variable is not None or
            self.valueCount is not None or
            self.variableTimeInterval is not None or
            self.valueType is not None or
            self.generalCategory is not None or
            self.sampleMedium is not None or
            self.Method is not None or
            self.Source is not None or
            self.QualityControlLevel is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='series'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.dataType is not None:
            showIndent(outfile, level)
            outfile.write(u'dataType=%s,\n' % quote_python(self.dataType))
        if self.variable is not None:
            showIndent(outfile, level)
            outfile.write(u'variable=model_.VariableInfoType(\n')
            self.variable.exportLiteral(outfile, level, name_='variable')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.valueCount is not None:
            showIndent(outfile, level)
            outfile.write(u'valueCount=model_.valueCount(\n')
            self.valueCount.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.variableTimeInterval is not None:
            showIndent(outfile, level)
            outfile.write(u'variableTimeInterval=model_.TimePeriodType(\n')
            self.variableTimeInterval.exportLiteral(outfile, level, name_='variableTimeInterval')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.valueType is not None:
            showIndent(outfile, level)
            outfile.write(u'valueType=%s,\n' % quote_python(self.valueType))
        if self.generalCategory is not None:
            showIndent(outfile, level)
            outfile.write(u'generalCategory=%s,\n' % quote_python(self.generalCategory))
        if self.sampleMedium is not None:
            showIndent(outfile, level)
            outfile.write(u'sampleMedium=%s,\n' % quote_python(self.sampleMedium))
        if self.Method is not None:
            showIndent(outfile, level)
            outfile.write(u'Method=model_.MethodType(\n')
            self.Method.exportLiteral(outfile, level, name_='Method')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.Source is not None:
            showIndent(outfile, level)
            outfile.write(u'Source=model_.SourceType(\n')
            self.Source.exportLiteral(outfile, level, name_='Source')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.QualityControlLevel is not None:
            showIndent(outfile, level)
            outfile.write(u'QualityControlLevel=model_.QualityControlLevelType(\n')
            self.QualityControlLevel.exportLiteral(outfile, level, name_='QualityControlLevel')
            showIndent(outfile, level)
            outfile.write(u'),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'dataType':
            dataType_ = child_.text
            self.dataType = dataType_
            self.validate_dataType(self.dataType)    # validate type dataType
        elif nodeName_ == 'variable': 
            obj_ = VariableInfoType.factory()
            obj_.build(child_)
            self.set_variable(obj_)
        elif nodeName_ == 'valueCount': 
            obj_ = valueCount.factory()
            obj_.build(child_)
            self.set_valueCount(obj_)
        elif nodeName_ == 'variableTimeInterval': 
            obj_ = TimePeriodType.factory()
            obj_.build(child_)
            self.set_variableTimeInterval(obj_)
        elif nodeName_ == 'valueType':
            valueType_ = child_.text
            self.valueType = valueType_
            self.validate_valueType(self.valueType)    # validate type valueType
        elif nodeName_ == 'generalCategory':
            generalCategory_ = child_.text
            self.generalCategory = generalCategory_
            self.validate_generalCategory(self.generalCategory)    # validate type generalCategory
        elif nodeName_ == 'sampleMedium':
            sampleMedium_ = child_.text
            self.sampleMedium = sampleMedium_
            self.validate_sampleMedium(self.sampleMedium)    # validate type sampleMedium
        elif nodeName_ == 'Method': 
            obj_ = MethodType.factory()
            obj_.build(child_)
            self.set_Method(obj_)
        elif nodeName_ == 'Source': 
            obj_ = SourceType.factory()
            obj_.build(child_)
            self.set_Source(obj_)
        elif nodeName_ == 'QualityControlLevel': 
            obj_ = QualityControlLevelType.factory()
            obj_.build(child_)
            self.set_QualityControlLevel(obj_)
# end class series


class valueCount(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, countIsEstimated=None, valueOf_=None):
        self.countIsEstimated = _cast(bool, countIsEstimated)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if valueCount.subclass:
            return valueCount.subclass(*args_, **kwargs_)
        else:
            return valueCount(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_countIsEstimated(self): return self.countIsEstimated
    def set_countIsEstimated(self, countIsEstimated): self.countIsEstimated = countIsEstimated
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='valueCount', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='valueCount')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='valueCount'):
        if self.countIsEstimated is not None and 'countIsEstimated' not in already_processed:
            already_processed.append('countIsEstimated')
            outfile.write(u' countIsEstimated="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.countIsEstimated)), input_name='countIsEstimated'))
    def exportChildren(self, outfile, level, namespace_='', name_='valueCount'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='valueCount'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.countIsEstimated is not None and 'countIsEstimated' not in already_processed:
            already_processed.append('countIsEstimated')
            showIndent(outfile, level)
            outfile.write(u'countIsEstimated = %s,\n' % (self.countIsEstimated,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('countIsEstimated')
        if value is not None and 'countIsEstimated' not in already_processed:
            already_processed.append('countIsEstimated')
            if value in ('true', '1'):
                self.countIsEstimated = True
            elif value in ('false', '0'):
                self.countIsEstimated = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class valueCount


class QualifiersType(GeneratedsSuper):
    """qualifying comments that accompany the data"""
    subclass = None
    superclass = None
    def __init__(self, qualifier=None):
        self.qualifier = qualifier
    def factory(*args_, **kwargs_):
        if QualifiersType.subclass:
            return QualifiersType.subclass(*args_, **kwargs_)
        else:
            return QualifiersType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_qualifier(self): return self.qualifier
    def set_qualifier(self, qualifier): self.qualifier = qualifier
    def export(self, outfile, level, namespace_='', name_='QualifiersType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='QualifiersType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='QualifiersType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='QualifiersType'):
        if self.qualifier:
            self.qualifier.export(outfile, level, namespace_, name_='qualifier', )
    def hasContent_(self):
        if (
            self.qualifier is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='QualifiersType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.qualifier is not None:
            showIndent(outfile, level)
            outfile.write(u'qualifier=model_.qualifier(\n')
            self.qualifier.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'qualifier': 
            obj_ = qualifier.factory()
            obj_.build(child_)
            self.set_qualifier(obj_)
# end class QualifiersType


class qualifier(GeneratedsSuper):
    """qualifying comments that accompany the data. value/@qaulifier is a
    space delimted list of qualifiers for a data value.
    @qualifierCode is the link to the value/@qualifier for a single
    value The value inside provides the textual description.
    @qualifierCode is the reference code. @qualifierCode=A qualifier
    value=Approved @vocabulary and @network are suggested. For
    example a value from the USGS may qualifiers from multiple
    vocabularies, and the network would be the data service."""
    subclass = None
    superclass = None
    def __init__(self, qualifierID=None, default=None, network=None, vocabulary=None, qualifierCode=None):
        self.qualifierID = _cast(int, qualifierID)
        self.default = _cast(bool, default)
        self.network = _cast(None, network)
        self.vocabulary = _cast(None, vocabulary)
        self.qualifierCode = qualifierCode
    def factory(*args_, **kwargs_):
        if qualifier.subclass:
            return qualifier.subclass(*args_, **kwargs_)
        else:
            return qualifier(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_qualifierCode(self): return self.qualifierCode
    def set_qualifierCode(self, qualifierCode): self.qualifierCode = qualifierCode
    def get_qualifierID(self): return self.qualifierID
    def set_qualifierID(self, qualifierID): self.qualifierID = qualifierID
    def get_default(self): return self.default
    def set_default(self, default): self.default = default
    def get_network(self): return self.network
    def set_network(self, network): self.network = network
    def get_vocabulary(self): return self.vocabulary
    def set_vocabulary(self, vocabulary): self.vocabulary = vocabulary
    def export(self, outfile, level, namespace_='', name_='qualifier', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='qualifier')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='qualifier'):
        if self.qualifierID is not None and 'qualifierID' not in already_processed:
            already_processed.append('qualifierID')
            outfile.write(u' qualifierID="%s"' % self.gds_format_integer(self.qualifierID, input_name='qualifierID'))
        if self.default is not None and 'default' not in already_processed:
            already_processed.append('default')
            outfile.write(u' default="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.default)), input_name='default'))
        if self.network is not None and 'network' not in already_processed:
            already_processed.append('network')
            outfile.write(u' network=%s' % (self.gds_format_string(quote_attrib(self.network), input_name='network'), ))
        if self.vocabulary is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            outfile.write(u' vocabulary=%s' % (self.gds_format_string(quote_attrib(self.vocabulary), input_name='vocabulary'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='qualifier'):
        if self.qualifierCode is not None:
            showIndent(outfile, level)
            outfile.write(u'<%squalifierCode>%s</%squalifierCode>\n' % (namespace_, self.gds_format_string(quote_xml(self.qualifierCode), input_name='qualifierCode'), namespace_))
    def hasContent_(self):
        if (
            self.qualifierCode is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='qualifier'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.qualifierID is not None and 'qualifierID' not in already_processed:
            already_processed.append('qualifierID')
            showIndent(outfile, level)
            outfile.write(u'qualifierID = %d,\n' % (self.qualifierID,))
        if self.default is not None and 'default' not in already_processed:
            already_processed.append('default')
            showIndent(outfile, level)
            outfile.write(u'default = %s,\n' % (self.default,))
        if self.network is not None and 'network' not in already_processed:
            already_processed.append('network')
            showIndent(outfile, level)
            outfile.write(u'network = "%s",\n' % (self.network,))
        if self.vocabulary is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            showIndent(outfile, level)
            outfile.write(u'vocabulary = "%s",\n' % (self.vocabulary,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.qualifierCode is not None:
            showIndent(outfile, level)
            outfile.write(u'qualifierCode=%s,\n' % quote_python(self.qualifierCode))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('qualifierID')
        if value is not None and 'qualifierID' not in already_processed:
            already_processed.append('qualifierID')
            try:
                self.qualifierID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
        value = attrs.get('default')
        if value is not None and 'default' not in already_processed:
            already_processed.append('default')
            if value in ('true', '1'):
                self.default = True
            elif value in ('false', '0'):
                self.default = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = attrs.get('network')
        if value is not None and 'network' not in already_processed:
            already_processed.append('network')
            self.network = value
        value = attrs.get('vocabulary')
        if value is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            self.vocabulary = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'qualifierCode':
            qualifierCode_ = child_.text
            self.qualifierCode = qualifierCode_
# end class qualifier


class TimeSeriesType(GeneratedsSuper):
    """Contains the source of the time series, the variable, and values
    element which is an array of value elements and thier associated
    metadata (qualifiers, methods, sources, quality control level,
    samples)Name of the time series. optional."""
    subclass = None
    superclass = None
    def __init__(self, name=None, sourceInfo=None, variable=None, values=None):
        self.name = _cast(None, name)
        self.sourceInfo = sourceInfo
        self.variable = variable
        self.values = values
    def factory(*args_, **kwargs_):
        if TimeSeriesType.subclass:
            return TimeSeriesType.subclass(*args_, **kwargs_)
        else:
            return TimeSeriesType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_sourceInfo(self): return self.sourceInfo
    def set_sourceInfo(self, sourceInfo): self.sourceInfo = sourceInfo
    def get_variable(self): return self.variable
    def set_variable(self, variable): self.variable = variable
    def get_values(self): return self.values
    def set_values(self, values): self.values = values
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def export(self, outfile, level, namespace_='', name_='TimeSeriesType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='TimeSeriesType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='TimeSeriesType'):
        outfile.write(u' name=%s' % (self.gds_format_string(quote_attrib(self.name), input_name='name'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='TimeSeriesType'):
        if self.sourceInfo:
            self.sourceInfo.export(outfile, level, namespace_, name_='sourceInfo', )
        if self.variable:
            self.variable.export(outfile, level, namespace_, name_='variable', )
        if self.values:
            self.values.export(outfile, level, namespace_, name_='values', )
    def hasContent_(self):
        if (
            self.sourceInfo is not None or
            self.variable is not None or
            self.values is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='TimeSeriesType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            showIndent(outfile, level)
            outfile.write(u'name = "%s",\n' % (self.name,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.sourceInfo is not None:
            showIndent(outfile, level)
            outfile.write(u'sourceInfo=model_.SourceInfoType(\n')
            self.sourceInfo.exportLiteral(outfile, level, name_='sourceInfo')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.variable is not None:
            showIndent(outfile, level)
            outfile.write(u'variable=model_.VariableInfoType(\n')
            self.variable.exportLiteral(outfile, level, name_='variable')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.values is not None:
            showIndent(outfile, level)
            outfile.write(u'values=model_.TsValuesSingleVariableType(\n')
            self.values.exportLiteral(outfile, level, name_='values')
            showIndent(outfile, level)
            outfile.write(u'),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('name')
        if value is not None and 'name' not in already_processed:
            already_processed.append('name')
            self.name = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'sourceInfo': 
            obj_ = SourceInfoType.factory()
            obj_.build(child_)
            self.set_sourceInfo(obj_)
        elif nodeName_ == 'variable': 
            obj_ = VariableInfoType.factory()
            obj_.build(child_)
            self.set_variable(obj_)
        elif nodeName_ == 'values': 
            obj_ = TsValuesSingleVariableType.factory()
            obj_.build(child_)
            self.set_values(obj_)
# end class TimeSeriesType


class NoteType(GeneratedsSuper):
    """NoteType defines the note element available in many defined types.
    the value should be the description of the note. @title should be
    the brief name that might be displayed as a label. @type can be
    used to allow for grouping of elements."""
    subclass = None
    superclass = None
    def __init__(self, title=None, href=None, type_=None, show=None, valueOf_=None):
        self.title = _cast(None, title)
        self.href = _cast(None, href)
        self.type_ = _cast(None, type_)
        self.show = _cast(None, show)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if NoteType.subclass:
            return NoteType.subclass(*args_, **kwargs_)
        else:
            return NoteType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_title(self): return self.title
    def set_title(self, title): self.title = title
    def get_href(self): return self.href
    def set_href(self, href): self.href = href
    def get_type(self): return self.type_
    def set_type(self, type_): self.type_ = type_
    def get_show(self): return self.show
    def set_show(self, show): self.show = show
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='NoteType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='NoteType')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='NoteType'):
        if self.title is not None and 'title' not in already_processed:
            already_processed.append('title')
            outfile.write(u' title=%s' % (self.gds_format_string(quote_attrib(self.title), input_name='title'), ))
        if self.href is not None and 'href' not in already_processed:
            already_processed.append('href')
            outfile.write(u' href=%s' % (self.gds_format_string(quote_attrib(self.href), input_name='href'), ))
        if self.type_ is not None and 'type_' not in already_processed:
            already_processed.append('type_')
            outfile.write(u' type=%s' % (self.gds_format_string(quote_attrib(self.type_), input_name='type'), ))
        if self.show is not None and 'show' not in already_processed:
            already_processed.append('show')
            outfile.write(u' show=%s' % (self.gds_format_string(quote_attrib(self.show), input_name='show'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='NoteType'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='NoteType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.title is not None and 'title' not in already_processed:
            already_processed.append('title')
            showIndent(outfile, level)
            outfile.write(u'title = "%s",\n' % (self.title,))
        if self.href is not None and 'href' not in already_processed:
            already_processed.append('href')
            showIndent(outfile, level)
            outfile.write(u'href = "%s",\n' % (self.href,))
        if self.type_ is not None and 'type_' not in already_processed:
            already_processed.append('type_')
            showIndent(outfile, level)
            outfile.write(u'type_ = "%s",\n' % (self.type_,))
        if self.show is not None and 'show' not in already_processed:
            already_processed.append('show')
            showIndent(outfile, level)
            outfile.write(u'show = "%s",\n' % (self.show,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('title')
        if value is not None and 'title' not in already_processed:
            already_processed.append('title')
            self.title = value
        value = attrs.get('href')
        if value is not None and 'href' not in already_processed:
            already_processed.append('href')
            self.href = value
        value = attrs.get('type')
        if value is not None and 'type' not in already_processed:
            already_processed.append('type')
            self.type_ = value
        value = attrs.get('show')
        if value is not None and 'show' not in already_processed:
            already_processed.append('show')
            self.show = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class NoteType


class option(GeneratedsSuper):
    """Option elements are key-value pair elements that control how a
    variable maght be utilized in a service. Examples: MODIS web
    service. Information is aggreated over land or ocean or both.
    The plotarea option can include: plotarea=land, plotarea=land,
    plotarea=landocean USGS uses a statistic code, 0003, to repesent
    a value type of 'Average'. The USGS statistic codes also several
    options that do not fit the ODM data model."""
    subclass = None
    superclass = None
    def __init__(self, optionCode=None, optionID=None, name=None, valueOf_=None):
        self.optionCode = _cast(None, optionCode)
        self.optionID = _cast(int, optionID)
        self.name = _cast(None, name)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if option.subclass:
            return option.subclass(*args_, **kwargs_)
        else:
            return option(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_optionCode(self): return self.optionCode
    def set_optionCode(self, optionCode): self.optionCode = optionCode
    def get_optionID(self): return self.optionID
    def set_optionID(self, optionID): self.optionID = optionID
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='option', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='option')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='option'):
        if self.optionCode is not None and 'optionCode' not in already_processed:
            already_processed.append('optionCode')
            outfile.write(u' optionCode=%s' % (self.gds_format_string(quote_attrib(self.optionCode), input_name='optionCode'), ))
        if self.optionID is not None and 'optionID' not in already_processed:
            already_processed.append('optionID')
            outfile.write(u' optionID="%s"' % self.gds_format_integer(self.optionID, input_name='optionID'))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            outfile.write(u' name=%s' % (self.gds_format_string(quote_attrib(self.name), input_name='name'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='option'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='option'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.optionCode is not None and 'optionCode' not in already_processed:
            already_processed.append('optionCode')
            showIndent(outfile, level)
            outfile.write(u'optionCode = "%s",\n' % (self.optionCode,))
        if self.optionID is not None and 'optionID' not in already_processed:
            already_processed.append('optionID')
            showIndent(outfile, level)
            outfile.write(u'optionID = %d,\n' % (self.optionID,))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            showIndent(outfile, level)
            outfile.write(u'name = "%s",\n' % (self.name,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('optionCode')
        if value is not None and 'optionCode' not in already_processed:
            already_processed.append('optionCode')
            self.optionCode = value
            self.optionCode = ' '.join(self.optionCode.split())
        value = attrs.get('optionID')
        if value is not None and 'optionID' not in already_processed:
            already_processed.append('optionID')
            try:
                self.optionID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
        value = attrs.get('name')
        if value is not None and 'name' not in already_processed:
            already_processed.append('name')
            self.name = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class option


class variableCode(GeneratedsSuper):
    """Text code used by the organization that collects the data to
    identify the variable. The attribute @vocabulary must be set to
    the data source name, so the clients can subbumit variable
    requests to a web service (net USGS discharge variableCode
    @vocabularyk=NWISDV @default=true “00060”"""
    subclass = None
    superclass = None
    def __init__(self, default=None, variableID=None, vocabulary=None, network=None, valueOf_=None):
        self.default = _cast(bool, default)
        self.variableID = _cast(int, variableID)
        self.vocabulary = _cast(None, vocabulary)
        self.network = _cast(None, network)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if variableCode.subclass:
            return variableCode.subclass(*args_, **kwargs_)
        else:
            return variableCode(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_default(self): return self.default
    def set_default(self, default): self.default = default
    def get_variableID(self): return self.variableID
    def set_variableID(self, variableID): self.variableID = variableID
    def get_vocabulary(self): return self.vocabulary
    def set_vocabulary(self, vocabulary): self.vocabulary = vocabulary
    def get_network(self): return self.network
    def set_network(self, network): self.network = network
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='variableCode', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='variableCode')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='variableCode'):
        if self.default is not None and 'default' not in already_processed:
            already_processed.append('default')
            outfile.write(u' default="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.default)), input_name='default'))
        if self.variableID is not None and 'variableID' not in already_processed:
            already_processed.append('variableID')
            outfile.write(u' variableID="%s"' % self.gds_format_integer(self.variableID, input_name='variableID'))
        if self.vocabulary is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            outfile.write(u' vocabulary=%s' % (self.gds_format_string(quote_attrib(self.vocabulary), input_name='vocabulary'), ))
        if self.network is not None and 'network' not in already_processed:
            already_processed.append('network')
            outfile.write(u' network=%s' % (self.gds_format_string(quote_attrib(self.network), input_name='network'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='variableCode'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='variableCode'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.default is not None and 'default' not in already_processed:
            already_processed.append('default')
            showIndent(outfile, level)
            outfile.write(u'default = %s,\n' % (self.default,))
        if self.variableID is not None and 'variableID' not in already_processed:
            already_processed.append('variableID')
            showIndent(outfile, level)
            outfile.write(u'variableID = %d,\n' % (self.variableID,))
        if self.vocabulary is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            showIndent(outfile, level)
            outfile.write(u'vocabulary = "%s",\n' % (self.vocabulary,))
        if self.network is not None and 'network' not in already_processed:
            already_processed.append('network')
            showIndent(outfile, level)
            outfile.write(u'network = "%s",\n' % (self.network,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('default')
        if value is not None and 'default' not in already_processed:
            already_processed.append('default')
            if value in ('true', '1'):
                self.default = True
            elif value in ('false', '0'):
                self.default = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = attrs.get('variableID')
        if value is not None and 'variableID' not in already_processed:
            already_processed.append('variableID')
            try:
                self.variableID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
        value = attrs.get('vocabulary')
        if value is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            self.vocabulary = value
        value = attrs.get('network')
        if value is not None and 'network' not in already_processed:
            already_processed.append('network')
            self.network = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class variableCode


class units(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, unitsAbbreviation=None, unitsCode=None, unitsType=None, valueOf_=None):
        self.unitsAbbreviation = _cast(None, unitsAbbreviation)
        self.unitsCode = _cast(None, unitsCode)
        self.unitsType = _cast(None, unitsType)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if units.subclass:
            return units.subclass(*args_, **kwargs_)
        else:
            return units(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_unitsAbbreviation(self): return self.unitsAbbreviation
    def set_unitsAbbreviation(self, unitsAbbreviation): self.unitsAbbreviation = unitsAbbreviation
    def get_unitsCode(self): return self.unitsCode
    def set_unitsCode(self, unitsCode): self.unitsCode = unitsCode
    def get_unitsType(self): return self.unitsType
    def set_unitsType(self, unitsType): self.unitsType = unitsType
    def validate_UnitsTypeEnum(self, value):
        # Validate type UnitsTypeEnum, a restriction on xsi:string.
        pass
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='units', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='units')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='units'):
        if self.unitsAbbreviation is not None and 'unitsAbbreviation' not in already_processed:
            already_processed.append('unitsAbbreviation')
            outfile.write(u' unitsAbbreviation=%s' % (self.gds_format_string(quote_attrib(self.unitsAbbreviation), input_name='unitsAbbreviation'), ))
        if self.unitsCode is not None and 'unitsCode' not in already_processed:
            already_processed.append('unitsCode')
            outfile.write(u' unitsCode=%s' % (self.gds_format_string(quote_attrib(self.unitsCode), input_name='unitsCode'), ))
        if self.unitsType is not None and 'unitsType' not in already_processed:
            already_processed.append('unitsType')
            outfile.write(u' unitsType=%s' % (quote_attrib(self.unitsType), ))
    def exportChildren(self, outfile, level, namespace_='', name_='units'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='units'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.unitsAbbreviation is not None and 'unitsAbbreviation' not in already_processed:
            already_processed.append('unitsAbbreviation')
            showIndent(outfile, level)
            outfile.write(u'unitsAbbreviation = "%s",\n' % (self.unitsAbbreviation,))
        if self.unitsCode is not None and 'unitsCode' not in already_processed:
            already_processed.append('unitsCode')
            showIndent(outfile, level)
            outfile.write(u'unitsCode = "%s",\n' % (self.unitsCode,))
        if self.unitsType is not None and 'unitsType' not in already_processed:
            already_processed.append('unitsType')
            showIndent(outfile, level)
            outfile.write(u'unitsType = "%s",\n' % (self.unitsType,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('unitsAbbreviation')
        if value is not None and 'unitsAbbreviation' not in already_processed:
            already_processed.append('unitsAbbreviation')
            self.unitsAbbreviation = value
        value = attrs.get('unitsCode')
        if value is not None and 'unitsCode' not in already_processed:
            already_processed.append('unitsCode')
            self.unitsCode = value
            self.unitsCode = ' '.join(self.unitsCode.split())
        value = attrs.get('unitsType')
        if value is not None and 'unitsType' not in already_processed:
            already_processed.append('unitsType')
            self.unitsType = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class units


class ValueSingleVariable(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, codedVocabularyTerm=None, metadataDateTime=None, qualityControlLevel=None, methodID=None, codedVocabulary=None, sourceID=None, oid=None, censorCode=None, offsetDescription=None, sampleID=None, offsetTypeID=None, accuracyStdDev=None, offsetUnitsAbbreviation=None, offsetValue=None, dateTime=None, qualifiers=None, offsetUnitsCode=None, valueOf_=None):
        self.codedVocabularyTerm = _cast(None, codedVocabularyTerm)
        self.metadataDateTime = _cast(None, metadataDateTime)
        self.qualityControlLevel = _cast(None, qualityControlLevel)
        self.methodID = _cast(int, methodID)
        self.codedVocabulary = _cast(bool, codedVocabulary)
        self.sourceID = _cast(int, sourceID)
        self.oid = _cast(None, oid)
        self.censorCode = _cast(None, censorCode)
        self.offsetDescription = _cast(None, offsetDescription)
        self.sampleID = _cast(int, sampleID)
        self.offsetTypeID = _cast(int, offsetTypeID)
        self.accuracyStdDev = _cast(float, accuracyStdDev)
        self.offsetUnitsAbbreviation = _cast(None, offsetUnitsAbbreviation)
        self.offsetValue = _cast(float, offsetValue)
        self.dateTime = _cast(None, dateTime)
        self.qualifiers = _cast(None, qualifiers)
        self.offsetUnitsCode = _cast(None, offsetUnitsCode)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if ValueSingleVariable.subclass:
            return ValueSingleVariable.subclass(*args_, **kwargs_)
        else:
            return ValueSingleVariable(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_codedVocabularyTerm(self): return self.codedVocabularyTerm
    def set_codedVocabularyTerm(self, codedVocabularyTerm): self.codedVocabularyTerm = codedVocabularyTerm
    def get_metadataDateTime(self): return self.metadataDateTime
    def set_metadataDateTime(self, metadataDateTime): self.metadataDateTime = metadataDateTime
    def get_qualityControlLevel(self): return self.qualityControlLevel
    def set_qualityControlLevel(self, qualityControlLevel): self.qualityControlLevel = qualityControlLevel
    def validate_QualityControlLevelEnum(self, value):
        # Validate type QualityControlLevelEnum, a restriction on xsi:string.
        pass
    def get_methodID(self): return self.methodID
    def set_methodID(self, methodID): self.methodID = methodID
    def get_codedVocabulary(self): return self.codedVocabulary
    def set_codedVocabulary(self, codedVocabulary): self.codedVocabulary = codedVocabulary
    def get_sourceID(self): return self.sourceID
    def set_sourceID(self, sourceID): self.sourceID = sourceID
    def get_oid(self): return self.oid
    def set_oid(self, oid): self.oid = oid
    def get_censorCode(self): return self.censorCode
    def set_censorCode(self, censorCode): self.censorCode = censorCode
    def validate_CensorCodeEnum(self, value):
        # Validate type CensorCodeEnum, a restriction on xsi:string.
        pass
    def get_offsetDescription(self): return self.offsetDescription
    def set_offsetDescription(self, offsetDescription): self.offsetDescription = offsetDescription
    def get_sampleID(self): return self.sampleID
    def set_sampleID(self, sampleID): self.sampleID = sampleID
    def get_offsetTypeID(self): return self.offsetTypeID
    def set_offsetTypeID(self, offsetTypeID): self.offsetTypeID = offsetTypeID
    def get_accuracyStdDev(self): return self.accuracyStdDev
    def set_accuracyStdDev(self, accuracyStdDev): self.accuracyStdDev = accuracyStdDev
    def get_offsetUnitsAbbreviation(self): return self.offsetUnitsAbbreviation
    def set_offsetUnitsAbbreviation(self, offsetUnitsAbbreviation): self.offsetUnitsAbbreviation = offsetUnitsAbbreviation
    def get_offsetValue(self): return self.offsetValue
    def set_offsetValue(self, offsetValue): self.offsetValue = offsetValue
    def get_dateTime(self): return self.dateTime
    def set_dateTime(self, dateTime): self.dateTime = dateTime
    def get_qualifiers(self): return self.qualifiers
    def set_qualifiers(self, qualifiers): self.qualifiers = qualifiers
    def get_offsetUnitsCode(self): return self.offsetUnitsCode
    def set_offsetUnitsCode(self, offsetUnitsCode): self.offsetUnitsCode = offsetUnitsCode
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='ValueSingleVariable', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='ValueSingleVariable')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='ValueSingleVariable'):
        if self.codedVocabularyTerm is not None and 'codedVocabularyTerm' not in already_processed:
            already_processed.append('codedVocabularyTerm')
            outfile.write(u' codedVocabularyTerm=%s' % (self.gds_format_string(quote_attrib(self.codedVocabularyTerm), input_name='codedVocabularyTerm'), ))
        if self.metadataDateTime is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            outfile.write(u' metadataDateTime=%s' % (self.gds_format_string(quote_attrib(self.metadataDateTime), input_name='metadataDateTime'), ))
        if self.qualityControlLevel is not None and 'qualityControlLevel' not in already_processed:
            already_processed.append('qualityControlLevel')
            outfile.write(u' qualityControlLevel=%s' % (quote_attrib(self.qualityControlLevel), ))
        if self.methodID is not None and 'methodID' not in already_processed:
            already_processed.append('methodID')
            outfile.write(u' methodID="%s"' % self.gds_format_integer(self.methodID, input_name='methodID'))
        if self.codedVocabulary is not None and 'codedVocabulary' not in already_processed:
            already_processed.append('codedVocabulary')
            outfile.write(u' codedVocabulary="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.codedVocabulary)), input_name='codedVocabulary'))
        if self.sourceID is not None and 'sourceID' not in already_processed:
            already_processed.append('sourceID')
            outfile.write(u' sourceID="%s"' % self.gds_format_integer(self.sourceID, input_name='sourceID'))
        if self.oid is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            outfile.write(u' oid=%s' % (self.gds_format_string(quote_attrib(self.oid), input_name='oid'), ))
        if self.censorCode is not None and 'censorCode' not in already_processed:
            already_processed.append('censorCode')
            outfile.write(u' censorCode=%s' % (quote_attrib(self.censorCode), ))
        if self.offsetDescription is not None and 'offsetDescription' not in already_processed:
            already_processed.append('offsetDescription')
            outfile.write(u' offsetDescription=%s' % (self.gds_format_string(quote_attrib(self.offsetDescription), input_name='offsetDescription'), ))
        if self.sampleID is not None and 'sampleID' not in already_processed:
            already_processed.append('sampleID')
            outfile.write(u' sampleID="%s"' % self.gds_format_integer(self.sampleID, input_name='sampleID'))
        if self.offsetTypeID is not None and 'offsetTypeID' not in already_processed:
            already_processed.append('offsetTypeID')
            outfile.write(u' offsetTypeID="%s"' % self.gds_format_integer(self.offsetTypeID, input_name='offsetTypeID'))
        if self.accuracyStdDev is not None and 'accuracyStdDev' not in already_processed:
            already_processed.append('accuracyStdDev')
            outfile.write(u' accuracyStdDev="%s"' % self.gds_format_double(self.accuracyStdDev, input_name='accuracyStdDev'))
        if self.offsetUnitsAbbreviation is not None and 'offsetUnitsAbbreviation' not in already_processed:
            already_processed.append('offsetUnitsAbbreviation')
            outfile.write(u' offsetUnitsAbbreviation=%s' % (self.gds_format_string(quote_attrib(self.offsetUnitsAbbreviation), input_name='offsetUnitsAbbreviation'), ))
        if self.offsetValue is not None and 'offsetValue' not in already_processed:
            already_processed.append('offsetValue')
            outfile.write(u' offsetValue="%s"' % self.gds_format_double(self.offsetValue, input_name='offsetValue'))
        outfile.write(u' dateTime=%s' % (self.gds_format_string(quote_attrib(self.dateTime), input_name='dateTime'), ))
        if self.qualifiers is not None and 'qualifiers' not in already_processed:
            already_processed.append('qualifiers')
            outfile.write(u' qualifiers=%s' % (self.gds_format_string(quote_attrib(self.qualifiers), input_name='qualifiers'), ))
        if self.offsetUnitsCode is not None and 'offsetUnitsCode' not in already_processed:
            already_processed.append('offsetUnitsCode')
            outfile.write(u' offsetUnitsCode=%s' % (self.gds_format_string(quote_attrib(self.offsetUnitsCode), input_name='offsetUnitsCode'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='ValueSingleVariable'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='ValueSingleVariable'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.codedVocabularyTerm is not None and 'codedVocabularyTerm' not in already_processed:
            already_processed.append('codedVocabularyTerm')
            showIndent(outfile, level)
            outfile.write(u'codedVocabularyTerm = "%s",\n' % (self.codedVocabularyTerm,))
        if self.metadataDateTime is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            showIndent(outfile, level)
            outfile.write(u'metadataDateTime = "%s",\n' % (self.metadataDateTime,))
        if self.qualityControlLevel is not None and 'qualityControlLevel' not in already_processed:
            already_processed.append('qualityControlLevel')
            showIndent(outfile, level)
            outfile.write(u'qualityControlLevel = "%s",\n' % (self.qualityControlLevel,))
        if self.methodID is not None and 'methodID' not in already_processed:
            already_processed.append('methodID')
            showIndent(outfile, level)
            outfile.write(u'methodID = %d,\n' % (self.methodID,))
        if self.codedVocabulary is not None and 'codedVocabulary' not in already_processed:
            already_processed.append('codedVocabulary')
            showIndent(outfile, level)
            outfile.write(u'codedVocabulary = %s,\n' % (self.codedVocabulary,))
        if self.sourceID is not None and 'sourceID' not in already_processed:
            already_processed.append('sourceID')
            showIndent(outfile, level)
            outfile.write(u'sourceID = %d,\n' % (self.sourceID,))
        if self.oid is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            showIndent(outfile, level)
            outfile.write(u'oid = "%s",\n' % (self.oid,))
        if self.censorCode is not None and 'censorCode' not in already_processed:
            already_processed.append('censorCode')
            showIndent(outfile, level)
            outfile.write(u'censorCode = "%s",\n' % (self.censorCode,))
        if self.offsetDescription is not None and 'offsetDescription' not in already_processed:
            already_processed.append('offsetDescription')
            showIndent(outfile, level)
            outfile.write(u'offsetDescription = "%s",\n' % (self.offsetDescription,))
        if self.sampleID is not None and 'sampleID' not in already_processed:
            already_processed.append('sampleID')
            showIndent(outfile, level)
            outfile.write(u'sampleID = %d,\n' % (self.sampleID,))
        if self.offsetTypeID is not None and 'offsetTypeID' not in already_processed:
            already_processed.append('offsetTypeID')
            showIndent(outfile, level)
            outfile.write(u'offsetTypeID = %d,\n' % (self.offsetTypeID,))
        if self.accuracyStdDev is not None and 'accuracyStdDev' not in already_processed:
            already_processed.append('accuracyStdDev')
            showIndent(outfile, level)
            outfile.write(u'accuracyStdDev = %e,\n' % (self.accuracyStdDev,))
        if self.offsetUnitsAbbreviation is not None and 'offsetUnitsAbbreviation' not in already_processed:
            already_processed.append('offsetUnitsAbbreviation')
            showIndent(outfile, level)
            outfile.write(u'offsetUnitsAbbreviation = "%s",\n' % (self.offsetUnitsAbbreviation,))
        if self.offsetValue is not None and 'offsetValue' not in already_processed:
            already_processed.append('offsetValue')
            showIndent(outfile, level)
            outfile.write(u'offsetValue = %e,\n' % (self.offsetValue,))
        if self.dateTime is not None and 'dateTime' not in already_processed:
            already_processed.append('dateTime')
            showIndent(outfile, level)
            outfile.write(u'dateTime = "%s",\n' % (self.dateTime,))
        if self.qualifiers is not None and 'qualifiers' not in already_processed:
            already_processed.append('qualifiers')
            showIndent(outfile, level)
            outfile.write(u'qualifiers = "%s",\n' % (self.qualifiers,))
        if self.offsetUnitsCode is not None and 'offsetUnitsCode' not in already_processed:
            already_processed.append('offsetUnitsCode')
            showIndent(outfile, level)
            outfile.write(u'offsetUnitsCode = "%s",\n' % (self.offsetUnitsCode,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('codedVocabularyTerm')
        if value is not None and 'codedVocabularyTerm' not in already_processed:
            already_processed.append('codedVocabularyTerm')
            self.codedVocabularyTerm = value
        value = attrs.get('metadataDateTime')
        if value is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            self.metadataDateTime = value
        value = attrs.get('qualityControlLevel')
        if value is not None and 'qualityControlLevel' not in already_processed:
            already_processed.append('qualityControlLevel')
            self.qualityControlLevel = value
        value = attrs.get('methodID')
        if value is not None and 'methodID' not in already_processed:
            already_processed.append('methodID')
            try:
                self.methodID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
        value = attrs.get('codedVocabulary')
        if value is not None and 'codedVocabulary' not in already_processed:
            already_processed.append('codedVocabulary')
            if value in ('true', '1'):
                self.codedVocabulary = True
            elif value in ('false', '0'):
                self.codedVocabulary = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = attrs.get('sourceID')
        if value is not None and 'sourceID' not in already_processed:
            already_processed.append('sourceID')
            try:
                self.sourceID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
        value = attrs.get('oid')
        if value is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            self.oid = value
        value = attrs.get('censorCode')
        if value is not None and 'censorCode' not in already_processed:
            already_processed.append('censorCode')
            self.censorCode = value
        value = attrs.get('offsetDescription')
        if value is not None and 'offsetDescription' not in already_processed:
            already_processed.append('offsetDescription')
            self.offsetDescription = value
        value = attrs.get('sampleID')
        if value is not None and 'sampleID' not in already_processed:
            already_processed.append('sampleID')
            try:
                self.sampleID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
        value = attrs.get('offsetTypeID')
        if value is not None and 'offsetTypeID' not in already_processed:
            already_processed.append('offsetTypeID')
            try:
                self.offsetTypeID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
        value = attrs.get('accuracyStdDev')
        if value is not None and 'accuracyStdDev' not in already_processed:
            already_processed.append('accuracyStdDev')
            try:
                self.accuracyStdDev = float(value)
            except ValueError, exp:
                raise ValueError('Bad float/double attribute (accuracyStdDev): %s' % exp)
        value = attrs.get('offsetUnitsAbbreviation')
        if value is not None and 'offsetUnitsAbbreviation' not in already_processed:
            already_processed.append('offsetUnitsAbbreviation')
            self.offsetUnitsAbbreviation = value
        value = attrs.get('offsetValue')
        if value is not None and 'offsetValue' not in already_processed:
            already_processed.append('offsetValue')
            try:
                self.offsetValue = float(value)
            except ValueError, exp:
                raise ValueError('Bad float/double attribute (offsetValue): %s' % exp)
        value = attrs.get('dateTime')
        if value is not None and 'dateTime' not in already_processed:
            already_processed.append('dateTime')
            self.dateTime = value
        value = attrs.get('qualifiers')
        if value is not None and 'qualifiers' not in already_processed:
            already_processed.append('qualifiers')
            self.qualifiers = value
        value = attrs.get('offsetUnitsCode')
        if value is not None and 'offsetUnitsCode' not in already_processed:
            already_processed.append('offsetUnitsCode')
            self.offsetUnitsCode = value
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class ValueSingleVariable


class VariablesResponseType(GeneratedsSuper):
    """VariablesResponseType is object type returned by the method
    GetVariableInfo. The elemnt name is variablesResponse. The
    request will contain a variables element containing a list of
    variable elements."""
    subclass = None
    superclass = None
    def __init__(self, queryInfo=None, variables=None):
        self.queryInfo = queryInfo
        self.variables = variables
    def factory(*args_, **kwargs_):
        if VariablesResponseType.subclass:
            return VariablesResponseType.subclass(*args_, **kwargs_)
        else:
            return VariablesResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_queryInfo(self): return self.queryInfo
    def set_queryInfo(self, queryInfo): self.queryInfo = queryInfo
    def get_variables(self): return self.variables
    def set_variables(self, variables): self.variables = variables
    def export(self, outfile, level, namespace_='', name_='VariablesResponseType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='VariablesResponseType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='VariablesResponseType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='VariablesResponseType'):
        if self.queryInfo:
            self.queryInfo.export(outfile, level, namespace_, name_='queryInfo', )
        if self.variables:
            self.variables.export(outfile, level, namespace_, name_='variables', )
    def hasContent_(self):
        if (
            self.queryInfo is not None or
            self.variables is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='VariablesResponseType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.queryInfo is not None:
            showIndent(outfile, level)
            outfile.write(u'queryInfo=model_.QueryInfoType(\n')
            self.queryInfo.exportLiteral(outfile, level, name_='queryInfo')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.variables is not None:
            showIndent(outfile, level)
            outfile.write(u'variables=model_.variables(\n')
            self.variables.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'queryInfo': 
            obj_ = QueryInfoType.factory()
            obj_.build(child_)
            self.set_queryInfo(obj_)
        elif nodeName_ == 'variables': 
            obj_ = variables.factory()
            obj_.build(child_)
            self.set_variables(obj_)
# end class VariablesResponseType


class TimeSeriesResponseType(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, queryInfo=None, timeSeries=None):
        self.queryInfo = queryInfo
        self.timeSeries = timeSeries
    def factory(*args_, **kwargs_):
        if TimeSeriesResponseType.subclass:
            return TimeSeriesResponseType.subclass(*args_, **kwargs_)
        else:
            return TimeSeriesResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_queryInfo(self): return self.queryInfo
    def set_queryInfo(self, queryInfo): self.queryInfo = queryInfo
    def get_timeSeries(self): return self.timeSeries
    def set_timeSeries(self, timeSeries): self.timeSeries = timeSeries
    def export(self, outfile, level, namespace_='', name_='TimeSeriesResponseType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='TimeSeriesResponseType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='TimeSeriesResponseType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='TimeSeriesResponseType'):
        if self.queryInfo:
            self.queryInfo.export(outfile, level, namespace_, name_='queryInfo', )
        if self.timeSeries:
            self.timeSeries.export(outfile, level, namespace_, name_='timeSeries', )
    def hasContent_(self):
        if (
            self.queryInfo is not None or
            self.timeSeries is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='TimeSeriesResponseType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.queryInfo is not None:
            showIndent(outfile, level)
            outfile.write(u'queryInfo=model_.QueryInfoType(\n')
            self.queryInfo.exportLiteral(outfile, level, name_='queryInfo')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.timeSeries is not None:
            showIndent(outfile, level)
            outfile.write(u'timeSeries=model_.TimeSeriesType(\n')
            self.timeSeries.exportLiteral(outfile, level, name_='timeSeries')
            showIndent(outfile, level)
            outfile.write(u'),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'queryInfo': 
            obj_ = QueryInfoType.factory()
            obj_.build(child_)
            self.set_queryInfo(obj_)
        elif nodeName_ == 'timeSeries': 
            obj_ = TimeSeriesType.factory()
            obj_.build(child_)
            self.set_timeSeries(obj_)
# end class TimeSeriesResponseType


class SiteInfoResponseType(GeneratedsSuper):
    """A sitesResponse contains a list of zero or more site elements. The
    siteInfo element contains the basic site information, siteName,
    location, siteCodes, properties. The seriesCatalog contains the
    list of observation series conducted at a site. A site element
    can have two parts: siteInfo, and one or more seriesCatalogs.
    Rules: GetSites(site[]) or GetSites(null), return no
    seriesCatalogs elements GetSiteInfo(site) return all information
    about a site, including the seriesCatalog."""
    subclass = None
    superclass = None
    def __init__(self, queryInfo=None, site=None):
        self.queryInfo = queryInfo
        if site is None:
            self.site = []
        else:
            self.site = site
    def factory(*args_, **kwargs_):
        if SiteInfoResponseType.subclass:
            return SiteInfoResponseType.subclass(*args_, **kwargs_)
        else:
            return SiteInfoResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_queryInfo(self): return self.queryInfo
    def set_queryInfo(self, queryInfo): self.queryInfo = queryInfo
    def get_site(self): return self.site
    def set_site(self, site): self.site = site
    def add_site(self, value): self.site.append(value)
    def insert_site(self, index, value): self.site[index] = value
    def export(self, outfile, level, namespace_='', name_='SiteInfoResponseType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='SiteInfoResponseType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='SiteInfoResponseType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='SiteInfoResponseType'):
        if self.queryInfo:
            self.queryInfo.export(outfile, level, namespace_, name_='queryInfo', )
        for site_ in self.site:
            site_.export(outfile, level, namespace_, name_='site')
    def hasContent_(self):
        if (
            self.queryInfo is not None or
            self.site
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='SiteInfoResponseType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.queryInfo is not None:
            showIndent(outfile, level)
            outfile.write(u'queryInfo=model_.QueryInfoType(\n')
            self.queryInfo.exportLiteral(outfile, level, name_='queryInfo')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        showIndent(outfile, level)
        outfile.write(u'site=[\n')
        level += 1
        for site_ in self.site:
            showIndent(outfile, level)
            outfile.write(u'model_.site(\n')
            site_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'queryInfo': 
            obj_ = QueryInfoType.factory()
            obj_.build(child_)
            self.set_queryInfo(obj_)
        elif nodeName_ == 'site': 
            obj_ = site.factory()
            obj_.build(child_)
            self.site.append(obj_)
# end class SiteInfoResponseType


class site(GeneratedsSuper):
    """A site element can have two parts: siteInfo, and one or more
    seriesCatalogs. The siteInfo element contains the basic site
    information, siteName, location, siteCodes, properties. The
    seriesCatalog contains the list of observation series conducted
    at a site. Rules: GetSites(site[]) or GetSites(null), return no
    seriesCatalogs elements GetSiteInfo(site) return all information
    about a site, including the seriesCatalog."""
    subclass = None
    superclass = None
    def __init__(self, siteInfo=None, seriesCatalog=None, extension=None):
        self.siteInfo = siteInfo
        if seriesCatalog is None:
            self.seriesCatalog = []
        else:
            self.seriesCatalog = seriesCatalog
        self.extension = extension
    def factory(*args_, **kwargs_):
        if site.subclass:
            return site.subclass(*args_, **kwargs_)
        else:
            return site(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_siteInfo(self): return self.siteInfo
    def set_siteInfo(self, siteInfo): self.siteInfo = siteInfo
    def get_seriesCatalog(self): return self.seriesCatalog
    def set_seriesCatalog(self, seriesCatalog): self.seriesCatalog = seriesCatalog
    def add_seriesCatalog(self, value): self.seriesCatalog.append(value)
    def insert_seriesCatalog(self, index, value): self.seriesCatalog[index] = value
    def get_extension(self): return self.extension
    def set_extension(self, extension): self.extension = extension
    def export(self, outfile, level, namespace_='', name_='site', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='site')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='site'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='site'):
        if self.siteInfo:
            self.siteInfo.export(outfile, level, namespace_, name_='siteInfo', )
        for seriesCatalog_ in self.seriesCatalog:
            seriesCatalog_.export(outfile, level, namespace_, name_='seriesCatalog')
        if self.extension is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sextension>%s</%sextension>\n' % (namespace_, self.gds_format_string(quote_xml(self.extension), input_name='extension'), namespace_))
    def hasContent_(self):
        if (
            self.siteInfo is not None or
            self.seriesCatalog or
            self.extension is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='site'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.siteInfo is not None:
            showIndent(outfile, level)
            outfile.write(u'siteInfo=model_.SiteInfoType(\n')
            self.siteInfo.exportLiteral(outfile, level, name_='siteInfo')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        showIndent(outfile, level)
        outfile.write(u'seriesCatalog=[\n')
        level += 1
        for seriesCatalog_ in self.seriesCatalog:
            showIndent(outfile, level)
            outfile.write(u'model_.seriesCatalogType(\n')
            seriesCatalog_.exportLiteral(outfile, level, name_='seriesCatalogType')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        if self.extension is not None:
            showIndent(outfile, level)
            outfile.write(u'extension=%s,\n' % quote_python(self.extension))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'siteInfo': 
            obj_ = SiteInfoType.factory()
            obj_.build(child_)
            self.set_siteInfo(obj_)
        elif nodeName_ == 'seriesCatalog': 
            obj_ = seriesCatalogType.factory()
            obj_.build(child_)
            self.seriesCatalog.append(obj_)
        elif nodeName_ == 'extension':
            extension_ = child_.text
            self.extension = extension_
# end class site


class qualityControlLevel(GeneratedsSuper):
    """quality control levels that are used for versioning data within the
    database. Code used to identify the level of quality control to
    which data values have been subjected."""
    subclass = None
    superclass = None
    def __init__(self, metadataDateTime=None, network=None, vocabulary=None, qualityControlLevelCode=None, oid=None, default=None, qualityControlLevelID=None):
        self.metadataDateTime = _cast(None, metadataDateTime)
        self.network = _cast(None, network)
        self.vocabulary = _cast(None, vocabulary)
        self.qualityControlLevelCode = _cast(None, qualityControlLevelCode)
        self.oid = _cast(None, oid)
        self.default = _cast(bool, default)
        self.qualityControlLevelID = qualityControlLevelID
    def factory(*args_, **kwargs_):
        if qualityControlLevel.subclass:
            return qualityControlLevel.subclass(*args_, **kwargs_)
        else:
            return qualityControlLevel(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_qualityControlLevelID(self): return self.qualityControlLevelID
    def set_qualityControlLevelID(self, qualityControlLevelID): self.qualityControlLevelID = qualityControlLevelID
    def get_metadataDateTime(self): return self.metadataDateTime
    def set_metadataDateTime(self, metadataDateTime): self.metadataDateTime = metadataDateTime
    def get_network(self): return self.network
    def set_network(self, network): self.network = network
    def get_vocabulary(self): return self.vocabulary
    def set_vocabulary(self, vocabulary): self.vocabulary = vocabulary
    def get_qualityControlLevelCode(self): return self.qualityControlLevelCode
    def set_qualityControlLevelCode(self, qualityControlLevelCode): self.qualityControlLevelCode = qualityControlLevelCode
    def get_oid(self): return self.oid
    def set_oid(self, oid): self.oid = oid
    def get_default(self): return self.default
    def set_default(self, default): self.default = default
    def export(self, outfile, level, namespace_='', name_='qualityControlLevel', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='qualityControlLevel')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='qualityControlLevel'):
        if self.metadataDateTime is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            outfile.write(u' metadataDateTime=%s' % (self.gds_format_string(quote_attrib(self.metadataDateTime), input_name='metadataDateTime'), ))
        if self.network is not None and 'network' not in already_processed:
            already_processed.append('network')
            outfile.write(u' network=%s' % (self.gds_format_string(quote_attrib(self.network), input_name='network'), ))
        if self.vocabulary is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            outfile.write(u' vocabulary=%s' % (self.gds_format_string(quote_attrib(self.vocabulary), input_name='vocabulary'), ))
        if self.qualityControlLevelCode is not None and 'qualityControlLevelCode' not in already_processed:
            already_processed.append('qualityControlLevelCode')
            outfile.write(u' qualityControlLevelCode=%s' % (self.gds_format_string(quote_attrib(self.qualityControlLevelCode), input_name='qualityControlLevelCode'), ))
        if self.oid is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            outfile.write(u' oid=%s' % (self.gds_format_string(quote_attrib(self.oid), input_name='oid'), ))
        if self.default is not None and 'default' not in already_processed:
            already_processed.append('default')
            outfile.write(u' default="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.default)), input_name='default'))
    def exportChildren(self, outfile, level, namespace_='', name_='qualityControlLevel'):
        if self.qualityControlLevelID is not None:
            showIndent(outfile, level)
            outfile.write(u'<%squalityControlLevelID>%s</%squalityControlLevelID>\n' % (namespace_, self.gds_format_string(quote_xml(self.qualityControlLevelID), input_name='qualityControlLevelID'), namespace_))
    def hasContent_(self):
        if (
            self.qualityControlLevelID is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='qualityControlLevel'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.metadataDateTime is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            showIndent(outfile, level)
            outfile.write(u'metadataDateTime = "%s",\n' % (self.metadataDateTime,))
        if self.network is not None and 'network' not in already_processed:
            already_processed.append('network')
            showIndent(outfile, level)
            outfile.write(u'network = "%s",\n' % (self.network,))
        if self.vocabulary is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            showIndent(outfile, level)
            outfile.write(u'vocabulary = "%s",\n' % (self.vocabulary,))
        if self.qualityControlLevelCode is not None and 'qualityControlLevelCode' not in already_processed:
            already_processed.append('qualityControlLevelCode')
            showIndent(outfile, level)
            outfile.write(u'qualityControlLevelCode = "%s",\n' % (self.qualityControlLevelCode,))
        if self.oid is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            showIndent(outfile, level)
            outfile.write(u'oid = "%s",\n' % (self.oid,))
        if self.default is not None and 'default' not in already_processed:
            already_processed.append('default')
            showIndent(outfile, level)
            outfile.write(u'default = %s,\n' % (self.default,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.qualityControlLevelID is not None:
            showIndent(outfile, level)
            outfile.write(u'qualityControlLevelID=%s,\n' % quote_python(self.qualityControlLevelID))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('metadataDateTime')
        if value is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            self.metadataDateTime = value
        value = attrs.get('network')
        if value is not None and 'network' not in already_processed:
            already_processed.append('network')
            self.network = value
        value = attrs.get('vocabulary')
        if value is not None and 'vocabulary' not in already_processed:
            already_processed.append('vocabulary')
            self.vocabulary = value
        value = attrs.get('qualityControlLevelCode')
        if value is not None and 'qualityControlLevelCode' not in already_processed:
            already_processed.append('qualityControlLevelCode')
            self.qualityControlLevelCode = value
        value = attrs.get('oid')
        if value is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            self.oid = value
        value = attrs.get('default')
        if value is not None and 'default' not in already_processed:
            already_processed.append('default')
            if value in ('true', '1'):
                self.default = True
            elif value in ('false', '0'):
                self.default = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'qualityControlLevelID':
            qualityControlLevelID_ = child_.text
            self.qualityControlLevelID = qualityControlLevelID_
# end class qualityControlLevel


class QualityControlLevelType(GeneratedsSuper):
    """Value is the text Code used to identify the level of quality control
    to which data values have been subjected.Integer identifier that
    indicates the level of quality control that the data values have
    been subjected to."""
    subclass = None
    superclass = None
    def __init__(self, qualityControlLevelID=None, valueOf_=None):
        self.qualityControlLevelID = _cast(int, qualityControlLevelID)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if QualityControlLevelType.subclass:
            return QualityControlLevelType.subclass(*args_, **kwargs_)
        else:
            return QualityControlLevelType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_qualityControlLevelID(self): return self.qualityControlLevelID
    def set_qualityControlLevelID(self, qualityControlLevelID): self.qualityControlLevelID = qualityControlLevelID
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='', name_='QualityControlLevelType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='QualityControlLevelType')
        if self.hasContent_():
            outfile.write(u'>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='QualityControlLevelType'):
        if self.qualityControlLevelID is not None and 'qualityControlLevelID' not in already_processed:
            already_processed.append('qualityControlLevelID')
            outfile.write(u' qualityControlLevelID="%s"' % self.gds_format_integer(self.qualityControlLevelID, input_name='qualityControlLevelID'))
    def exportChildren(self, outfile, level, namespace_='', name_='QualityControlLevelType'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='QualityControlLevelType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write(u'valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.qualityControlLevelID is not None and 'qualityControlLevelID' not in already_processed:
            already_processed.append('qualityControlLevelID')
            showIndent(outfile, level)
            outfile.write(u'qualityControlLevelID = %d,\n' % (self.qualityControlLevelID,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('qualityControlLevelID')
        if value is not None and 'qualityControlLevelID' not in already_processed:
            already_processed.append('qualityControlLevelID')
            try:
                self.qualityControlLevelID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        pass
# end class QualityControlLevelType


class UnitsType(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, UnitID=None, UnitName=None, UnitDescription=None, UnitType=None, UnitAbbreviation=None):
        self.UnitID = _cast(int, UnitID)
        self.UnitName = UnitName
        self.UnitDescription = UnitDescription
        self.UnitType = UnitType
        self.UnitAbbreviation = UnitAbbreviation
    def factory(*args_, **kwargs_):
        if UnitsType.subclass:
            return UnitsType.subclass(*args_, **kwargs_)
        else:
            return UnitsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_UnitName(self): return self.UnitName
    def set_UnitName(self, UnitName): self.UnitName = UnitName
    def get_UnitDescription(self): return self.UnitDescription
    def set_UnitDescription(self, UnitDescription): self.UnitDescription = UnitDescription
    def get_UnitType(self): return self.UnitType
    def set_UnitType(self, UnitType): self.UnitType = UnitType
    def validate_UnitType(self, value):
        # validate type UnitType
        pass
    def get_UnitAbbreviation(self): return self.UnitAbbreviation
    def set_UnitAbbreviation(self, UnitAbbreviation): self.UnitAbbreviation = UnitAbbreviation
    def get_UnitID(self): return self.UnitID
    def set_UnitID(self, UnitID): self.UnitID = UnitID
    def export(self, outfile, level, namespace_='', name_='UnitsType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='UnitsType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='UnitsType'):
        if self.UnitID is not None and 'UnitID' not in already_processed:
            already_processed.append('UnitID')
            outfile.write(u' UnitID="%s"' % self.gds_format_integer(self.UnitID, input_name='UnitID'))
    def exportChildren(self, outfile, level, namespace_='', name_='UnitsType'):
        if self.UnitName is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sUnitName>%s</%sUnitName>\n' % (namespace_, self.gds_format_string(quote_xml(self.UnitName), input_name='UnitName'), namespace_))
        if self.UnitDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sUnitDescription>%s</%sUnitDescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.UnitDescription), input_name='UnitDescription'), namespace_))
        if self.UnitType is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sUnitType>%s</%sUnitType>\n' % (namespace_, self.gds_format_string(quote_xml(self.UnitType), input_name='UnitType'), namespace_))
        if self.UnitAbbreviation is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sUnitAbbreviation>%s</%sUnitAbbreviation>\n' % (namespace_, self.gds_format_string(quote_xml(self.UnitAbbreviation), input_name='UnitAbbreviation'), namespace_))
    def hasContent_(self):
        if (
            self.UnitName is not None or
            self.UnitDescription is not None or
            self.UnitType is not None or
            self.UnitAbbreviation is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='UnitsType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.UnitID is not None and 'UnitID' not in already_processed:
            already_processed.append('UnitID')
            showIndent(outfile, level)
            outfile.write(u'UnitID = %d,\n' % (self.UnitID,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.UnitName is not None:
            showIndent(outfile, level)
            outfile.write(u'UnitName=%s,\n' % quote_python(self.UnitName))
        if self.UnitDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'UnitDescription=%s,\n' % quote_python(self.UnitDescription))
        if self.UnitType is not None:
            showIndent(outfile, level)
            outfile.write(u'UnitType=%s,\n' % quote_python(self.UnitType))
        if self.UnitAbbreviation is not None:
            showIndent(outfile, level)
            outfile.write(u'UnitAbbreviation=%s,\n' % quote_python(self.UnitAbbreviation))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('UnitID')
        if value is not None and 'UnitID' not in already_processed:
            already_processed.append('UnitID')
            try:
                self.UnitID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'UnitName':
            UnitName_ = child_.text
            self.UnitName = UnitName_
        elif nodeName_ == 'UnitDescription':
            UnitDescription_ = child_.text
            self.UnitDescription = UnitDescription_
        elif nodeName_ == 'UnitType':
            UnitType_ = child_.text
            self.UnitType = UnitType_
            self.validate_UnitType(self.UnitType)    # validate type UnitType
        elif nodeName_ == 'UnitAbbreviation':
            UnitAbbreviation_ = child_.text
            self.UnitAbbreviation = UnitAbbreviation_
# end class UnitsType


class MethodType(GeneratedsSuper):
    """Method used to collect the data and any additional information about
    the method. @methodId is the link to value/@method As per
    communication from the ODM designers, multiple instruments
    observing the same variable, should be different methods.
    Methods should describe the manner in which the observation was
    collected (i.e., collected manually, or collected using an
    automated sampler) or measured (i.e., measured using a
    temperature sensor or measured using a turbidity sensor).
    Details about the specific sensor models and manufacturers can
    be included in the MethodDescription"""
    subclass = None
    superclass = None
    def __init__(self, methodID=None, MethodDescription=None, MethodLink=None):
        self.methodID = _cast(int, methodID)
        self.MethodDescription = MethodDescription
        self.MethodLink = MethodLink
    def factory(*args_, **kwargs_):
        if MethodType.subclass:
            return MethodType.subclass(*args_, **kwargs_)
        else:
            return MethodType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_MethodDescription(self): return self.MethodDescription
    def set_MethodDescription(self, MethodDescription): self.MethodDescription = MethodDescription
    def get_MethodLink(self): return self.MethodLink
    def set_MethodLink(self, MethodLink): self.MethodLink = MethodLink
    def get_methodID(self): return self.methodID
    def set_methodID(self, methodID): self.methodID = methodID
    def export(self, outfile, level, namespace_='', name_='MethodType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='MethodType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='MethodType'):
        if self.methodID is not None and 'methodID' not in already_processed:
            already_processed.append('methodID')
            outfile.write(u' methodID="%s"' % self.gds_format_integer(self.methodID, input_name='methodID'))
    def exportChildren(self, outfile, level, namespace_='', name_='MethodType'):
        if self.MethodDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sMethodDescription>%s</%sMethodDescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.MethodDescription), input_name='MethodDescription'), namespace_))
        if self.MethodLink is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sMethodLink>%s</%sMethodLink>\n' % (namespace_, self.gds_format_string(quote_xml(self.MethodLink), input_name='MethodLink'), namespace_))
    def hasContent_(self):
        if (
            self.MethodDescription is not None or
            self.MethodLink is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='MethodType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.methodID is not None and 'methodID' not in already_processed:
            already_processed.append('methodID')
            showIndent(outfile, level)
            outfile.write(u'methodID = %d,\n' % (self.methodID,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.MethodDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'MethodDescription=%s,\n' % quote_python(self.MethodDescription))
        if self.MethodLink is not None:
            showIndent(outfile, level)
            outfile.write(u'MethodLink=%s,\n' % quote_python(self.MethodLink))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('methodID')
        if value is not None and 'methodID' not in already_processed:
            already_processed.append('methodID')
            try:
                self.methodID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'MethodDescription':
            MethodDescription_ = child_.text
            self.MethodDescription = MethodDescription_
        elif nodeName_ == 'MethodLink':
            MethodLink_ = child_.text
            self.MethodLink = MethodLink_
# end class MethodType


class SampleType(GeneratedsSuper):
    """information about physical samples analyzed in a laboratory.
    @sampleID is the link to the datavalues/@sampleID LabSampleCode
    is the sample code. In WaterML 1.1 this will be the link to the
    dataValue SampleType describes the the sample type LabMethod is
    a LabMethodType containing infomration about lab methods"""
    subclass = None
    superclass = None
    def __init__(self, sampleID=None, labSampleCode=None, SampleType=None, LabMethod=None):
        self.sampleID = _cast(int, sampleID)
        self.labSampleCode = labSampleCode
        self.SampleType = SampleType
        self.LabMethod = LabMethod
    def factory(*args_, **kwargs_):
        if SampleType.subclass:
            return SampleType.subclass(*args_, **kwargs_)
        else:
            return SampleType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_labSampleCode(self): return self.labSampleCode
    def set_labSampleCode(self, labSampleCode): self.labSampleCode = labSampleCode
    def get_SampleType(self): return self.SampleType
    def set_SampleType(self, SampleType): self.SampleType = SampleType
    def validate_SampleType(self, value):
        # validate type SampleType
        pass
    def get_LabMethod(self): return self.LabMethod
    def set_LabMethod(self, LabMethod): self.LabMethod = LabMethod
    def get_sampleID(self): return self.sampleID
    def set_sampleID(self, sampleID): self.sampleID = sampleID
    def export(self, outfile, level, namespace_='', name_='SampleType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='SampleType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='SampleType'):
        if self.sampleID is not None and 'sampleID' not in already_processed:
            already_processed.append('sampleID')
            outfile.write(u' sampleID="%s"' % self.gds_format_integer(self.sampleID, input_name='sampleID'))
    def exportChildren(self, outfile, level, namespace_='', name_='SampleType'):
        if self.labSampleCode is not None:
            showIndent(outfile, level)
            outfile.write(u'<%slabSampleCode>%s</%slabSampleCode>\n' % (namespace_, self.gds_format_string(quote_xml(self.labSampleCode), input_name='labSampleCode'), namespace_))
        if self.SampleType is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sSampleType>%s</%sSampleType>\n' % (namespace_, self.gds_format_string(quote_xml(self.SampleType), input_name='SampleType'), namespace_))
        if self.LabMethod:
            self.LabMethod.export(outfile, level, namespace_, name_='LabMethod')
    def hasContent_(self):
        if (
            self.labSampleCode is not None or
            self.SampleType is not None or
            self.LabMethod is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='SampleType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.sampleID is not None and 'sampleID' not in already_processed:
            already_processed.append('sampleID')
            showIndent(outfile, level)
            outfile.write(u'sampleID = %d,\n' % (self.sampleID,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.labSampleCode is not None:
            showIndent(outfile, level)
            outfile.write(u'labSampleCode=%s,\n' % quote_python(self.labSampleCode))
        if self.SampleType is not None:
            showIndent(outfile, level)
            outfile.write(u'SampleType=%s,\n' % quote_python(self.SampleType))
        if self.LabMethod is not None:
            showIndent(outfile, level)
            outfile.write(u'LabMethod=model_.LabMethodType(\n')
            self.LabMethod.exportLiteral(outfile, level, name_='LabMethod')
            showIndent(outfile, level)
            outfile.write(u'),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('sampleID')
        if value is not None and 'sampleID' not in already_processed:
            already_processed.append('sampleID')
            try:
                self.sampleID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'labSampleCode':
            labSampleCode_ = child_.text
            self.labSampleCode = labSampleCode_
        elif nodeName_ == 'SampleType':
            SampleType_ = child_.text
            self.SampleType = SampleType_
            self.validate_SampleType(self.SampleType)    # validate type SampleType
        elif nodeName_ == 'LabMethod': 
            obj_ = LabMethodType.factory()
            obj_.build(child_)
            self.set_LabMethod(obj_)
# end class SampleType


class LabMethodType(GeneratedsSuper):
    """contains descriptions of the laboratory methods used to analyze
    physical samples for specific constituents.Unique integer
    identifier for each laboratory method. This is the key used by
    the Samples table to reference a laboratory method."""
    subclass = None
    superclass = None
    def __init__(self, labMethodID=None, labName=None, labOrganization=None, LabMethodName=None, labMethodDescription=None, labMethodLink=None):
        self.labMethodID = _cast(int, labMethodID)
        self.labName = labName
        self.labOrganization = labOrganization
        self.LabMethodName = LabMethodName
        self.labMethodDescription = labMethodDescription
        self.labMethodLink = labMethodLink
    def factory(*args_, **kwargs_):
        if LabMethodType.subclass:
            return LabMethodType.subclass(*args_, **kwargs_)
        else:
            return LabMethodType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_labName(self): return self.labName
    def set_labName(self, labName): self.labName = labName
    def get_labOrganization(self): return self.labOrganization
    def set_labOrganization(self, labOrganization): self.labOrganization = labOrganization
    def get_LabMethodName(self): return self.LabMethodName
    def set_LabMethodName(self, LabMethodName): self.LabMethodName = LabMethodName
    def get_labMethodDescription(self): return self.labMethodDescription
    def set_labMethodDescription(self, labMethodDescription): self.labMethodDescription = labMethodDescription
    def get_labMethodLink(self): return self.labMethodLink
    def set_labMethodLink(self, labMethodLink): self.labMethodLink = labMethodLink
    def get_labMethodID(self): return self.labMethodID
    def set_labMethodID(self, labMethodID): self.labMethodID = labMethodID
    def export(self, outfile, level, namespace_='', name_='LabMethodType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='LabMethodType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='LabMethodType'):
        if self.labMethodID is not None and 'labMethodID' not in already_processed:
            already_processed.append('labMethodID')
            outfile.write(u' labMethodID="%s"' % self.gds_format_integer(self.labMethodID, input_name='labMethodID'))
    def exportChildren(self, outfile, level, namespace_='', name_='LabMethodType'):
        if self.labName is not None:
            showIndent(outfile, level)
            outfile.write(u'<%slabName>%s</%slabName>\n' % (namespace_, self.gds_format_string(quote_xml(self.labName), input_name='labName'), namespace_))
        if self.labOrganization is not None:
            showIndent(outfile, level)
            outfile.write(u'<%slabOrganization>%s</%slabOrganization>\n' % (namespace_, self.gds_format_string(quote_xml(self.labOrganization), input_name='labOrganization'), namespace_))
        if self.LabMethodName is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sLabMethodName>%s</%sLabMethodName>\n' % (namespace_, self.gds_format_string(quote_xml(self.LabMethodName), input_name='LabMethodName'), namespace_))
        if self.labMethodDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'<%slabMethodDescription>%s</%slabMethodDescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.labMethodDescription), input_name='labMethodDescription'), namespace_))
        if self.labMethodLink is not None:
            showIndent(outfile, level)
            outfile.write(u'<%slabMethodLink>%s</%slabMethodLink>\n' % (namespace_, self.gds_format_string(quote_xml(self.labMethodLink), input_name='labMethodLink'), namespace_))
    def hasContent_(self):
        if (
            self.labName is not None or
            self.labOrganization is not None or
            self.LabMethodName is not None or
            self.labMethodDescription is not None or
            self.labMethodLink is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='LabMethodType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.labMethodID is not None and 'labMethodID' not in already_processed:
            already_processed.append('labMethodID')
            showIndent(outfile, level)
            outfile.write(u'labMethodID = %d,\n' % (self.labMethodID,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.labName is not None:
            showIndent(outfile, level)
            outfile.write(u'labName=%s,\n' % quote_python(self.labName))
        if self.labOrganization is not None:
            showIndent(outfile, level)
            outfile.write(u'labOrganization=%s,\n' % quote_python(self.labOrganization))
        if self.LabMethodName is not None:
            showIndent(outfile, level)
            outfile.write(u'LabMethodName=%s,\n' % quote_python(self.LabMethodName))
        if self.labMethodDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'labMethodDescription=%s,\n' % quote_python(self.labMethodDescription))
        if self.labMethodLink is not None:
            showIndent(outfile, level)
            outfile.write(u'labMethodLink=%s,\n' % quote_python(self.labMethodLink))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('labMethodID')
        if value is not None and 'labMethodID' not in already_processed:
            already_processed.append('labMethodID')
            try:
                self.labMethodID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'labName':
            labName_ = child_.text
            self.labName = labName_
        elif nodeName_ == 'labOrganization':
            labOrganization_ = child_.text
            self.labOrganization = labOrganization_
        elif nodeName_ == 'LabMethodName':
            LabMethodName_ = child_.text
            self.LabMethodName = LabMethodName_
        elif nodeName_ == 'labMethodDescription':
            labMethodDescription_ = child_.text
            self.labMethodDescription = labMethodDescription_
        elif nodeName_ == 'labMethodLink':
            labMethodLink_ = child_.text
            self.labMethodLink = labMethodLink_
# end class LabMethodType


class SourceType(GeneratedsSuper):
    """original sources of the data, providing information sufficient to
    retrieve and reconstruct the data value from the original data
    files if necessaryUnique integer identifier that identifies each
    data source. link to datavalues/@sourceID"""
    subclass = None
    superclass = None
    def __init__(self, sourceID=None, Organization=None, SourceDescription=None, Metadata=None, ContactInformation=None, SourceLink=None):
        self.sourceID = _cast(int, sourceID)
        self.Organization = Organization
        self.SourceDescription = SourceDescription
        self.Metadata = Metadata
        self.ContactInformation = ContactInformation
        self.SourceLink = SourceLink
    def factory(*args_, **kwargs_):
        if SourceType.subclass:
            return SourceType.subclass(*args_, **kwargs_)
        else:
            return SourceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_Organization(self): return self.Organization
    def set_Organization(self, Organization): self.Organization = Organization
    def get_SourceDescription(self): return self.SourceDescription
    def set_SourceDescription(self, SourceDescription): self.SourceDescription = SourceDescription
    def get_Metadata(self): return self.Metadata
    def set_Metadata(self, Metadata): self.Metadata = Metadata
    def get_ContactInformation(self): return self.ContactInformation
    def set_ContactInformation(self, ContactInformation): self.ContactInformation = ContactInformation
    def get_SourceLink(self): return self.SourceLink
    def set_SourceLink(self, SourceLink): self.SourceLink = SourceLink
    def get_sourceID(self): return self.sourceID
    def set_sourceID(self, sourceID): self.sourceID = sourceID
    def export(self, outfile, level, namespace_='', name_='SourceType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='SourceType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='SourceType'):
        if self.sourceID is not None and 'sourceID' not in already_processed:
            already_processed.append('sourceID')
            outfile.write(u' sourceID="%s"' % self.gds_format_integer(self.sourceID, input_name='sourceID'))
    def exportChildren(self, outfile, level, namespace_='', name_='SourceType'):
        if self.Organization is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sOrganization>%s</%sOrganization>\n' % (namespace_, self.gds_format_string(quote_xml(self.Organization), input_name='Organization'), namespace_))
        if self.SourceDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sSourceDescription>%s</%sSourceDescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.SourceDescription), input_name='SourceDescription'), namespace_))
        if self.Metadata:
            self.Metadata.export(outfile, level, namespace_, name_='Metadata')
        if self.ContactInformation:
            self.ContactInformation.export(outfile, level, namespace_, name_='ContactInformation')
        if self.SourceLink is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sSourceLink>%s</%sSourceLink>\n' % (namespace_, self.gds_format_string(quote_xml(self.SourceLink), input_name='SourceLink'), namespace_))
    def hasContent_(self):
        if (
            self.Organization is not None or
            self.SourceDescription is not None or
            self.Metadata is not None or
            self.ContactInformation is not None or
            self.SourceLink is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='SourceType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.sourceID is not None and 'sourceID' not in already_processed:
            already_processed.append('sourceID')
            showIndent(outfile, level)
            outfile.write(u'sourceID = %d,\n' % (self.sourceID,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.Organization is not None:
            showIndent(outfile, level)
            outfile.write(u'Organization=%s,\n' % quote_python(self.Organization))
        if self.SourceDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'SourceDescription=%s,\n' % quote_python(self.SourceDescription))
        if self.Metadata is not None:
            showIndent(outfile, level)
            outfile.write(u'Metadata=model_.MetaDataType(\n')
            self.Metadata.exportLiteral(outfile, level, name_='Metadata')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.ContactInformation is not None:
            showIndent(outfile, level)
            outfile.write(u'ContactInformation=model_.ContactInformationType(\n')
            self.ContactInformation.exportLiteral(outfile, level, name_='ContactInformation')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.SourceLink is not None:
            showIndent(outfile, level)
            outfile.write(u'SourceLink=%s,\n' % quote_python(self.SourceLink))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('sourceID')
        if value is not None and 'sourceID' not in already_processed:
            already_processed.append('sourceID')
            try:
                self.sourceID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'Organization':
            Organization_ = child_.text
            self.Organization = Organization_
        elif nodeName_ == 'SourceDescription':
            SourceDescription_ = child_.text
            self.SourceDescription = SourceDescription_
        elif nodeName_ == 'Metadata': 
            obj_ = MetaDataType.factory()
            obj_.build(child_)
            self.set_Metadata(obj_)
        elif nodeName_ == 'ContactInformation': 
            obj_ = ContactInformationType.factory()
            obj_.build(child_)
            self.set_ContactInformation(obj_)
        elif nodeName_ == 'SourceLink':
            SourceLink_ = child_.text
            self.SourceLink = SourceLink_
# end class SourceType


class ContactInformationType(GeneratedsSuper):
    """Contains information about a contact. A contact can be a person or
    an agency. The name of the contact is required. And address,
    email or phone is suggested. (in 1.1 one of these will be
    required."""
    subclass = None
    superclass = None
    def __init__(self, ContactName=None, TypeOfContact=None, Phone=None, Email=None, Address=None):
        self.ContactName = ContactName
        self.TypeOfContact = TypeOfContact
        self.Phone = Phone
        self.Email = Email
        self.Address = Address
    def factory(*args_, **kwargs_):
        if ContactInformationType.subclass:
            return ContactInformationType.subclass(*args_, **kwargs_)
        else:
            return ContactInformationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ContactName(self): return self.ContactName
    def set_ContactName(self, ContactName): self.ContactName = ContactName
    def get_TypeOfContact(self): return self.TypeOfContact
    def set_TypeOfContact(self, TypeOfContact): self.TypeOfContact = TypeOfContact
    def get_Phone(self): return self.Phone
    def set_Phone(self, Phone): self.Phone = Phone
    def get_Email(self): return self.Email
    def set_Email(self, Email): self.Email = Email
    def get_Address(self): return self.Address
    def set_Address(self, Address): self.Address = Address
    def export(self, outfile, level, namespace_='', name_='ContactInformationType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='ContactInformationType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='ContactInformationType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='ContactInformationType'):
        if self.ContactName is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sContactName>%s</%sContactName>\n' % (namespace_, self.gds_format_string(quote_xml(self.ContactName), input_name='ContactName'), namespace_))
        if self.TypeOfContact is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sTypeOfContact>%s</%sTypeOfContact>\n' % (namespace_, self.gds_format_string(quote_xml(self.TypeOfContact), input_name='TypeOfContact'), namespace_))
        if self.Phone is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sPhone>%s</%sPhone>\n' % (namespace_, self.gds_format_string(quote_xml(self.Phone), input_name='Phone'), namespace_))
        if self.Email is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sEmail>%s</%sEmail>\n' % (namespace_, self.gds_format_string(quote_xml(self.Email), input_name='Email'), namespace_))
        if self.Address is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sAddress>%s</%sAddress>\n' % (namespace_, self.gds_format_string(quote_xml(self.Address), input_name='Address'), namespace_))
    def hasContent_(self):
        if (
            self.ContactName is not None or
            self.TypeOfContact is not None or
            self.Phone is not None or
            self.Email is not None or
            self.Address is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='ContactInformationType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.ContactName is not None:
            showIndent(outfile, level)
            outfile.write(u'ContactName=%s,\n' % quote_python(self.ContactName))
        if self.TypeOfContact is not None:
            showIndent(outfile, level)
            outfile.write(u'TypeOfContact=%s,\n' % quote_python(self.TypeOfContact))
        if self.Phone is not None:
            showIndent(outfile, level)
            outfile.write(u'Phone=%s,\n' % quote_python(self.Phone))
        if self.Email is not None:
            showIndent(outfile, level)
            outfile.write(u'Email=%s,\n' % quote_python(self.Email))
        if self.Address is not None:
            showIndent(outfile, level)
            outfile.write(u'Address=%s,\n' % quote_python(self.Address))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'ContactName':
            ContactName_ = child_.text
            self.ContactName = ContactName_
        elif nodeName_ == 'TypeOfContact':
            TypeOfContact_ = child_.text
            self.TypeOfContact = TypeOfContact_
        elif nodeName_ == 'Phone':
            Phone_ = child_.text
            self.Phone = Phone_
        elif nodeName_ == 'Email':
            Email_ = child_.text
            self.Email = Email_
        elif nodeName_ == 'Address':
            Address_ = child_.text
            self.Address = Address_
# end class ContactInformationType


class MetaDataType(GeneratedsSuper):
    """MetadataType contains the information from the ODM table
    IsoMetadata. It is anticpated that many data sources may not
    have this fully available. IsoMetadata table contains dataset
    and project level metadata required by the CUAHSI HIS metadata
    system (http://www.cuahsi.org/his/documentation.html) for
    compliance with standards such as the draft ISO 19115 or ISO
    8601. The mandatory fields in this table must be populated to
    provide a complete set of ISO compliant metadata in the
    database."""
    subclass = None
    superclass = None
    def __init__(self, TopicCategory=None, Title=None, Abstract=None, ProfileVersion=None, MetadataLink=None):
        self.TopicCategory = TopicCategory
        self.Title = Title
        self.Abstract = Abstract
        self.ProfileVersion = ProfileVersion
        self.MetadataLink = MetadataLink
    def factory(*args_, **kwargs_):
        if MetaDataType.subclass:
            return MetaDataType.subclass(*args_, **kwargs_)
        else:
            return MetaDataType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_TopicCategory(self): return self.TopicCategory
    def set_TopicCategory(self, TopicCategory): self.TopicCategory = TopicCategory
    def get_Title(self): return self.Title
    def set_Title(self, Title): self.Title = Title
    def get_Abstract(self): return self.Abstract
    def set_Abstract(self, Abstract): self.Abstract = Abstract
    def get_ProfileVersion(self): return self.ProfileVersion
    def set_ProfileVersion(self, ProfileVersion): self.ProfileVersion = ProfileVersion
    def get_MetadataLink(self): return self.MetadataLink
    def set_MetadataLink(self, MetadataLink): self.MetadataLink = MetadataLink
    def export(self, outfile, level, namespace_='', name_='MetaDataType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='MetaDataType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='MetaDataType'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='MetaDataType'):
        if self.TopicCategory is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sTopicCategory>%s</%sTopicCategory>\n' % (namespace_, self.gds_format_string(quote_xml(self.TopicCategory), input_name='TopicCategory'), namespace_))
        if self.Title is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sTitle>%s</%sTitle>\n' % (namespace_, self.gds_format_string(quote_xml(self.Title), input_name='Title'), namespace_))
        if self.Abstract is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sAbstract>%s</%sAbstract>\n' % (namespace_, self.gds_format_string(quote_xml(self.Abstract), input_name='Abstract'), namespace_))
        if self.ProfileVersion is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sProfileVersion>%s</%sProfileVersion>\n' % (namespace_, self.gds_format_string(quote_xml(self.ProfileVersion), input_name='ProfileVersion'), namespace_))
        if self.MetadataLink is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sMetadataLink>%s</%sMetadataLink>\n' % (namespace_, self.gds_format_string(quote_xml(self.MetadataLink), input_name='MetadataLink'), namespace_))
    def hasContent_(self):
        if (
            self.TopicCategory is not None or
            self.Title is not None or
            self.Abstract is not None or
            self.ProfileVersion is not None or
            self.MetadataLink is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='MetaDataType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.TopicCategory is not None:
            showIndent(outfile, level)
            outfile.write(u'TopicCategory=%s,\n' % quote_python(self.TopicCategory))
        if self.Title is not None:
            showIndent(outfile, level)
            outfile.write(u'Title=%s,\n' % quote_python(self.Title))
        if self.Abstract is not None:
            showIndent(outfile, level)
            outfile.write(u'Abstract=%s,\n' % quote_python(self.Abstract))
        if self.ProfileVersion is not None:
            showIndent(outfile, level)
            outfile.write(u'ProfileVersion=%s,\n' % quote_python(self.ProfileVersion))
        if self.MetadataLink is not None:
            showIndent(outfile, level)
            outfile.write(u'MetadataLink=%s,\n' % quote_python(self.MetadataLink))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'TopicCategory':
            TopicCategory_ = child_.text
            self.TopicCategory = TopicCategory_
        elif nodeName_ == 'Title':
            Title_ = child_.text
            self.Title = Title_
        elif nodeName_ == 'Abstract':
            Abstract_ = child_.text
            self.Abstract = Abstract_
        elif nodeName_ == 'ProfileVersion':
            ProfileVersion_ = child_.text
            self.ProfileVersion = ProfileVersion_
        elif nodeName_ == 'MetadataLink':
            MetadataLink_ = child_.text
            self.MetadataLink = MetadataLink_
# end class MetaDataType


class OffsetType(GeneratedsSuper):
    """OffsetType contains full descriptive information for each of the
    measurement offsets. A set of observations may be done at an
    offset for the central location. offsetTypeID links to
    dataValue/@offsetTypeIdUnique integer identifier that identifies
    the type of measurement offset. Suggested that this is
    offsetType from ODM database."""
    subclass = None
    superclass = None
    def __init__(self, offsetTypeID=None, offsetValue=None, offsetDescription=None, units=None, offsetIsVertical='true', offsetHorizDirectionDegrees=None):
        self.offsetTypeID = _cast(int, offsetTypeID)
        self.offsetValue = offsetValue
        self.offsetDescription = offsetDescription
        self.units = units
        self.offsetIsVertical = offsetIsVertical
        self.offsetHorizDirectionDegrees = offsetHorizDirectionDegrees
    def factory(*args_, **kwargs_):
        if OffsetType.subclass:
            return OffsetType.subclass(*args_, **kwargs_)
        else:
            return OffsetType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_offsetValue(self): return self.offsetValue
    def set_offsetValue(self, offsetValue): self.offsetValue = offsetValue
    def get_offsetDescription(self): return self.offsetDescription
    def set_offsetDescription(self, offsetDescription): self.offsetDescription = offsetDescription
    def get_units(self): return self.units
    def set_units(self, units): self.units = units
    def get_offsetIsVertical(self): return self.offsetIsVertical
    def set_offsetIsVertical(self, offsetIsVertical): self.offsetIsVertical = offsetIsVertical
    def get_offsetHorizDirectionDegrees(self): return self.offsetHorizDirectionDegrees
    def set_offsetHorizDirectionDegrees(self, offsetHorizDirectionDegrees): self.offsetHorizDirectionDegrees = offsetHorizDirectionDegrees
    def get_offsetTypeID(self): return self.offsetTypeID
    def set_offsetTypeID(self, offsetTypeID): self.offsetTypeID = offsetTypeID
    def export(self, outfile, level, namespace_='', name_='OffsetType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='OffsetType')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='OffsetType'):
        if self.offsetTypeID is not None and 'offsetTypeID' not in already_processed:
            already_processed.append('offsetTypeID')
            outfile.write(u' offsetTypeID="%s"' % self.gds_format_integer(self.offsetTypeID, input_name='offsetTypeID'))
    def exportChildren(self, outfile, level, namespace_='', name_='OffsetType'):
        if self.offsetValue is not None:
            showIndent(outfile, level)
            outfile.write(u'<%soffsetValue>%s</%soffsetValue>\n' % (namespace_, self.gds_format_string(quote_xml(self.offsetValue), input_name='offsetValue'), namespace_))
        if self.offsetDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'<%soffsetDescription>%s</%soffsetDescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.offsetDescription), input_name='offsetDescription'), namespace_))
        if self.units:
            self.units.export(outfile, level, namespace_, name_='units', )
        if self.offsetIsVertical is not None:
            showIndent(outfile, level)
            outfile.write(u'<%soffsetIsVertical>%s</%soffsetIsVertical>\n' % (namespace_, self.gds_format_string(quote_xml(self.offsetIsVertical), input_name='offsetIsVertical'), namespace_))
        if self.offsetHorizDirectionDegrees is not None:
            showIndent(outfile, level)
            outfile.write(u'<%soffsetHorizDirectionDegrees>%s</%soffsetHorizDirectionDegrees>\n' % (namespace_, self.gds_format_string(quote_xml(self.offsetHorizDirectionDegrees), input_name='offsetHorizDirectionDegrees'), namespace_))
    def hasContent_(self):
        if (
            self.offsetValue is not None or
            self.offsetDescription is not None or
            self.units is not None or
            self.offsetIsVertical is not None or
            self.offsetHorizDirectionDegrees is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='OffsetType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.offsetTypeID is not None and 'offsetTypeID' not in already_processed:
            already_processed.append('offsetTypeID')
            showIndent(outfile, level)
            outfile.write(u'offsetTypeID = %d,\n' % (self.offsetTypeID,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.offsetValue is not None:
            showIndent(outfile, level)
            outfile.write(u'offsetValue=%s,\n' % quote_python(self.offsetValue))
        if self.offsetDescription is not None:
            showIndent(outfile, level)
            outfile.write(u'offsetDescription=%s,\n' % quote_python(self.offsetDescription))
        if self.units is not None:
            showIndent(outfile, level)
            outfile.write(u'units=model_.units(\n')
            self.units.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.offsetIsVertical is not None:
            showIndent(outfile, level)
            outfile.write(u'offsetIsVertical=%s,\n' % quote_python(self.offsetIsVertical))
        if self.offsetHorizDirectionDegrees is not None:
            showIndent(outfile, level)
            outfile.write(u'offsetHorizDirectionDegrees=%s,\n' % quote_python(self.offsetHorizDirectionDegrees))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('offsetTypeID')
        if value is not None and 'offsetTypeID' not in already_processed:
            already_processed.append('offsetTypeID')
            try:
                self.offsetTypeID = int(value)
            except ValueError, exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'offsetValue':
            offsetValue_ = child_.text
            self.offsetValue = offsetValue_
        elif nodeName_ == 'offsetDescription':
            offsetDescription_ = child_.text
            self.offsetDescription = offsetDescription_
        elif nodeName_ == 'units': 
            obj_ = units.factory()
            obj_.build(child_)
            self.set_units(obj_)
        elif nodeName_ == 'offsetIsVertical':
            offsetIsVertical_ = child_.text
            self.offsetIsVertical = offsetIsVertical_
        elif nodeName_ == 'offsetHorizDirectionDegrees':
            offsetHorizDirectionDegrees_ = child_.text
            self.offsetHorizDirectionDegrees = offsetHorizDirectionDegrees_
# end class OffsetType


class SiteInfoType(SourceInfoType):
    """A sampling station is any place where data are collected.
    SiteInfoType is the Element that for the core information about
    a point sampling location. The core information includes
    SiteName, SiteCode(s), location, elevation, timeZone information
    and note(s). SiteInfoType is <siteInfo> in a <site> of a
    <sitesResponse>. It is derived from SourceType so that other
    geographic location descriptions can be utilized in the
    <sourceInfo> of the <timeSeriesResponse>"""
    subclass = None
    superclass = SourceInfoType
    def __init__(self, metadataDateTime=None, oid=None, siteName=None, siteCode=None, timeZoneInfo=None, geoLocation=None, elevation_m=None, verticalDatum=None, note=None, extension=None, altname=None):
        super(SiteInfoType, self).__init__()
        self.metadataDateTime = _cast(None, metadataDateTime)
        self.oid = _cast(None, oid)
        self.siteName = siteName
        if siteCode is None:
            self.siteCode = []
        else:
            self.siteCode = siteCode
        self.timeZoneInfo = timeZoneInfo
        self.geoLocation = geoLocation
        self.elevation_m = elevation_m
        self.verticalDatum = verticalDatum
        if note is None:
            self.note = []
        else:
            self.note = note
        self.extension = extension
        self.altname = altname
    def factory(*args_, **kwargs_):
        if SiteInfoType.subclass:
            return SiteInfoType.subclass(*args_, **kwargs_)
        else:
            return SiteInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_siteName(self): return self.siteName
    def set_siteName(self, siteName): self.siteName = siteName
    def get_siteCode(self): return self.siteCode
    def set_siteCode(self, siteCode): self.siteCode = siteCode
    def add_siteCode(self, value): self.siteCode.append(value)
    def insert_siteCode(self, index, value): self.siteCode[index] = value
    def get_timeZoneInfo(self): return self.timeZoneInfo
    def set_timeZoneInfo(self, timeZoneInfo): self.timeZoneInfo = timeZoneInfo
    def get_geoLocation(self): return self.geoLocation
    def set_geoLocation(self, geoLocation): self.geoLocation = geoLocation
    def get_elevation_m(self): return self.elevation_m
    def set_elevation_m(self, elevation_m): self.elevation_m = elevation_m
    def get_verticalDatum(self): return self.verticalDatum
    def set_verticalDatum(self, verticalDatum): self.verticalDatum = verticalDatum
    def get_note(self): return self.note
    def set_note(self, note): self.note = note
    def add_note(self, value): self.note.append(value)
    def insert_note(self, index, value): self.note[index] = value
    def get_extension(self): return self.extension
    def set_extension(self, extension): self.extension = extension
    def get_altname(self): return self.altname
    def set_altname(self, altname): self.altname = altname
    def get_metadataDateTime(self): return self.metadataDateTime
    def set_metadataDateTime(self, metadataDateTime): self.metadataDateTime = metadataDateTime
    def get_oid(self): return self.oid
    def set_oid(self, oid): self.oid = oid
    def export(self, outfile, level, namespace_='', name_='SiteInfoType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write(u'<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='SiteInfoType')
        outfile.write(u' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(u' xsi:type="SiteInfoType"')
        if self.hasContent_():
            outfile.write(u'>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write(u'</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write(u'/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='SiteInfoType'):
        super(SiteInfoType, self).exportAttributes(outfile, level, already_processed, namespace_, name_='SiteInfoType')
        if self.metadataDateTime is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            outfile.write(u' metadataDateTime=%s' % (self.gds_format_string(quote_attrib(self.metadataDateTime), input_name='metadataDateTime'), ))
        if self.oid is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            outfile.write(u' oid=%s' % (self.gds_format_string(quote_attrib(self.oid), input_name='oid'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='SiteInfoType'):
        super(SiteInfoType, self).exportChildren(outfile, level, namespace_, name_)
        if self.siteName is not None:
            showIndent(outfile, level)
            outfile.write(u'<%ssiteName>%s</%ssiteName>\n' % (namespace_, self.gds_format_string(quote_xml(self.siteName), input_name='siteName'), namespace_))
        for siteCode_ in self.siteCode:
            siteCode_.export(outfile, level, namespace_, name_='siteCode')
        if self.timeZoneInfo:
            self.timeZoneInfo.export(outfile, level, namespace_, name_='timeZoneInfo')
        if self.geoLocation:
            self.geoLocation.export(outfile, level, namespace_, name_='geoLocation')
        if self.elevation_m is not None:
            showIndent(outfile, level)
            outfile.write(u'<%selevation_m>%s</%selevation_m>\n' % (namespace_, self.gds_format_string(quote_xml(self.elevation_m), input_name='elevation_m'), namespace_))
        if self.verticalDatum is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sverticalDatum>%s</%sverticalDatum>\n' % (namespace_, self.gds_format_string(quote_xml(self.verticalDatum), input_name='verticalDatum'), namespace_))
        for note_ in self.note:
            note_.export(outfile, level, namespace_, name_='note')
        if self.extension is not None:
            showIndent(outfile, level)
            outfile.write(u'<%sextension>%s</%sextension>\n' % (namespace_, self.gds_format_string(quote_xml(self.extension), input_name='extension'), namespace_))
        if self.altname is not None:
            showIndent(outfile, level)
            outfile.write(u'<%saltname>%s</%saltname>\n' % (namespace_, self.gds_format_string(quote_xml(self.altname), input_name='altname'), namespace_))
    def hasContent_(self):
        if (
            self.siteName is not None or
            self.siteCode or
            self.timeZoneInfo is not None or
            self.geoLocation is not None or
            self.elevation_m is not None or
            self.verticalDatum is not None or
            self.note or
            self.extension is not None or
            self.altname is not None or
            super(SiteInfoType, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='SiteInfoType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.metadataDateTime is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            showIndent(outfile, level)
            outfile.write(u'metadataDateTime = "%s",\n' % (self.metadataDateTime,))
        if self.oid is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            showIndent(outfile, level)
            outfile.write(u'oid = "%s",\n' % (self.oid,))
        super(SiteInfoType, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(SiteInfoType, self).exportLiteralChildren(outfile, level, name_)
        if self.siteName is not None:
            showIndent(outfile, level)
            outfile.write(u'siteName=%s,\n' % quote_python(self.siteName))
        showIndent(outfile, level)
        outfile.write(u'siteCode=[\n')
        level += 1
        for siteCode_ in self.siteCode:
            showIndent(outfile, level)
            outfile.write(u'model_.siteCode(\n')
            siteCode_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        if self.timeZoneInfo is not None:
            showIndent(outfile, level)
            outfile.write(u'timeZoneInfo=model_.timeZoneInfo(\n')
            self.timeZoneInfo.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.geoLocation is not None:
            showIndent(outfile, level)
            outfile.write(u'geoLocation=model_.geoLocation(\n')
            self.geoLocation.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write(u'),\n')
        if self.elevation_m is not None:
            showIndent(outfile, level)
            outfile.write(u'elevation_m=%s,\n' % quote_python(self.elevation_m))
        if self.verticalDatum is not None:
            showIndent(outfile, level)
            outfile.write(u'verticalDatum=%s,\n' % quote_python(self.verticalDatum))
        showIndent(outfile, level)
        outfile.write(u'note=[\n')
        level += 1
        for note_ in self.note:
            showIndent(outfile, level)
            outfile.write(u'model_.NoteType(\n')
            note_.exportLiteral(outfile, level, name_='NoteType')
            showIndent(outfile, level)
            outfile.write(u'),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write(u'],\n')
        if self.extension is not None:
            showIndent(outfile, level)
            outfile.write(u'extension=%s,\n' % quote_python(self.extension))
        if self.altname is not None:
            showIndent(outfile, level)
            outfile.write(u'altname=%s,\n' % quote_python(self.altname))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('metadataDateTime')
        if value is not None and 'metadataDateTime' not in already_processed:
            already_processed.append('metadataDateTime')
            self.metadataDateTime = value
        value = attrs.get('oid')
        if value is not None and 'oid' not in already_processed:
            already_processed.append('oid')
            self.oid = value
        super(SiteInfoType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, nodeName_, from_subclass=False):
        if nodeName_ == 'siteName':
            siteName_ = child_.text
            self.siteName = siteName_
        elif nodeName_ == 'siteCode': 
            obj_ = siteCode.factory()
            obj_.build(child_)
            self.siteCode.append(obj_)
        elif nodeName_ == 'timeZoneInfo': 
            obj_ = timeZoneInfo.factory()
            obj_.build(child_)
            self.set_timeZoneInfo(obj_)
        elif nodeName_ == 'geoLocation': 
            obj_ = geoLocation.factory()
            obj_.build(child_)
            self.set_geoLocation(obj_)
        elif nodeName_ == 'elevation_m':
            elevation_m_ = child_.text
            self.elevation_m = elevation_m_
        elif nodeName_ == 'verticalDatum':
            verticalDatum_ = child_.text
            self.verticalDatum = verticalDatum_
        elif nodeName_ == 'note': 
            obj_ = NoteType.factory()
            obj_.build(child_)
            self.note.append(obj_)
        elif nodeName_ == 'extension':
            extension_ = child_.text
            self.extension = extension_
        elif nodeName_ == 'altname':
            altname_ = child_.text
            self.altname = altname_
        super(SiteInfoType, self).buildChildren(child_, nodeName_, True)
# end class SiteInfoType




def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = globals().get(tag)
    return tag, rootClass


__all__ = [
    "ContactInformationType",
    "DataSetInfoType",
    "DocumentationType",
    "GeogLocationType",
    "LabMethodType",
    "LatLonBoxType",
    "LatLonPointType",
    "MetaDataType",
    "MethodType",
    "NoteType",
    "OffsetType",
    "QualifiersType",
    "QualityControlLevelType",
    "QueryInfoType",
    "SampleType",
    "SiteInfoResponseType",
    "SiteInfoType",
    "SourceInfoType",
    "SourceType",
    "TimeIntervalType",
    "TimePeriodRealTimeType",
    "TimePeriodType",
    "TimeSeriesResponseType",
    "TimeSeriesType",
    "TimeSingleType",
    "TsValuesSingleVariableType",
    "UnitsType",
    "ValueSingleVariable",
    "VariableInfoType",
    "VariablesResponseType",
    "criteria",
    "daylightSavingsTimeZone",
    "defaultTimeZone",
    "geoLocation",
    "localSiteXY",
    "option",
    "optionGroup",
    "options",
    "parentID",
    "qualifier",
    "qualityControlLevel",
    "related",
    "relatedID",
    "series",
    "seriesCatalogType",
    "site",
    "siteCode",
    "timeParam",
    "timeSupport",
    "timeZoneInfo",
    "units",
    "valueCount",
    "variableCode",
    "variables"
    ]
