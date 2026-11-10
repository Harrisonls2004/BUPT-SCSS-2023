(() => {
  'use strict';
  const data = window.COURSE_DATA;
  const $ = (selector) => document.querySelector(selector);
  const escape = (text) => String(text).replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const shortSemester = (name) => name.split('-')[0];
  const formatSize = (bytes) => bytes >= 1073741824 ? `${(bytes / 1073741824).toFixed(1)} GB` : bytes >= 1048576 ? `${(bytes / 1048576).toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1024))} KB`;
  const repo = `https://github.com/${data.repository}`;
  const fileUrl = (path, raw = false) => `${raw ? `https://raw.githubusercontent.com/${data.repository}/${data.branch}` : `${repo}/blob/${data.branch}`}/${path.split('/').map(encodeURIComponent).join('/')}`;
  const courseMap = new Map(data.courses.map((course) => [course.id, course]));
  const state = {q: '', semester: '', category: '', type: '', course: '', mode: 'courses', sort: 'latest', page: 1};
  const pageSize = 20;
  document.querySelectorAll('[data-repo]').forEach((link) => { link.href = repo; });
  document.querySelectorAll('[data-issues]').forEach((link) => { link.href = `${repo}/issues`; });
  const totalSize = data.files.reduce((sum, file) => sum + file.size, 0);
  $('#stats').innerHTML = [[data.semesters.filter((semester) => semester !== '英语体育公选课').length, '个学期 · 持续积累'], [data.courses.length, '门课程与选课指南'], [data.files.length.toLocaleString(), '份资料 · 开放共享'], [formatSize(totalSize), '学习资源 · 共同建设']].map(([number, label]) => `<div class="stat"><strong>${number}</strong><span>${label}</span></div>`).join('');
  $('#semester-grid').innerHTML = data.semesters.map((semester, index) => {
    const courses = data.courses.filter((course) => course.semester === semester);
    return `<button class="semester-card" data-semester="${escape(semester)}"><span class="semester-number">${String(index + 1).padStart(2, '0')} / ${semester === '英语体育公选课' ? 'GUIDE' : index === 6 ? 'PRACTICE' : 'SEMESTER'}</span><span class="arrow">↗</span><h3>${shortSemester(semester)}</h3><p>${semester === '英语体育公选课' ? '英语、体育与公选课选课经验' : `${courses.length} 门课程 · ${courses.reduce((sum, course) => sum + course.count, 0)} 份资料`}</p></button>`;
  }).join('');
  function courseCard(course, count = course.count) {
    return `<button class="course-card" data-course="${escape(course.id)}"><span class="course-icon" aria-hidden="true">${course.name.includes('数学') ? '∑' : '{ }'}</span><div><small>${shortSemester(course.semester)}</small><h3>${escape(course.name)}</h3><p>${count} 份资料 ${course.overview ? '· 含课程介绍与学习经验' : '· 课程学习资料合集'}</p></div><span class="arrow" aria-hidden="true">↗</span></button>`;
  }
  const featuredNames = ['数据结构', '操作系统', '计算机网络', '现代密码学', '高等数学A上', '编译原理与技术'];
  $('#featured-courses').innerHTML = featuredNames.map((name) => data.courses.find((course) => course.name === name)).filter(Boolean).map((course) => courseCard(course)).join('');
  $('#semester-filters').innerHTML = ['', ...data.semesters].map((semester) => `<button class="filter-button" data-filter-semester="${escape(semester)}">${semester ? shortSemester(semester) : '全部学期'}<span>${semester ? data.courses.filter((course) => course.semester === semester).length : data.courses.length}</span></button>`).join('');
  function updateCourseOptions() {
    const courses = data.courses.filter((course) => !state.semester || course.semester === state.semester);
    $('#course-select').innerHTML = '<option value="">全部课程</option>' + courses.map((course) => `<option value="${escape(course.id)}">${escape(course.name)}</option>`).join('');
    $('#course-select').value = state.course;
  }
  const markdownFiles = new Map(data.files.filter((file) => typeof file.markdown === 'string').map((file) => [file.path, file]));
  function renderMarkdown(container, source, sourcePath) {
    container.innerHTML = DOMPurify.sanitize(marked.parse(source, {gfm: true}), {USE_PROFILES: {html: true}, FORBID_TAGS: ['style'], FORBID_ATTR: ['style']});
    container.querySelectorAll('a[href]').forEach((link) => {
      const href = link.getAttribute('href');
      if (href.startsWith('#')) {
        link.href = fileUrl(sourcePath) + href;
      } else {
        try {
          const url = new URL(href, fileUrl(sourcePath));
          if (!['https:', 'http:', 'mailto:'].includes(url.protocol)) { link.removeAttribute('href'); return; }
          link.href = url.href;
          const prefix = `/${data.repository}/blob/${data.branch}/`;
          if (url.hostname === 'github.com' && url.pathname.startsWith(prefix)) {
            const path = decodeURIComponent(url.pathname.slice(prefix.length));
            if (markdownFiles.has(path) && !url.hash) link.dataset.markdown = path;
          }
        } catch { link.removeAttribute('href'); return; }
      }
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
    });
    container.querySelectorAll('img[src]').forEach((image) => {
      try {
        const url = new URL(image.getAttribute('src'), fileUrl(sourcePath, true));
        if (!['http:', 'https:'].includes(url.protocol)) { image.remove(); return; }
        image.src = url.href;
        image.loading = 'lazy';
      } catch { image.remove(); }
    });
    container.querySelectorAll('table').forEach((table) => {
      const headings = [...table.querySelectorAll('thead th')].map((cell) => cell.textContent.trim());
      if (headings.join('|') === '项目|内容') table.classList.add('course-facts');
      const wrapper = document.createElement('div');
      wrapper.className = 'table-scroll';
      table.before(wrapper);
      wrapper.append(table);
    });
  }
  function openMarkdown(path) {
    const file = markdownFiles.get(path);
    if (!file) return;
    $('#markdown-title').textContent = `${courseMap.get(file.course).name} / ${file.name}`;
    renderMarkdown($('#markdown-content'), file.markdown, path);
    const dialog = $('#markdown-dialog');
    if (!dialog.open) openDialog(dialog);
    else dialog.scrollTop = 0;
  }
  const typeCounts = new Map();
  data.files.forEach((file) => typeCounts.set(file.type, (typeCounts.get(file.type) || 0) + 1));
  $('#file-type').insertAdjacentHTML('beforeend', [...typeCounts].sort((a, b) => b[1] - a[1]).map(([type, count]) => `<option value="${escape(type)}">${escape(type)} (${count})</option>`).join(''));
  function filteredFiles() {
    const terms = state.q.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    return data.files.filter((file) => (!state.course || file.course === state.course) && (!state.semester || file.semester === state.semester) && (!state.category || file.category === state.category) && (!state.type || file.type === state.type) && terms.every((term) => `${file.path} ${file.category}`.toLocaleLowerCase().includes(term)));
  }
  function iconColor(type) { return type === 'PDF' ? 'red' : ['DOC','DOCX'].includes(type) ? 'blue' : ['PPT','PPTX'].includes(type) ? 'orange' : ['XLS','XLSX'].includes(type) ? 'green' : ['PNG','JPG','JPEG','GIF'].includes(type) ? 'cyan' : ''; }
  function fileRow(file) {
    const course = courseMap.get(file.course);
    return `<article class="file-row"><span class="file-badge ${iconColor(file.type)}">${escape(file.type.slice(0, 7))}</span><div class="file-info"><h3>${escape(file.name)}</h3><p>${escape(course.name)} · ${shortSemester(file.semester)} · ${file.category} · ${formatSize(file.size)}</p></div><div class="file-actions">${markdownFiles.has(file.path) ? `<button data-markdown="${escape(file.path)}">阅读文档</button>` : ''}<a href="${fileUrl(file.path)}" target="_blank" rel="noopener noreferrer" aria-label="在 GitHub 查看 ${escape(file.name)}">GitHub ↗</a><a href="${fileUrl(file.path, true)}" target="_blank" rel="noopener noreferrer" aria-label="打开原文件 ${escape(file.name)}">原文件 ↓</a></div></article>`;
  }
  const byLatest = (a, b) => (b.updated || '').localeCompare(a.updated || '') || a.path.localeCompare(b.path, 'zh-CN');
  function renderResults() {
    const files = filteredFiles().sort(state.sort === 'name' ? (a, b) => a.name.localeCompare(b.name, 'zh-CN') : state.sort === 'size' ? (a, b) => b.size - a.size : byLatest);
    const counts = new Map();
    files.forEach((file) => counts.set(file.course, (counts.get(file.course) || 0) + 1));
    const courses = data.courses.filter((course) => counts.has(course.id));
    const items = state.mode === 'courses' ? courses : files;
    const pages = Math.max(1, Math.ceil(items.length / pageSize));
    state.page = Math.min(pages, Math.max(1, state.page));
    $('#result-count').textContent = `${courses.length} 门课程 · ${files.length.toLocaleString()} 份资料${state.q ? ` · “${state.q}”` : ''}`;
    $('#query').value = state.q;
    $('#category').value = state.category;
    $('#file-type').value = state.type;
    $('#view-mode').value = state.mode;
    $('#sort-order').value = state.sort;
    document.querySelectorAll('[data-filter-semester]').forEach((button) => {
      const active = button.dataset.filterSemester === state.semester;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    updateCourseOptions();
    const visible = items.slice((state.page - 1) * pageSize, state.page * pageSize);
    $('#results').innerHTML = !items.length ? '<div class="empty-state"><strong>暂时没有找到相关资料</strong><p>试试更短的关键词，或清除学期与格式筛选。</p><button class="primary-button" data-reset>清除全部筛选</button></div>' : state.mode === 'courses' ? `<div class="course-grid">${visible.map((course) => courseCard(course, counts.get(course.id))).join('')}</div>` : `<div class="file-list">${visible.map(fileRow).join('')}</div>`;
    $('#pagination').innerHTML = pages > 1 ? `<button data-page="${state.page - 1}" ${state.page === 1 ? 'disabled' : ''}>上一页</button><span>${state.page} / ${pages}</span><button data-page="${state.page + 1}" ${state.page === pages ? 'disabled' : ''}>下一页</button>` : '';
  }
  function libraryLink(changes = {}) {
    const next = {...state, ...changes};
    const params = new URLSearchParams();
    for (const key of ['q', 'semester', 'course', 'category', 'type']) if (next[key]) params.set(key, next[key]);
    if (next.mode !== 'courses') params.set('mode', next.mode);
    if (next.sort !== 'latest') params.set('sort', next.sort);
    if (next.page > 1) params.set('page', next.page);
    return `#library${params.size ? `?${params}` : ''}`;
  }
  function navigate(changes) { window.location.hash = libraryLink({...changes, page: changes.page || 1}); }
  function route() {
    const hash = location.hash || '#home';
    const isLibrary = hash.startsWith('#library');
    $('#home-view').hidden = isLibrary;
    $('#library-view').hidden = !isLibrary;
    document.querySelectorAll('[data-nav]').forEach((link) => link.classList.toggle('active', link.dataset.nav === (isLibrary ? 'library' : 'home')));
    if (isLibrary) {
      const params = new URLSearchParams(hash.split('?')[1] || '');
      state.q = params.get('q') || '';
      state.semester = data.semesters.includes(params.get('semester')) ? params.get('semester') : '';
      state.category = [...$('#category').options].some((option) => option.value === params.get('category')) ? params.get('category') : '';
      state.type = typeCounts.has(params.get('type')) ? params.get('type') : '';
      state.course = courseMap.has(params.get('course')) && (!state.semester || courseMap.get(params.get('course')).semester === state.semester) ? params.get('course') : '';
      state.mode = ['files','list'].includes(params.get('mode')) ? 'list' : 'courses';
      state.sort = ['name','size'].includes(params.get('sort')) ? params.get('sort') : 'latest';
      state.page = Math.max(1, Number.parseInt(params.get('page'), 10) || 1);
      renderResults();
      document.title = `${state.q || (state.semester ? shortSemester(state.semester) : '资料大厅')} · BUPT 学习资料库`;
    } else { document.title = 'BUPT 学习资料库 · 网安 2023'; }
    if (hash === '#home' || isLibrary) window.scrollTo({top:0, behavior:'instant'});
  }
  const dialogFocus = new WeakMap();
  function openDialog(dialog) { dialogFocus.set(dialog, document.activeElement); dialog.showModal(); }
  function openCourse(id) {
    const course = courseMap.get(id);
    if (!course) return;
    const files = data.files.filter((file) => file.course === id);
    $('#course-detail').innerHTML = `<h2>${escape(course.name)}</h2><p class="dialog-meta">${shortSemester(course.semester)} · ${course.count} 份资料</p>${course.overview ? '<h3>课程介绍与学习经验</h3><div class="overview markdown-body"></div>' : ''}<div class="dialog-files-title"><h3>课程资料 · 前 ${Math.min(files.length, 30)} 份</h3><a class="text-link" href="${libraryLink({q: '', semester: course.semester, course: course.id, category: '', type: '', mode: 'list', page: 1})}" data-dismiss>查看全部资料与筛选 ↗</a></div><div class="file-list">${files.slice(0, 30).map(fileRow).join('')}</div>`;
    if (course.overview) renderMarkdown($('#course-detail .overview'), course.overview, course.overviewPath || `${course.id}/README.md`);
    openDialog($('#course-dialog'));
  }
  document.addEventListener('click', (event) => {
    const button = event.target.closest('button, a');
    if (!button) return;
    if (button.hasAttribute('data-semester')) {
      navigate({semester:button.dataset.semester,q:'',course:'',category:'',type:'',mode:'courses'});
    }
    if (button.hasAttribute('data-filter-semester')) navigate({semester:button.dataset.filterSemester,course:''});
    if (button.hasAttribute('data-markdown')) { event.preventDefault(); openMarkdown(button.dataset.markdown); }
    if (button.hasAttribute('data-query')) navigate({q:button.dataset.query,semester:'',course:'',category:'',type:'',mode:'courses'});
    if (button.hasAttribute('data-course')) openCourse(button.dataset.course);
    if (button.hasAttribute('data-page')) { navigate({page:Number(button.dataset.page)}); }
    if (button.hasAttribute('data-reset') || button.id === 'reset') navigate({q:'',semester:'',course:'',category:'',type:'',mode:'courses',sort:'latest'});
    if (button.hasAttribute('data-close') || button.hasAttribute('data-dismiss')) button.closest('dialog').close();
  });
  $('#hero-search').addEventListener('submit', (event) => { event.preventDefault(); navigate({q:$('#home-query').value.trim(),semester:'',course:'',category:'',type:'',mode:'courses'}); });
  $('#library-search').addEventListener('submit', (event) => { event.preventDefault(); navigate({q:$('#query').value.trim()}); });
  for (const [selector,key] of [['#category','category'],['#file-type','type'],['#view-mode','mode'],['#course-select','course'],['#sort-order','sort']]) $(selector).addEventListener('change', (event) => navigate({[key]:event.target.value}));
  $('#contribute-open').addEventListener('click', () => openDialog($('#contribute-dialog')));
  document.querySelectorAll('dialog').forEach((dialog) => {
    dialog.addEventListener('click', (event) => { if (event.target === dialog) { const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close(); } });
    dialog.addEventListener('close', () => dialogFocus.get(dialog)?.focus());
  });
  function updateThemeButton() {
    const dark = document.documentElement.dataset.theme === 'dark';
    $('#theme').setAttribute('aria-label', dark ? '切换浅色模式' : '切换深色模式');
    $('#theme').title = dark ? '切换浅色模式' : '切换深色模式';
    $('#theme').setAttribute('aria-pressed', String(dark));
  }
  $('#theme').addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('bupt-theme',theme); } catch {}
    updateThemeButton();
  });
  document.addEventListener('keydown', (event) => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); if (!document.querySelector('dialog[open]')) ($('#library-view').hidden ? $('#home-query') : $('#query')).focus(); } });
  window.addEventListener('hashchange', route);
  updateThemeButton();
  route();
})();
