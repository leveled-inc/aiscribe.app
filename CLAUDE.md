# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll static site using the Minima theme. Jekyll version 4.4.1.

## Commands

```bash
# Install dependencies
bundle install

# Run development server (with live reload)
bundle exec jekyll serve

# Build site for production (outputs to _site/)
bundle exec jekyll build
```

Note: Changes to `_config.yml` require a server restart.

## Architecture

- `_config.yml` - Site configuration (title, description, theme settings)
- `_posts/` - Blog posts in markdown (filename format: `YYYY-MM-DD-title.markdown`)
- `index.markdown` - Homepage
- `about.markdown` - About page
- `_site/` - Generated output (gitignored)

Posts use YAML front matter for metadata (layout, title, date, categories).
