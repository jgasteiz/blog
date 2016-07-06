from datetime import datetime
from settings import CONTENT_PATH


def main():
    file_name = datetime.now().strftime('%Y-%m-%d')
    new_post_file = open('{}/{}.md'.format(CONTENT_PATH, file_name), 'w')
    post_content = 'Title: Post title goes here\nDate: {}\n\nPost content goes here'.format(file_name)
    new_post_file.write(post_content)
    new_post_file.close()

if __name__ == '__main__':
    main()
