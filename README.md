# Javi's Blog

This is Javi Manzano's personal blog.

## How to build and run this thing

Assuming python3 is the default python,
create a virtual environment and install python dependencies:
```shell
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

Install yarn dependencies and build static files:
```shell
yarn install
yarn build
```

Build the blog:
```shell
make generate
```

Adding new blog posts:
```shell
make new_post
```
