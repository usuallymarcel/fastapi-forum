import markdown
import bleach

ALLOWED_TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {
    "p","pre","code","h1","h2","h3","h4","h5","h6",
    "img","table","thead","tbody","tr","th","td"
}

ALLOWED_ATTRS = {
    "a": ["href", "title"],
    "img": ["src", "alt"]
}

def render_markdown(content: str):

    html = markdown.markdown(
        content,
        extensions=["fenced_code", "tables"]
    )

    clean = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS
    )

    return clean