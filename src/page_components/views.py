from typing import Dict, Optional

import asset_definitions
import django.conf

from . import page_component  # noqa

NOT_SPECIFIED = object()


__all__ = ("PageComponentsView",)


class PageComponentsView(asset_definitions.MediaDefiningView):

    page_components_context_name = NOT_SPECIFIED

    def get_context_data(self, **kwargs):
        page_components_context_name = self.get_page_components_context_name()
        if page_components_context_name:
            kwargs[page_components_context_name] = self.get_page_components()
        else:
            kwargs.update(self.get_page_components())
        # noinspection PyUnresolvedReferences
        return super(PageComponentsView, self).get_context_data(**kwargs)

    def get_media(self):
        media = super(PageComponentsView, self).get_media()
        # noinspection PyShadowingNames
        for page_component in self.get_page_components().values():
            media += page_component.media
        return media

    def get_page_components(self) -> Dict[str, page_component.PageComponent]:
        return {}

    def get_page_components_context_name(self) -> Optional[str]:
        if self.page_components_context_name is NOT_SPECIFIED:
            return getattr(
                django.conf.settings, "PAGE_COMPONENTS_CONTEXT_NAME", "page_components"
            )
        return self.page_components_context_name
