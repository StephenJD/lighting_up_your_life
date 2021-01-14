---
title: "Home Page"
---

This is in content/_index.md

Homepage is based on /themes/zen/layouts/index.html

Shows this content followed by summaries of "mainSections" specified in config.yaml

#### Menu and sidebar layouts [](https://themes.gohugo.io/hugo-theme-zen/#menu-and-sidebar-layouts)

The template will automatically add menu entries for the home page, each page in /content and each section, in that order.

A section is created by a folder under /content/ which also has sub-folders.

If it contains an _index.md then it creates a list-page listing the contents of that folder.

If instead it contains an index.md then it creates a single page with the contents of index.md. Other files are hidden.

If no index.md file exists then the contents of that folder are listed with the _index above it in the tree. The server needs restarting if an index is added to an existing folder.

Section-pages list the sub-pages (with summary content if defined in /layouts/_default/list.html).

If the folder has a _index.md file, its title is used as the menu item. otherwise the folder name is used.

If the default sidebar is activated it will display each section with all its pages listed below.

They are set up in `layouts/partials/menu.html`,
`layouts/partials/mobilmenu.html` 
and `layouts/partials/sidebar.html`.

### Site Organisation

To make _index pages list all nested pages, use the following code in /layouts/_default/list.html

`{{ define "main" -}}
`<main class="main layout__main">
`<h1 class="title">{{ .Title }}</h1>
`{{ $paginator := .Paginate (.Pages) -}}
`{{ range $paginator.Pages -}}
`<p><a href="{{ .Permalink }}">{{ .Title }}</a></p>
`{{ end -}}
`{{ partial "pagination.html" . }}
`</main>
`{{ end }}</pre>

see https://gohugo.io/content-management/sections/

To list other pages in the same folder as the current page create siblingPages.html in \layout\partials:

`<aside class="related layout__related">
`{{ $title := .Title }}
`<h3>{{ i18n "string_see_also" }}</h3>
`<ul>
`{{ range where .CurrentSection.Pages "Title" "!=" $title }}
`<li><a href="{{ .RelPermalink }}">{{ .Title }}</a></li>
`{{ end }}
`</ul>
`</aside>

To layouts/_default/single.html, before `<h1 class="title add `{{ partial "sibling-pages.html" . }}

To show breadcrumb navigation to current page create "breadcrumb-path.html" containing:

`<ol  class="nav navbar-nav">
`  {{ template "breadcrumbnav" (dict "p1" . "p2" .) }}
`</ol>
`{{/* .p1 is the previous folder each time round 
`	 .p2 is always the current page 
`*/}}
`{{ define "breadcrumbnav" }}
`{{ if .p1.Parent }}
`	{{ template "breadcrumbnav" (dict "p1" .p1.Parent "p2" .p2 ) }}
`{{ else if not .p1.IsHome }}
`	{{ template "breadcrumbnav" (dict "p1" .p1.Site.Home "p2" .p2 ) }}
`{{ end }}
`{{ if ne .p1 .p2 }}
`<span>
`  /<a href="{{ .p1.Permalink }}">{{ .p1.Title }}</a>
`</span>
`{{ end }}
`{{ end }}

To layouts/_default/single.html and list.html, before `<h1 class="title add `{{ partial "breadcrumb-path.html" . }}

### Layouts [](https://themes.gohugo.io/hugo-theme-zen/#layouts)

To customise a layout included in the zen theme, copy it to the root layout directory and edit it there. Make sure to maintain the directory structure inside the layouts directory.

Add any new layouts to the root layout directory as well. This way they will not be overwritten when updating the theme.

### Add anchor links to headers [](https://themes.gohugo.io/hugo-theme-zen/#add-anchor-links-to-headers)

You can add anchor links (links that appear when you hover over the end of heading text). To activate it copy the file
`~/theme/zen/layouts/_default/_markup/render-heading.html.example` 
to `layouts/_default/_markup/render-heading.html`.

Needed styles are in the `_zen.scss` file.

### Search
Add the shortcode `{{ < search > }} to a page. The search and flexsearch js files gets loaded automatically on pages that use the shortcode.

Your search page will now have a search field where all the posts of the site can be searched.

### Contact form [](https://themes.gohugo.io/hugo-theme-zen/#contact-form)
----------------------------------------------------------------------

If your server support php with the mail() command (very common) you can use the included contact form feature to get a contact form for your site.

1.  Copy the file `themes/zen/php/contact.php.example` to `static/php/contact.php`.
2.  Edit the contact.php file so it has your own e-mail address. You may also change the mail subject prefix.
3.  Add the shortcode `{{ < contact > }} to a page. The contact.js file gets loaded automatically on pages that use the shortcode.

If you have a SPF record for your domain, make sure the web server is listed or other mail server may mark the mail as spam.