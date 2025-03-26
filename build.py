from staticjinja import Site

contexts = [
    ("index.html", {}),
]

if __name__ == "__main__":
    site = Site.make_site(contexts=contexts, outpath="docs")
    # enable automatic reloading
    site.render(use_reloader=True)
