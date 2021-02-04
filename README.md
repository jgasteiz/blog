# Javi's Blog

This is Javi Manzano's personal blog.

## How to build the thing

- Create a virtualenv and activate it
    - `python3 -m venv env`
    - `source ./env/bin/activate`
- Install the dependencies
    - `pip install -r requirements.txt`
    - `yarn install`
- Build the static files
    - `yarn build`
- Generate the blog
    - `./generate_blog.sh`


## Adding new blog posts

- `./new_post.sh` Will create a `.md` file under the path specified in `CONTENT_PATH`
