---
layout: default
title: 洪清档案
---

<div class="title-wrap">
  <h1>洪清档案</h1>
  <div class="title-underline"></div>
</div>

<div class="grid">
  <a class="card history" href="{{ '/pages/history' | relative_url }}">
    <div class="topline"></div>
    <h3>真实史料</h3>
    <p>有明确出处与考据价值的原始/次生文献。自动按事件时间排序。<br>
    记录官方档案、私人笔记、信件等第一手资料，以及经由专业整理与分析的二手资料。</p>
  </a>

  <a class="card ent" href="{{ '/pages/entertainment' | relative_url }}">
    <div class="topline"></div>
    <h3>娱乐信息</h3>
    <p>影视、小说、游戏中的洪清题材演绎，区分史实与艺术加工。<br>
    探索文化表达与历史真实之间的关系，帮助读者辨析虚构与事实。</p>
  </a>

  <a class="card meta" href="{{ '/pages/metaphysics' | relative_url }}">
    <div class="topline"></div>
    <h3>玄学信息</h3>
    <p>命理、志怪、风水等材料与学术性讨论，强调来源与注释。<br>
    收录古籍整理与现代学术研究，关注文化现象的历史脉络与可信度。</p>
  </a>
</div>

<div class="section">
  <h2>最近更新</h2>
  <ul class="list">
  {% assign all = site.history | concat: site.entertainment | concat: site.metaphysics %}
  {% assign approved = all | where: "verification_status","approved" %}
  {% assign sorted = approved | sort: "date_event" | reverse %}
  {% for doc in sorted limit:10 %}
    <li class="row">
      <span class="date">{{ doc.date_event }}</span>
      <a href="{{ doc.url | relative_url }}">{{ doc.title }}</a>
      <span class="badges">
        <span class="badge {% if doc.area == 'history' %}h{% endif %}{% if doc.area == 'metaphysics' %} m{% endif %}">{{ doc.area }} / {{ doc.type }}</span>
      </span>
    </li>
  {% endfor %}
  </ul>
</div>
