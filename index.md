---
layout: default
title: 洪清档案
---

# 洪清档案

<div class="grid">
  <a class="card" href="{{ '/pages/history' | relative_url }}">
    <span class="badge">History</span>
    <h3>真实史料</h3>
    <p>有明确出处与考据价值的原始/次生文献。自动按事件时间排序。</p>
  </a>

  <a class="card" href="{{ '/pages/entertainment' | relative_url }}">
    <span class="badge">Entertainment</span>
    <h3>娱乐信息</h3>
    <p>影视/小说/游戏中的相关演绎，区分史实与艺术加工。</p>
  </a>

  <a class="card" href="{{ '/pages/metaphysics' | relative_url }}">
    <span class="badge">Metaphysics</span>
    <h3>玄学信息</h3>
    <p>命理、志怪、风水等材料与学术性讨论，强调来源与注释。</p>
  </a>
</div>

## 最近更新
<p class="meta">以下为三个专区的最新 10 条（按事件时间降序）。</p>

<div class="list">
<ul>
{% assign all = site.history | concat: site.entertainment | concat: site.metaphysics %}
{% assign approved = all | where: "verification_status","approved" %}
{% assign sorted = approved | sort: "date_event" | reverse %}
{% for doc in sorted limit:10 %}
  <li>
    <strong>{{ doc.date_event }}</strong> — 
    <a href="{{ doc.url | relative_url }}">{{ doc.title }}</a>
    <span class="meta">（{{ doc.area }} / {{ doc.type }}）</span>
  </li>
{% endfor %}
</ul>
</div>
