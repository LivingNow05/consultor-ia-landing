import subprocess
try:
    result = subprocess.run(['git', 'push'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, stdin=subprocess.DEVNULL)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("RETURN CODE:", result.returncode)
except Exception as e:
    print("ERROR:", str(e))
