## UPP

UPP: Uplift Power Play

A tool for parsing, dumping and modifying data in Radeon PowerPlay tables

### Introduction

UPP is able to parse and modify binary data structures of PowerPlay tables
commonly found on certain AMD Radeon GPUs. Drivers on recent AMD GPUs
allow PowerPlay tables to be dynamically modified on runtime, which may be
known as "soft-PowerPlay" in coin-mining community. On Linux, the PP table
is by default found at: `/sys/class/drm/card0/device/pp_table`.

### Requirements

Python 2.7 or 3.6+, codecs, collections, struct, click. Should work on
Windows as well, but modified table needs to be uploaded to registry instead
of sysfs file.

### Usage

At its current form this is a CLI only tool. Getting help:

    Usage: upp [OPTIONS] COMMAND [ARGS]...

      UPP: Uplift Power Play

      A tool for parsing, dumping and modifying data in Radeon PowerPlay tables.

      UPP is able to parse and modify binary data structures of PowerPlay tables
      commonly found on certain AMD Radeon GPUs. Drivers on recent AMD GPUs
      allow PowerPlay tables to be dynamically modified on runtime, which may be
      known as "soft PowerPlay tables". On Linux, the PowerPlay table is by
      default found at:

         /sys/class/drm/card0/device/pp_table

      This tool currently supports reading and modifying PowerPlay tables found
      on the following AMD GPU families:

        - Polaris
        - Vega
        - Radeon VII
        - Navi 10
        - Navi 14

      Note: iGPUs found in many recent AMD APUs are using completely different
      PowerPlay control methods, this tool does not support them.

      If you have bugs to report or features to request please check:

        github.com/sibradzic/upp

    Options:
      -i, --pp-file <filename>  Input/output PP table binary file
      -d, --debug / --no-debug  Debug mode
      -h, --help                Show this message and exit.

    Commands:
      dump     Dumps all PowerPlay parameters to console
      extract  Extract PowerPlay table from Video BIOS ROM image
      get      Get current value of a PowerPlay parameter
      set      Set value(s) to PowerPlay parameter(s)

Dumping all data:

    Usage: upp dump [OPTIONS]

      Dump all PowerPlay data to console

      De-serializes PowerPlay binary data into a Python dictionary.

      In standard mode all data will be dumped to console, where data hierarchy
      is indicated by indentation.

      In raw mode a table showing all hex and binary data, as well as variable
      names and values, will be dumped.

    Options:
      -r, --raw / --no-raw  Show raw binary data
      -h, --help            Show this message and exit.

Extracting PowerPlay table from Video ROM image:

    Usage: upp extract [OPTIONS]

      Extracts PowerPlay data from full VBIOS ROM image

      Default output file name will be an original ROM file name with an
      additional .pp_table extension.

    Options:
      -r, --video-rom <filename>  Input Video ROM binary image file   [required]
      -h, --help                  Show this message and exit.

Getting parameter:

    Usage: upp get [OPTIONS] VARIABLE_PATH

      Retrieves current value of a particular PP parameter

      The parameter variable path must be specified in "/<param> notation", for
      example:

          /FanTable/TargetTemperature
          /VddgfxLookupTable/7/Vdd

      The raw value of the parameter will be retrieved, decoded and displayed on
      console.

    Options:
      -h, --help  Show this message and exit.

Setting parameters:

    Usage: upp set [OPTIONS] VARIABLE_PATH_SET...

      Sets values to one or multiple PP parameters

      The parameter path and value must be specified in "/<param>=<value>
      notation", for example:

          /PowerTuneTable/TDP=75 /SclkDependencyTable/7/Sclk=107000

      Multiple PP parameters can be set at the same time. The PP tables will not
      be changed unless additional --write option is set.

    Options:
      -w, --write  Write changes to PP binary
      -h, --help   Show this message and exit.

