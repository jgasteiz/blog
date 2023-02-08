# Javi's Blog

This is Javi Manzano's personal blog.

## How to build and run this thing

1. Install python dependencies
```shell
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```
2. Build the static files
```shell
yarn install
yarn build
```
3. Generate the blog
```shell
make generate
```
(4. Adding new blog posts)
```shell
make new_post
```
