import argparse

parser = argparse.ArgumentParser(description="自动发布")

parser.add_argument('--env', '-e', default='dev', choices=['dev', 'prod'], dest='env')

args = parser.parse_args()

print(args.env)




