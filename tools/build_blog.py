#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "blog-src"
OUTPUT_DIR = ROOT / "blog"


@dataclass(frozen=True)
class Post:
    title: str
    date: date
    slug: str
    tags: tuple[str, ...]
    summary: str
    source: Path
    body_markdown: str

    @property
    def url(self) -> str:
        return f"{self.slug}/"

    @property
    def formatted_date(self) -> str:
        return self.date.strftime("%B %-d, %Y")

    @property
    def meta_text(self) -> str:
        tags = ", ".join(self.tags)
        return f"{self.formatted_date} - {tags}" if tags else self.formatted_date


def parse_front_matter(path: Path) -> Post:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path} must start with YAML-style front matter")

    try:
        _, raw_meta, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError(f"{path} has an unterminated front matter block") from exc

    meta: dict[str, str | tuple[str, ...]] = {}
    for line in raw_meta.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"{path}: invalid front matter line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("[") and value.endswith("]"):
            value = tuple(item.strip().strip('"').strip("'") for item in value[1:-1].split(",") if item.strip())
        meta[key] = value

    required = ("title", "date", "slug", "summary")
    missing = [key for key in required if key not in meta]
    if missing:
        raise ValueError(f"{path}: missing front matter keys: {', '.join(missing)}")

    tags = meta.get("tags", ())
    if isinstance(tags, str):
        tags = (tags,)

    return Post(
        title=str(meta["title"]),
        date=datetime.strptime(str(meta["date"]), "%Y-%m-%d").date(),
        slug=str(meta["slug"]),
        tags=tuple(tags),
        summary=str(meta["summary"]),
        source=path,
        body_markdown=body.lstrip(),
    )


def render_markdown(markdown: str) -> str:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        raise RuntimeError("pandoc is required to build the blog HTML")

    result = subprocess.run(
        [
            pandoc,
            "-f",
            "markdown-smart+tex_math_dollars",
            "-t",
            "html",
            "--mathjax",
            "--wrap=none",
        ],
        input=markdown,
        text=True,
        check=True,
        capture_output=True,
    )
    return result.stdout


def strip_leading_h1(fragment: str) -> str:
    return re.sub(r"^\s*<h1\b[^>]*>.*?</h1>\s*", "", fragment, count=1, flags=re.DOTALL)


def page_shell(title: str, body: str, extra_head: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
{extra_head}  <style>
    :root {{
      color-scheme: light;
      --ink: #172026;
      --muted: #52606d;
      --line: #d9e2ec;
      --accent: #0a7c86;
      --accent-soft: #e6f4f1;
      --bg: #f8fafc;
      --paper: #ffffff;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--bg);
      line-height: 1.6;
    }}

    main {{
      width: min(900px, calc(100% - 32px));
      margin: 0 auto;
      padding: 48px 0;
    }}

    .nav {{
      display: flex;
      gap: 16px;
      margin-bottom: 28px;
      font-size: 0.95rem;
      font-weight: 650;
    }}

    a {{
      color: var(--accent);
    }}

    .nav a {{
      text-decoration: none;
    }}

    header {{
      padding-bottom: 24px;
      border-bottom: 1px solid var(--line);
    }}

    h1 {{
      margin: 0 0 10px;
      font-size: clamp(2rem, 5vw, 3rem);
      line-height: 1.1;
      letter-spacing: 0;
    }}

    .tagline {{
      max-width: 720px;
      margin: 0;
      color: var(--muted);
      font-size: 1.04rem;
    }}

    section {{
      padding-top: 28px;
    }}

    .post {{
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--paper);
    }}

    .post + .post {{
      margin-top: 14px;
    }}

    .post h2 {{
      margin: 0 0 8px;
      font-size: 1.12rem;
      line-height: 1.35;
      letter-spacing: 0;
      text-transform: none;
    }}

    .post h2 a {{
      color: var(--ink);
      text-decoration: none;
    }}

    .post h2 a:hover {{
      color: var(--accent);
    }}

    .meta,
    .post-meta {{
      color: var(--muted);
      font-size: 0.95rem;
    }}

    .meta {{
      margin: 0 0 8px;
    }}

    .summary {{
      margin: 0;
      color: var(--muted);
    }}

    .article-card {{
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--paper);
      line-height: 1.68;
    }}

    .article-card h2 {{
      margin: 34px 0 12px;
      color: var(--accent);
      font-size: 1rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    .article-card h3 {{
      margin: 28px 0 10px;
      font-size: 1.12rem;
      line-height: 1.35;
    }}

    .article-card p {{
      margin: 0 0 16px;
    }}

    .post-meta {{
      margin: 0 0 24px;
    }}

    blockquote {{
      margin: 20px 0;
      padding: 12px 18px;
      border-left: 4px solid var(--accent);
      background: var(--bg);
      color: var(--muted);
    }}

    .math.display {{
      display: block;
      max-width: 100%;
      overflow-x: auto;
      padding: 2px 0;
    }}

    @media (max-width: 720px) {{
      main {{
        padding-top: 32px;
      }}

      .article-card {{
        padding: 20px;
      }}
    }}
  </style>
</head>
<body>
{body}</body>
</html>
"""


def render_index(posts: list[Post]) -> str:
    items = "\n".join(
        f"""      <article class="post">
        <h2><a href="{html.escape(post.url)}">{html.escape(post.title)}</a></h2>
        <p class="meta">{html.escape(post.meta_text)}</p>
        <p class="summary">{html.escape(post.summary)}</p>
      </article>"""
        for post in posts
    )
    body = f"""  <main>
    <nav class="nav">
      <a href="../">Home</a>
      <a href="../resume.pdf">Resume</a>
    </nav>

    <header>
      <h1>Blog</h1>
      <p class="tagline">Technical notes on machine learning systems, theory, and infrastructure.</p>
    </header>

    <section aria-label="Posts">
{items}
    </section>
  </main>
"""
    return page_shell("Blog | Jiarui Zhang", body)


def render_post(post: Post) -> str:
    fragment = strip_leading_h1(render_markdown(post.body_markdown))
    body = f"""  <main>
    <nav class="nav">
      <a href="../../">Home</a>
      <a href="../">Blog</a>
    </nav>

    <article class="article-card">
      <h1>{html.escape(post.title)}</h1>
      <p class="post-meta">{html.escape(post.meta_text)}</p>
{indent(fragment.rstrip(), "      ")}
    </article>
  </main>
"""
    mathjax = """  <script>
    window.MathJax = {
      tex: {
        inlineMath: [['\\\\(', '\\\\)']],
        displayMath: [['\\\\[', '\\\\]']],
        processEscapes: true
      },
      svg: {
        fontCache: 'global'
      }
    };
  </script>
  <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
"""
    return page_shell(f"{post.title} | Jiarui Zhang", body, mathjax)


def indent(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_assets() -> None:
    source_assets = SOURCE_DIR / "assets"
    if not source_assets.exists():
        return

    output_assets = OUTPUT_DIR / "assets"
    output_assets.mkdir(parents=True, exist_ok=True)
    for source in source_assets.iterdir():
        if source.is_file() and source.suffix.lower() in {".avif", ".gif", ".jpg", ".jpeg", ".png", ".svg", ".webp"}:
            shutil.copy2(source, output_assets / source.name)


def main() -> int:
    try:
        posts = [parse_front_matter(path) for path in sorted(SOURCE_DIR.glob("*.md"))]
        posts.sort(key=lambda post: post.date, reverse=True)
        if not posts:
            raise RuntimeError(f"no posts found in {SOURCE_DIR}")

        write(OUTPUT_DIR / "index.html", render_index(posts))
        for post in posts:
            write(OUTPUT_DIR / post.slug / "index.html", render_post(post))
        copy_assets()
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"build_blog.py: {exc}", file=sys.stderr)
        return 1

    print(f"Built {len(posts)} post(s) into {OUTPUT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
