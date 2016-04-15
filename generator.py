import os
from bs4 import BeautifulSoup
from datetime import datetime
import markdown
from slugify import slugify


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
        for article_file in os.listdir(self.content_path):
            if article_file.endswith(".md"):
                content_files.append('{}/{}'.format(self.content_path, article_file))

        content_files.reverse()
        return content_files

    def get_html_from_md(self, html_content):
        return markdown.markdown(html_content)

    def get_article(self, article_file_path, include_title_link):
        # Get the blog post content in html
        article_file = open(article_file_path, 'r')

        # Get the post date and title from the md file.
        article_title = article_file.readline().strip('Title:').strip('\n').strip()
        article_date = article_file.readline().strip('Date:').strip('\n').strip()
        article_date = datetime.strptime(article_date, '%Y-%m-%d').strftime('%A, %d %B %Y')
        # Get the rest of the content from the md file.
        md_content = article_file.read()
        article_content = self.get_html_from_md(md_content)
        # Close the md file.
        article_file.close()

        # Get the article from the template and populate the title, date and content.
        article = self.get_post_html_soup().find('article')

        article_title_element = article.find(attrs={'class': 'blog-post__title'})
        if include_title_link:
            article_title_anchor = self.get_base_html_soup().new_tag(
                'a', href='{}.html'.format(slugify(article_title)))
            article_title_anchor.append(article_title)
            article_title_element.append(article_title_anchor)
        else:
            article_title_element.append(article_title)

        article.find(attrs={'class': 'blog-post__date'}).append(article_date)
        article.find(attrs={'class': 'blog-post__content'}).append(
            self.get_content_html_soup(article_content)
        )

        return article, article_title

    def generate(self):
        # Find the main content container
        main_soup = self.get_base_html_soup()
        main_content = main_soup.find(id="main")

        # Generate detail pages
        for file_path in self.get_content_files():
            article, article_title = self.get_article(file_path, include_title_link=False)

            # Create a detail page
            detail_soup = self.get_base_html_soup()
            detail_content = detail_soup.find(id="main")
            detail_content.append(BeautifulSoup(str(article), self.parser))

            # Write the output detail html page.
            output_html_file = open('public/{}.html'.format(slugify(article_title)), 'w')
            output_html_file.write(str(detail_soup))
            output_html_file.close()

        # Generate general index page.
        for file_path in self.get_content_files():
            article, article_title = self.get_article(file_path, include_title_link=True)

            # Append the article to the main content.
            main_content.append(BeautifulSoup(str(article), self.parser))

        output_html_file = open('public/index.html', 'w')
        output_html_file.write(str(main_soup))
        output_html_file.close()
