generate:
	PYTHONBREAKPOINT=ipdb.set_trace python generator/generate.py

new_post:
	python generator/new_post.py

serve:
	cd public && python -m http.server 8000

publish:
	# Publish the site, using today's date as the commit message
	cd public
	git add --all
	# Use today's date and the current local time as the commit message
	git commit -m "Publish $(shell date +'%Y-%m-%d %H:%M:%S')"
	git push origin master