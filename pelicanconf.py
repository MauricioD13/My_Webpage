AUTHOR = 'Mauricio Cuello'
SITENAME = 'Tech&Coffee'
SITEURL = ""

PATH = "content"

STATIC_PATHS = ["extra/custom.css","images"]

EXTRA_PATH_METADATA = {
    "extra/custom.css": {"path": "static/custom.css"},
}

MAIN_MENU = True

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True

# Default theme language.
I18N_TEMPLATES_LANG = "en"



# Pelican-search Configuration
STORK_INPUT_OPTIONS = {"stemming": "German", "url_prefix": SITEURL}

TIMEZONE = 'Europe/Madrid'

DEFAULT_LANG = 'en'
THEME = "Flex"
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Categories","/categories.html"),
)

# Social widget
SOCIAL = (
    ("github", "https://github.com/MauricioD13"),
    ("linkedin", "https://www.linkedin.com/in/mauricio-cuello-a1369b1b5/"),
    ("medium", "https://medium.com/@mdavidcuello"),
    
)

MENUITEMS = {
    ("Archives","/archives.html"),
    ("Tags","/tags.html"),
}

DEFAULT_PAGINATION = 5
OUTPUT_PATH = "docs/"
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

USE_LESS = True