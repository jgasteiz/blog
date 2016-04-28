import os
import unittest

from bs4 import BeautifulSoup

from generator import BlogGenerator


class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = BlogGenerator(
            base_path='./base',
            content_path='./generator/test_posts',
            output_path='./generator/test_output',
            page_size=2,
        )

    def test_get_base_html_soup(self):
        """
        Expecting at least this:

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Fuzzing the Web</title>
        </head>
        <body>
            <header id="header">
                <h1 id="site-title"></h1>
                <h2 id="site-subtitle"></h2>
            </header>
            <div id="main"></div>
            <div id="pagination"></div>
            <footer id="footer"></footer>
        </body>
        </html>
        """
        base_html_soup = self.generator.get_base_html_soup()
        self.assertIn('<html lang="en">', str(base_html_soup))
        self.assertIn('</html>', str(base_html_soup))
        self.assertIn('<head>', str(base_html_soup))
        self.assertIn('<title>Fuzzing the Web</title>', str(base_html_soup))
        self.assertIn('</head>', str(base_html_soup))
        self.assertIn('<body>', str(base_html_soup))
        self.assertIn('</body>', str(base_html_soup))
        self.assertIn('id="header"', str(base_html_soup))
        self.assertIn('id="site-title"', str(base_html_soup))
        self.assertIn('id="site-subtitle"', str(base_html_soup))
        self.assertIn('id="main"', str(base_html_soup))
        self.assertIn('id="pagination"', str(base_html_soup))
        self.assertIn('id="footer"', str(base_html_soup))

    def test_get_post_html_soup(self):
        """
        Expecting at least this:

        <article class="blog-post">
            <div class="blog-post__header">
                <h1 class="blog-post__title"></h1>
                <span class="blog-post__date"></span>
            </div>
            <div class="blog-post__content"></div>
        </article>
        """
        post_html_soup = self.generator.get_post_html_soup()
        self.assertIn('<article class="blog-post">', str(post_html_soup))
        self.assertIn('blog-post__header"', str(post_html_soup))
        self.assertIn('blog-post__title"', str(post_html_soup))
        self.assertIn('blog-post__date"', str(post_html_soup))
        self.assertIn('blog-post__content"', str(post_html_soup))

    def test_get_content_files(self):
        content_files = self.generator.get_content_files()

        # Make sure the items are sorted and no files are missing.
        self.assertEqual(content_files[0], './generator/test_posts/2015-11-22.md')
        self.assertEqual(content_files[1], './generator/test_posts/2015-07-18.md')
        self.assertEqual(content_files[2], './generator/test_posts/2015-05-05.md')
        self.assertEqual(content_files[3], './generator/test_posts/2015-02-02.md')

    def test_get_article(self):
        article_file_path = './generator/test_posts/2015-11-22.md'
        article, article_title = self.generator.get_article(
            article_file_path, include_title_link=True)

        # Make sure the title is correct
        self.assertEqual(article_title, 'Thailand, November 2015')

        # Make sure we keep the post structure
        self.assertIn('<article class="blog-post">', str(article))
        self.assertIn('blog-post__header"', str(article))
        self.assertIn('blog-post__title"', str(article))
        self.assertIn('blog-post__date"', str(article))
        self.assertIn('blog-post__content"', str(article))

        # Make sure the file content is in the article.
        expected_url = """
            https://lh3.googleusercontent.com/VbAQCGBmP475cnziXJIF9TIWXhtAeGxiYH9HTZv70Gv4gopX5Np8=w800
        """.strip()
        expected_content = """
            It\'s great to be part of this family.
        """.strip()
        self.assertIn(expected_url, str(article))
        self.assertIn(expected_content, str(article))

        # Make sure there is a link to the article
        self.assertIn('href="thailand-november-2015.html"', str(article))

    def test_get_articles_in_page(self):
        article_list = []
        for file_path in self.generator.get_content_files():
            article_list.append(self.generator.get_article(file_path, include_title_link=True)[0])

        articles_in_page = self.generator.get_articles_in_page(article_list, 1)

        # Make sure we get the expected articles
        self.assertIn('Thailand, November 2015', str(articles_in_page[0]))
        self.assertIn('Mountain View &amp; San Francisco 2015', str(articles_in_page[1]))

        articles_in_page = self.generator.get_articles_in_page(article_list, 2)
        # Make sure we get the expected articles
        self.assertIn('Visiting Bristol', str(articles_in_page[0]))
        self.assertIn('What I\'ve been up to', str(articles_in_page[1]))

        # It should return empty lists if the pages don't exist.
        self.assertEqual(self.generator.get_articles_in_page(article_list, 3), [])
        self.assertEqual(self.generator.get_articles_in_page(article_list, 4), [])

    def test_generate(self):
        self.generator.generate()

        # Make sure the blog files have been generated properly
        html_files = os.listdir(self.generator.output_path)
        self.assertIn('index.html', html_files)
        self.assertIn('page2.html', html_files)

        # An html file per article.
        self.assertIn('thailand-november-2015.html', html_files)
        self.assertIn('mountain-view-san-francisco-2015.html', html_files)
        self.assertIn('visiting-bristol.html', html_files)
        self.assertIn('what-i-ve-been-up-to.html', html_files)

        # index.html and page2.html should have links to the articles
        index_file = open('{}/index.html'.format(self.generator.output_path), 'r')
        index_soup = BeautifulSoup(index_file.read(), 'html.parser')
        index_file.close()
        page2_file = open('{}/page2.html'.format(self.generator.output_path), 'r')
        page2_soup = BeautifulSoup(page2_file.read(), 'html.parser')
        page2_file.close()

        # index.html should have links to the first and second posts.
        # index_titles = index_soup.findAll(attrs={'class': 'blog-post__title'})

        self.assertIn('href="thailand-november-2015.html"', str(index_soup))
        self.assertIn('href="mountain-view-san-francisco-2015.html"', str(index_soup))

        # page2.html should have links to the third and fourth posts.
        self.assertIn('href="visiting-bristol.html"', str(page2_soup))
        self.assertIn('href="what-i-ve-been-up-to.html"', str(page2_soup))

        # index.html should have a pagination link to the next page.
        # self.assertIn('href="thailand-november-2015.html"', index_content)


if __name__ == '__main__':
    unittest.main()
