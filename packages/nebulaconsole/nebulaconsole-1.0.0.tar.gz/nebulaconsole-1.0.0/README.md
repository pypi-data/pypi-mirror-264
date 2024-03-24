<p align="center"><img src="https://github.com/kozmoai/nebula/assets/3407835/c654cbc6-63e8-4ada-a92a-efd2f8f24b85" width=1000></p>

<p align="center">
    <a href="https://pypi.python.org/pypi/nebula/" alt="PyPI version">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/nebula?color=0052FF&labelColor=090422"></a>
    <a href="https://github.com/kozmoai/nebula/" alt="Stars">
        <img src="https://img.shields.io/github/stars/kozmoai/nebula?color=0052FF&labelColor=090422" /></a>
    <a href="https://pepy.tech/badge/nebula/" alt="Downloads">
        <img src="https://img.shields.io/pypi/dm/nebula?color=0052FF&labelColor=090422" /></a>
    <a href="https://github.com/kozmoai/nebula/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/kozmoai/nebula?color=0052FF&labelColor=090422" /></a>
    <br>
    <a href="https://nebula.io/slack" alt="Slack">
        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=0052FF&labelColor=090422&logo=slack" /></a>
    <a href="https://discourse.nebula.io/" alt="Discourse">
        <img src="https://img.shields.io/badge/discourse-browse_forum-red.svg?color=0052FF&labelColor=090422&logo=discourse" /></a>
    <a href="https://www.youtube.com/c/NebulaIO/" alt="YouTube">
        <img src="https://img.shields.io/badge/youtube-watch_videos-red.svg?color=0052FF&labelColor=090422&logo=youtube" /></a>
</p>

# Nebula

Nebula is an orchestration and observability platform for building, observing, and triaging workflows. 
It's the simplest way to transform Python code into an interactive workflow application.

Nebula allows you to expose your workflows through an API so teams dependent on you can programmatically access your pipelines, business logic, and more.
Nebula also allows you to standardize workflow development and deployment across your organization.

With Nebula, you can build resilient, dynamic workflows that react to the world around them and recover from unexpected changes.
With just a few decorators, Nebula supercharges your code with features like automatic retries, distributed execution, scheduling, caching, and much more.

Every activity is tracked and can be monitored with a self-hosted [Nebula server](https://docs.Nebula.io/latest/guides/host/) instance or managed [Nebula Cloud](https://www.nebula.io/cloud-vs-oss?utm_source=oss&utm_medium=oss&utm_campaign=oss_gh_repo&utm_term=none&utm_content=none) dashboard.

## Getting started

Nebula requires Python 3.8 or later. To [install Nebula](https://docs.nebula.io/getting-started/installation/), run the following command:

```bash
pip install nebula
```

Then create and run a Python file that uses Nebula `flow` and `task` decorators to orchestrate and observe your workflow - in this case, a simple script that fetches the number of GitHub stars from a repository:

```python
from nebula import flow, task
from typing import List
import httpx


@task(log_prints=True)
def get_stars(repo: str):
    url = f"https://api.github.com/repos/{repo}"
    count = httpx.get(url).json()["stargazers_count"]
    print(f"{repo} has {count} stars!")


@flow(name="GitHub Stars")
def github_stars(repos: List[str]):
    for repo in repos:
        get_stars(repo)


# run the flow!
if __name__=="__main__":
    github_stars(["kozmoai/nebula"])
```

Fire up the Nebula UI to see what happened:

```bash
nebula server start
```

![Nebula UI dashboard](/docs/img/ui/cloud-dashboard.png)

To run your workflow on a schedule, turn it into a deployment and schedule it to run every minute by changing the last line of your script to the following:

```python
    github_stars.serve(name="first-deployment", cron="* * * * *")
```

You now have a server running locally that is looking for scheduled deployments!
Additionally you can run your workflow manually from the UI or CLI - and if you're using Nebula Cloud, you can even run deployments in response to [events](https://docs.nebula.io/latest/concepts/automations/).

## Nebula Cloud

Stop worrying about your workflows.
Nebula Cloud allows you to centrally deploy, monitor, and manage the data workflows you support. With managed orchestration, automations, and webhooks, all backed by enterprise-class security, build production-ready code quickly and reliably.

Read more about Nebula Cloud [here](https://www.nebula.io/cloud-vs-oss?utm_source=oss&utm_medium=oss&utm_campaign=oss_gh_repo&utm_term=none&utm_content=none) or sign up to [try it for yourself](https://app.nebula.cloud?utm_source=oss&utm_medium=oss&utm_campaign=oss_gh_repo&utm_term=none&utm_content=none).

![Nebula Automations](/docs/img/ui/automations.png)

## nebula-client

If your use case is geared towards communicating with Nebula Cloud or a remote Nebula server, check out our 
[nebula-client](https://pypi.org/project/nebula-client/). It was designed to be a lighter-weight option for accessing 
client-side functionality in the nebula SDK and is ideal for use in ephemeral execution environments.

## Next steps

There's lots more you can do to orchestrate and observe your workflows with nebula!
Start with our [friendly tutorial](https://docs.nebula.io/tutorials) or explore the [core concepts of nebula workflows](https://docs.nebula.io/concepts/).

