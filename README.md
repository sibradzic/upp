## UPP

UPP: Uplift Power Play

A tool for parsing, dumping and modifying data in Radeon PowerPlay tables

### Introduction

UPP is able to parse and modify binary data structures of PowerPlay tables
commonly found on certain AMD Radeon GPUs. Drivers on recent AMD GPUs
allow PowerPlay tables to be dynamically modified on runtime, which may be
known as "soft" PowerPlay table. On Linux, the PowerPlay table is by default
found at: `/sys/class/drm/card0/device/pp_table`.

This tool does very minimal interpretation of actual PowerPlay table values.
By design, it is mostly up to the user to do such thing.

Alternatively, one can use this tool to get PowerPlay data by:

* Extracting PowerPlay table from Video ROM image (see extract command)
* Importing "Soft PowerPlay" table from Windows registry, directly from
  offline Windows/System32/config/SYSTEM file on disk, so it would work
  from Linux distro that has access to mounted Windows partition
  (path to SYSTEM registry file is specified with `--from-registry` option)
* Importing "Soft PowerPlay" table from "More Powe Tool" MPT file
  (path to MPT file is specified with `--from-mpt option`)

This tool currently supports parsing and modifying PowerPlay tables found
on the following AMD GPU families:

* Polaris
* Vega
* Radeon VII
* Navi 10
* Arcturus (MI100)
* Navi 12 (PRO V520)
* Navi 14
* Navi 21 (Sienna Cichlid)
* Navi 22 (Navy Flounder)
* Navi 23 (Dimgrey Cavefish)
* Navi 3x
* Navi 4x

Notes:
* iGPUs found in many recent AMD APUs are using completely different
  PowerPlay control methods, this tool does not support them.
* The amdgpu kernel driver does not fully implement modifying the PowerPlay
  tables on runtime for Navi 3x and Navi 4x cards.
* The amdgpu kernel driver does the incomplete PowerPlay table data dump
  to the `/sys/class/drm/cardX/device/pp_table` file, for Navi 3x AND 4x.
  The pp_table file is truncated to first 4095 bytes. Likely a driver bug.

**WARNING**: Authors of this tool are in no way responsible for any damage
that may happen to your expansive graphics card if you choose to modify
card voltages, power limits, or any other PowerPlay parameters. Always
remember that you are doing it entirely on your own risk!

If you have bugs to report or features to request please create an issue on:
https://github.com/sibradzic/upp

### Requirements

Python 3.7+, click library. Optionally, for reading "soft" PowerPlay table
from Windows registry: python-registry. Should work on Windows as well
(testers wanted).

### Installation

Either get it with pip:

    pip install upp

or use it as is directly from the source tree:

    cd src
    python3 -m upp.upp --help

### Usage

At its current form this is a CLI only tool. Getting help:

    upp --help

or

    upp <command> --help

Upp will only work by specifying a command which tells it what to do to one's
Radeon PowerPlay table data. Currently available commands are:

* **dump** - Dumps all PowerPlay data to console
* **extract** - Extracts PowerPlay data from full VBIOS ROM image
* **inject** - Injects PowerPlay data from file into VBIOS ROM image
* **get** - Retrieves current value of one or multiple PowerPlay parameter(s)
* **set** - Sets value to one or multiple PowerPlay parameters
* **undump** - Sets all PowerPlay parameters to pp file or registry
* **version** - Shows UPP version

So, an usage pattern would be like this:

    upp [OPTIONS] COMMAND [ARGS]...

Some generic options applicable to all commands may be used, but please note
that they have to be specified *before* an actual command:

    -p, --pp-file <filename>        Input/output PP table binary file.
    -f, --from-registry <filename>  Import PP_PhmSoftPowerPlayTable from Windows
                                    registry (overrides -p / --pp-file option).
    -m, --from-mpt <filename>       Import PowerPlay Table from More Power Tool
                                    (overrides --pp-file and --from-registry optios).
    -d, --debug / --no-debug        Debug mode.
    -h, --help                      Show this message and exit.

#### Dumping all data:

The **dump** command de-serializes PowerPlay binary data into a human-readable
text output. For example:

    upp dump

In standard mode all data will be dumped to console, where data tree hierarchy
is indicated by indentation. In raw mode a table showing all hex and binary
data, as well as variable names and values, will be dumped.

#### Extracting PowerPlay table from Video ROM image:

Use **extract** command for this. The source video ROM binary must be specified
with `-r/--video-rom` parameter, and extracted PowerPlay table will be saved
into file specified with generic `-p/--pp-file` option. For example:

    upp --pp-file=extracted.pp_table extract -r VIDEO.rom

Default output file name will be an original ROM file name with an
additional .pp_table extension.

#### Injecting PowerPlay data from file into VBIOS ROM image:

Use **inject** command for this. The input video ROM binary must be specified
with `-i/--input-rom` parameter, and the output ROM can be specified with an
optional `-o/--output-rom parameter`. For example:

    upp -p modded.pp_table inject -i original.rom -o modded.rom

**WARNING**: Modified vROM image is probably not going to work if flashed as is
to your card, due to ROM signature checks on recent Radeon cards. Authors of
this tool are in no way responsible for any damage that may happen to your
expansive graphics card if you choose to flash the modified video ROM, you are
doing it entirely on your own risk.

#### Getting PowerPlay table parameter value(s):

The **get** command retrieves current value of one or multiple PowerPlay table
parameter value(s). The parameter variable path must be specified in `/<param>`
notation, for example:

    upp get smc_pptable/FreqTableGfx/1 smc_pptable/FreqTableGfx/2
    1850
    1400

The order of the output values will match the order of the parameter variable
paths specified.

#### Setting PowerPlay table parameter value(s):

The **set** command sets value to one or multiple PowerPlay table
parameter(s). The parameter path and value must be specified in
`/<param>=<value>` notation, for example:

    upp -p /tmp/custom-pp_table set --write  \
      smc_pptable/SocketPowerLimitAc/0=100   \
      smc_pptable/SocketPowerLimitDc/0=100   \
      smc_pptable/FanStartTemp=100           \
      smc_pptable/FreqTableGfx/1=1550

It is possible to set parameters from a configuration file with one
"/<param>=<value>" per line using -c/--from-conf instead of directly
passing parameters from command line

    upp set --from-conf=card0.conf

Note the `--write` parameter, which has to be specified to actually commit
changes to the PowerPlay table file.

#### Undumps all PowerPlay parameters:

The **undump** command sets all values from previously dumped PowerPlay table parameter(s) back to pp_table or registry. It allows you to make changes in dumped text file and write back all changes at once. Basically it's a convenient way to set multiple values. For example:

    # extract pp_table from vbios
    upp --pp-file=vbios.pp_table extract -r vbios.rom
    # dump powerplay table to text file
    upp --pp-file=vbios.pp_table dump > vbios.pp_table.dump
    # make changes in vbios.pp_table.dump
    # undump all changes back into pp_table
    upp --pp-file=vbios.pp_table undump -d vbios.pp_table.dump -w

Note the `--write` parameter, which has to be specified to actually commit
changes to the PowerPlay table file.

#### Getting upp version

    upp version

#### Running as sudo

Note that if you need to run upp deployed with **pip** in `--user` mode with
sudo, you'll need to add some parameters to sudo command to make user env
available to super-user. For example:

    sudo -E env "PATH=$PATH" upp --help

