import collections
import threading

import django.conf
import django.core.exceptions
import django.http
import django.utils.module_loading
import django.utils.six
from typing import *  # noqa

from . import page_component

_local_cache = threading.local()
_local_cache.global_components_declarations = None


def get_global_page_components_declarations():
    # type: () -> Dict[str, Type[page_component.GlobalPageComponent]]
    global _local_cache

    if _local_cache.global_components_declarations is None:
        declaration = getattr(django.conf.settings, "GLOBAL_PAGE_COMPONENTS", {})
        if not isinstance(declaration, dict):
            raise django.core.exceptions.ImproperlyConfigured("GLOBAL_PAGE_COMPONENTS must be a dict")

        _local_cache.global_components_declarations = collections.OrderedDict()
        for component_name, component_class in declaration.items():
            if isinstance(component_class, django.utils.six.string_types):
                component_class = django.utils.module_loading.import_string(component_class)

            if not issubclass(component_class, page_component.GlobalPageComponent):
                raise django.core.exceptions.ImproperlyConfigured(
                    "{} must be a sub-class of GlobalPageComponent".format(component_class)
                )
            _local_cache.global_components_declarations[component_name] = component_class

    return _local_cache.global_components_declarations


def get_global_page_components(request):
    # type: (django.http.HttpRequest) -> Dict[str, page_component.GlobalPageComponent]
    if not hasattr(request, "_global_page_components"):
        global_page_components = collections.OrderedDict()
        for component_name, component_class in get_global_page_components_declarations().items():
            global_page_components[component_name] = component_class(request)
        request._global_page_components = global_page_components
    # noinspection PyProtectedMember
    return request._global_page_components
