---
layout: default
title: 首页
---
<h2>最近更新</h2>
<p>以下为三个专区的最新 10 条（按事件时间降序）。</p>

{% assign all = site.history | concat: site.entertainment | concat: site.metaphysics %}
{% assign approved = all | where: "verification_status","approved" %}
{% assign sorted = approved | sort: "date_event" | reverse %}
<ul>
{% for doc in sorted limit:10 %}
  <li>
    <strong>{{ doc.date_event }}</strong>
    — <a href="{{ doc.url | relative_url }}">{{ doc.title }}</a>
    <small>（{{ doc.area }} / {{ doc.type }}）</small>
  </li>
{% endfor %}
</ul>
