# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt.
"""

    >>> from mobi.rendering.widgets import *
    >>> from mobi.interfaces.rendering import *
    >>> from zope.interface.verify import verifyClass

    A wigdet implements the IWidget interface.

    >>> verifyClass(IWidget, Widget)
    True
    >>> verifyClass(IPage, Page)
    True

    We define a minimal model class with an attribute defined in a zope.schema
    interface.

    >>> from zope.interface import implements, Interface
    >>> from zope.schema import TextLine

    The schema interface define one attribute "name" which is a simple line
    of text.

    >>> class IModel(Interface):
    ...     name = TextLine(title=u'a name')

    The model implements that interface.

    >>> class Model(object):
    ...     implements(IModel)
    ...     name = u'default name'

    A fake request.

    >>> class TestRequest(object):
    ...    pass

    Now we can instantiate the page.

    >>> context = Model()
    >>> request = TestRequest()
    >>> page = Page(context, request)
    >>> page # doctest: +ELLIPSIS
    <mobi.rendering.widgets.Page ...>


    We define a widget to render the IModel implementers.

    >>> class ModelDefaultWidget(Widget):
    ...     pass

    We register the widget as an adapter for the model, the parent view, and
    the request.

    Since the view is not specialized we will only set the model interface.

    When the page will be displayed. It will try to find to find an adapter
    for its context to an IWidget interface and use is as is content.

    Since we don't have register the widget as adapter, rendering the
    page will fail.

    >>> page.render() # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ComponentLookupError: ...

    We register the widget as adapter.

    >>> from zope.component import getGlobalSiteManager, getMultiAdapter
    >>> gsm = getGlobalSiteManager()
    >>> registerAdapter = gsm.registerAdapter
    >>> registerAdapter(ModelDefaultWidget, (IModel,None,None,), IWidget)

    Have a look at the page template :

    >>> page_template = \\
    ...     open(os.path.dirname(__file__) + '/templates/page.pt', 'r').read()
    >>> print page_template # doctest: +NORMALIZE_WHITESPACE
    <html>
    <head>
    </head>
    <body tal:content="structure content" />
    </html>

    and at the widget template :

    >>> widget_template = \\
    ...     open(os.path.dirname(__file__) + \\
    ...             '/templates/model_default_widget.pt', 'r').read()
    >>> print widget_template # doctest: +NORMALIZE_WHITESPACE
    <strong>${context.name}</strong>

    Now we can render the page and it will render the widget inside.

    >>> print page.render() # doctest: +NORMALIZE_WHITESPACE
    <html>
    <head>
    </head>
    <body><strong>default name</strong></body>
    </html>

    Now we want to customize the rendering of the model for a set of devices.
    We will also make the field "name" capable of being rendered differently.

    >>> class ModelWidgetStandard(Widget):
    ...     pass

    We register the widget for the standard device type.

    >>> from mobi.interfaces.devices import (IAdvancedDeviceType,
    ...    IStandardDeviceType)
    >>> registerAdapter(ModelWidgetStandard,
    ...     (IModel, None, IStandardDeviceType,),
    ...     IFieldWidget)

    We also create two field widgets to render TextLine fields.
    Field widgets are special widgets that allows device specific rendering
    of zope schema fields.

    >>> class TextLineWidgetDefault(FieldWidget):
    ...     pass

    >>> class TextLineWidgetAdvanced(FieldWidget):
    ...     pass

    and we register them.

    >>> from zope.schema.interfaces import ITextLine

    >>> registerAdapter(TextLineWidgetDefault,
    ...    (ITextLine, None, None), IFieldWidget)
    >>> registerAdapter(TextLineWidgetAdvanced,
    ...    (ITextLine, None, IAdvancedDeviceType), IFieldWidget)

    Let's have a look at the template for ModelWidgetAdvanced widget :

    >>> widget_template = \\
    ...     open(os.path.dirname(__file__) + \\
    ...             '/templates/model_widget_standard.pt', 'r').read()
    >>> print widget_template # doctest: +NORMALIZE_WHITESPACE
    <!-- widget to render IModel on IStandardDeviceType devices -->
    <div class="fancy widget">
      <div class="for standard devices">
        <div class="to render a model"
            tal:content="structure fieldwidget: context#name" />
      </div>
    </div>
    <!-- end widget -->

    Here how looks like the basic widget for ITextLine :

    >>> basic_field_widget_template = \\
    ...     open(os.path.dirname(__file__) + \\
    ...             '/templates/text_line_widget_default.pt', 'r').read()
    >>> print basic_field_widget_template # doctest: +NORMALIZE_WHITESPACE
    <!-- start basic field widget to render a ITextLine -->
    <strong>${value}</strong>
    <!-- end widget -->

    And then the advanced field widget for ITextLine :

    >>> advanced_field_widget_template = \\
    ...     open(os.path.dirname(__file__) + \\
    ...             '/templates/text_line_widget_advanced.pt', 'r').read()
    >>> print advanced_field_widget_template # doctest: +NORMALIZE_WHITESPACE
    <!-- start widget to render ITextLine on IAdvancedDeviceType devices -->
    <div class="fancy_templace">
      <div class="for advanced devices">
        ${value}
      </div>
    </div>
    <!-- end widget -->

    The "fieldwidget" chameleon expression is NOT real python. It is a python
    like expression meaning "render the widget for the field name of the object
    context".

    Now we will create two request two request simulating to phones a 
    Blackberry with touch capabilities and an iPhone.
    The blackberry is considered to be in the IStandardDeviceType category and
    the iPhone in the IAdvancedDeviceType because the iPhone is considered to
    have a more capable browser.

    >>> from zope.interface import alsoProvides

    >>> blackberry_touch = TestRequest()
    >>> alsoProvides(blackberry_touch, IStandardDeviceType)

    >>> iphone = TestRequest()
    >>> alsoProvides(iphone, IAdvancedDeviceType)

    We create a page for each device.

    >>> blackberry_touch_page = Page(context, blackberry_touch)
    >>> iphone_page = Page(context, iphone)

    We render the blackberry page. It render the model with the standard widget
    and the field with the default one.

    >>> print blackberry_touch_page.render()
    <html>
    <head>
    </head>
    <body><div class="fancy widget">
      <div class="for standard devices">
        <div class="to render a model"><strong>default name</strong></div>
      </div>
    </div></body>
    </html>

    The model widget is also used to render for the iphone (advanced) since
    their is no better but the field is rendered using the field widget for
    advanced devices.

    >>> print iphone_page.render()
    <html>
    <head>
    </head>
    <body><div class="fancy widget">
      <div class="for standard devices">
        <div class="to render a model"><div class="fancy_templace">
      <div class="for advanced devices">
        default name
      </div>
    </div></div>
      </div>
    </div></body>
    </html>

"""


from zope.component import getGlobalSiteManager
from mobi.rendering.engine import TemplateEngine
from mobi.interfaces.rendering import IRenderingEngine
from mobi.rendering.expressions import (widget_translator,
    field_widget_translator,)
import os

gsm = getGlobalSiteManager()
te = TemplateEngine()
te.search_path = [os.path.dirname(__file__) + '/templates']
gsm.registerUtility(te, IRenderingEngine)
gsm.registerUtility(field_widget_translator, name=u"fieldwidget")
gsm.registerUtility(widget_translator, name=u"widget")


