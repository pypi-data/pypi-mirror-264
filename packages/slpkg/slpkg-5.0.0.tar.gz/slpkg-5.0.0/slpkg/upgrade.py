#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Generator
from pkg_resources import parse_version
from pathlib import Path

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.repositories import Repositories


class Upgrade(Configs):
    """ Upgrade the installed packages. """

    def __init__(self, repository: str, data: dict):
        super(Configs, self).__init__()
        self.repository: str = repository
        self.data: dict = data

        self.utils = Utilities()
        self.repos = Repositories()
        self.id: int = 0
        self.sum_upgrade: int = 0
        self.sum_removed: int = 0
        self.sum_added: int = 0
        self.installed_names: list = []
        self.installed_packages: list = []

    def load_installed_packages(self):
        if self.repository in [self.repos.slack_repo_name, self.repos.salixos_repo_name]:
            installed: dict = self.utils.all_installed()

            for name, package in installed.items():
                tag: str = self.utils.split_package(package)['tag']
                if not tag:
                    self.installed_packages.append(Path(package))
                    self.installed_names.append(name)
        else:
            repo_tag: str = self.repos.repositories[self.repository]['repo_tag']
            self.installed_packages: list = list(self.log_packages.glob(f'*{repo_tag}'))

    def packages(self) -> Generator:
        """ Returns the upgradable packages. """
        self.load_installed_packages()

        for inst in self.installed_packages:
            name: str = self.utils.split_package(inst.name)['name']
            if self.is_package_upgradeable(inst.name):
                yield name

            if self.repository == self.repos.slack_repo_name and self.removed_packages:
                if name not in self.data.keys():
                    yield name + '_Removed.'

        if self.repository == self.repos.slack_repo_name and self.new_packages:
            for name in self.data.keys():
                # if not self.utils.is_package_installed(name):
                if name not in self.installed_names:
                    yield name

    def is_package_upgradeable(self, installed: str) -> bool:
        inst_name: str = self.utils.split_package(installed)['name']
        if self.data.get(inst_name):
            repo_package: str = self.data[inst_name]['package'][:-4]
            try:
                if parse_version(repo_package) > parse_version(installed):
                    return True
            except ValueError:
                return False
        return False

    def check_packages(self) -> None:
        found_packages: dict = {}
        self.load_installed_packages()

        for installed in self.installed_packages:
            name: str = self.utils.split_package(installed.name)['name']

            if self.data.get(name):
                repo_package: str = self.data[name]['package'][:-4]

                if parse_version(repo_package) > parse_version(installed.name):
                    self.id += 1
                    self.sum_upgrade += 1
                    inst_version: str = self.utils.split_package(installed.name)['version']
                    inst_build: str = self.utils.split_package(installed.name)['build']
                    repo_version: str = self.data[name]['version']
                    repo_build: str = self.data[name]['build']

                    found_packages[self.id]: dict = {
                        'name': name,
                        'inst_version': inst_version,
                        'inst_build': inst_build,
                        'repo_version': repo_version,
                        'repo_build': repo_build,
                        'type': 'upgrade'
                    }

            if self.repository == self.repos.slack_repo_name and self.removed_packages:
                if name not in self.data.keys():
                    self.id += 1
                    self.sum_removed += 1
                    inst_version: str = self.utils.split_package(installed.name)['version']
                    inst_build: str = self.utils.split_package(installed.name)['build']
                    repo_version: str = ''
                    repo_build: str = ''

                    found_packages[self.id]: dict = {
                        'name': name + '_Removed.',
                        'inst_version': inst_version,
                        'inst_build': inst_build,
                        'repo_version': repo_version,
                        'repo_build': repo_build,
                        'type': 'remove'
                    }

        if self.repository == self.repos.slack_repo_name and self.new_packages:
            for name in self.data.keys():
                # if not self.utils.is_package_installed(name):
                if name not in self.installed_names:
                    self.id += 1
                    self.sum_added += 1
                    inst_version: str = ''
                    inst_build: str = ''
                    repo_version: str = self.data[name]['version']
                    repo_build: str = self.data[name]['build']

                    found_packages[self.id]: dict = {
                        'name': name,
                        'inst_version': inst_version,
                        'inst_build': inst_build,
                        'repo_version': repo_version,
                        'repo_build': repo_build,
                        'type': 'add'
                    }

        if found_packages:
            title: str = f"{'packages':<18} {'Version':<15} {'Build':<6} {'Repository':<15} {'Build':<5} {'Repo':>15}"
            print(len(title) * '=')
            print(f'{self.bgreen}{title}{self.endc}')
            print(len(title) * '=')

            for data in found_packages.values():
                name: str = data['name']
                repo_version: str = data['repo_version']
                repo_build: str = data['repo_build']
                inst_version: str = data['inst_version']
                inst_build: str = data['inst_build']
                mode: str = data['type']

                if len(name) > 17:
                    name: str = f'{name[:14]}...'
                if len(inst_version) > 15:
                    inst_version: str = f"{inst_version[:11]}..."
                if len(repo_version) > 15:
                    repo_version: str = f"{repo_version[:11]}..."

                color: str = self.violet
                if mode == 'remove':
                    color: str = self.red
                if mode == 'add':
                    color: str = self.cyan

                print(f"{color}{name:<18}{self.endc} {inst_version:<15} {inst_build:<6} {repo_version:<15} "
                      f"{repo_build:<5} {self.repository:>15}")

            print(len(title) * '=')
            print(f'{self.grey}Packages to upgrade {self.sum_upgrade}, packages to remove '
                  f'{self.sum_removed} and packages added {self.sum_added}.{self.endc}\n')
        else:
            print('\nEverything is up-to-date!\n')
        raise SystemExit(0)
