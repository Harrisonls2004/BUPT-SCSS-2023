# 北邮网安课程资料网页

## 本地预览

在仓库根目录执行：

```sh
python3 scripts/serve_site.py
```

打开 http://localhost:4173 。修改课程 README 后刷新网页，预览服务会自动重新生成资料索引，并禁用浏览器缓存。可以用 `--port 4174` 指定其他端口。

发布前可单独执行 `python3 scripts/build_site.py`。课程索引随代码附带，也可以直接打开 `site/index.html`；直接打开文件时，修改 README 后需要手动重新生成索引。构建脚本会为资料、脚本和样式附上内容版本号，避免页面继续使用旧缓存。

## 功能

- 首页展示真实课程、学期资料数量与文件总大小，独立的英语、体育与公选课指南入口。
- 按关键词、学期、资料分类、文件格式查找，支持课程目录 / 文件列表两种视图及分页，提供按提交日期、文件名和大小排序。
- 课程 README 的老师、学期、分数占比与完整注意事项统一放入表格；注意事项的小标题各占一行，通过纵向合并单元格保留层级。使用 HTML 表格，以便在 GitHub 和网页中展示合并单元格。
- 课程详情直接渲染 README，支持标题、加粗、链接、列表、表格、图片和代码块；其他 Markdown 文件也提供“阅读文档”入口。相对链接与图片按文档所在目录解析，内容经 DOMPurify 清理。
- 文件提供 GitHub 查看与原文件入口；PDF 等格式是否在线预览取决于浏览器和 GitHub，较大的文件可能需要下载。
- 筛选条件保存在 URL 中，可以复制链接或使用浏览器前进、后退。
- 手机适配、深浅色切换、Ctrl / Command + K 搜索、键盘可操作弹窗。
- 关于区域直接展示项目介绍、交流方式与特别鸣谢，保留全部署名和原始链接。

## 更新资料

资料存放在“学期 / 课程”目录；选课指南存放在 `英语体育公选课/README.md`，各公选课条目放在该目录的独立子文件夹中。脚本从 `git ls-files --cached --others --exclude-standard` 生成索引，包含已跟踪文件和未被忽略的新资料；本地预览会自动更新；发布前请重新生成索引并将静态网页推送到 `gh-pages` 分支。

索引包含学期目录下的文件，排除隐藏目录、缓存、常见编译产物与可执行文件。分类根据路径关键词自动推断，可能需要随目录命名调整 `scripts/build_site.py` 中的规则。统计反映索引文件，而非整个 Git 仓库大小。

## GitHub Pages 发布

网页地址：https://Harrisonls2004.github.io/BUPT-SCSS-2023/

使用 `gh-pages` 分支发布，Pages 的 Source 为 **Deploy from a branch**，分支选择 **gh-pages / (root)**。

更新资料和网页后，在仓库根目录执行：

```sh
python3 scripts/build_site.py
git add .
git commit -m "Update course resource site"
git push origin main
git subtree push --prefix=site origin gh-pages
```

发布分支只包含 `site/` 中的静态网页，不复制原始课程大文件。资料通过 `main` 分支上的 GitHub 链接访问，因此请先推送课程更新，再推送网页。`site/.nojekyll` 保证静态文件直接提供服务。

## Markdown 渲染依赖

本地附带 Marked 和 DOMPurify，预览时无需连接 CDN。版本、来源和许可证见 [依赖说明](vendor/README.md)。
