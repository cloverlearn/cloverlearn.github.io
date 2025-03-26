watch:
	staticjinja watch --static static --srcpath templates --outpath docs

build:
	staticjinja build --srcpath templates --outpath docs --static static
