"""
Commands for git operations
"""

from os import makedirs, path
from shutil import which
from subprocess import check_call, check_output, run

import click

from brewblox_dev import utils

WORKDIR = path.expanduser('~/.cache/brewblox-dev/git')
REPOS = [
    'brewblox-documentation',
    'brewblox-devcon-spark',
    'brewblox-history',
    'brewblox-ui',
    'brewblox-ctl',
    'brewblox-firmware',
    'brewblox-auth',
    'brewblox-tilt',
    'brewblox-hass',
    'brewblox-images',
    'node-red-contrib-brewblox',
]


@click.group()
def cli():
    """Command collector"""


def create_repos():
    makedirs(WORKDIR, exist_ok=True)
    [
        check_output(
            f'git clone --no-checkout https://github.com/BrewBlox/{repo}.git', shell=True, cwd=WORKDIR)
        for repo in REPOS
        if not path.exists(f'{WORKDIR}/{repo}/.git')
    ]


def install_gh():
    check_output('sudo apt update', shell=True)
    check_output('sudo apt install -y curl', shell=True)
    check_output('curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg'
                 + ' | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg', shell=True)
    check_output('sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg', shell=True)
    check_output('echo "deb [arch=$(dpkg --print-architecture)'
                 + ' signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg]'
                 + ' https://cli.github.com/packages stable main"'
                 + ' | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null', shell=True)
    check_output('sudo apt update', shell=True)
    check_output('sudo apt install -y gh', shell=True)


def prepare():
    create_repos()
    if not which('gh') and utils.confirm('GitHub cli not found - do you want to install it?'):
        install_gh()


@cli.command()
def git_info():
    print('Stash directory:', WORKDIR)
    print('Github repositories:', *REPOS, sep='\n\t')
    check_call('gh --version', shell=True)


@cli.command()
def delta():
    """Show commit delta for all managed repositories"""
    prepare()

    headers = ['repository'.ljust(25), 'develop >', 'edge']
    print(*headers)
    # will include separators added by print()
    print('-' * len(' '.join(headers)))
    for repo in REPOS:
        check_output('git fetch --tags --quiet',
                     shell=True,
                     cwd=f'{WORKDIR}/{repo}')
        dev_edge = check_output(
            'git rev-list --count origin/edge..origin/develop',
            shell=True,
            cwd=f'{WORKDIR}/{repo}').decode().rstrip()
        vals = [repo, dev_edge, '-']
        print(*[v.ljust(len(headers[idx])) for idx, v in enumerate(vals)])


@cli.command()
def compare():
    """Show GitHub comparison URLs for all managed repositories"""
    for repo in REPOS:
        print(f'https://github.com/BrewBlox/{repo}/compare/edge...develop')


@cli.command()
def release_edge():
    """Create develop -> edge PRs for all managed repositories"""
    prepare()

    for repo in REPOS:
        if not utils.confirm(f'Do you want to create a develop -> edge PR for {repo}?'):
            continue

        run(f'gh pr create --repo BrewBlox/{repo} --title "Edge release" --body "" --base edge --head develop',
            shell=True,
            check=False)
