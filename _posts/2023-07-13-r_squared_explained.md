---
layout: post
title: R-Squared Explained
date: 2023-07-11 08:57:00-0400
description: R-Squared Explained
tags: general
categories: machine-learning
# thumbnail: assets/img/9.jpg
featured: false
related_posts: false
---

{::nomarkdown}
{% assign jupyter_path = "assets/jupyter/r_squared_explained.ipynb" | relative_url %}
{% capture notebook_exists %}{% file_exists assets/jupyter/r_squared_explained.ipynb %}{% endcapture %}
{% if notebook_exists == "true" %}
    {% jupyter_notebook jupyter_path %}
{% else %}
    <p>Sorry, the notebook you are looking for does not exist.</p>
{% endif %}
{:/nomarkdown}