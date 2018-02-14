import abc

import asset_definitions
import django.core.exceptions
import django.forms
import django.http
import django.template.loader
import django.utils.encoding
import django.utils.six
from typing import *

TemplateContext = Dict[str, Any]


__all__ = (
    "PageComponent",
    "TemplatePageComponent",
    "GlobalPageComponent",
    "GlobalTemplatePageComponent",
)


@django.utils.encoding.python_2_unicode_compatible
class PageComponent(django.utils.six.with_metaclass(
    abc.ABCMeta,
    asset_definitions.MediaDefiningClass
)):

    @abc.abstractmethod
    def render(self):
        # type: () -> str
        return ""

    def __str__(self):
        return self.render()


class GlobalPageComponent(PageComponent):

    def __init__(self, request):
        # type: (django.http.HttpRequest) -> None
        self.request = request


class TemplatePageComponentMixin(PageComponent):
    template_name = None

    def render(self):
        # type: () -> str
        template_name = self.get_template_name()
        context_data = self.get_context_data()
        return django.template.loader.render_to_string(template_name, context=context_data)

    # noinspection PyMethodMayBeStatic
    def get_template_name(self):
        # type: () -> str
        if not self.template_name:
            raise django.core.exceptions.ImproperlyConfigured("template_name is missing")
        return self.template_name

    # noinspection PyMethodMayBeStatic
    def get_context_data(self, **kwargs):
        # type: () -> TemplateContext
        context_data = dict(kwargs)
        return context_data


class TemplatePageComponent(
    TemplatePageComponentMixin,
    PageComponent
):
    pass


class GlobalTemplatePageComponent(
    TemplatePageComponentMixin,
    GlobalPageComponent
):
    pass
