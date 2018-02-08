import app.models
import app.page_components.article


def test_template_page_component():

    article = app.models.Article(
        title="Foo",
        body="Bar",
    )

    article_page_component = app.page_components.article.ArticlePageComponent(article)

    assert article_page_component.render() == (
        "<h1>Foo</h1>\n"
        "<p>Bar</p>\n"
    )
