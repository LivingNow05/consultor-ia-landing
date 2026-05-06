import subprocess

try:
    print("Adding Docker files...")
    subprocess.run(['git', 'add', 'Dockerfile', 'Dosckerfile', '-f'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("Committing...")
    subprocess.run(['git', 'commit', '-m', 'fix(deploy): add Dosckerfile and Dockerfile to fix EasyPanel build error'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("Pushing...")
    res = subprocess.run(['git', 'push'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, stdin=subprocess.DEVNULL)
    print("PUSH STDOUT:", res.stdout)
    print("PUSH STDERR:", res.stderr)
    print("PUSH RETURN CODE:", res.returncode)
except Exception as e:
    print("ERROR:", str(e))
