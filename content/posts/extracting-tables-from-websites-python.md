---
title: "Extracting Tables with Python"
date: 2026-08-30
draft: false
---

Automation with Python is some pretty cool stuff once you start digging deep and understanding how simple it really is. I got most of my information from [this freeCodeCamp video](https://youtu.be/PXMJ6FS7llk?t=31). By no means am I an expert at this (yet) but I gotta say this is a pretty cool and simple script for an educated idiot like me so ima try and break it down as simple as possible... even though it's like 5 lines.

## My spiel

The main part of the video starts with extracting tables from websites using Python. To be honest, I thought it'd be as simple as those three basic lines of code in the video. But back in 2025, Wikipedia started getting hammered by automated scrapers and bot traffic, so now you have to set a proper User-Agent header and follow their rules just to pull data. For someone who's never done web scraping before, it's a cool reminder of how quickly simple code can need extra steps to keep up with how the web works.

In short, the User-Agent identifies *what software* is making the request, and the contact info lets Wikimedia's operators reach the person responsible *if* that script causes a problem.

## So how do you extract the table then??

- First, make sure you have the pandas library installed for scraping static HTML tables to return them as a list of DataFrames.
- Second, install lxml for parsing these tables since it serves as the fastest parsing engine for `pd.read_html()`.

```bash
pip install pandas lxml
```

Once that's done, start by adding your library into your main.py file:

```python
import pandas as pd
```

Then add your ua (user-agent) key

```python
ua = 'xtract-tables/0.1 (your@email.com)'
```

Then copy your Wikipedia link, paste it, and also make sure to pass the user agent key through as well.

```python
df = pd.read_html('https://whatever/link/you/choose', storage_options={'User-Agent': ua})
```

Once those are set, add these lines to print the output of your tables by passing your variable through:

```python
print(len(df))
print(df[0])
```

Run the file `python3 main.py` and boom, you've now webscraped using Python!

## Extra

### So what's really going on in the back end and does every website require this??

When you run `pd.read_html` without a user-agent, pandas on the backend is calling `urllib.request.urlopen(url)` to fetch the page, and the user agent field now sees `urllib.request.Request(url, headers=None)`.

Simply put, that means: no custom headers → urllib uses its default (None) → sends 'Python-urllib/3.11' as the User-Agent. That's anonymous and unidentifiable, the kind of identity Wikipedia now rejects, since they want to know *who* you are.

Most sites require nothing at all. No UA, no email, no registration. The vast majority of the web (personal blogs, government pages, small businesses, most news sites) just serves HTML to whoever asks, worried less about who you are and simply "do you look like a human using a browser?"

## Summary

While this is just a basic tutorial, it offers a practical look at how the web is adapting to automated tools and AI scraping. On one side, platforms are simply protecting their infrastructure, managing server loads, and keeping their data under control. On the other, it means standard public access is becoming more gated and controlled by default. For anyone automating tasks or scraping data, it is a small but important change in how we interact with web resources.

Cool stuff, right?
