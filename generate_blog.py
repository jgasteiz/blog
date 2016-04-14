from generator import BlogGenerator


def main():
    generator = BlogGenerator(base_path='./base', content_path='./blog_posts')
    output = generator.generate_output()

    # Write output html
    output_html_file = open('public/index.html', 'w')
    output_html_file.write(output.get('index_html'))
    output_html_file.close()

    for page in output.get('pages'):
        output_html_file = open('public/{}.html'.format(page.get('slug')), 'w')
        output_html_file.write(page.get('html'))
        output_html_file.close()


if __name__ == '__main__':
    main()
