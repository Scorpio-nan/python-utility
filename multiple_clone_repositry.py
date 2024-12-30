import requests
import subprocess

def clone_all_repos(user):
    """
    快速 clone 指定用户下面的所有的 git repository
    :param user:
    :return:
    """
    page = 1
    per_page = 100  # 每页获取的仓库数量，可以根据实际情况调整
    all_repos = []
    clone_repos = []
    while True:
        url = f"https://api.github.com/users/{user}/repos?page={page}&per_page={per_page}"
        response = requests.get(url)
        repos = response.json()
        if not repos:  # 如果获取到的仓库列表为空，说明已经获取完所有页的数据了
            break
        all_repos.extend(repos)
        page += 1

    for repo in all_repos:
        clone_url = repo["clone_url"]
        repo_name = repo["name"]
        clone_repos.append(clone_url)
        try:
             subprocess.call(["git", "clone", "--depth", "1", "-b", "17.0", clone_url, f"D:/workspace/python-project/odoo/oca_addons/{repo_name}"])
        except Exception as e:
            subprocess.call(["git", "clone", clone_url, f"D:/workspace/python-project/odoo/oca_addons/{repo_name}"])
    return clone_repos

clone_all_repos("OCA")
