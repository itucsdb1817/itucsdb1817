import mistune

def render(text, **options):
    markdown = mistune.Markdown(escape=True)
    return markdown(text)