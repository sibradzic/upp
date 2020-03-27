# To run without install relative imports needs to match the module ones, which
# is true when in 'src' directory, then: python3 -m upp.upp --help

import click
from upp import decode

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def _normalize_var_path(var_path_str):
    var_path_list = var_path_str.strip('/').split('/')
    normalized_var_path_list = [
      int(item) if item.isdigit() else item for item in var_path_list]
    return normalized_var_path_list


def _is_int_or_float(value):
    if value.isdigit():
        return True
    try:
        float(value)
        return True
    except ValueError:
        pass
    return False


def _validate_set_pair(set_pair):
    valid = False
    if '=' in set_pair and _is_int_or_float(set_pair.split('=')[-1]):
        return set_pair.split('=')
    else:
        print("ERROR: Invalid variable assignment '{}'. ".format(set_pair),
              "Assignment must be specified in <variable-path>=<value> ",
              "format. For example: /PowerTuneTable/TDP=75")
        return None, None


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--pp-file', help='Input/output PP table binary file',
              metavar='<filename>',
              default='/sys/class/drm/card0/device/pp_table')
@click.option('--debug/--no-debug', '-d/ ', default='False',
              help='Debug mode')
@click.pass_context
def cli(ctx, debug, pp_file):
    """UPP: Uplift Power Play

    A tool for parsing, dumping and modifying data in Radeon PowerPlay tables.

    UPP is able to parse and modify binary data structures of PowerPlay
    tables commonly found on certain AMD Radeon GPUs. Drivers on recent
    AMD GPUs allow PowerPlay tables to be dynamically modified on runtime,
    which may be known as "soft PowerPlay tables". On Linux, the PowerPlay
    table is by default found at:

    \b
       /sys/class/drm/card0/device/pp_table

    This tool currently supports reading and modifying PowerPlay tables
    found on the following AMD GPU families:

    \b
      - Polaris
      - Vega
      - Radeon VII
      - Navi 10
      - Navi 14

    Note: iGPUs found in many recent AMD APUs are using completely different
    PowerPlay control methods, this tool does not support them.

    If you have bugs to report or features to request please check:

      github.com/sibradzic/upp
    """
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    ctx.obj['PPBINARY'] = pp_file


@click.command(short_help='Dumps all PowerPlay parameters to console')
@click.option('--raw/--no-raw', '-r/ ', help='Show raw binary data',
              default='False')
@click.pass_context
def dump(ctx, raw):
    """Dump all PowerPlay data to console

    De-serializes PowerPlay binary data into a Python dictionary.
    For example:

    \b
        upp --pp-file=radeon.pp_table dump

    In standard mode all data will be dumped to console, where
    data hierarchy is indicated by indentation.

    In raw mode a table showing all hex and binary data, as well
    as variable names and values, will be dumped.
    """
    debug = ctx.obj['DEBUG']
    pp_file = ctx.obj['PPBINARY']
    msg = "Dumping {} PP table from '{}' binary..."
    decode.dump_pp_table(pp_file, rawdump=raw, debug=debug)
    return 0


@click.command(short_help='Extract PowerPlay table from Video BIOS ROM image')
@click.option('-r', '--video-rom', required=True, metavar='<filename>',
              help='Input Video ROM binary image file')
@click.pass_context
def extract(ctx, video_rom):
    """Extracts PowerPlay data from full VBIOS ROM image

    The source video ROM binary must be specified with -r/--video-rom
    parameter, and extracted PowerPlay table will be saved into file
    specified with -p/--pp-file. For example:

    \b
        upp --pp-file=extracted.pp_table extract -r VIDEO.rom

    Default output file name will be an original ROM file name with an
    additional .pp_table extension.
    """
    pp_file = ctx.obj['PPBINARY']
    ctx.obj['ROMBINARY'] = video_rom
    # Override default, we don't want to extract any random VBIOS into sysfs
    if pp_file.endswith('device/pp_table'):
        pp_file = video_rom + '.pp_table'
    msg = "Extracting PP table from '{}' ROM image..."
    print(msg.format(video_rom))
    decode.extract_rom(video_rom, pp_file)
    print('Done')
    return 0


@click.command(short_help='Get current value of a PowerPlay parameter(s)')
@click.argument('variable-path-set', nargs=-1, required=True)
@click.pass_context
def get(ctx, variable_path_set): 
    """Retrieves current value of one or multiple PP parameters

    The parameter variable path must be specified in
    "/<param> notation", for example:

    \b
        upp get /FanTable/TargetTemperature /VddgfxLookupTable/7/Vdd

    The raw value of the parameter will be retrieved,
    decoded and displayed on console.
    Multiple PP parameters can be specified at the same time.
    """
    debug = ctx.obj['DEBUG']
    pp_file = ctx.obj['PPBINARY']

    pp_bytes = decode._read_binary_file(pp_file)
    data = decode.select_pp_struct(pp_bytes, debug=debug)

    for set_pair_str in variable_path_set:
        var_path = _normalize_var_path(set_pair_str)
        res = decode.get_value(pp_file, var_path, data, debug=debug)
        if res:
            print(res['value'])
        else:
            print('ERROR: Incorrect variable path:', set_pair_str)
            return 2

    return 0


@click.command(short_help='Set value to PowerPlay parameter(s)')
@click.argument('variable-path-set', nargs=-1, required=True)
@click.option('-w', '--write', is_flag=True,
              help='Write changes to PP binary', default=False)
@click.pass_context
def set(ctx, variable_path_set, write):
    """Sets value to one or multiple PP parameters

    The parameter path and value must be specified in
    "/<param>=<value> notation", for example:

    \b
        upp set /PowerTuneTable/TDP=75 /SclkDependencyTable/7/Sclk=107000

    Multiple PP parameters can be set at the same time.
    The PP tables will not be changed unless additional
    --write option is set.
    """
    debug = ctx.obj['DEBUG']
    pp_file = ctx.obj['PPBINARY']
    set_pairs = []
    for set_pair_str in variable_path_set:
        var, val = _validate_set_pair(set_pair_str)
        if var and val:
            var_path = _normalize_var_path(var)
            res = decode.get_value(pp_file, var_path)
            if res:
                if (val.isdigit()):
                    set_pairs += [var_path + [int(val)]]
                else:
                    set_pairs += [var_path + [float(val)]]
            else:
                print('ERROR: Incorrect variable path:', var)
                return 2
        else:
            return 2

    pp_bytes = decode._read_binary_file(pp_file)
    data = decode.select_pp_struct(pp_bytes)

    for set_list in set_pairs:
        decode.set_value(pp_file, pp_bytes, set_list[:-1], set_list[-1],
                         data_dict=data, write=False, debug=debug)
    if write:
        print("Commiting changes to '{}'.".format(pp_file))
        decode._write_pp_tables_file(pp_file, pp_bytes)
    else:
        print("WARNING: Nothing was written to '{}'.".format(pp_file),
              "Add --write option to commit the changes for real!")

    return 0


cli.add_command(extract)
cli.add_command(dump)
cli.add_command(get)
cli.add_command(set)


def main():
    cli(obj={})()


if __name__ == "__main__":
    main()
