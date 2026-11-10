# Bundled browser dependencies

These files are bundled locally so document rendering also works without a CDN.

- `marked.umd.js`: Marked 18.2.0, https://github.com/markedjs/marked, MIT. See `../licenses/marked-LICENSE`.
- `purify.min.js`: DOMPurify 3.4.17, https://github.com/cure53/DOMPurify, Apache-2.0 OR MPL-2.0. See `../licenses/DOMPurify-LICENSE`.

Markdown is parsed with Marked and sanitized with DOMPurify before insertion. Relative links resolve against the source document on GitHub; relative images resolve against the raw source directory.
