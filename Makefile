generate:
	PYTHONBREAKPOINT=ipdb.set_trace python generator/generate.py

new_post:
	python generator/new_post.py

serve:
	cd public && python -m http.server 8000