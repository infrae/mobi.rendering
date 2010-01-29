from zope.component import getMultiAdapter, providedBy
from zope.schema.interfaces import IObject
from zope.schema import getFieldNames

from chameleon.core import types
from chameleon.zpt import expressions

from playmobile.interfaces.rendering import IFieldWidget, IWidget

def get_field(context, field_name):
    schema_interfaces = []
    if hasattr(context, 'schema'):
        schema_interfaces = [context.schema]

    for interface in (schema_interfaces or providedBy(context)):
        if field_name in getFieldNames(interface):
            return interface[field_name]
    return None


class FieldWidgetFactory(object):

    def __call__(self, context, field_name, view, request, name=u''):
        field = get_field(context, field_name)
        if field is None:
            raise TypeError, 'invalid field name %s' % field_name
        field.bind(context)
        if IObject.providedBy(field):
            widget = getMultiAdapter((field.get(context), view,
                request,), name=name)
        else:
            widget = getMultiAdapter((field, view, request,),
                IFieldWidget, name=name)
        return widget.render()


class WidgetFactory(object):

    def __call__(self, context, view, request, name=u''):
        widget = getMultiAdapter((context, view, request,),
            IWidget, name=name)

        return widget.render()


class WidgetTranslator(expressions.ExpressionTranslator):

    factory = WidgetFactory()
    symbol = '_get_widget'

    # NormalObject
    # tal:replace tal:replace="structure widget:context.address"

    def translate(self, string, escape=None):
        python_translator = expressions.PythonTranslator()
        # just validate
        python_translator.translate(string)
        value = types.value("%s(%s, view, request)" % \
                            (self.symbol, string.strip()))

        value.symbol_mapping[self.symbol] = self.factory
        return value


class FieldWidgetTranslator(expressions.ExpressionTranslator):

    factory = FieldWidgetFactory()
    symbol = '_get_field_widget'

    # NormalObject
    # tal:replace tal:replace="structure field_widget:context#phone_number"

    def validate(self, string):
        return len(string.strip().split('#')) == 2

    def translate(self, string, escape=None):
        obj, field_name = string.strip().split('#')

        value = types.value("%s(%s, '%s', view, request)" % \
                            (self.symbol, obj, field_name))

        value.symbol_mapping[self.symbol] = self.factory
        return value


# utility
widget_translator = WidgetTranslator()
field_widget_translator = FieldWidgetTranslator()
