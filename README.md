# 📔 Static Site Generator

A lightweight Python-based static site generator that converts Markdown files into styled HTML pages. It uses a modular architecture to parse, structure, and render content using customizable templates.

[Live demo](https://bulbasaur854.github.io/static-site-generator/)

## 📝 Notes  
Markdown parsers often support nested inline elements. For example, you can have a bold word inside of italics:
```markdown
This is an _italic and **bold** word_.
```
This is not implemtneted yet! coming soon...

The generator supports 8 types of markdown blocks:
- Paragraph
- Heading
- Code
- Quote
- Unordered List
- Ordered List

And inline markdown:
- Normal text
- Bold
- Italic
- Links
- Images

## 🛍️ Prerequisites
- Python 3.7+
- A Unix-like terminal (macOS, Linux, or WSL for Windows)
- Bash shell (used to run scripts)

## 🛠️ Building The Website
1. Download and extract the latest release zip file [here](https://github.com/Bulbasaur854/static-site-generator/releases)
2. Add your markdown files to the `content` folder, for example:
   
   ```bash
    content/
    ├── index.md
    ├── contact/
    │   └── index.md
    └── blog/
        ├── glorfindel/
        │   └── index.md
        └── majesty/
            └── index.md
   ```

3. Build the website files by running this command in bash terminal

   ```bash
    bash main.sh
   ```

4. Preview the website by running:

   ```bash
    start docs\index.html     # Windows
    open docs/index.html      # macOS
    xdg-open docs/index.html  # Linux
   ```

## ⛵ Deploying to GitHub Pages
1. Commit the generated `docs/` folder
2. Go to your GitHub repo settings
3. Under **Pages**, set the source to `docs/` on the main branch
4. Your site will be live at `https://your-username.github.io/your-repo-name`
