import math
import os
from bs4 import BeautifulSoup
from datetime import datetime
import markdown
from slugify import slugify


class BlogGenerator(object):
    def __init__(self, base_path, content_path, output_path, page_size, parser='html.parser'):
        self.base_path = base_path
        self.content_path = content_path
        self.output_path = output_path
        self.parser = parser
        self.page_size = page_size

    def get_base_html_soup(self):
        """
        Create a BeautifulSoup object with the content of the base template.
        """
        base_html_file = open('{}/index.html'.format(self.base_path), 'r')
        base_html = base_html_file.read()
        base_html_file.close()
        return BeautifulSoup(base_html, self.parser)

    def get_about_html_soup(self):
        """
        Create a BeautifulSoup object with the content of the about template.
        """
        about_html_file = open('{}/about.html'.format(self.base_path), 'r')
        about_html = about_html_file.read()
        about_html_file.close()
        return BeautifulSoup(about_html, self.parser)

    def get_post_html_soup(self):
        """
        Create a BeautifulSoup object with the content of the post template.
        """
        post_html_file = open('{}/post.html'.format(self.base_path), 'r')
        post_html = post_html_file.read()
        post_html_file.close()
        return BeautifulSoup(post_html, self.parser)

    def get_content_files(self):
        """
        Get the list of md content files ordered by file name.
        """
        content_files = []
        for article_file in os.listdir(self.content_path):
            if article_file.endswith(".md"):
                content_files.append('{}/{}'.format(self.content_path, article_file))
        content_files = sorted(content_files)
        content_files.reverse()
        return content_files

    def get_article(self, article_file_path, include_title_link=False):
        """
        Get an article with the content of the given article file path.
        The title will be a link to the article detail depending on
        the value of `include_title_link`.
        """
        # Get the blog post content in html
        article_file = open(article_file_path, 'r')

        # Get the post date and title from the md file.
        article_title = article_file.readline().strip('Title:').strip('\n').strip()
        article_date = article_file.readline().strip('Date:').strip('\n').strip()
        article_date = datetime.strptime(article_date, '%Y-%m-%d').strftime('%A, %d %B %Y')
        # Get the rest of the content from the md file.
        md_content = article_file.read()
        article_content = markdown.markdown(md_content)
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
            BeautifulSoup(article_content, self.parser)
        )

        return article, article_title

    def get_articles_in_page(self, articles_list, page_num):
        """
        Get the articles in a given page for a given article list.
        """
        last_article_index = page_num * self.page_size
        first_article_index = last_article_index - self.page_size
        return articles_list[first_article_index:last_article_index]

    def generate_detail_pages(self):
        # Generate detail pages
        for file_path in self.get_content_files():
            article, article_title = self.get_article(file_path)

            # Create a detail page
            detail_soup = self.get_base_html_soup()
            detail_soup.find(id='pagination').extract()
            detail_content = detail_soup.find(id="main")
            detail_content.append(BeautifulSoup(str(article), self.parser))
            detail_soup.find(name='title').string = '{} | {}'.format(article_title, detail_soup.find(name='title').text)

            # Write the output detail html page.
            output_html_file = open('{}/{}.html'.format(self.output_path, slugify(article_title)), 'w')
            output_html_file.write(str(detail_soup))
            output_html_file.close()

    def generate_main_pages(self):
        # Generate the articles for the index page.
        all_articles = []
        for file_path in self.get_content_files():
            article, _ = self.get_article(file_path, include_title_link=True)
            all_articles.append(article)

        # Generate an index.html per page.
        num_pages = math.ceil(len(all_articles) / self.page_size)
        for i in range(1, num_pages + 1):
            # Find the main content container
            main_soup = self.get_base_html_soup()
            main_content = main_soup.find(id='main')
            pagination = main_soup.find(id='pagination')

            # Append the articles to the main content.
            articles_to_append = self.get_articles_in_page(all_articles, i)
            for article in articles_to_append:
                main_content.append(BeautifulSoup(str(article), self.parser))

            if i == 1:
                output_html_file = open('{}/index.html'.format(self.output_path), 'w')
            else:
                output_html_file = open('{}/page{}.html'.format(self.output_path, i), 'w')

            if num_pages > 1:
                pagination.find(id='page-number').append(str(i))
                pagination.find(id='num-pages').append(str(num_pages))

                if i == 1:
                    pagination.find(id='previous-page').extract()
                elif i == 2:
                    pagination.find(id='previous-page').attrs['href'] = 'index.html'
                else:
                    pagination.find(id='previous-page').attrs['href'] = 'page{}.html'.format(str(i - 1))

                if num_pages > i:
                    pagination.find(id='next-page').attrs['href'] = 'page{}.html'.format(str(i + 1))
                else:
                    pagination.find(id='next-page').extract()
            else:
                pagination.extract()

            output_html_file.write(str(main_soup))
            output_html_file.close()

    def generate_about_page(self):
        # Generate the about.html
        about_content = self.get_about_html_soup().find('article')

        about_soup = self.get_base_html_soup()
        about_soup.find(id='pagination').extract()
        about_soup.find(id='main').append(BeautifulSoup(str(about_content), self.parser))

        output_html_file = open('{}/about.html'.format(self.output_path), 'w')
        output_html_file.write(str(about_soup))
        output_html_file.close()

    def generate(self):
        """
        Main function, generate the main index.html files and a detail html
        file per blog post.
        """
        self.generate_detail_pages()
        self.generate_main_pages()
        self.generate_about_page()
