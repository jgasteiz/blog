from blog_generator import BlogGenerator
from settings import (
    BASE_PATH,
    CONTENT_PATH,
    OUTPUT_PATH,
    PAGE_SIZE,
)


def main():
    BlogGenerator(
        base_path=BASE_PATH,
        content_path=CONTENT_PATH,
        output_path=OUTPUT_PATH,
        page_size=PAGE_SIZE,
    ).generate()

if __name__ == '__main__':
    main()
