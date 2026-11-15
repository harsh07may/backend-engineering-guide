# Backend Engineering Field Guide

A single-page guide to backend engineering fundamentals, taught through Node.js, Express 5 and TypeScript. It covers 14 chapters, from how the internet works to observability, and closes with a capstone project that specifies the running example so you can rebuild it from scratch.

Read it: https://harsh07may.github.io/backend-engineering-guide/

## Editing

Each chapter is one file in `src/sections/`. The page shell (styles, sidebar, scripts) is `src/shell.html`, and the logo is `src/favicon.svg`.

```bash
python3 build.py   # rebuilds index.html and favicon.svg, fails on duplicate ids or broken internal links
```

The code samples are teaching code written against the library docs as of November 2026. They have not been run as a complete project.
