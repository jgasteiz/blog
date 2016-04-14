import os
from bs4 import BeautifulSoup
import markdown

# Grab base html file
base_html_file = open('base/index.html', 'r')
soup = BeautifulSoup(base_html_file.read(), 'html.parser')

# Find the main content container
main_content = soup.find(id="main")

# Turn the content into html and append it to the main content.
for blog_post_file in os.listdir("./blog_posts"):
    if blog_post_file.endswith(".md"):
        blog_post_file = open('./blog_posts/{}'.format(blog_post_file), 'r')
        file_content = blog_post_file.read()
        html_content = markdown.markdown(file_content)
        main_content.append(BeautifulSoup(html_content, 'html.parser'))

# Write output html
output_html_file = open('public/index.html', 'w')
output_html_file.write(soup.prettify())
output_html_file.close()
