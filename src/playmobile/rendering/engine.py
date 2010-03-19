from zope.interface import implements
from zope.component import getUtility
from chameleon.zpt.template import PageTemplateFile

from playmobile.interfaces.rendering import IRenderingEngine
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


