import sys
import logging
import argparse
from scrippy_installer import logger
from scrippy_installer.installer import ScrippyInstaller


def parse_args():
  parser = argparse.ArgumentParser(prog="scrippy",
                                   description="Scrippy framework installation and configuration helper.")
  subparsers = parser.add_subparsers(dest="subcommand")
  inst = subparsers.add_parser("install", description="Install Scrippy")
  inst.add_argument("-i", "--interactive",
                    action="store_true",
                    required=False,
                    help="Optional. Prompt for configuration values.")
  inst.add_argument("-c", "--config",
                    required=False,
                    help="Optional. Configure Scrippy framework according to specified YAML file.")
  inst.add_argument("-y", "--yes",
                    action="store_true",
                    required=False,
                    help="Optional. Answer `yes` to all questions.")
  uninst = subparsers.add_parser("uninstall",
                                 description="Uninstall Scrippy ")
  uninst.add_argument("-p", "--prune",
                      action="store_true",
                      required=False,
                      help="Optional. Remove all Scrippy directories and content (confdir, logdir, histdir, datadir, reportdir, templatedir, tmpdir)")
  args = parser.parse_args()
  try:
    if args.subcommand == "install" and \
            args.interactive and \
            args.config is not None:
      logging.critical("Error: --interactive and --config options are mutually exclusive")
      inst.print_help()
      sys.exit(1)
    if args.subcommand is None:
      raise AttributeError(

      )
  except AttributeError:
    logging.critical("Error: missing keyword or option")
    inst.print_help()
    sys.exit(1)
  return args


def main():
  log_manager = logger.Manager()
  log_manager.set_log_level(logging.INFO)
  installer = ScrippyInstaller()
  args = parse_args()
  if args.subcommand == "install":
    if args.config is not None:
      installer.load_config(args.config)
    if args.interactive:
      installer.build_config()
    installer.install(yes=args.yes)
  else:
    installer.uninstall(prune=args.prune)


if __name__ == "__main__":
  main()
