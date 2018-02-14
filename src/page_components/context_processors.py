import asset_definitions
import django.conf
import django.http
from typing import *  # noqa

from . import page_component, utils

GlobalPageComponents = Dict[str, page_component.GlobalPageComponent]


def global_page_components(request):
    # type: (django.http.HttpRequest) -> Union[GlobalPageComponents, Dict[str, GlobalPageComponents]]

    # noinspection PyShadowingNames
    global_page_components = utils.get_global_page_components(request)

    global_page_components_context_name = getattr(
        django.conf.settings,
        "GLOBAL_PAGE_COMPONENTS_CONTEXT_NAME",
        "global_page_components",
    )

    if global_page_components_context_name:
        context = {
            global_page_components_context_name: global_page_components
        }
    else:
        context = global_page_components

    media = asset_definitions.Media()
    for component in global_page_components.values():
        media += component.media

    context["global_components_media"] = media

    return context
