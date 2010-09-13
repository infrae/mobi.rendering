# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt.
from zope.interface import implements
from mobi.interfaces.rendering import IResource, IHTMLTagResource


class Resource(object):
    implements(IResource)

    name = ''

    def __eq__(self, other):
        if not isinstance(other, Resource):
            return False
        return self.name == other.name


class HTMLTagResource(Resource):
    implements(IHTMLTagResource)

    name = ''
    attributes = {}
    default_attributes = {}
    content = ""
    autoclose = True

    def __init__(self, name, content='', autoclose=True, **attributes):
        self.name = name
        self.content = content
        self.autoclose = autoclose
        self.attributes = self.default_attributes.copy()
        self.attributes.update(attributes)

    def __eq__(self, other):
        if not isinstance(other, HTMLTagResource):
            return False
        return self.name == other.name and \
               self.attributes == other.attributes and \
               self.content == other.content

    def __call__(self):
        autoclose = not self.content and self.autoclose
        attributes_html = " ".join(
            ['%s="%s"' % (name, value,)
                for (name, value,) in self.attributes.iteritems()])
        if autoclose:
            return "<%s %s />" % (self.name, attributes_html,)
        else:
            return "<%s %s>%s</%s>" % (self.name,
                                     attributes_html,
                                     self.content,
                                     self.name)


class CSS(HTMLTagResource):

    name = 'link'
    default_attributes = {'rel': 'stylesheet', 'type': 'text/css',
        'media': 'all'}

    def __init__(self, href, **attributes):
        attributes['href'] = href
        super(CSS, self).__init__(self.name, content='',
            autoclose=True, **attributes)


class JS(HTMLTagResource):
    name = 'script'
    default_attributes = {'type': 'text/javascript'}

    def __init__(self, src, **attributes):
        attributes['src'] = src
        super(JS, self).__init__(self.name, content='',
            autoclose=False, **attributes)


