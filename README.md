# `gen_vpo_sfizz_presets`

## Overview

Given the 400+ SFZ files distributed by the [Virtual Playing
Orchestra](http://virtualplaying.com/virtual-playing-orchestra/), it can be useful
to define presets for the [`sfizz LV2 plugin](<https://sfz.tools/sfizz/>), to
speed up the process of finding them.


## Installation

Install it in a new virtual environment:

```bash
$ python3 -m venv /tmp/venv
$ /tmp/venv/bin/pip install gen_vpo_sfizz_presets
...
$ /tmp/venv/bin/gen_vpo_sfizz_presets --help
```

Install it in a your "user-local" area:

```bash
$ python3 -m pip install --user gen_vpo_sfizz_presets
$ gen_vpo_sfizz_presets --help
```


## Example:  Create a preset for a single SFZ file

```bash
$ gen_vpo_sfizz_presets /path/to/VPO/Brass/trombone-SEC-PERF.sfz
- Creating LV2 preset: VPO_Brass_trombone-SEC-PERF
```


## Example:  Create presets for multiple SFZ files

```bash
$ gen_vpo_sfizz_presets /path/to/VPO/Brass/*-SEC-PERF.sfz
- Creating LV2 preset: VPO_Brass_all-brass-SEC-PERF
- Creating LV2 preset: VPO_Brass_french-horn-SEC-PERF
- Creating LV2 preset: VPO_Brass_trombone-SEC-PERF
- Creating LV2 preset: VPO_Brass_trumpet-SEC-PERF
```


## Example:  Create presets for SFZ files under a directory

```bash
$ gen_vpo_sfizz_presets /path/to/VPO/Brass/
Use this SFZ: all-brass-SEC-staccato.sfz? [yNq] y
- Creating LV2 preset: VPO_Brass_all-brass-SEC-staccato
Use this SFZ: trombone-SOLO-normal-mod-wheel.sfz? [yNq] n
Use this SFZ: french-horn-SEC-PERF-staccato.sfz? [yNq] q
```
