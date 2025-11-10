---
layout: default
title: 洪清档案
---
<div class="filters" id="filters">
  <div class="group">
    <label>🔎 搜索</label>
    <input id="q" type="text" placeholder="按标题关键字过滤…" />
  </div>
  <div class="group">
    <label>📅 年份</label>
    <select id="year">
      <option value="">全部年份</option>
      <!-- 年份选项会在脚本中自动填充 -->
    </select>
  </div>
  <small>提示：三栏同时过滤，仅匹配“时间 + 标题”。</small>
</div>

<div class="triple-grid">

  <!-- 真实史料（红） -->
  <section class="column history" id="history">
    <div class="col-head">
      <div class="bar"></div><h2>真实史料</h2>
    </div>
    <ul class="mini-list">
      {%- assign history_items = site.history | where: "verification_status","approved" | sort: "date_event" -%}
      {%- for doc in history_items -%}
      <li class="mini-row">
        <span class="date">{{ doc.date_event }}</span>
        <a href="{{ doc.url | relative_url }}">{{ doc.title }}</a>
      </li>
      {%- endfor -%}
    </ul>
  </section>

  <!-- 文学娱乐（蓝） -->
  <section class="column ent" id="entertainment">
    <div class="col-head">
      <div class="bar"></div><h2>文学娱乐</h2>
    </div>
    <ul class="mini-list">
      {%- assign ent_items = site.entertainment | where: "verification_status","approved" | sort: "date_event" -%}
      {%- for doc in ent_items -%}
      <li class="mini-row">
        <span class="date">{{ doc.date_event }}</span>
        <a href="{{ doc.url | relative_url }}">{{ doc.title }}</a>
      </li>
      {%- endfor -%}
    </ul>
  </section>

  <!-- 玄学推背（绿） -->
  <section class="column meta" id="metaphysics">
    <div class="col-head">
      <div class="bar"></div><h2>玄学推背</h2>
    </div>
    <ul class="mini-list">
      {%- assign meta_items = site.metaphysics | where: "verification_status","approved" | sort: "date_event" -%}
      {%- for doc in meta_items -%}
      <li class="mini-row">
        <span class="date">{{ doc.date_event }}</span>
        <a href="{{ doc.url | relative_url }}">{{ doc.title }}</a>
      </li>
      {%- endfor -%}
    </ul>
  </section>

</div>

<script>
(function(){
  const $ = (sel, root=document) => root.querySelector(sel);
  const $$ = (sel, root=document) => Array.from(root.querySelectorAll(sel));

  // 收集所有行，并为每行打上所属栏目与年份标签
  const rows = [];
  [["history","#history"],["entertainment","#entertainment"],["metaphysics","#metaphysics"]]
    .forEach(([area, anchor])=>{
      const list = $(`${anchor} .mini-list`);
      $$('.mini-row', list).forEach(li=>{
        const dateText = $('.date', li)?.textContent.trim() || "";
        const year = (dateText.match(/^(\d{4})/)||[])[1] || "";
        li.dataset.area = area;
        li.dataset.year = year;
        rows.push(li);
      });
    });

  // 动态填充年份下拉：从所有条目年份里取去重排序
  const years = Array.from(new Set(rows.map(r=>r.dataset.year).filter(Boolean)))
                    .sort((a,b)=>a.localeCompare(b));
  const yearSel = $('#year');
  years.forEach(y=>{
    const opt = document.createElement('option');
    opt.value = y; opt.textContent = y;
    yearSel.appendChild(opt);
  });

  // 过滤逻辑
  const qInput = $('#q');
  function applyFilter(){
    const q = qInput.value.trim().toLowerCase();
    const y = yearSel.value;
    // 逐行过滤
    rows.forEach(li=>{
      const title = li.querySelector('a')?.textContent.toLowerCase() || "";
      const inYear = !y || li.dataset.year === y;
      const inQuery = !q || title.includes(q);
      li.classList.toggle('hidden', !(inYear && inQuery));
    });
    // 更新每列计数
    ["history","entertainment","metaphysics"].forEach(area=>{
      const all = rows.filter(r=>r.dataset.area===area);
      const vis = all.filter(r=>!r.classList.contains('hidden')).length;
      const counter = document.querySelector(`.counter[data-counter-for="${area}"]`);
      if (counter) counter.textContent = `共 ${vis} 条`;
    });
  }
  qInput.addEventListener('input', applyFilter);
  yearSel.addEventListener('change', applyFilter);
  applyFilter();
})();
</script>
