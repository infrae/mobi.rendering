from zope.interface import implements
from zope.component import adapts, getMultiAdapter, getUtility
from zope.schema.interfaces import IField, IURI

from playmobile.interfaces.devices import (IBasicDeviceType,
    IStandardDeviceType, IAdvancedDeviceType,)
from playmobile.interfaces.rendering import (IWidget, IFieldWidget, IPage,
    IRenderingEngine)
from playmobile.interfaces.schema import IPhoneNumber, IAddress
from playmobile.rendering.engine import render_widget

import urllib


# TODO
# ----
# 
#  - widget should not render itself it should get rendered (IRenderingEngine)
#  - add ability for a widget to register some css and js into the header
#


class Widget(object):
    """ If their is not implementation of content type
    or device, return context as unicode text
    """
    implements(IWidget)
    adapts(None, None, None)

    page = None

    def __init__(self, context, parent_widget, request):
        self.context = context
        self.request = request
        self.parent = parent_widget
        if IPage.providedBy(parent_widget):
            self.page = parent_widget
        else:
            self.page = parent_widget.page

    def update(self):
        pass

    def _template_locals(self):
        return {'context': self.context,
                'request': self.request,
                'view': self}


class Page(Widget):
    """ Page adapts context and request without parent because it has none
    """

    implements(IPage)
    adapts(None, None)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.parent = None
        self.content = ''
        self.facilities = {'head'  : list()}

    def update(self):
        pass

    def register_resource(self, resource, facility='head'):
        l = self.facilities[facility]
        if resource not in l:
            l.append(resource)
        return resource

    def _template_locals(self):
        return {'content': self.content,
                'context': self.context,
                'request': self.request,
                'view': self}

    def render_resources(self, facility='head'):
        return "\n".join([i() for i in self.facilities[facility]])

    def render(self):
        render_engine = getUtility(IRenderingEngine)
        main_widget = \
            getMultiAdapter((self.context, self, self.request,), IWidget)
        main_widget.update()
        self.content = render_engine.render_widget(main_widget)
        return render_engine.render_widget(self)


class FieldWidget(Widget):
    implements(IFieldWidget)
    adapts(IField, None, None)

    def _template_locals(self):
        tlocals = super(FieldWidget, self)._template_locals()
        tlocals.update({'value': self.get_value()})
        return tlocals

    def get_value(self):
        return self.context.get(self.parent.context)


class BasicPhoneNumberWidget(FieldWidget):
    adapts(IPhoneNumber, None, IBasicDeviceType)

    def render(self):
        return unicode(self.get_value())


class AdvancedPhoneNumberWidget(FieldWidget):
    adapts(IPhoneNumber, None , IAdvancedDeviceType)

    def render(self):
        return u'<a href="tel:%s" class="phone"></a>' % (self.get_value(), self.get_value())


class BasicAddressWidget(Widget):
    adapts(IAddress, None, IBasicDeviceType)


class GMWidget(Widget):
    """ Google map widget
    """

    API_KEY = "ABQIAAAAIt9s0bdfR5Od4DreqvmckxS7QSeUpOtCYzRjfvthYEaCVh0HbhQAvIJtRk-ZGzltUZRngBeyJoCWBQ"

    def _template_locals(self):
        tlocals = super(GMWidget, self)._template_locals()
        tlocals.update({'quoted_gm_address': self.get_quoted_gm_address(),
            'gm_address': self.get_gm_address(),
            'api_key': self.API_KEY})
        return tlocals

    def get_gm_address(self):
        address = self.context
        return ",".join([address.street, address.postal_code,
            address.city, address.country])

    def get_quoted_gm_address(self):
        return urllib.quote(self.get_gm_address())


class StaticGoogleMapWidget(GMWidget):
    adapts(IAddress, None, IStandardDeviceType)


class GoogleMapWidget(GMWidget):
    adapts(IAddress, None, IAdvancedDeviceType)


class NullImageURLWidget(FieldWidget):
    adapts(IURI, None, IBasicDeviceType)
    def render(self):
        return ''


class ImageURLWidget(FieldWidget):
    adapts(IURI, None, IStandardDeviceType)


