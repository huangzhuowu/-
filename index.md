---
layout: default
title: 洪清档案
---

<div class="title-wrap">
  <h1>洪清档案</h1>
  <div class="title-underline"></div>
</div>

<a id="history"></a>
<div class="subhero history">
  <h1><span class="badge-dot history"></span>真实史料</h1>
  <p>仅展示 <code>verification_status: approved</code> 的条目；按 <strong>事件时间</strong> 升序排列。</p>
</div>

{%- assign history_items = site.history | where: "verification_status","approved" | sort: "date_event" -%}
<div class="list-cards">
  {%- for doc in history_items -%}
  <div class="entry">
    <div class="top">
      <div class="date">{{ doc.date_event | default: "未知时间" }}</div>
      <div class="title"><a href="{{ doc.url | relative_url }}">{{ doc.title }}</a></div>
      <div class="pills">
        <span class="pill">history / {{ doc.type }}</span>
        {%- if doc.tags -%}{% for t in doc.tags limit:2 %}<span class="pill sec">{{ t }}</span>{% endfor %}{%- endif -%}
      </div>
    </div>
    <div class="meta">
      出处：
      {%- if doc.source_url -%}<a href="{{ doc.source_url }}">{{ doc.source_title }}</a>{%- else -%}{{ doc.source_title }}{%- endif -%}
      {%- if doc.location -%} · 地点：{{ doc.location }}{%- endif -%}
      {%- if doc.source_author -%} · 作者：{{ doc.source_author }}{%- endif -%}
    </div>
  </div>
  {%- endfor -%}
</div>

<a id="entertainment"></a>
<div class="subhero ent" style="margin-top:28px">
  <h1><span class="badge-dot ent"></span>娱乐信息</h1>
  <p>仅展示 <code>verification_status: approved</code> 的条目；按 <strong>事件时间</strong> 降序展示近期内容。</p>
</div>

{%- assign ent_items = site.entertainment | where: "verification_status","approved" | sort: "date_event" | reverse -%}
<div class="list-cards">
  {%- for doc in ent_items -%}
  <div class="entry">
    <div class="top">
      <div class="date">{{ doc.date_event | default: "未知时间" }}</div>
      <div class="title"><a href="{{ doc.url | relative_url }}">{{ doc.title }}</a></div>
      <div class="pills">
        <span class="pill sec">entertainment / {{ doc.type }}</span>
        {%- if doc.tags -%}{% for t in doc.tags limit:2 %}<span class="pill sec">{{ t }}</span>{% endfor %}{%- endif -%}
      </div>
    </div>
    <div class="meta">
      出处：
      {%- if doc.source_url -%}<a href="{{ doc.source_url }}">{{ doc.source_title }}</a>{%- else -%}{{ doc.source_title }}{%- endif -%}
      {%- if doc.location -%} · 地点：{{ doc.location }}{%- endif -%}
      {%- if doc.source_author -%} · 作者：{{ doc.source_author }}{%- endif -%}
    </div>
  </div>
  {%- endfor -%}
</div>

<a id="metaphysics"></a>
<div class="subhero meta" style="margin-top:28px">
  <h1><span class="badge-dot meta"></span>玄学信息</h1>
  <p>仅展示 <code>verification_status: approved</code> 的条目；按 <strong>事件时间</strong> 降序展示。</p>
</div>

{%- assign meta_items = site.metaphysics | where: "verification_status","approved" | sort: "date_event" | reverse -%}
<div class="list-cards">
  {%- for doc in meta_items -%}
  <div class="entry">
    <div class="top">
      <div class="date">{{ doc.date_event | default: "未知时间" }}</div>
      <div class="title"><a href="{{ doc.url | relative_url }}">{{ doc.title }}</a></div>
      <div class="pills">
        <span class="pill meta">metaphysics / {{ doc.type }}</span>
        {%- if doc.tags -%}{% for t in doc.tags limit:2 %}<span class="pill meta">{{ t }}</span>{% endfor %}{%- endif -%}
      </div>
    </div>
    <div class="meta">
      出处：
      {%- if doc.source_url -%}<a href="{{ doc.source_url }}">{{ doc.source_title }}</a>{%- else -%}{{ doc.source_title }}{%- endif -%}
      {%- if doc.location -%} · 地点：{{ doc.location }}{%- endif -%}
      {%- if doc.source_author -%} · 作者：{{ doc.source_author }}{%- endif -%}
    </div>
  </div>
  {%- endfor -%}
</div>
