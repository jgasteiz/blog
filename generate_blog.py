from generator import BlogGenerator


def main():
    generator = BlogGenerator(base_path='./base', content_path='./blog_posts')
    generator.generate()

if __name__ == '__main__':
    main()
