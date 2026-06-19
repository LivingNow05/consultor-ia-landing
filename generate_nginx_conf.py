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
    location /api/chat {
        proxy_pass https://openrouter.ai/api/v1/chat/completions;
        proxy_ssl_server_name on;
        proxy_set_header Host openrouter.ai;
        proxy_set_header Content-Type "application/json";
        set $op_k1 "Bearer sk-or-v1-";
        set $op_k2 "6aae9b1ad8404d1585f166de82ec6dbd3feed768aeec21c1a0da536a562f311b";
        proxy_set_header Authorization "$op_k1$op_k2";
        proxy_set_header HTTP-Referer "https://consultor-ia.com.co";
        proxy_set_header X-Title "Consultor IA Landing Demo";
        
        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization';
        
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }

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
