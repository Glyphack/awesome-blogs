# Awesome Blogs

This project is a blog post scraper I wrote for my favourite blogs. It extracts post links and exports them as JSON files, making it easy to add them to a reader like [Readwise](https://readwise.io/).

## Supported Blogs

The scraper currently supports the following blogs, as indicated by the file names in the `src` folder:

- Command Center (Rob Pike) Blog
- Joel on Software
- Matklad

## Usage

```
uv run ./src/robpike.py
```

Or to update all blogs

```
make update
```

## Blog List

| Blog | JSON File |
|------|-----------|
| Joelonsoftware | [joelonsoftware.json](https://github.com/Glyphack/awesome-blogs/blob/master/joelonsoftware.json) |
| Matklad | [matklad.json](https://github.com/Glyphack/awesome-blogs/blob/master/matklad.json) |
| Nullprogram | [nullprogram.json](https://github.com/Glyphack/awesome-blogs/blob/master/nullprogram.json) |
| Robpike | [robpike.json](https://github.com/Glyphack/awesome-blogs/blob/master/robpike.json) |