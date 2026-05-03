import re

with open('build.py', 'r') as file:
    content = file.read()

new_mega_menu = """def get_mega_menu(data):
    # data is a list of dicts (rows)
    # Structure: Industria -> Pais -> list of (Ciudad, URL)
    tree = {}
    for row in data:
        if row.get('Estado') != 'PUBLICAR': continue
        ind = row['Industria']
        pais = row['País']
        ciudad = row['Ciudad']
        url = row['URL_Final']
        
        if ind not in tree:
            tree[ind] = {}
        if pais not in tree[ind]:
            tree[ind][pais] = []
            
        tree[ind][pais].append((ciudad, url))
        
    html = '<ul class="text-sm">'
    for ind, paises in tree.items():
        html += f'<li class="group/ind relative py-2.5 px-2 flex items-center justify-between cursor-pointer rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800/50">'
        html += f'<span class="font-normal text-zinc-900 dark:text-zinc-100 group-hover/ind:text-brand transition-colors">{ind}</span>'
        html += f'<i class="fas fa-chevron-right text-[10px] text-zinc-400 dark:text-zinc-600"></i>'
        
        # Paises submenu
        html += f'<div class="absolute left-full top-0 pl-2 w-48 hidden group-hover/ind:block z-50">'
        html += f'<div class="bg-white/95 dark:bg-zinc-950/95 backdrop-blur-xl border border-gray-200 dark:border-zinc-800 shadow-2xl rounded-xl p-2">'
        html += f'<ul class="space-y-0.5">'
        
        for pais, ciudades in paises.items():
            html += f'<li class="group/pais relative py-2 px-3 flex items-center justify-between cursor-pointer rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800/50">'
            html += f'<span class="font-normal text-zinc-700 dark:text-zinc-300 group-hover/pais:text-brand transition-colors">{pais}</span>'
            html += f'<i class="fas fa-chevron-right text-[10px] text-zinc-400 dark:text-zinc-600"></i>'
            
            # Cities submenu
            html += f'<div class="absolute left-full top-0 pl-2 w-48 hidden group-hover/pais:block z-50">'
            html += f'<div class="bg-white/95 dark:bg-zinc-950/95 backdrop-blur-xl border border-gray-200 dark:border-zinc-800 shadow-2xl rounded-xl p-2">'
            html += f'<ul class="space-y-0.5">'
            for ciudad, url in ciudades:
                html += f'<li><a href="{url}" class="block py-1.5 px-3 rounded-lg text-zinc-500 dark:text-zinc-400 hover:text-brand dark:hover:text-brand hover:bg-brand/5 dark:hover:bg-brand/10 transition-all duration-200">{ciudad}</a></li>'
            html += f'</ul></div></div></li>'
            
        html += f'</ul></div></div></li>'
    html += '</ul>'
    return html"""

content = re.sub(r'def get_mega_menu\(data\):.*?return html', new_mega_menu, content, flags=re.DOTALL)

with open('build.py', 'w') as file:
    file.write(content)

print("Mega menu fixed")
