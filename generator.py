import os
from bs4 import BeautifulSoup
import markdown


class BlogGenerator(object):
    def __init__(self, base_path, content_path, parser='html.parser'):
        self.base_path = base_path
        self.content_path = content_path
        self.parser = parser

    def get_base_html_soup(self):
        base_html_file = open('{}/index.html'.format(self.base_path), 'r')
        base_html = base_html_file.read()
        return BeautifulSoup(base_html, self.parser)

    def get_post_html_soup(self):
        post_html_file = open('{}/post.html'.format(self.base_path), 'r')
        post_html = post_html_file.read()
        return BeautifulSoup(post_html, self.parser)

    def get_content_html_soup(self, html_content):
        return BeautifulSoup(html_content, self.parser)

    def get_content_files(self):
        content_files = []
        for blog_post_file in os.listdir(self.content_path):
            if blog_post_file.endswith(".md"):
                content_files.append('{}/{}'.format(self.content_path, blog_post_file))

        content_files.reverse()
        return content_files

    def get_html_from_md(self, html_content):
        return markdown.markdown(html_content)

    def generate_output_html(self):
        # Find the main content container
        main_soup = self.get_base_html_soup()
        main_content = main_soup.find(id="main")

        # Turn the content into html and append it to the main content.
        for file_path in self.get_content_files():
            # Get the blog post content in html
            blog_post_file = open(file_path, 'r')
            md_content = blog_post_file.read()
            html_content = self.get_html_from_md(md_content)

            # Append the blog post content to the main soup.
            article_soup = self.get_post_html_soup().find('article')
            article_soup.append(self.get_content_html_soup(html_content))
            main_content.append(article_soup)
            blog_post_file.close()

        return unicode(main_soup)
