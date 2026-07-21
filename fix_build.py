with open("build.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("faqs_html = build_faqs(mock_row, {})", "faqs_html, schema_faq = build_faqs(mock_row, {})")
content = content.replace("html = html.replace('{SCHEMA_FAQ}', '')", "html = html.replace('{SCHEMA_FAQ}', schema_faq)")

with open("build.py", "w", encoding="utf-8") as f:
    f.write(content)
