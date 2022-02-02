from __future__ import absolute_import

import django.views.generic

import app.page_components
import page_components


class DisplayArticleView(
    page_components.PageComponentsView, django.views.generic.TemplateView
):

    article = None

    def get_page_components(self):
        return {
            "article": app.page_components.ArticlePageComponent(self.article),
        }

    def get_media(self):
        return super(DisplayArticleView, self).get_media()
