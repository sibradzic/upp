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

    ./upp.py -h
    Usage: upp.py [OPTIONS] COMMAND [ARGS]...

      UPP: Uplift Power Play

      A tool for parsing, dumping and modifying data in Radeon PowerPlay tables.

      UPP is able to parse and modify binary data structures of PowerPlay tables
      commonly found on certain AMD Radeon GPUs. Drivers on recent AMD GPUs
      allow PowerPlay tables to be dynamically modified on runtime, which may be
      known as "soft-PowerPlay" in coin-mining community. On Linux, the PP table
      is by default found at:

         /sys/class/drm/card0/device/pp_table

      This tool currently supports reading and modifying PowerPlay tables found
      on the following AMD GPU families:

        - Polaris
        - Vega
        - Radeon VII

      Note: iGPUs found in many recent AMD APUs are using completely different
      PowerPlay control methods, this tool does not support them.

      I you have bugs to report or features to request please check:

        github.com/sibradzic/upp

    Options:
      -i, --input-file TEXT  Path to PP table binary file
      -d, --debug            Debug mode
      -h, --help             Show this message and exit.

    Commands:
      dump  Dumps all PowerPlay parameters to console
      get   Gets current value of a particular PP parameter
      set   Sets values to PP parameters

Dumping all data:

    $ ./upp.py dump -h
    Usage: upp.py dump [OPTIONS]

      Dumps all PowerPlay data to console

      De-serializes PowerPlay binary data into a Python dictionary.

      In standard mode all data will be dumped to console, where data hierarchy
      is indicated by indentation.

      In raw mode a table showing all hex and binary data, as well as variable
      names and values, will be dumped.

    Options:
      -r, --raw   Show raw binary data
      -h, --help  Show this message and exit.

Getting single parameter:

    $ ./upp.py get -h
    Usage: upp.py get [OPTIONS] VARIABLE_PATH

      Retrieves current value of a particular PP parameter

      The parameter variable path must be specified in "/<param> notation", for
      example:

          /FanTable/TargetTemperature
          /VddGfxLookupTable/7/Vdd

      The raw value of the parameter will be retrieved, decoded and displayed on
      console.

    Options:
      -h, --help  Show this message and exit.

Setting parameters:

    $ ./upp.py set -h
    Usage: upp.py set [OPTIONS] VARIABLE_PATH_SET...

      Sets values to one or multiple PP parameters

      The parameter path and value must be specified in "/<param>=<value>
      notation", for example:

          /PowerTuneTable/TDP=75
          /SocClockDependencyTable/7/SocClock=107000

      Multiple PP parameters can be set at the same time. The PP tables will not
      be changed unless additional --write option is set.

    Options:
      -w, --write  Write changes to PP binary
      -h, --help   Show this message and exit.

