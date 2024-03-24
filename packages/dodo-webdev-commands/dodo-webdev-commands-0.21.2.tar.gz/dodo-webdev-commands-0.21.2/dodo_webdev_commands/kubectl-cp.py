import os
from argparse import ArgumentParser

from dodo_commands import Dodo
from dodo_commands.extra.dodo_docker_commands.decorators.kubectl import (
    Decorator as KubeCtlDecorator,
)


def _args():
    parser = ArgumentParser(description="")
    parser.add_argument("filename")
    parser.add_argument("--rev", action="store_true")

    # Use the parser to create the command arguments
    args = Dodo.parse_args(parser, config_args=[])

    return args


# Use safe=False if the script makes changes other than through Dodo.run
if Dodo.is_main(__name__, safe=True):
    args = _args()
    container_name = KubeCtlDecorator.get_full_container_name(Dodo.get_config)

    if args.rev:
        Dodo.run(
            [
                "kubectl",
                "cp",
                f"{container_name}:/app/{args.filename}",
                f"./{os.path.basename(args.filename)}",
            ]
        )
    else:
        Dodo.run(["kubectl", "cp", args.filename, f"{container_name}:/app"])
