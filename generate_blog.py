from bs4 import BeautifulSoup
import markdown

THE_CONTENT = """
# Hey, this is the title
## This is a subtitle

And this is just a paragraph
"""

# Grab base html file
base_html_file = open('base/index.html', 'r')
soup = BeautifulSoup(base_html_file.read(), 'html.parser')

# Find the main content container
main_content = soup.find(id="main-content")

# Turn the content into html and append it to the main content.
html_content = markdown.markdown(THE_CONTENT)
main_content.append(BeautifulSoup(html_content, 'html.parser'))

# Write output html
output_html_file = open('public/index.html', 'w')
output_html_file.write(soup.prettify())
output_html_file.close()
