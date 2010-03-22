"""
    >>> from playmobile.rendering.engine import TemplateEngine
    >>> from playmobile.interfaces.rendering import IRenderingEngine

    A IRenderingEngine is an utility to render widgets / views.

    The TemplateEngine implementation is a aims at looking up chameleon
    templates.

    >>> from zope.interface.verify import verifyClass
    >>> verifyClass(IRenderingEngine, TemplateEngine)
    True

    If the widget does not have a template attribute the engine will search
    for one in the search path.

    >>> from playmobile.rendering.widgets import BasicAddressWidget
    >>> te = TemplateEngine()
    >>> te.get_template_paths(TestWidget(), 'name') # doctest: +ELLIPSIS
    ['...playmobile/rendering/default_skin/TestWidget/name.pt']

    You can modify the search path to add locations.
    >>> te.search_path.append('/tmp/themedir')
    >>> te.get_template_paths(TestWidget(), 'name') # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    ['.../playmobile/rendering/default_skin/TestWidget/name.pt',
     '/tmp/themedir/TestWidget/name.pt']

    For the default name index (the default), you get some extras locations.
    >>> te.get_template_paths(TestWidget()) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    ['...playmobile/rendering/default_skin/test_widget.pt',
     '...playmobile/rendering/default_skin/TestWidget/index.pt',
     '/tmp/themedir/test_widget.pt',
     '/tmp/themedir/TestWidget/index.pt']

"""

from playmobile.rendering.widgets import Widget

class TestWidget(Widget):
    def __init__(self):
        pass
