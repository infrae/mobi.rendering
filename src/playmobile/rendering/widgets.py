from zope.interface import implements, Interface
from zope.component import adapts, getUtility
from zope.schema.interfaces import IField, IURI

from playmobile.interfaces.devices import (IBasicDeviceType,
    IStandardDeviceType, IAdvancedDeviceType,)
from playmobile.interfaces.rendering import (IWidget, IFieldWidget,
    IRenderingEngine,)
from playmobile.interfaces.schema import (IPhoneNumber, IAddress,)


import urllib


class Widget(object):
    """ If their is not implementation of content type
    or device, return context as unicode text
    """
    implements(IWidget)
    adapts(None, None, None)

    def __init__(self, context, parent_widget, request):
        self.context = context
        self.request = request
        self.parent = parent_widget

    def _template_locals(self):
        return {'context': self.context,
                'request': self.request,
                'view': self}

    def render(self):
        template_engine = getUtility(IRenderingEngine)
        return template_engine.render_widget(self, self.request)


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
        return u'<a href="tel:%s">%s</a>' % (self.get_value(), self.get_value())


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


