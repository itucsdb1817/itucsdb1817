import mistune

def render(text, **options):
    markdown = mistune.Markdown()
    return markdown(text)