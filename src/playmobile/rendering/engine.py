from playmobile.interfaces.rendering import IRenderingEngine
from playmobile.interfaces.devices import IDeviceType
from playmobileaddressbook.cache import cache
from zope.interface import implements, providedBy
from chameleon.zpt.template import PageTemplateFile
import os.path


class TemplateLookupError(Exception): pass


def get_class_name(instance):
    return instance.__class__.__name__


class TemplateEngine(object):
    implements(IRenderingEngine)
    name = 'default_skin'
    base_path = None

    def lookup_template(self, widget, name):
        template_path = self.get_template_path(widget, name)
        if os.path.exists(template_path):
            return template_path
        template_path = None
        parent = super(TemplateEngine, self)
        if IRenderingEngine.providedBy(parent):
            template_path = parent.lookup_template(widget, name)
        return template_path

    def get_template_path(self, widget, name):
        widget_name = get_class_name(widget)
        return os.path.join(self.get_base_path(), widget_name, '%s.pt' % name)

    def get_base_path(self):
        if self.base_path:
            return self.base_path
        return os.path.join(os.path.os.path.dirname(__file__), self.name)

    def render_widget(self, widget, request, name='index'):
        template = self.lookup_template(widget, name)
        if template is None:
            raise TemplateLookupError, "no template found for name %s" % name
        def load_template():
            return PageTemplateFile(template)
        page_template = cache('template:%s' % template, load_template)
        page_template.render(**widget._template_locals())


