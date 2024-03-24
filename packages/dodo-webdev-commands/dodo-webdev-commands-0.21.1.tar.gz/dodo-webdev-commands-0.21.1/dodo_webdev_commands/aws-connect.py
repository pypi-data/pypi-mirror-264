from argparse import ArgumentParser

from dodo_commands import Dodo


def _args():
    parser = ArgumentParser(description="")
    choices = Dodo.get_config("/AWS/profiles", {}).keys()
    parser.add_argument("profile", choices=choices)

    # Use the parser to create the command arguments
    args = Dodo.parse_args(parser, config_args=[])

    return args


# Use safe=False if the script makes changes other than through Dodo.run
if Dodo.is_main(__name__, safe=True):
    args = _args()
    region = Dodo.get_config("/AWS/region", "eu-central-1")
    profiles = Dodo.get_config("/AWS/profiles", {})
    profile = profiles[args.profile]

    Dodo.run(["pass", "landler/aws"])
    Dodo.run(["aws", "configure", "sso", f"--profile={profile}"])
    Dodo.run(["aws", "sts", "get-caller-identity", f"--profile={profile}"])

    for key, value in dict(AWS_PROFILE=profile).items():
        Dodo.get_container().command_line.env_vars_from_input_args.append(
            f"{key}={value}"
        )

    print("Connecting to tailscale")
    Dodo.run(["sudo", "tailscale", "up", "--accept-dns", "--accept-routes"])
    Dodo.run(
        [
            "aws",
            "eks",
            "update-kubeconfig",
            f"--region={region}",
            f"--name={profile}-eks",
            f"--alias={profile}",
        ],
    )
