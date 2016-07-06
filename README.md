# Javi's Blog

This is the personal blog of Javi Manzano.

## How to build the thing

- Create a virtualenv and activate it
    - `python3 -m venv env`
    - `source ./env/bin/activate`
- Install the dependencies
    - `pip install -r requirements.txt`
    - `npm install`
- Generate the blog
    - `./generate_blog.sh`
- Serve it locally
    - `gulp`


## Adding new blog posts

- `./new_post.sh` Will create a `.md` file under the path specified in `CONTENT_PATH`
