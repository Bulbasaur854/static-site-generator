# 🌐 Static Site Generator

A lightweight Python-based static site generator that converts Markdown files into styled HTML pages. It uses a modular architecture to parse, structure, and render content using customizable templates. [Live demo](https://bulbasaur854.github.io/static-site-generator/)

The generator supports 8 types of markdown blocks:
- Paragraph
- Heading
- Code
- Quote
- Unordered List
- Ordered List

Currently supported inline markdown:
- Normal text
- Bold
- Italic
- Links
- Images

## ❓How To

1. **Clone the repository**
   
    ```bash
    git clone https://github.com/your-username/static-site-generator.git
    cd static-site-generator
    ```
3. **Add your markdown content**, place your Markdown files inside the `content/` folder, Example:
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
4. **Build the site**, to convert your Markdown files into a full HTML site, run:
    ```bash
    bash main.sh
    ```
    The output will be placed in the `docs/` folder, which you can open in your browser or deploy to GitHub Pages.
5. **Preview your site**, open the generated site locally:
    ```bash
    open docs/index.html      # macOS
    xdg-open docs/index.html  # Linux
    start docs\index.html     # Windows
    ```

## 📝 Notes  
Markdown parsers often support nested inline elements. For example, you can have a bold word inside of italics:
```markdown
This is an _italic and **bold** word_.
```
This is not implemtneted yet! coming soon...
