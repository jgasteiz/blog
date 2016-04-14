from generator import BlogGenerator


def main():
    generator = BlogGenerator(base_path='./base', content_path='./blog_posts')
    output_html = generator.generate_output_html()

    # Write output html
    output_html_file = open('public/index.html', 'w')
    output_html_file.write(output_html)
    output_html_file.close()


if __name__ == '__main__':
    main()
