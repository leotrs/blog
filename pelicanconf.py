#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import date
import os

AUTHOR = 'leotrs'
SITENAME = 'Leo Torres'
SITEURL = ''
SIDEBAR_DIGEST = 'Network Scientist'
CURRENTYEAR = date.today().year

PATH = 'content'
THEME_PATH = '../pelican/pelican-themes/'
THEME = os.path.join(THEME_PATH, 'pelican-bootstrap3')
TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'

ARTICLE_PATHS = ['blog']
ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{slug}.html'
ARTICLE_EXCLUDES = ['images', 'static']
PAGE_PATHS = ['']
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
PAGE_EXCLUDES = ['images', 'static']

# Paths containing files that are not to be fed to any template. Relative
# to PATH
STATIC_PATHS = ['images', 'static']

# Social links
SOCIAL = (('email', 'mailto:leo@leotrs.com', 'envelope'),
          ('github', 'https://www.github.com/leotrs'),
          ('twitter', 'https://www.twitter.com/_leotrs'),
          ('scholar', 'https://scholar.google.com/citations?user=xjyYHz0AAAAJ&hl=en', 'check'),
          ('resume', 'static/resume.pdf', 'file-text'),
)

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Allow relative urls
RELATIVE_URLS = True

# These templates don't need files that use them: they are rendered directly
DIRECT_TEMPLATES = ['index'] # 'tags', 'authors', '404'

# Keep empty to not generate these page
AUTHOR_SAVE_AS = ''
TAGS_SAVE_AS = ''

# How many articles per page
DEFAULT_PAGINATION = False

# Pelican plugins
PLUGIN_PATHS = ['../pelican/pelican-plugins/']
PLUGINS = ['render_math', 'tag_cloud', 'jinja2content']

JINJA2CONTENT_TEMPLATES = ['static']

# bootstrap3 theme tweaks
CATEGORIES_URL = 'do.html'
TAGS_URL = 'do.html'
DISPLAY_CATEGORIES_ON_SIDEBAR = False
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
DISPLAY_TAGS_INLINE = True
DISPLAY_TAGS_ON_SIDEBAR = False
DISPLAY_CATEGORIES_INLINE = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = False
HIDE_SIDEBAR = False
#HIDE_SIDEBAR_ON = ('index.html',
                   # 'am.html',
                   # 'science.html',
                   # 'did.html',
                   # 'read.html',
                   # 'do.html'
                   #)
INDEX_SAVE_AS = 'do.html'
BANNER = 'images/banner_small.png'
BANNER_ALL_PAGES = True
BANNER_SUBTITLE = 'Network Scientist'
PYGMENTS_STYLE = 'solarizedlight'
DISPLAY_ARTICLE_INFO_ON_INDEX = True
MENUITEMS = (
    # ('Who I am', '/am.html'),
    ('Home', '/index.html'),
    ('Projects', '/projects.html'),
    ('Publications', '/science.html'),
    # ('What I did', '/did.html'),
    # ('What I read', '/read.html'),
    # ('What I do', '/do.html')
)
