import sys
import logging
import argparse

from .main import DockerGhaRunner
from .version import get_version
from .const import PACKAGE_NAME

def main():
    """CLI entrypoint for the docker_gha_runner package
    """
    parser = argparse.ArgumentParser(prog=PACKAGE_NAME, usage='docker_gha_runner -f config.json', description=PACKAGE_NAME + ': GitHub Action Self-hosted Runner Operator for Docker')
    parser.add_argument('-f', '--file', help='Config file', type=str, required=True)
    parser.add_argument('-v', '--version', help='Get version', action='version', version=PACKAGE_NAME + ": v" + get_version())
    parser.add_argument('--debug', help='Show debug logs', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if args.debug else logging.INFO)

    client = DockerGhaRunner()
    client.set_config_from_file(args.file)
    client.run()

if __name__ == "__main__":
    main()
