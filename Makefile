generate:
	PYTHONBREAKPOINT=ipdb.set_trace python generator/generate.py

new_post:
	python generator/new_post.py

serve:
	cd public && python -m http.server 8000

publish:
	# Generate the site
	python generator/generate.py
	# Publish the site, using today's date as the commit message
	cd public && git add --all && git commit -m "Publish $(shell date +'%Y-%m-%d %H:%M:%S')" && git push origin master
	# Update the blog
	git add --all && git commit -m "Added new blog posts" && git push origin master