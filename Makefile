SITE= _site
RM= rm -rf

all : build

build :
	jekyll build --destination $(SITE)

publish: clean build archives push

archives:
	cp -r _site/category .
	git add category

push:
	git commit -m "Updates"
	git push

clean :
	$(RM) $(SITE)
