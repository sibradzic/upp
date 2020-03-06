#!/usr/bin/env python3

import click
import decode

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
              help='Input Video ROM binary image file ',)
@click.pass_context
def extract(ctx, video_rom):
    """Extracts PowerPlay data from full VBIOS ROM image

    Putput is original file with additional .pp_table extension.
    """
    pp_file = ctx.obj['PPBINARY']
    ctx.obj['ROMBINARY'] = video_rom
    msg = "Extracting PP table from '{}' ROM image..."
    print(msg.format(video_rom))
    decode.extract_rom(video_rom, pp_file)
    print('Done')
    return 0


@click.command(short_help='Get current value of a PowerPlay parameter')
@click.argument('variable-path')
@click.pass_context
def get(ctx, variable_path):
    """Retrieves current value of a particular PP parameter

    The parameter variable path must be specified in
    "/<param> notation", for example:

    \b
        /FanTable/TargetTemperature
        /VddGfxLookupTable/7/Vdd

    The raw value of the parameter will be retrieved,
    decoded and displayed on console.
    """
    debug = ctx.obj['DEBUG']
    pp_file = ctx.obj['PPBINARY']
    var_path = _normalize_var_path(variable_path)
    res = decode.get_value(pp_file, var_path, debug=debug)
    if res:
        print(res['value'])
    return 0


@click.command(short_help='Set value(s) to PowerPlay parameter(s)')
@click.argument('variable-path-set', nargs=-1, required=True)
@click.option('-w', '--write', is_flag=True,
              help='Write changes to PP binary', default=False)
@click.pass_context
def set(ctx, variable_path_set, write):
    """Sets values to one or multiple PP parameters

    The parameter path and value must be specified in
    "/<param>=<value> notation", for example:

    \b
        /PowerTuneTable/TDP=75 /SocClockDependencyTable/7/SocClock=107000

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

if __name__ == "__main__":
    cli(obj={})()
