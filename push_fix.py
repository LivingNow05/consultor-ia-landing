import subprocess

try:
    print("Adding files...")
    subprocess.run(['git', 'add', '.'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("Committing...")
    subprocess.run(['git', 'commit', '-m', 'fix(seo): update build.py hardcoded templates to 115 stars and clean favicons'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("Pushing...")
    res = subprocess.run(['git', 'push'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, stdin=subprocess.DEVNULL)
    print("PUSH STDOUT:", res.stdout)
    print("PUSH STDERR:", res.stderr)
    print("PUSH RETURN CODE:", res.returncode)
except Exception as e:
    print("ERROR:", str(e))
