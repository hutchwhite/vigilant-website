"""Blog support for the Vigilant static site.

Weekly briefings live as Markdown files in content/briefings/YYYY-MM-DD.md with a small header:

    ---
    title: CMMC Weekly Briefing: Phase 2 on hold, task force report pending
    date: 2026-09-28
    week: Sep 21–25, 2026
    summary: One or two sentences for the blog index and search results.
    ---
    ## Top story
    ...

Archive editions (written later about an earlier week) add `archive: true` and `compiled: YYYY-MM-DD`.
They keep the Monday-after-the-week `date` for ordering. The page shows no publish date for them; structured data,
the feed and the sitemap use the compiled date so nothing is backdated.

build() turns them into /blog/<date>-cmmc-weekly-briefing.html, the /blog index, feed.xml and sitemap.xml,
and adds a "Latest briefing" teaser to the home page. Files whose header has `draft: true` are skipped.
"""
import datetime as dt
import glob
import html
import json
import os
import re

CONTENT = "content/briefings"


# ------------------------------------------------------------------ minimal Markdown (what the briefings use)
def _inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
                  lambda m: f'<a href="{html.escape(m.group(2))}" rel="noopener">{m.group(1)}</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r'<span class="cite">\1</span>', text)
    return text


def markdown(md):
    out, para, items = [], [], []

    def flush():
        if para:
            out.append("<p>" + _inline(" ".join(para)) + "</p>")
            para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{_inline(i)}</li>" for i in items) + "</ul>")
            items.clear()

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        m = re.match(r"^(#{2,3})\s+(.*)", line)
        if m:
            flush()
            lvl = len(m.group(1))
            text = m.group(2).strip()
            anchor = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append(f'<h{lvl} id="{anchor}">{_inline(text)}</h{lvl}>')
            continue
        m = re.match(r"^\s*[-*]\s+(.*)", line)
        if m:
            if para:
                flush()
            items.append(m.group(1))
            continue
        if items and raw.startswith("  "):  # continuation of a list item
            items[-1] += " " + line.strip()
            continue
        if items:
            flush()
        para.append(line.strip())
    flush()
    return "\n".join(out)


# ------------------------------------------------------------------ content loading
def load_posts(root):
    posts = []
    for path in sorted(glob.glob(os.path.join(root, CONTENT, "*.md"))):
        text = open(path, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            raise ValueError(f"{path}: missing --- header")
        meta = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        if meta.get("draft", "").lower() == "true":
            continue
        for key in ("title", "date", "summary"):
            if not meta.get(key):
                raise ValueError(f"{path}: header needs '{key}'")
        date = dt.date.fromisoformat(meta["date"])
        slug = meta.get("slug") or f"{date.isoformat()}-cmmc-weekly-briefing"
        archive = meta.get("archive", "").lower() == "true"
        compiled = dt.date.fromisoformat(meta["compiled"]) if archive else date
        posts.append({**meta, "archive": archive, "compiled": compiled, "date": date, "slug": slug, "url": f"/blog/{slug}", "body": markdown(m.group(2))})
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def nice(d):
    return d.strftime("%B %-d, %Y")


def byline(p):
    if p["archive"]:
        return ""  # archive posts carry no publish date on the page (never backdated)
    return f"Published {nice(p['date'])}"


# ------------------------------------------------------------------ builders
def build(page, cta_band, SITE, OUT):
    posts = load_posts(OUT)
    os.makedirs(os.path.join(OUT, "blog"), exist_ok=True)

    for p in posts:
        esc_title = html.escape(p["title"])
        week = f'<p class="eyebrow">CMMC Weekly Briefing · {html.escape(p["week"])}</p>' if p.get("week") else '<p class="eyebrow">CMMC Weekly Briefing</p>'
        note = ""
        body = f"""
  <section class="hero">
    <div class="wrap">
      {week}
      <h1 class="post-title">{esc_title}</h1>
      <p class="byline">{" · ".join(x for x in (byline(p), "Compiled by Vigilant Cybersecurity") if x)}</p>
    </div>
  </section>

  <section class="section" aria-label="Briefing">
    <div class="wrap">
      <article class="doc post">
{note}{p["body"]}
        <p class="post-note">This briefing summarizes public sources for general awareness. It is not legal advice. Check the linked primary sources before acting on any item.</p>
        <p><a href="/blog">All weekly briefings</a></p>
      </article>
    </div>
  </section>
{cta_band("Turn the news into a plan", "Not sure how this week's changes affect your contracts? A free scoping call is the fastest way to find out.")}
"""
        graph = [{"@type": "BlogPosting", "@id": f"{SITE}{p['url']}#post", "headline": p["title"][:110],
                  "description": p["summary"], "datePublished": p["compiled"].isoformat(),
                  "dateModified": p["compiled"].isoformat(), "mainEntityOfPage": f"{SITE}{p['url']}",
                  "author": {"@id": f"{SITE}/#business"}, "publisher": {"@id": f"{SITE}/#business"},
                  "image": f"{SITE}/assets/og-image.png"}]
        extra_head = f'\n<meta property="article:published_time" content="{p["compiled"].isoformat()}">'
        doc = page(p["url"], f"{esc_title} | Vigilant Cybersecurity", html.escape(p["summary"]), esc_title, body,
                   graph, og_type="article", extra_head=extra_head, nav_path="/blog")
        open(os.path.join(OUT, "blog", p["slug"] + ".html"), "w", encoding="utf-8").write(doc)

    # remove pages for posts that no longer exist (or became drafts)
    keep = {p["slug"] + ".html" for p in posts}
    for f in glob.glob(os.path.join(OUT, "blog", "*.html")):
        if os.path.basename(f) not in keep:
            os.remove(f)

    # blog index
    if posts:
        cards = "\n".join(
            f"""        <li class="post-card">
          <p class="label">{html.escape(p.get("week", nice(p["date"])))}</p>
          <h2><a href="{p["url"]}">{html.escape(p["title"])}</a></h2>
          <p>{html.escape(p["summary"])}</p>
{f'          <p class="meta">{byline(p)}</p>' + chr(10) if byline(p) else ""}        </li>""" for p in posts)
        listing = f'      <ol class="post-list">\n{cards}\n      </ol>'
    else:
        listing = '      <p class="prose">The first weekly briefing is on its way. In the meantime, the <a href="/cmmc">CMMC status page</a> covers where things stand right now.</p>'
    index_body = f"""
  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">Every Monday</p>
      <h1>CMMC Weekly Briefing</h1>
      <p class="lede">The past week's CMMC rule changes, Cyber AB news and enforcement actions, in plain English for Alaska defense contractors. Each briefing links to its primary sources.</p>
      <div class="actions">
        <a class="btn btn-primary" href="/contact?topic=updates">Get briefings by email</a>
        <a class="btn btn-ghost" href="/feed.xml">RSS feed</a>
      </div>
    </div>
  </section>

  <section class="section" aria-label="Briefings">
    <div class="wrap">
{listing}
    </div>
  </section>
"""
    blog_schema = [{"@type": "Blog", "@id": f"{SITE}/blog#blog", "name": "CMMC Weekly Briefing",
                    "publisher": {"@id": f"{SITE}/#business"},
                    "blogPost": [{"@id": f"{SITE}{p['url']}#post"} for p in posts]}]
    open(os.path.join(OUT, "blog.html"), "w", encoding="utf-8").write(
        page("/blog", "CMMC Weekly Briefing | Vigilant Cybersecurity",
             "A weekly, plain-English roundup of CMMC rule changes, Cyber AB news and enforcement actions for Alaska defense contractors.",
             "CMMC Weekly Briefing", index_body, blog_schema))

    # "Latest briefing" teaser on the home page
    if posts:
        p = posts[0]
        teaser = f"""  <section class="section" id="latest" aria-labelledby="latest-h">
    <div class="wrap">
      <div class="teaser">
        <p class="label">Latest weekly briefing · {html.escape(p.get("week", nice(p["date"])))}</p>
        <h2 id="latest-h"><a href="{p["url"]}">{html.escape(p["title"])}</a></h2>
        <p>{html.escape(p["summary"])}</p>
        <p><a class="more" href="/blog">All briefings</a></p>
      </div>
    </div>
  </section>

"""
        idx_path = os.path.join(OUT, "index.html")
        idx = open(idx_path, encoding="utf-8").read()
        idx = re.sub(r'  <section class="section" id="latest".*?</section>\n\n', "", idx, flags=re.S)
        idx = idx.replace('  <section class="section" aria-labelledby="svc-h">', teaser + '  <section class="section" aria-labelledby="svc-h">', 1)
        open(idx_path, "w", encoding="utf-8").write(idx)

    # sitemap
    today = dt.date.today().isoformat()
    urls = [("/", today), ("/cmmc", today), ("/services", today), ("/blog", posts[0]["date"].isoformat() if posts else today),
            ("/about", today), ("/contact", today), ("/privacy", today)] + [(p["url"], p["compiled"].isoformat()) for p in posts]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls]
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")

    # RSS feed
    def rfc822(d):
        return dt.datetime(d.year, d.month, d.day, 15, 0).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = "".join(f"""
    <item>
      <title>{html.escape(p["title"])}</title>
      <link>{SITE}{p["url"]}</link>
      <guid isPermaLink="true">{SITE}{p["url"]}</guid>
      <pubDate>{rfc822(p["compiled"])}</pubDate>
      <description>{html.escape(p["summary"])}</description>
    </item>""" for p in posts[:20])
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>CMMC Weekly Briefing | Vigilant Cybersecurity</title>
    <link>{SITE}/blog</link>
    <description>A weekly, plain-English roundup of CMMC rule changes, Cyber AB news and enforcement actions for Alaska defense contractors.</description>
    <language>en-us</language>{items}
  </channel>
</rss>
"""
    open(os.path.join(OUT, "feed.xml"), "w").write(feed)
    return posts
