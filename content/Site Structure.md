---
title: "Site Structure"

---

see https://gohugo.io/content-management/sections/

1/. Organize content in the content folder/
Organize the content in your content folder the way you want it to be organized in your site.

2/. You can put complex HTML into the content pages, or just use Markdown, or a combination/
Below the front matter you can put HTML if you want. Alternativly simply rename the content file with an .html extension. HUGO treats them exactly the same except it won't try to change any of the html inside.

3/. Setup and use layouts to construct your final html pages/
I had been stumped how to construct list layouts for sub-sections since Hugo by default only recognizes a top folder as a section. For example, how would you construct a layout summarizing all of the articles under writing/history? However, the easy answer seems to be to use frontmatter./
a) First, assign each content page a type. Start broad, because Hugo's excellent abstraction abilities let you save being specific and narrow for when you need to be which is later. So start with setting type = "page" in content/writing/history.md (or content/writing/history.html). Then assign the content a layout, like layout = "page1"./
b) Then create a folder layouts/page and a layout at layouts/page/page1.html/
c) The layout can look like this:

{ { partial "header1.html" . }}

{ { partial "headerNAV.html" . }} - in the header, you can use things like {{ .Title }} and {{ .Params.___ }} to pull out things specific to the piece of content that were set in the front matter.

{ { Here is where you put your Go and HTML code to list the pieces of content you want to list, likely filtering by a custom parameter you set in the front matter and access with .Params.parameter. For example, you can list just pieces of content having to do with history.}}

{ { partial "footer.html" . }}

OR Say you don't need to list pieces of content. That is, on the [http://domain/writing/history/ 35](http://domain/writing/history/) page, you just want to write something and show images, all marked up in a lot of HTML and javascript. All of that HTML stays in the content file as per above (at content/writing/history.html for example). The Javascript goes in the footer partial. And the rendering layout (layouts/page/page1.html) just looks like this:

{ { partial "header1.html" . }}/
{ { partial "headerNAV.html" . }}/
{ { .Content }}/
{ { partial "footer.html" . }}

Remember: Keep things simple by using custom front matter parameters and accessing them in partials with .Params.____ so you don't have to use a lot of layouts. Then when you need, create a new layout and set it in the front matter with layout = "newlayout". Then when you have a lot of layouts, create a new type and a new type folder. Scale up in this order and you can have a complex site without too many layouts.

4/. Addressing relative links/
Most people here are probably much more experienced than I at HTML coding, but as I built out a site with many pages and subsections I stumbled on setting up links correctly. In case it's needed, I found it easier to set the basehref in the frontmatter of a bunch of files and that way I only need a single header1.html partial that includes the following line:

"<base href={ { .Params.basehref }}>"

Just passing it along as another useful way to use Hugo's variables and front matter.

To sum up:

1.  Files in /layout are layout files, chosen by some rules by Hugo to render content. Putting static files in here is very unusual, and you should know the whats.
2.  HTML files in /static ... is static, so what you put in the file is what gets published
3.  HTML files in /content:/
    -- if it has front matter (even only empty), it gets rendered as a content file with layout file, partials, shortcodes etc./
    -- if it does not have front matter, it behaves as it was placed in /static