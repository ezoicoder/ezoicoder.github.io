---
layout: home
title: "Jiarui Zhang 张家瑞"
---

![Jiarui Zhang]({{ '/assets/portrait.png' | relative_url }}){: .portrait }

# Jiarui Zhang <span class="name-cn">张家瑞</span>
{: .home-title }

Undergraduate @ Yao Class, Tsinghua University
{: .tagline }

Beijing, China
{: .contact-line }

jiarui-z23@mails.tsinghua.edu.cn
{: .contact-line }

[Download Resume]({{ '/assets/resume.pdf' | relative_url }}){: .button download="download" }
[Blog]({{ '/blog/' | relative_url }}){: .text-link }
{: .actions }

## About Me

I am a fourth-year undergraduate researcher interested in AI infrastructure and ML systems.
I am currently conducting research under the supervision of
[Binhang Yuan](https://binhangyuan.github.io/site/) on efficient systems for
large language model training and inference, with recent work on Tree Attention and
distributed training for multi-turn reinforcement learning. Before that, I conducted research
under the supervision of [Yi Wu](https://jxwuyi.weebly.com/) on reinforcement
learning systems.
{: .about }

## Publications

<section class="publication">
  <span class="badge">ICML 2026 Accepted</span>

  <h3>AREAL-DTA: Dynamic Tree Attention for Efficient Reinforcement Learning of Large Language Models</h3>

<p class="meta">
  <strong>Jiarui Zhang*</strong>, Yuchen Yang*, Ran Yan*, Zhiyu Mei, Liyuan Zhang, Daifeng Li,
  Wei Fu, Jiaxuan Gao, Shusheng Xu, Yi Wu, Binhang Yuan.
</p>

<p class="paper-links">
  <a href="https://arxiv.org/abs/2602.00482">Paper</a>
  <a href="https://github.com/areal-project/AReaL/tree/feat/dta">Code</a>
</p>
</section>

<section class="publication">
  <span class="badge">arXiv preprint</span>

  <h3>D<sup>2</sup>SD: Accelerating Speculative Decoding with Dual Diffusion Draft Models</h3>

<p class="meta">
  Liyuan Zhang, <strong>Jiarui Zhang</strong>, Jinwei Yao, Ran Yan, Yuchen Yang,
  Jiahao Zhang, Tongkai Yang, Yi Wu, Binhang Yuan.
</p>

<p class="paper-links">
  <a href="https://arxiv.org/abs/2606.04446">Paper</a>
</p>
</section>

## Blog

{% for post in site.posts limit: 3 %}
<section class="blog-post">

  <h3><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h3>

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

  <p class="detail">{{ post.summary }}</p>

</section>
{% endfor %}
