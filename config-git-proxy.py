import argparse
import subprocess
import sys

parser = argparse.ArgumentParser(description="设置本地 git 代理脚本")

parser.add_argument('--op', '-o', default='set', choices=['set', 'unset'], dest='op')

args = parser.parse_args()

op = args.op

if op == 'set':
    subprocess.run(['git', 'config', '--global', 'http.proxy', 'http://127.0.0.1:7890'])
    subprocess.run(['git', 'config', '--global', 'https.proxy', 'http://127.0.0.1:7890'])
elif op == 'unset':
    subprocess.run(['git', 'config', '--global', '--unset', 'http.proxy'])
    subprocess.run(['git', 'config', '--global', '--unset', 'https.proxy'])

config = subprocess.run(['git', 'config', '--global', '--list'], capture_output=True, text=True, check=True)
print(config.stdout)
sys.exit(0)