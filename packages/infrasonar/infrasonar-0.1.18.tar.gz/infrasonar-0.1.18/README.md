[![CI](https://github.com/infrasonar/toolkit/workflows/CI/badge.svg)](https://github.com/infrasonar/toolkit/actions)
[![Release Version](https://img.shields.io/github/release/infrasonar/toolkit)](https://github.com/infrasonar/toolkit/releases)

The InfraSonar tool can be used to manage assets for a container. The tool has two main features. One is to read all assets from a container to YAML output. If needed, all collector and label information can be included.
The other feature of this tool is to apply a YAML file to InfraSonar. These two features combined allow you to easily add new assets as well as managing existing assets for a container.

## Installation

Using pip:

```shell
pip install infrasonar
```

Or, clone this project and use the setup

```shell
python setup.py install
```

## Apply assets

Create a _yaml_ file, for example: `assets.yaml` _(you may also use [get-assets](#get-assets) to export the current assets and make modifications)_

```yaml
container: 12345

labels:
  windows: 3257

configs:
  tcp:
    checkCertificatePorts: [443, 995, 993, 465, 3389, 989, 990, 636, 5986]

assets:
- name: foo.local
  kind: Windows
  labels: ["windows"]
  collectors:
  - key: lastseen
  - key: ping
  - key: tcp
    config: tcp
  - key: wmi
```

Next, use the following command to apply the assets: _(**-a** will **only add** labels and collectors, **-d** performs a **dry-run** without actually applying the changes)_

```bash
infrasonar apply-assets assets.yaml -a -d
```

The script will create a new asset if an asset with the given name cannot be found, otherwise it will apply the changes to the existing asset. Existing labels and/or collectors will _not_ be removed, but a _kind_ will be overwritten if one is given. The properties _kind_, _description_, _mode_, _labels_ and _collectors_ are all optional.

### Token

A token might be included in the yaml file:
```yaml
token: xxxxxx
```

Or, it will be asked in a prompt when starting the script.

> :point_right: Note that a **token** with **Agent** flags must be used for the _apply-assets_ action to work. A **container token** is required when no _container Id_ is given or when one or more assets without an _asset Id_ are used.


## Get asset

Get a single asset. _(in the example below, 123 is a asset Id)_

```bash
infrasonar get-asset 123 -o yaml
```

## Get assets

Get container assets. _(in the example below, 123 is a container Id)_

```bash
infrasonar get-assets 123 -o yaml
```


## VMware guests

Generate YAML (or JSON) with VMware Guests which are found on ESX or vCenter but wherefore no asset with the `vmwareguest` collector is found. This YAML can then be used to install the VMware Guest collector with a single command. The default is to use the VCenter. For ESX the `-c esx` argument.

Example:  _(in the example below, 123 is a container Id)_

```bash
infrasonar vmware-guests 123 > missing.yaml
```

Review the missing.yaml file _(open in editor or apply a dry-run)_

```
infrasonar apply-assets missing.yaml -a -d
```

> :point_right: Do not forget to use **-a** to prevent removing other collectors and use **-d** to perform a dry-run for verifying the changes.

## Hyper-V guests

Generate YAML (or JSON) with Hyper-V Guests which are found on a Hyper-V asset(s) but wherefore no asset with the `hypervguest` collector is found. This YAML can then be used to install the Hyper-V Guest collector with a single command.

Example:  _(in the example below, 123 is a container Id)_

```bash
infrasonar hyperv-guests 123 > missing.yaml
```

Review the missing.yaml file _(open in editor or apply a dry-run)_

```
infrasonar apply-assets missing.yaml -a -d
```

> :point_right: Do not forget to use **-a** to prevent removing other collectors and use **-d** to perform a dry-run for verifying the changes.

## UniFi devices

Generate YAML (or JSON) with UniFi devices which are found on a UniFi Controller asset(s) but wherefore no asset with the `unifidevice` or `unifidevicesvc` collector is found. This YAML can then be used to install the UniFi Device collector with a single command. The default is to use the `unificontroller`. For using the _service_ variant, use the `-c unificontrollersvc` argument.

Example:  _(in the example below, 123 is a container Id)_

```bash
infrasonar unifi-devices 123 > missing.yaml
```

Review the missing.yaml file _(open in editor or apply a dry-run)_

```
infrasonar apply-assets missing.yaml -a -d
```

> :point_right: Do not forget to use **-a** to prevent removing other collectors and use **-d** to perform a dry-run for verifying the changes.

## Help

```
infrasonar -h
infrasonar get-asset -h
infrasonar get-assets -h
infrasonar apply-assets -h
infrasonar vmware-guests -h
```
