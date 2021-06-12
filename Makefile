SITE= _site
RM= rm -rf
ARCHIVES= category

all : build

build: clean build_jekyll archives

build_jekyll:
	jekyll build --destination $(SITE)

archives:
	cp -r _site/$(ARCHIVES) .
	git add $(ARCHIVES)

push:
	git commit -m "Updates"
	git push

serve:
	bundle exec jekyll serve

clean :
	$(RM) $(ARCHIVES)
	$(RM) $(SITE)
