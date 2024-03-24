import os
import sys
import shutil
import logging
import subprocess
import yaml
from scrippy_installer.error import ScrippyCoreError


DEFAULT_PACKAGES = {"packages": {"scrippy-core": "latest",
                                 "scrippy-remote": "latest",
                                 "scrippy-api": "latest",
                                 "scrippy-db": "latest",
                                 "scrippy-mail": "latest",
                                 "scrippy-git": "latest",
                                 "scrippy-template": "latest",
                                 "scrippy-snmp": "latest"}}

HOME_DIR = os.path.expanduser("~")
DEFAULT_ENV = {"env": {"logdir": "log",
                       "histdir": "hist",
                       "reportdir": "reports",
                       "tmpdir": "tmp",
                       "datadir": "data",
                       "templatedir": "templates",
                       "confdir": "conf"}}


class ScrippyInstaller:
  def __init__(self):
    self.env = self.load_env()
    self.packages = DEFAULT_PACKAGES

  def load_env(self):
    scrippy_base_dir = os.path.join(HOME_DIR, ".local/share/scrippy/")
    if os.getuid() == 0:
      scrippy_base_dir = "/etc/scrippy/"
    for key, value in DEFAULT_ENV.get("env").items():
      DEFAULT_ENV.get("env")[key] = os.path.join(scrippy_base_dir, value)
    return DEFAULT_ENV

  def build_config(self):
    logging.info("[+] Configuration edition")
    for key, value in self.env.get("env").items():
      logging.warning(f"  {key} [{value}]:")
      self.env.get("env")[key] = input() or value
    logging.info("[+] Package versions")
    for key, value in self.packages.get("packages").items():
      logging.warning(f"  {key} [{value}]:")
      self.packages.get("packages")[key] = input() or value

  def load_config(self, config):
    logging.info(f"[+] Loading configuration from: {config}")
    if os.path.isfile(config):
      with open(config, mode="r", encoding="utf-8") as conf_file:
        scrippy_conf = yaml.load(conf_file, Loader=yaml.FullLoader)
        if scrippy_conf.get("env") is not None:
          for key, value in self.env.get("env").items():
            try:
              conf_value = os.path.expanduser(scrippy_conf.get("env").get(key))
            except TypeError:
              conf_value = None
            self.env.get("env")[key] = conf_value or value
        if scrippy_conf.get("packages") is not None:
          for key, value in self.packages.get("packages").items():
            self.packages.get("packages")[key] = scrippy_conf.get("packages").get(key) or value
    else:
      raise ScrippyCoreError(f"File `{config}` not found")

  def get_config_filename(self):
    logging.info(" '-> Looking for Scrippy installation...")
    main_config_dir = os.path.join(HOME_DIR, ".config/scrippy")
    if os.getuid() == 0:
      main_config_dir = "/etc/scrippy"
    config_file = os.path.join(main_config_dir, "scrippy.yml")
    if os.getuid() == 0:
      if os.path.isfile(config_file):
        logging.warning(f"  '-> Warning: System level configuration found: ({config_file})")
        logging.warning("  '-> Would you like to uninstall the system wide Scrippy installation ? [y/N] ")
        resp = input().upper() or "N"
        if resp == "Y":
          return config_file
        else:
          logging.warning("   '-> System wide installation kept")
      else:
        logging.info("  '-> No system level configuration file found")
    else:
      if os.path.isfile(config_file):
        return config_file
      else:
        logging.info("  '-> No user level configuration file found")
        return None

  def install(self, yes=False):
    logging.info("[+] Configuration to be installed:")
    logging.warning("  env:")
    for key, value in self.env.get("env").items():
      logging.warning(f"    {key}: {value}")
    logging.info("Confirm new configuration (overwrites preexisting configuration) [Y/n]")
    resp = "Y"
    if not yes:
      resp = input().upper() or "Y"
    if resp == "Y":
      main_config_dir = os.path.join(HOME_DIR, ".config/scrippy")
      if os.getuid() == 0:
        main_config_dir = "/etc/scrippy"
      main_config_file = os.path.join(main_config_dir, "scrippy.yml")
      os.makedirs(main_config_dir, mode=0o750, exist_ok=True)
      for key, value in self.env.get("env").items():
        logging.info(f"[+] Creating {key}")
        try:
          os.makedirs(value, mode=0o750, exist_ok=True)
        except Exception as err:
          logging.critical(f"[{err.__class__.__name__}] {err}")
          sys.exit(1)
      logging.info(f"[+] Saving main configuration file: {main_config_file}")
      with open(main_config_file, mode="w", encoding="utf-8") as scrippy_conf:
        yaml.dump(self.env, scrippy_conf)
        logging.info("  => Configuration updated.")
        self.install_packages(yes=yes)
    else:
      logging.info("  => Installation cancelled")

  def get_package_list(self):
    packages = list()
    for key, value in self.packages.get("packages").items():
      if value == "latest":
        packages.append(key)
      else:
        packages.append(f"{key}=={value}")
    return packages

  def install_packages(self, yes=False):
    logging.info("[+] Packages to be installed:")
    packages = self.get_package_list()
    for pkg in packages:
      logging.warning(f"  - {pkg}")
    logging.info("Confirm package installation (automatic downgrade/upgrade) [Y/n]")
    resp = "Y"
    if not yes:
      resp = input().upper() or "Y"
    if resp == "Y":
      logging.info("[+] Installing Scrippy packages")
      try:
        subprocess.check_call([sys.executable,
                              "-m",
                               "pip",
                               "install",
                               "--upgrade",
                               *packages])
      except Exception as err:
        logging.critical(f"[{err.__class__.__name__}] {err}")
        sys.exit(1)
    else:
      logging.info("  => Installation cancelled")

  def uninstall(self, prune=False):
    logging.info("[+] Uninstalling Scrippy")
    config = self.get_config_filename()
    if config is not None:
      self.load_config(config)
      if prune:
        logging.warning(" '-> Confirm Scrippy directories definitive deletion [y/N]")
        resp = input().upper() or "N"
        if resp == "Y":
          for key, value in self.env.get("env").items():
            logging.info(f" '-> Removing {key}: {value}")
            shutil.rmtree(path=value, ignore_errors=False)
        else:
          logging.info("  '-> Scrippy directories not deleted")
      packages = self.get_package_list()
      logging.info(" '-> Packages to be uninstalled")
      for pkg in packages:
        logging.info(f"    - {pkg}")
      subprocess.check_call([sys.executable,
                             "-m",
                             "pip",
                             "uninstall",
                             *packages])
    else:
      logging.error(" '-> Uninstall aborted")
