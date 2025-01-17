import glob
import importlib.util
import json
import os
import re
import subprocess


def get_blog_name(json_file):
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                if "source" in data[0]:
                    return data[0]["source"]
    except Exception:
        pass

    base = os.path.basename(json_file)
    name = os.path.splitext(base)[0]
    return name.replace("_", " ").title()


def update_readme():
    json_files = glob.glob("*.json")

    repo_url = None
    try:
        with os.popen("git config --get remote.origin.url") as f:
            repo_url = f.read().strip()
            ssh_pattern = r"git@github\.com:(.+)\.git"
            if match := re.match(ssh_pattern, repo_url):
                repo_url = f"https://github.com/{match.group(1)}"
            repo_url = repo_url.rstrip(".git")
    except Exception:
        print("Warning: Could not determine repository URL")
        return

    if not repo_url:
        print("Error: No repository URL found")
        return

    table_rows = []
    for json_file in sorted(json_files):
        blog_name = get_blog_name(json_file)
        json_url = f"{repo_url}/blob/master/{json_file}"
        table_rows.append(f"| {blog_name} | [{json_file}]({json_url}) |")

    with open("README.md", "r") as f:
        content = f.read()

    table_section = """
## Blog List

| Blog | JSON File |
|------|-----------|
""" + "\n".join(table_rows)

    if "## Blog List" in content:
        content = re.sub(
            r"## Blog List\n\n\|[^#]*(?=\n#|$)",
            table_section.strip(),
            content,
            flags=re.DOTALL,
        )
    else:
        content += "\n" + table_section

    with open("README.md", "w") as f:
        f.write(content)


def run_scrapers():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    py_files = glob.glob(os.path.join(src_dir, "*.py"))

    utility_scripts = {"update.py", "save.py", "__init__.py", "main.py"}
    scraper_files = [f for f in py_files if os.path.basename(f) not in utility_scripts]

    for scraper in scraper_files:
        print(f"Running {os.path.basename(scraper)}...")
        try:
            spec = importlib.util.spec_from_file_location("module", scraper)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "fetch"):
                module.fetch()
            else:
                print(f"Error running {scraper}: No fetch method found")
        except Exception as e:
            print(f"Error running {scraper}: {str(e)}")


def commit_changes():
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True
        )
        if not result.stdout.strip():
            print("No changes to commit")
            return

        subprocess.run(["git", "add", "*.json", "README.md"], check=True)
        subprocess.run(
            ["git", "commit", "-m", "Update blog data and README"], check=True
        )
        subprocess.run(["git", "push"], check=True)

        print("Changes committed and pushed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error in Git operations: {str(e)}")


def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    run_scrapers()
    update_readme()

    if os.environ.get("CI"):
        commit_changes()


if __name__ == "__main__":
    main()
