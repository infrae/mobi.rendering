from playmobile.interfaces.rendering import IRenderingEngine
from playmobile.interfaces.devices import IDeviceType
from playmobile.caching import Cache, NoCacheBackend
from zope.interface import implements, providedBy
from chameleon.zpt.template import PageTemplateFile
import os.path

cache_engine = Cache(namespace='playmobile.rendering')
cache = cache_engine.cache

class TemplateLookupError(Exception): pass


def get_class_name(instance):
    return instance.__class__.__name__


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

    def render_widget(self, widget, request, name='index'):
        def lookup_template():
            return self.lookup_template(widget, name)
        template = cache('lookup:%s-%s' % (get_class_name(widget), name),
            lookup_template)
        if template is None:
            raise TemplateLookupError, "no template found for name %s" % name
        def load_template():
            return PageTemplateFile(template)
        page_template = cache('template:%s' % template, load_template)
        return page_template.render(**widget._template_locals())


