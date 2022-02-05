import abc
from typing import Any, Dict

import asset_definitions
import django.core.exceptions
import django.forms
import django.template.loader

TemplateContext = Dict[str, Any]


__all__ = (
    "PageComponent",
    "TemplatePageComponent",
)


class PageComponent(abc.ABC, asset_definitions.MediaDefiningClass):
    @abc.abstractmethod
    def render(self) -> str:
        return ""

    def __str__(self):
        return self.render()


class TemplatePageComponent(PageComponent):

    template_name = None

    def render(self) -> str:
        template_name = self.get_template_name()
        context_data = self.get_context_data()
        return django.template.loader.render_to_string(
            template_name, context=context_data
        )

    # noinspection PyMethodMayBeStatic
    def get_template_name(self) -> str:
        if not self.template_name:
            raise django.core.exceptions.ImproperlyConfigured(
                "template_name is missing"
            )
        return self.template_name

    # noinspection PyMethodMayBeStatic
    def get_context_data(self, **kwargs) -> TemplateContext:
        context_data = dict(kwargs)
        return context_data
