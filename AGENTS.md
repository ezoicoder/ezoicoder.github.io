# Repository Instructions

## Blog Source And Generated HTML

- Blog source files live in `blog-src/*.md`.
- Generated public HTML lives in `blog/`.
- Do not edit generated blog HTML by hand unless explicitly requested. Prefer
  editing the Markdown source and then running:

  ```bash
  python3 tools/build_blog.py
  ```

- After editing any `blog-src/*.md` file, always rebuild the blog HTML and
  include the corresponding generated files in the same commit.
- The root homepage `index.html` is currently hand-maintained. Adding or
  retitling a blog post does not automatically update the homepage Blog section;
  update `index.html` manually when the homepage list should change.

## Blog Front Matter

Each blog source file should start with YAML-style front matter:

```yaml
---
title: "Post title"
date: YYYY-MM-DD
updated: YYYY-MM-DD
slug: stable-url-slug
tags: [tag one, tag two]
summary: "Short list-page summary."
---
```

- `date` is the original publication date.
- `updated` is the last substantive update date. If omitted, the build script
  treats it as equal to `date`, but new posts should include it explicitly.
- `slug` controls the public URL under `/blog/<slug>/`. The title does not
  control the URL.
- Changing a title is safe for existing links if `slug` is unchanged.
- Changing a `slug` breaks the old URL unless a redirect file is kept under the
  old `blog/<old-slug>/index.html`.

## Links, Redirects, And References

- Internal blog references should use Markdown links in source files, for
  example:

  ```markdown
  [*Post title*](../post-slug/)
  ```

- If an old blog URL should remain valid, keep or add a small redirect HTML file
  at the old generated path. The current build script does not create redirects
  automatically.
- When one post references a newer post, make sure the older post has an
  `updated` date reflecting the update.

## Assets

- Source assets for posts should go in `blog-src/assets/`.
- Web-facing image assets are copied to `blog/assets/` by
  `tools/build_blog.py`.
- Commit both source assets and generated/copied assets when publishing.

## Publishing Checklist

Before committing blog changes:

1. Edit `blog-src/*.md`.
2. Run `python3 tools/build_blog.py`.
3. If the root homepage blog list should change, update `index.html`.
4. Check `git diff --check`.
5. Check that generated `blog/index.html` and relevant
   `blog/<slug>/index.html` reflect the source changes.
6. Commit source Markdown, generated HTML, assets, and any homepage updates
   together.

## GitHub Pages

- GitHub Pages serves files from `main` at the repository root.
- After pushing, Pages may take a few minutes to build and CDN/browser caches
  may take additional time to refresh.
- If the GitHub raw file is updated but `https://ezoicoder.github.io/` is not,
  it is usually a Pages build or cache delay.
