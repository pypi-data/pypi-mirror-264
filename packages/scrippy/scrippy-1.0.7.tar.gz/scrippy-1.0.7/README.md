![Version](https://img.shields.io/static/v1?label=version&color=informational&message=1.0.7)
![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

# Scrippy installer

This is the [**Scrippy**](https://codeberg.org/scrippy) framework installer.

## Configure and install [*the Scrippy scripting framework*](https://codeberg.org/scrippy/) with default value

   - With configuration setting confirmation

      ```shell
      export PATH=${HOME}/.local/bin:${PATH}
      pip install scrippy
      scrippy install
      ```

   - Without configuration setting confirmation

      ```shell
      export PATH=${HOME}/.local/bin:${PATH}
      pip install scrippy
      scrippy install -y
      ```

## Configure and install [*the Scrippy scripting framework*](https://codeberg.org/scrippy/) interactively

  ```shell
  pip install scrippy
  scrippy install -i
  ```

## Configure and install [*the Scrippy scripting framework*](https://codeberg.org/scrippy/) from custom configuration file

  ```shell
  pip install scrippy
  scrippy install -c /path/to/config.yml
  ```

### Configuration file example

```yaml
env:
  confdir: ~/.local/share/scrippy/conf
  datadir: ~/.local/share/scrippy/data
  histdir: ~/.local/share/scrippy/hist
  logdir: ~/.local/share/scrippy/log
  reportdir: ~/.local/share/scrippy/reports
  templatedir: ~/.local/share/scrippy/templates
  tmpdir: ~/.local/share/scrippy/tmp
packages:
  scrippy-core: latest
  scrippy-remote: latest
  scrippy-api: latest
  scrippy-mail: latest
  scrippy-git: latest
  scrippy-template: latest
  scrippy-snmp: latest
```

## Uninstall [*the Scrippy scripting framework*](https://codeberg.org/scrippy/)

  ```shell
  scrippy uninstall
  ```

## Uninstall [*the Scrippy scripting framework*](https://codeberg.org/scrippy/) and delete all scippy directories

  ```shell
  scrippy uninstall --prune
  ```
