## UPP

UPP: Uplift Power Play

A tool for parsing, dumping and modifying data in Radeon PowerPlay tables

### Introduction

UPP is able to parse and modify binary data structures of PowerPlay tables
commonly found on certain AMD Radeon GPUs. Drivers on recent AMD GPUs
allow PowerPlay tables to be dynamically modified on runtime, which may be
known as "soft" PowerPlay table. On Linux, the PowerPlay table is by default
found at: `/sys/class/drm/card0/device/pp_table`.

### Requirements

Python 2.7 or 3.6+, click library. Optionally, for reading "soft" PowerPlay
table from Windows registry: python-registry. Should work on Windows as well
(testers wanted).

### Usage

Note that if you need to run upp deployed with pip in '--user' mode with sudo,
you'll need to add some parameters to sudo command to make user env available
to super-user. For example:

    sudo -E env "PATH=$PATH" upp --help

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

      There are also two alternative ways of getting PowerPlay data that this
      tool supports:

       - By extracting PowerPlay table from Video ROM image (see extract command)
       - Import "Soft PowerPlay" table from Windows registry, directly from
         offline Windows/System32/config/SYSTEM file on disk, so it would work
         from Linux distro that has acces to mounted Windows partition
         (path to SYSTEM registry file is specified with --from-registry option)

      This tool currently supports parsing and modifying PowerPlay tables found
      on the following AMD GPU families:

        - Polaris
        - Vega
        - Radeon VII
        - Navi 10
        - Navi 14
        - Navi 20 (Sienna Cichlid)

      Note: iGPUs found in many recent AMD APUs are using completely different
      PowerPlay control methods, this tool does not support them.

      If you have bugs to report or features to request please check:

        github.com/sibradzic/upp

    Options:
      -p, --pp-file <filename>        Input/output PP table binary file.
      -f, --from-registry <filename>  Import PP_PhmSoftPowerPlayTable from Windows
                                      registry (overrides -p / --pp-file option).
      -d, --debug / --no-debug        Debug mode.
      -h, --help                      Show this message and exit.

    Commands:
      dump     Dumps all PowerPlay parameters to console.
      extract  Extract PowerPlay table from Video BIOS ROM image.
      get      Get current value of a PowerPlay parameter(s).
      set      Set value to PowerPlay parameter(s).
      version  Show UPP version.

Dumping all data:

    Usage: upp dump [OPTIONS]

      Dump all PowerPlay data to console

      De-serializes PowerPlay binary data into a human-readable text output. For
      example:

          upp --pp-file=radeon.pp_table dump

      In standard mode all data will be dumped to console, where data tree
      hierarchy is indicated by indentation.

      In raw mode a table showing all hex and binary data, as well as variable
      names and values, will be dumped.

    Options:
      -r, --raw / --no-raw  Show raw binary data.
      -h, --help            Show this message and exit.

Extracting PowerPlay table from Video ROM image:

    Usage: upp extract [OPTIONS]

      Extracts PowerPlay data from full VBIOS ROM image

      The source video ROM binary must be specified with -r/--video-rom
      parameter, and extracted PowerPlay table will be saved into file specified
      with -p/--pp-file. For example:

          upp --pp-file=extracted.pp_table extract -r VIDEO.rom

      Default output file name will be an original ROM file name with an
      additional .pp_table extension.

    Options:
      -r, --video-rom <filename>  Input Video ROM binary image file  [required].
      -h, --help                  Show this message and exit.

Getting parameter:

    Usage: upp get [OPTIONS] VARIABLE_PATH_SET...

      Retrieves current value of one or multiple PP parameters

      The parameter variable path must be specified in "/<param> notation", for
      example:

          upp get /FanTable/TargetTemperature /VddgfxLookupTable/7/Vdd

      The raw value of the parameter will be retrieved, decoded and displayed on
      console. Multiple PP parameters can be specified at the same time.

    Options:
      -h, --help  Show this message and exit.

Setting parameters:

    Usage: upp set [OPTIONS] VARIABLE_PATH_SET...

      Sets value to one or multiple PP parameters

      The parameter path and value must be specified in "/<param>=<value>
      notation", for example:

          upp set /PowerTuneTable/TDP=75 /SclkDependencyTable/7/Sclk=107000

      Multiple PP parameters can be set at the same time. The PP tables will not
      be changed unless additional --write option is set.

      Optionally, if --to-reg output is used an additional Windows registry
      format file will be generated, named same as PowerPlay output target
      filename with an additional '.reg' extension.

    Options:
      -t, --to-reg  Save output to Windows registry .reg file as well.
      -w, --write   Write changes to PP binary.
      -h, --help    Show this message and exit.

