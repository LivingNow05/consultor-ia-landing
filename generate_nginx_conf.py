import csv

conf = """server {
    listen       80;
    server_name  localhost;

    # Redirects generated from slugs
"""

with open('programatic.csv', 'r') as f:
    reader = csv.DictReader(f)
    slugs = set(row['Industria_Slug'] for row in reader)

for new_slug in slugs:
    if new_slug.startswith('chatbot-whatsapp-para-'):
        base = new_slug.replace('chatbot-whatsapp-para-', '')
        # Nginx rewrites
        conf += f"    rewrite ^/ia-para-{base}/(.*)$ /{new_slug}/$1 permanent;\n"
        conf += f"    rewrite ^/ia-para-{base}$ /{new_slug}/ permanent;\n"
        conf += f"    rewrite ^/{base}/(.*)$ /{new_slug}/$1 permanent;\n"
        conf += f"    rewrite ^/{base}$ /{new_slug}/ permanent;\n"

conf += """
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        # Optional: try_files $uri $uri/ /index.html;
    }
    
    # Custom 404 page if it exists
    error_page 404 /404.html;
}
"""

with open('nginx.conf', 'w') as f:
    f.write(conf)

print("Generated nginx.conf")
