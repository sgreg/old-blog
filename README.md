# An old blog

## Disclaimer

This repository is an ancient web project requiring EOL components that simply shouldn't be ran by anyone anymore, anywhere. Anyhow, I'm also weirdly proud to have actually done this, and all the things of questionable practical use I've learned along the way. So for the sake of preserving the history (with all its lack of tests, commenting, and common sense), I decided to resurrect it and publish its source code - something I didn't dare to back in the day when this was actually running live.

## Background
### History

The year is 2016, I recently began publishing my electronics tinkerings with content going on several platforms, and I wanted to collect it all under a single domain. It's been years since I built some personal website with CMS and all, so that seemed like a good project on the side. Of course, 2016 me was all about "real nerds build their own stuff!", so using some ready-made system just wasn't an option, it had to be handmade from scratch. And in Python!

As this was all a fresh idea that may or may not take off, I didn't want to commit too hard on it and chose a cheap, no-frills web hosting plan to start with. The result was raw CGI with a Python 2 interpreter and nothing but a handful of external modules (like `python-mysqldb`), running on Apache (luckily with `.htaccess` possibility), and one MySQL database. Well, things don't get much more from-scratch than that, so perfect.

Eventually I moved on to a VPS, as things just got too limiting for other projects. However, by that time, the site has become pretty stale, and I mostly kept it around just for the sake of it, and because some external links pointed to the content. So there was no real reason to invest time other than setting up nginx and uWSGI and keep it running as-is.

And then it was gone, and life moved on.

### Present

In an attempt to rekindle the spark that got me creating it in the first, I decided to go digging in my backups and get it up and running again. Just not as active, editable CMS anymore, but as a static snapshot. Still, for that to happen, I had to get the initial code set up. Python 2 code, originally running on a Debian Jessie distribution. Both have been end-of-life for years, and while you get Docker images for the latter, its package repository isn't available anymore.

The good news, the Linux distro itself isn't really relevant, as long as Python 2, `python-mysqldb`, and MySQL server is available, I should manage to set it all up. After some trial and error, Ubuntu 18.04 LTS ended up fitting the bill.

Once it was up and running locally, `wget -m` mirrored the whole page in static HTML, which is now running on http://sgreg.craplab.fi.

## Repository

### Website source code

The full glory of the CMS and all is in the `src/` directory, with the original Apache `.htaccess` configuration found in `src/www/`. Have fun.

### Docker

Everything else is pretty much for the Docker setup, the `Dockerfile`, configurations for nginx and uWSGI in `etc/`, database setup in `db/` (including the whole content dump of the original database)

As the primary intention is to just mirror the original content as static HTML pages and not actually run the code in a dockerized environment, it's purposely designed to be in a single image rather than orchestrated with external database image, volumes, etc. In other words, DO NOT use this `Dockerfile` as template for your own web projects!

## How things worked

### Tech stack

- vanilla Python 2 behind the scenes
  - `python-mysqldb` as only external installed package
  - [`mistune`](https://github.com/lepture/mistune/) Markdown parser (src/engine/ext/mistune.py) \*
  - [`quik`](https://github.com/avelino/quik) template engine (src/engine/ext/quik.py) \*
- MySQL database
  - no ORM, raw SQL handling \*\*
- vanilla fronted
  - handwritten HTML templates
  - handwritten main CSS (src/css/sgreg-1.0.6.css)
  - [`normalize.css`](https://github.com/necolas/normalize.css) \*
  - [Font Awesome 4](https://fontawesome.com/v4/icons/)
  - additional own font-sgreg for icons font awesome was missing
  - [`prism.js`](https://github.com/PrismJS/prism) for syntax highlighting (src/js/prims.js) \*



\* fine, some parts I didn't insist on writing from scratch and went with 3rd party options  
\*\* weird flex, I know :#  

### Funcionality

#### Content

Entry point: `index.sg` with main arrangements are done via `.htaccess` / nginx config to rewrite paths as parameters passed to it. 

E.g.
```
# Apache src/www/.htaccess
RewriteRule ^blog/([a-zA-Z]*)/?([a-zA-Z0-9+\-_]*/?[0-9]*)/?$ index.sg?page=blog&filter=$1&content=$2

# nginx etc/nginx/sites-available/sgreg.fi
rewrite ^/blog/([a-zA-Z]*)/?([a-zA-Z0-9+\-_]*/?[0-9]*)/?$ /index.sg?page=blog&filter=$1&content=$2 last;
```

Example: `/blog/article/random-article` -> `index.sg?page=blog&filter=article&content=random-article`

Code path from here is
1. Entry point creating [`PageBuilder`](src/engine/builder.py)
1. `PageBuilder` finds "`?page=blog`", creates [`BlogPage`](src/engine/content/blog.py)
1. `BlogPage` finds "`&filter=article`"
1. `BlogPage` makes sure there's also non-empty "`&content=...`", finds `"random-article"`
1. `BlogPage` looks up database for blog article with `random-article` as title and displays it if found, 404 otherwise otherwise


#### Content Management

Entry point: `uberuser.sg`, Basic Auth via `.htpasswd` setup

- Blog articles handling
  - add, modify, delete, (un)publish
  - add and modify tags and categories
- Project handling
  - add and modify projects
  - add, modify, delete, (un)publish project pages
- Static content handling
  - modifiy _About_ page

All content is written and handled in Markdown with the CMS. When saved, it gets converted to HTML and the website itself only uses the HTML version, as writing happens a lot less than displaying, so it felt pointless to always convert it on the fly. Database stores therefore both the Markdown and HTML version.

Whole management implementation is in `src/engine/admin.py` and was targeted to a single user who knows what they're doing. In other words, looks like crap and is likely to break easily.