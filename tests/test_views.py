import django.utils.encoding
import pytest

import app.models
import app.views

NOT_SPECIFIED = object()


@pytest.mark.parametrize(
    "page_components_context_name,template_name",
    (
        (NOT_SPECIFIED, "display-article.html"),
        (None, "display-article-with-blank-namespace.html"),
        (
            "custom_page_components_namespace",
            "display-article-with-custom-namespace.html",
        ),
    ),
)
def test_page_component_view(page_components_context_name, template_name, rf):

    view_kwargs = {
        "template_name": template_name,
        "article": app.models.Article(title="Foo", body="Bar"),
    }
    if page_components_context_name is not NOT_SPECIFIED:
        view_kwargs["page_components_context_name"] = page_components_context_name

    view_function = app.views.DisplayArticleView.as_view(**view_kwargs)

    request = rf.get("/display-article")
    response = view_function(request)
    response.render()

    assert django.utils.encoding.force_str(response.content) == (
        """<!DOCTYPE html>\n"""
        """<html>"""
        """<head>"""
        """<link href="/static/article.css" type="text/css" media="all" rel="stylesheet">"""
        """</head>"""
        """<body>"""
        """<h1>Foo</h1>"""
        """<p>Bar</p>"""
        """<script type="text/javascript" src="/static/article.js"></script>"""
        """</body>"""
        """</html>\n"""
    )
