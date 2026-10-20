import argparse
import csv
import os
import time

from dotenv import load_dotenv
from github import Auth, Github
from github.ContentFile import ContentFile
from github.GithubException import UnknownObjectException

load_dotenv()

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")

WORKFLOWS_PATH = ".github/workflows"
OUTPUT_FIELDS = ["repo_slug", "repo_url", "deployment_count", "deployment_url_latest"]

parser = argparse.ArgumentParser(
    prog="workflow_check",
    description="Checks repositories listed in a given CSV file for GitHub Workflows directories."
)
parser.add_argument(
    "file",
    help="Specify the file to check through."
)
parser.add_argument(
    "--header",
    help="The CSV header to use as the repository column.",
    default="Slug"
)
parser.add_argument(
    "-o", "--output",
    help="file path to output results to (always has .csv appended as the type).",
    default="output/output"
)
args=vars(parser.parse_args())

def main():

    csv_filename = args["file"]
    csv_header = args["header"]
    output_filename = str(args["output"]) + ".csv"

    if not os.path.exists(output_filename):
        with open(output_filename, "w") as new_file:
            new_file.write("")

    auth = Auth.Token(GITHUB_API_TOKEN)
    github_api = Github(auth=auth)

    with open(csv_filename, newline="") as csv_file, open(output_filename, "w") as output_file:
        reader = csv.DictReader(csv_file)
        writer = csv.DictWriter(output_file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()

        for row in reader:
            repo_slug = str(row[csv_header])
            workflow_check = False
            deployment_check = False
            try:
                repo = github_api.get_repo(repo_slug)

                # check for workflows
                contents = repo.get_contents(".github")
                if (type(contents) == ContentFile) and (contents.path == WORKFLOWS_PATH):
                    print(f"{repo_slug} contains workflows!")
                    workflow_check = True
                    break

                if type(contents) != list: 
                    raise TypeError("The contents of the .github directory had some unknown issue.")

                for dir in contents:
                    if dir.path == WORKFLOWS_PATH:
                        print(f"{repo_slug} contains workflows!")
                        workflow_check = True
                        break

                # check for deployments
                deployments = repo.get_deployments()
                if deployments.totalCount > 0:
                    print(f"{repo_slug} has deployments!")
                    deployment_check = True

                if workflow_check and deployment_check:
                    writer.writerow({
                        "repo_slug": repo_slug,
                        "repo_url": repo.url,
                        "deployment_count": deployments.totalCount,
                        "deployment_url_latest": deployments.get_page(0)[0].url
                    })
                
            except UnknownObjectException:
                print(f"Repository {repo_slug} no longer exists or could not be found.")
            
            time.sleep(0.005)
            

if __name__ == "__main__":
    main()