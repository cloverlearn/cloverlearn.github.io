SITE= _site
RM= rm -rf
ARCHIVES= category

all : publish

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
	$(RM) $(ARCHIVES)
	$(RM) $(SITE)
