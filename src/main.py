from htmlnode import *
from textnode import *
from inline_markdown import *

def main():
    md = """
This is **bolded** paragraph text in a p tag here

## h2 header

```
This is my code...
Bla bla bla
```

> This is my quote:
> "I love bananas"
> Thank you

- banana
- apple
- cherry

1. first item
2. second item
3. third item
"""

    markdown_to_html_node(md)

if __name__=="__main__":
    main()