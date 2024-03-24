import mkdocs.plugins
from mkdocs.config import config_options


class SampleMkDocsPlugin(mkdocs.plugins.BasePlugin):
    """
    Sample MkDocs plugin to add custom text to the markdown pages,
    with an option to underline the text.
    """
    config_scheme = (
        ('text', config_options.Type(str, default='Default text')),
        ('underline', config_options.Type(bool, default=False)),
    )

    def on_page_markdown(self, markdown, page=None, config=None, site_navigation=None, **kwargs):
        """
        Hook to modify the Markdown text of each page. Adds specified text,
        optionally underlined, at the end of the page content.

        :param markdown: The original markdown content of the page.
        :param page: The page object (unused in this example).
        :param config: The site config (unused in this example).
        :param site_navigation: The site navigation object (unused in this example).
        :return: Modified markdown content.
        """
        # Decide if the text should be underlined
        text_to_add = f"<u>{self.config['text']}</u>" if self.config['underline'] else self.config['text']
        # Ensure clear separation from existing content
        return markdown + f"\n\n<!-- Custom Plugin Content -->\n{text_to_add}"
