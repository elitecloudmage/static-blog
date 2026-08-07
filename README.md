# [Static Blog](https://jadonsblog.com/)

A fast, low-ops blog built with Hugo and the hello-friend-ng theme, customized with a clean homepage, centered social icons, and simple content sections for posts, projectsi and more. No app servers. No databases. Just pages.

---

How it works:
-
1. I write posts as simple Markdown files.

2. Hugo (a static site generator) turns those files into finished HTML, CSS, and image pages.

3. When I push changes to GitHub, an automated workflow builds the site and publishes it on GitHub Pages.

4. Cloudflare acts like the phone book for the internet, it points my domain to the live site and secures it with HTTPS.

---

Why this setup?
-

• **Speed & reliability:** Static pages are fast and rarely break.

• **hello-friend-ng:** → Minimal, beautiful theme with clean defaults that just work.

• **Security:** No running code on the server = small attack surface.

• **Minimal overrides** → A single custom CSS file and a few partials keep it lightweight but personal.

• **CI/CD deploy** → GitHub Actions builds on every push and ships to GitHub Pages, with Cloudflare managing DNS and HTTPS.

---

Content model
-
• **Posts** → content/posts/<slug>.md
>Short articles and notes.

• **Projects** → content/projects/<slug>/index.md
> Each project is a leaf bundle: the page and its images live together:
```
content/projects/self-healing-ec2/
  index.md
  diagram.png
  result.png
```
In the Markdown, I can reference images directly: ![diagram](diagram.png).

• **About** → content/about/index.md
A single page with a short bio and links.

• **Styling** → static/css/custom.css
One small stylesheet for tweaks (fonts, spacing, social icon look).

---

Run it Locally
-
```
hugo version        # extended build, same-ish or newer than mine
hugo server -D      # -D shows drafts while writing
# open http://localhost:1313
```

Create content:
```
hugo new posts/my-first-post.md
hugo new projects/self-healing-ec2/index.md   # project bundle with images
```
Build Static files:
```
hugo --minify
# output in ./public
```

---

How the domain and hosting are wired
-

I keep infrastructure in a separate repo: ghostoptimizer/iac-infra.

That Terraform code does the glue work so this site stays repeatable:

• **Cloudflare:** zone + DNS records for jadonsblog.com (and subdomains if needed).

• **Either:** 
- GitHub Pages: CNAME to Pages with flattening at the apex

In short: Hugo + GitHub builds the site, and Terraform (Cloudflare) makes the internet route to it.
