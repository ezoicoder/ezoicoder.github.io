# Repository Instructions

## Site Structure

- This is a GitHub Pages site built with Jekyll from the repository root.
- The homepage source is `index.md` and uses Jekyll front matter plus Liquid.
- The blog listing source is `blog.md`, with `permalink: /blog/`.
- Shared layouts live in `_layouts/`.
- Shared CSS lives in `assets/css/site.css`.
- Blog images and other public assets live under `assets/`.
- The resume source and PDF live at `assets/resume.tex` and
  `assets/resume.pdf`.
- For generated figures, keep the source `.tex` and corresponding `.pdf` under
  `assets/` alongside the web-facing image when they are useful for future
  edits.

## Blog Posts

- Blog posts live in `_posts/*.md`.
- Do not edit generated `_site/` output. Jekyll builds it locally and GitHub
  Pages builds it remotely.
- Each post should start with YAML front matter:

  ```yaml
  ---
  title: "Post title"
  date: YYYY-MM-DD
  updated: YYYY-MM-DD
  slug: stable-url-slug
  permalink: /blog/stable-url-slug/
  tags: [tag one, tag two]
  summary: "Short list-page summary."
  ---
  ```

- `date` is the original publication date.
- `updated` is the last substantive update date. New posts should include it
  explicitly.
- `permalink` controls the public URL and should keep the `/blog/<slug>/`
  shape unless intentionally changing URLs.
- The title does not control the URL when `permalink` is present.
- Do not put a duplicate top-level `# Title` at the start of a post body; the
  post layout renders the page title.
- For inline math in blog Markdown, prefer Kramdown math spans
  `$$...$$` instead of single-dollar `$...$`. Single-dollar spans are left as
  ordinary text until browser-side MathJax runs, so Kramdown can first parse
  TeX underscores such as `\mathcal{G}_{L,n}` and later `x_{n-2}` as Markdown
  emphasis, producing broken HTML like `<em>...</em>` inside formulas.
- Enable the Markdown math pre-commit hook with `tools/install_hooks.sh`.

## Links, Redirects, And References

- Internal blog references should use Jekyll-aware links where practical, for
  example:

  ```markdown
  [*Post title*]({{ '/blog/post-slug/' | relative_url }})
  ```

- Static blog assets should live under `assets/blog/`.
- Old generated blog HTML should not be kept unless a specific legacy URL must
  remain valid.
- Do not commit LaTeX intermediate files such as `.aux`, `.log`, `.fls`,
  `.fdb_latexmk`, or `.out`.
- When one post references a newer post, make sure the older post has an
  `updated` date reflecting the update.

## Publishing Checklist

Before committing blog or site changes:

1. Edit source files such as `_posts/*.md`, layouts, CSS, or `index.md`.
2. For Markdown changes, run `ruby tools/check_kramdown_math.rb` if the
   pre-commit hook is not enabled.
3. Check `git diff --check`.
4. Check that homepage and blog Liquid loops still point at the intended posts.
5. Commit source files, layouts, CSS, and assets together.

## GitHub Pages

- GitHub Pages serves files from `main` at the repository root and runs Jekyll
  automatically.
- After pushing, Pages may take a few minutes to build and CDN/browser caches
  may take additional time to refresh.
- If the GitHub raw file is updated but `https://ezoicoder.github.io/` is not,
  it is usually a Pages build or cache delay.
