from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": {
            "entry": {"nr_components": "./js/nr/custom-components.js"},
            "dependencies": {},
            "devDependencies": {},
            "aliases": {
                "@nr": "./js/nr",
            },
        }
    },
)
