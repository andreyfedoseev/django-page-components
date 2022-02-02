from __future__ import absolute_import

import page_components

__all__ = ("ArticlePageComponent",)


class ArticlePageComponent(page_components.TemplatePageComponent):

    template_name = "page_components/article.html"

    class Media:
        js = ("article.js",)
        css = {"all": ("article.css",)}

    def __init__(self, article):
        self.article = article

    def get_context_data(self, **kwargs):
        kwargs.update(
            title=self.article.title,
            body=self.article.body,
        )
        return super(ArticlePageComponent, self).get_context_data(**kwargs)
