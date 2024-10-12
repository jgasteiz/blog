from blog_generator import BlogGenerator
import settings


def main():
    BlogGenerator(
        base_path=settings.BASE_PATH,
        content_path=settings.CONTENT_PATH,
        images_path=settings.IMAGES_PATH,
        output_path=settings.OUTPUT_PATH,
        page_size=settings.PAGE_SIZE,
    ).generate()


if __name__ == '__main__':
    main()
