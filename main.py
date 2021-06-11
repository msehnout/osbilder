"""OSBilder.

Usage:
  osbilder init [--workdir=<directory>]
  osbilder build --distro=<distro> --image-type=<imgtype> --blueprint=<blueprint> [--workdir=<directory>]
  osbilder (-h | --help)
  osbilder --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import json
import os
import shutil
import subprocess
import platform

from typing import Optional
from os import PathLike

import tomli

from docopt import docopt


class WorkDir:

    def __init__(self, dir: Optional[PathLike]):
        self.root = dir if dir is not None else os.getcwd()
        self.blueprints = os.path.join(self.root, "blueprints")
        self.repositories = os.path.join(self.root, "repositories")

    def create(self) -> None:
        scriptdir = os.path.dirname(os.path.realpath(__file__))
        os.mkdir(self.blueprints)
        shutil.copytree(os.path.join(scriptdir, "data", "repositories"), self.repositories)


def build(distro: Optional[str], image_type: Optional[str], blueprint: Optional[str], workdir: Optional[str]):
    wd = WorkDir(workdir)
    with open(os.path.join(wd.blueprints, f"{blueprint}.toml"), "r") as f:
        blueprint = f.read()
        bp_dict = tomli.loads(blueprint)
    with open(os.path.join(wd.repositories, f"{distro}.json"), "r") as f:
        repositories = json.load(fp=f)
    arch = platform.machine()
    composer_request = {
        "distro": distro,
        "image-type": image_type,
        "arch": arch,
        "blueprint": bp_dict,
        "repositories": repositories[arch]
    }
    print("Running osbuild-pipeline")
    #print(json.dumps(composer_request))
    res = subprocess.run(["osbuild-pipeline", "-"], capture_output=True, check=False, input=json.dumps(composer_request),
                         encoding="utf-8")
    if res.returncode != 0:
        print(res.stderr)
        exit(1)

    manifest = res.stdout
    #print(manifest)
    print("Run osbuild")
    res = subprocess.run(["osbuild", "--output-directory", os.getcwd(), "-"], capture_output=True, check=False,
                         input=json.dumps(manifest),
                         encoding="utf-8")
    if res.returncode != 0:
        print(res.stderr)
        exit(1)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='OSBilder 1.0')
    print(arguments)
    if arguments["init"]:
        wd = WorkDir(arguments["--workdir"])
        wd.create()
    elif arguments["build"]:
        build(arguments["--distro"], arguments["--image-type"], arguments["--blueprint"], arguments["--workdir"])
