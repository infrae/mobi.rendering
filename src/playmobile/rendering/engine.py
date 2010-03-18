from zope.interface import implements
from zope.component import getUtility
from chameleon.zpt.template import PageTemplateFile

from playmobile.interfaces.rendering import IRenderingEngine
from playmobile.interfaces.rendering import IResource, IHTMLTagResource
from playmobile.caching import Cache

import os.path
import sys

cache_engine = Cache(namespace='playmobile.rendering')
cache = cache_engine.cache


class TemplateLookupError(Exception): pass


def get_class_name(instance):
    return instance.__class__.__name__

def module_base_path(obj):
    return os.path.dirname(sys.modules[obj.__class__.__module__].__file__)


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
        autoclose = self.content and False or self.autoclose
        attributes_html = " ".join(
            ['%s="%s"' % (name, value,)
                for (name, value,) in self.attributes.iteritems()])
        if autoclose:
            return "<%s %s />" % (self.name, attributes_html,)
        else:
            return "<%s %s>%s</%s>" (self.name,
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
        super(CSS, self).__init__(self.name, content='',
            autoclose=False, **attributes)


class TemplateEngine(object):
    implements(IRenderingEngine)
    name = 'default_skin'
    search_path = [os.path.join(os.path.os.path.dirname(__file__), name)]

    def lookup_template(self, widget, name):
        template_paths = self.get_template_paths(widget, name)
        for path in template_paths:
            if os.path.exists(path):
                return path
        raise TemplateLookupError('No template found in %s' %
            repr(template_paths))

    def get_template_paths(self, widget, name):
        widget_name = get_class_name(widget)
        return [os.path.join(path, widget_name, '%s.pt') % name
            for path in self.search_path]

    def render_widget(self, widget, name='index'):
        if hasattr(widget, 'template'):
            template = getattr(widget, 'template')
            if not template.startswith('/'):
                template = os.path.join(module_base_path(widget),
                    'templates', template)
        else:
            def lookup_template():
                return self.lookup_template(widget, name)
            template = cache('lookup:%s-%s' % (get_class_name(widget), name),
                lookup_template)
            if template is None:
                raise TemplateLookupError(
                    "no template found for name %s" % name)
        def load_template():
            return PageTemplateFile(template)
        page_template = cache('template:%s' % template, load_template)
        return page_template.render(**widget._template_locals())


def render_widget(widget):
    widget.update()
    if hasattr(widget, 'render'):
        return widget.render()
    render_engine = getUtility(IRenderingEngine)
    return render_engine.render_widget(widget)


