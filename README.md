# 愚公柚子的网页剪报

这里堆放了一些从网上摘下来的文章。

摘抄通过[Circle阅读助手](https://circlereader.com)实现。

## 维护

只需要在 `docs/` 的对应文件夹（`inbox` / `archived` / `wastebasket`）里增删改 markdown 文件，然后 `git push` 即可。侧边栏和全文搜索索引在发布时由 [Cloudflare Pages](https://pages.cloudflare.com) 自动生成（构建命令 `python scripts/gen.py`，输出目录 `docs`），无需手动维护。

## 本地预览

```bash
python scripts/gen.py
python -m http.server -d docs
```

然后访问 http://localhost:8000 （注意不要用 `file://` 直接打开，浏览器会拦截跨目录读取）。
