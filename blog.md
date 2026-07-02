---
layout: blog
title: "Blog | Jiarui Zhang"
permalink: /blog/
---

# Blog

Technical notes on machine learning systems, theory, and infrastructure.
{: .tagline }

{% for post in site.posts %}
<section class="post">

  <h2><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h2>

<p class="meta">
  Published {{ post.date | date: "%B %-d, %Y" }}
  {% assign published = post.date | date: "%Y-%m-%d" %}
  {% assign updated = post.updated | date: "%Y-%m-%d" %}
  {% if post.updated and updated != published %}
    - Updated {{ post.updated | date: "%B %-d, %Y" }}
  {% endif %}
  {% if post.tags and post.tags.size > 0 %}
    - {{ post.tags | join: ", " }}
  {% endif %}
</p>

  <p class="summary">{{ post.summary }}</p>

</section>
{% endfor %}
