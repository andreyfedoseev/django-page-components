======================
django-page-components
======================

"Page component" is a unit of a user interface (think ReactJS components). ``django-page-components`` provide
a minimalistic framework for creating page components and using them in your Django views and templates.

To define a page component you need to create a sub-class of ``page_components.PageComponent``
and implement ``render`` method like so:

.. code-block:: python

    import page_components
    import django.utils.html


    class AddToCartButton(page_components.PageComponent):

        def __init__(self, product):
            self.product = product

        class Media:
            js = (
                "add-to-cart.js",  # this is where addToCart is defined
            )
            css = {
                "all": (
                    "add-to-cart.css"  # this is where `.add-to-card` styles are defined
                )
            }

        def render(self):
            return django.utils.html.format_html(
                """<button class="add-to-cart" onclick="addToCart({ product_id })">Add to cart</button>""",
                product_id=self.product.id
            )


You can also use a ``TemplatePageComponent`` base class to implement page components based on templates.
In that case you may want to implement ``get_context_data`` method:

.. code-block:: python

    class AddToCartButton(page_components.TemplatePageComponent):

        template_name = "add-to-cart-button.html"

        ...

        def get_context_data(self, **kwargs):
            kwargs["product_id"] = self.product_id
            return super(AddToCartButton, self).get_context_data(**kwargs)

Note that it's up to you to decide how to implement the ``render`` method and what additional methods should be added
to your page components. One general recommendation is to keep the ``__init__`` method as lightweight as possible and do
all the heavy lifting in the ``render`` method.

A proposed convention is to store your page components classes in ``page_components`` package/module inside your app::

    myapp.page_components.AddToCartButton

Now, when we have some page components defined it is time to use them in views:

.. code-block:: python

    import django.views.generic
    import page_components

    import myapp.models
    import myapp.page_components

    class ProductPage(
        page_components.PageComponentsView,
        django.views.generic.DetailView,
    ):

        model = myapp.models.Product
        template_name = "product.html"

        def get_page_components(self):
            return {
                "add_to_cart_button": myapp.page_components.AddToCartButton(self.object)
            }


and templates:

.. code-block:: html

    <html>
      <head>
        /* this will include CSS files for all page components on that page */
        {{ view.media.css.render }}
      </head>
      <body>
        <h1>{{ object.title }}</h1>
        {{ page_components.add_to_cart_button }}

        /* this will include JavaScript files for all page components on that page */
        {{ view.media.js.render }}
      </body>
    </html>

Note that page components are placed to ``page_components`` namespace in template context by default. You can change
that namespace on per-view basis by adding ``page_components_context_name`` attribute to a view class, or globally with
``PAGE_COMPONENTS_CONTEXT_NAME`` setting. If you set ``page_components_context_name`` to ``None`` it will disable
the namespace entirely.
