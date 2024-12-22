import codecs
import struct
import ctypes

from upp.atom_gen import atombios
from collections import OrderedDict
from importlib import import_module

# These two used to be imported from drivers/gpu/drm/amd/amdgpu/atom.h, but
# from kernel v 6.6 the ATOM_ROM_PART_NUMBER_PTR got removed, so harcoding them
rom_tbl_ptr = 0x48
part_num_ptr = 0x6e

common_hdr = atombios.struct__ATOM_COMMON_TABLE_HEADER
master_dt_tbl_struct = atombios.struct__ATOM_MASTER_DATA_TABLE
atom_rom_header = atombios.struct__ATOM_ROM_HEADER
atom_rom_header_v2 = atombios.struct__ATOM_ROM_HEADER_V2_1
leagcy_vrom_offset = 0x40000

# Base ctypes variables, in order to distinguish from structures and arrays
primitives = [
    ctypes.c_byte, ctypes.c_ubyte,
    ctypes.c_int16, ctypes.c_uint16,
    ctypes.c_int32, ctypes.c_uint32,
    ctypes.c_float
]

# Defined as uint in kernel, but in reality these are float
float_fields = ['a', 'b', 'c', 'm',
                'VcBtcPsmA', 'VcBtcPsmB', 'VcBtcVminA', 'VcBtcVminB',
                'DfllBtcMasterScalerM', 'DfllBtcSlaveScalerM',
                'DfllBtcMasterScalerB', 'DfllBtcSlaveScalerB']
float_arrays = ['Fset', 'Vdroop', 'VcBtcPsmA', 'VcBtcPsmB', 'VcBtcVminA',
                'VcBtcVminB', 'Droop_PWL_F', 'Droop_PWL_a', 'Droop_PWL_b',
                'Droop_PWL_c']


def odict(init_data=None):
    """
    Returns ordered dictionary (for consistent behavior on Python 2.7 & 3.6+)
    """
    if init_data:
        return OrderedDict(init_data)
    else:
        return OrderedDict()


def _read_binary_file(filename):
    f = open(filename, 'rb')
    raw_data = f.read()
    f.close()
    return bytearray(raw_data)


def _write_binary_file(filename, raw_data):
    try:
        f = open(filename, 'wb')
        f.write(raw_data)
        f.close()
    except PermissionError as e:
        msg = 'ERROR: {}\n' + \
              'To make PowerPlay table file writable: sudo chmod o+w {}'
        print(msg.format(e, filename, filename))
        print(e)


def _bytes2hex(bytes):
    """
    Hex decoding helper

    Does special gymnastics to ensure consistent decoding on Python 2.7 & 3.x
    """
    return codecs.encode(bytes, 'hex_codec').decode()


def _checksum(rom_bytes):
    checksum = 0
    checksum_bytes_length = rom_bytes[0x2] * 512
    for byte in rom_bytes[:checksum_bytes_length]:
        checksum += byte
    checksum = checksum & 0xff

    return checksum


def _rom_info(vrom_file):
    """
    Displays the VROM image info and returns PowerPlay table offset and size

    Returns:
    pp_offset, pp_length (tuple): pp_offset (int): pp table offset in vROM
                                   pp_length (int): pp table length

    """

    rom_bytes = _read_binary_file(vrom_file)

    # VROM magic validation
    rom_magic_bytes = rom_bytes[:2]
    rom_magic_str = _bytes2hex(rom_magic_bytes).upper()
    rom_offset = 0

    # Since Navi 3x the UEFI VBIOS comes first, the legacy VBIOS is at 0x40000
    if rom_magic_str == 'AA55':
        rom_offset = leagcy_vrom_offset
        msg = 'UEFIU video ROM magic detected: {}, using legacy VBIOS ' + \
              'at offset 0x{:X}'
        print(msg.format(rom_magic_str, rom_offset))
        rom_bytes = rom_bytes[rom_offset:]
        rom_magic_bytes = rom_bytes[:2]
        rom_magic_str = _bytes2hex(rom_magic_bytes).upper()

    if rom_magic_str != '55AA':
        err_msg = 'Invalid Video ROM magic: {}, must be 55AA'
        print(err_msg.format(rom_magic_str))
        return None, None

    # Fetching ATOM 'Common Table'
    rom_tbl_offset_bytes = rom_bytes[rom_tbl_ptr:rom_tbl_ptr+2]
    rom_tbl_offset = struct.unpack('<H', rom_tbl_offset_bytes)[0]

    rom_tbl_header_bytes = rom_bytes[rom_tbl_offset:rom_tbl_offset+5]
    rom_tbl_header = common_hdr.from_buffer(rom_tbl_header_bytes)
    rom_tbl_rev = rom_tbl_header.ucTableFormatRevision
    rom_tbl_len = rom_tbl_header.usStructureSize

    rom_tbl_bytes = rom_bytes[rom_tbl_offset:rom_tbl_offset+rom_tbl_len]

    if rom_tbl_rev == 1:
        rom_tbl = atom_rom_header.from_buffer(rom_tbl_bytes)
    elif rom_tbl_rev == 2:
        rom_tbl = atom_rom_header_v2.from_buffer(rom_tbl_bytes)
    else:
        err_msg = 'Can not handle ATOM Common Table revision {}'
        print(err_msg.format(rom_tbl_rev))
        return None, None

    print('Found ATOM Common Table rev. {}'.format(rom_tbl_rev))

    rom_signature = bytearray(rom_tbl.uaFirmWareSignature).decode()
    if rom_signature != 'ATOM':
        err_msg = 'Invalid Video ROM signature: "{}", must match "ATOM".'
        print(err_msg.format(rom_signature))
        return None, None

    # Dump some VROM info
    rom_partn_offset_bytes = rom_bytes[part_num_ptr:part_num_ptr+2]
    rom_partn_offset = struct.unpack('<H', rom_partn_offset_bytes)[0]
    boot_msg_offset = rom_tbl.usBIOS_BootupMessageOffset
    cfg_file_offset = rom_tbl.usConfigFilenameOffset
    crc_blck_offset = rom_tbl.usCRC_BlockOffset

    part_info = rom_bytes[rom_partn_offset:boot_msg_offset-1].split(b'\x00')
    boot_msgs = rom_bytes[boot_msg_offset:rom_tbl_offset-1].split(b'\x00')
    chksm = rom_bytes[0x21:0x22]
    crc32 = rom_bytes[crc_blck_offset:crc_blck_offset+4]

    print('Video ROM information:\n')
    for msg in part_info + boot_msgs:
        if msg:
            print('  ' + msg.decode().strip('\r\n'))
    print('')
    print('CHKSUM: 0x{} (off by {}), CRC: 0x{}'.format(chksm.hex().upper(),
                                                       _checksum(rom_bytes),
                                                       crc32.hex().upper()))

    # Fetching 'Master Data Table'
    master_dt_tbl_ofst = rom_tbl.usMasterDataTableOffset

    msg = 'Looking into MasterDataTable at offset 0x{:04X}'
    print(msg.format(master_dt_tbl_ofst))

    master_dt_hdr_bytes = rom_bytes[master_dt_tbl_ofst:master_dt_tbl_ofst+5]
    master_dt_tbl_header = common_hdr.from_buffer(master_dt_hdr_bytes)
    master_dt_tbl_len = master_dt_tbl_header.usStructureSize
    master_dt_tbl_end = master_dt_tbl_ofst + master_dt_tbl_len
    master_dt_tbl_bytes = rom_bytes[master_dt_tbl_ofst:master_dt_tbl_end]
    master_dt_tbl = master_dt_tbl_struct.from_buffer(master_dt_tbl_bytes)

    # Fetching 'PowerPlayInfo' table
    pp_tbl_offset = master_dt_tbl.ListOfDataTables.PowerPlayInfo

    # TODO: For The PowerPlayInfo table offset info on RDNA3+ VBIOS is not at
    # expected place. It seems to be right behind $PS1P magic. Investigate.
    if (rom_offset != 0 and pp_tbl_offset == 0):
        print('Invalid PowerPlayInfo offset, checking for $PS1P magic...')
        ps1p_offset = rom_bytes.find(b'$PS1P')
        if ps1p_offset > 0:
            print('Found $PS1P at 0x{:X}'.format(rom_offset + ps1p_offset))
            pp_tbl_offset = ps1p_offset + 0x110
            print('OFFSET at 0x{:X}'.format(pp_tbl_offset))
        else:
            print('ERROR: Can not find PowerPlay table!')
            return 0, 0

    msg = 'Looking into PowerPlayInfo at offset 0x{:04X}'
    print(msg.format(rom_offset + pp_tbl_offset))

    pp_tbl_header_bytes = rom_bytes[pp_tbl_offset:pp_tbl_offset+5]
    pp_tbl_header = common_hdr.from_buffer(pp_tbl_header_bytes)
    pp_tbl_len = pp_tbl_header.usStructureSize

    msg = 'Found {} bytes long PowerPlayInfo table v{}.{} at offset 0x{:04X}'
    print(msg.format(pp_tbl_len, pp_tbl_header.ucTableFormatRevision,
                     pp_tbl_header.ucTableContentRevision,
                     rom_offset + pp_tbl_offset))

    return rom_offset + pp_tbl_offset, pp_tbl_len


def extract_rom(vrom_file, out_pp_file):
    """
    Extracts PowerPlay table from VROM image
    """

    pp_tbl_offset, pp_tbl_len = _rom_info(vrom_file)
    if not pp_tbl_offset:
        return None
    rom_bytes = _read_binary_file(vrom_file)
    pp_tbl = rom_bytes[pp_tbl_offset:pp_tbl_offset+pp_tbl_len]

    print('Saving PowerPlay table to {}'.format(out_pp_file))
    _write_binary_file(out_pp_file, pp_tbl)


def inject_pp_table(input_rom, output_rom, pp_bin_file):
    """
    Injects PowerPlay table into VROM image
    """

    pp_tbl_offset, pp_tbl_len = _rom_info(input_rom)
    if not pp_tbl_offset:
        return None
    pp_bytes = _read_binary_file(pp_bin_file)
    if len(pp_bytes) != pp_tbl_len:
        msg = 'ERROR: The length of {} PowerPlay table must match the ' + \
              'length of PowerPlay table in {} vROM image ({} bytes)'
        print(msg.format(pp_bin_file, input_rom, pp_tbl_len))
        return None
    rom_bytes = _read_binary_file(input_rom)
    print('Replacing PowerPlay data...')
    rom_bytes[pp_tbl_offset:pp_tbl_offset+pp_tbl_len] = pp_bytes
    new_checksum = _checksum(rom_bytes)
    print('Shifting checksum by {}...'.format(new_checksum))
    rom_bytes[0x21] = (rom_bytes[0x21] - new_checksum) & 0xff
    _write_binary_file(output_rom, rom_bytes)

    return True


def validate_pp(header, rawbytes, rawdump):
    """
    Validates PowerPlay master table header
    """

    pp_frev = header.ucTableFormatRevision
    pp_crev = header.ucTableContentRevision
    pp_len = header.usStructureSize
    rw_len = len(rawbytes)

    if pp_len != rw_len and pp_frev in [20, 21, 22] and rw_len == 4095:
        msg = 'WARNING: Trying to work around rev {}.{} table truncated ' + \
              'at 0x{:04x}, setting all missing values to zeroes.'
        print(msg.format(pp_frev, pp_crev, rw_len))
        rawbytes.extend(bytearray(pp_len-rw_len))
        rw_len = len(rawbytes)
    if pp_len != rw_len:
        msg = 'ERROR: Header length ({}) differs from file length ({}). ' + \
              'Is this a valid PowerPlay table?'
        print(msg.format(pp_len, rw_len))
        return None
    if rawdump:
        msg = 'PowerPlay table rev {}.{} size {} bytes'
        print(msg.format(pp_frev, pp_crev, pp_len))
    return pp_frev, pp_crev


def decode_pp_table(rawdata, c_struct):
    """
    De-serializes PowerPlay binary data into a ctypes structure
    """

    return c_struct.from_buffer(rawdata)


def _get_bigcap_indices(string):
    """
    Returns list of positions in a string where separate words start

    PowerPlay sub-tables have names like 'VddcLookupTable', 'VCEStateTable' or
    'PCIETable'. We need to split this into separate words, but some words are
    upper-caps acronyms, followed by another word starting with upper-cap.
    Here we do special gymnastics to return the starting position of all words.
    """

    indices = []
    i = 0
    while i < len(string)-1:  # yes, finish with 2nd last char in the string
        is_i_big = True if string[i].isupper() else False
        is_i_plus1_big = True if string[i+1].isupper() else False
        is_i_plus1_small = not is_i_plus1_big
        if is_i_big:
            if (is_i_plus1_small and i not in indices) or i == 0:
                indices.append(i)
        else:
            if is_i_plus1_big:
                indices.append(i+1)
        i = i + 1

    return indices


def _print_raw_value(offset, symbol, rawbytes, name, desc, value):
    hexval = _bytes2hex(rawbytes)
    raw_msg = ' 0x{:04x} ({:04n}) {} {:>8} {:42s}:{: n}'
    # Polaris variable names have small-caps prefixes that we don't want
    big_caps = _get_bigcap_indices(name)
    if big_caps:
        name = name[big_caps[0]:]
    if desc:
        name = name + ' ' + desc
    print(raw_msg.format(offset, offset, symbol, hexval, name, value))


def _get_ofst_cstruct(module, name, header_bytes, debug=False):
    """
    Resolves C structure name and its size from parent table's name

    For Polaris and Vega 10 generations of GPUs Linux kernel ATOM BIOS C data
    structures points to nested child sub-tables using relative pointers.
    Which table is behind which pointer can only be guessed by a table name in
    the master PowerPlay tables. Furthermore, some nested tables come in
    few different versions, depending on particular GPU chip. This function
    implements logic that does this guess game, some table versioning logic as
    well as nested tables size calculation. Finally, it has some workarounds
    for semi-broken (or just very unusual) fields in some nested tables.

    Parameters:
    module (string): Points to cstruct module defining data structures for the
                     appropriate generation of GPUs
    name (string): Name of the child table used for data structure resolution
    header_bytes (bytearray): A 2-byte array where 1st byte contains the nested
                              table revision id and 2nd byte number of entries
    debug (bool): Debugging output enabled

    Returns:
    cs, total_len (tuple): cs (class): resolved C structure
                           total_len (int): structure's data length in bytes

    """

    cs = None
    total_len = 0
    revid = struct.unpack('B', header_bytes[:1])[0]
    pp_module = import_module(module)
    module_suffix = '.'.join(module.split('.')[-2:])
    if module_suffix == 'atom_gen.pptable_v1_0':
        family = 'Tonga'
    elif module_suffix == 'atom_gen.vega10_pptable':
        family = 'Vega10'
    else:
        print('ERROR: Module {} does not contain jump structures.', module)
        return cs, total_len

    # A helper for translating table names into resolvable ctype identifiers
    def resolve_cstruct(name, family=family):
        big_caps = _get_bigcap_indices(name)
        words = []
        for big_letter in big_caps:
            i = big_caps.index(big_letter)
            last = None if big_letter == big_caps[-1] else big_caps[i+1]
            word = name[big_letter:last]
            if word.endswith('clk'):
                word = word.upper()
            if word.startswith('Vdd'):
                word = 'Voltage'
            if word == 'PPM':
                word = 'PowerTune'
            elif word == 'Tune':  # 'Power' + 'Tune' -> 'PowerTune'
                words[-1] = words[-1] + word
            elif word == 'Clk':   # 'Disp' + 'Clk' -> 'DISPCLK'
                words[-1] = words[-1].upper() + word.upper()
            else:
                words.append(word)
        ext_cstruct = '_'.join(['ATOM', family] + words)
        if debug:
            print('DEBUG: Resolved external struct "{}"'.format(ext_cstruct),
                  'from "{}"'.format(family), 'family and', words, 'keywords')
        return ext_cstruct

    # These are the 'simple' version-less tables that don't depend on GPU gen.
    simple_tables = [
        'StateArray', 'ThermalController', 'MclkDependencyTable',
        'SocclkDependencyTable', 'DcefclkDependencyTable',
        'VddgfxLookupTable', 'VddcLookupTable', 'VddmemLookupTable',
        'VddciLookupTable', 'PixclkDependencyTable', 'DispClkDependencyTable',
        'PhyClkDependencyTable', 'MMDependencyTable', 'HardLimitTable',
        'VCEStateTable', 'GPIOTable'
    ]

    if name in simple_tables:
        cs = getattr(pp_module, resolve_cstruct(name))

    # The rest are 'complex' tables, that may have versions and suffixes
    elif name == 'SclkDependencyTable':  # ATOM_Polaris_SCLK_Dependency_Table
        cs = getattr(pp_module, resolve_cstruct(name, 'Polaris'))
    elif name == 'GfxclkDependencyTable':
        # This by default points to ATOM_Vega10_GFXCLK_Dependency_Record but it
        # needs override to ATOM_Vega10_GFXCLK_Dependency_Record_V2 for rev > 0
        if revid in [0, 1]:              # ATOM_Vega10_GFXCLK_Dependency_Table
            cs = getattr(pp_module, resolve_cstruct(name))
            entries_class = cs._fields_[-1][-1]
            entry_name, entry_type = cs._fields_[-1]
            assert entry_type._length_ == 0
            if revid == 0:
                record_struct = 'ATOM_Vega10_GFXCLK_Dependency_Record'
            else:
                record_struct = 'ATOM_Vega10_GFXCLK_Dependency_Record_V2'
            entry_type = getattr(pp_module, record_struct)

            class FixedEntriesTypeArray(ctypes.LittleEndianStructure):
                _pack_ = cs._pack_
                _fields_ = cs._fields_[:-1] + [(entry_name, entry_type * 1)]

            cs = FixedEntriesTypeArray
        else:
            cs = getattr(pp_module, resolve_cstruct(name))
    elif name == 'FanTable':
        if revid == 8:                   # ATOM_Tonga_Fan_Table (v8)
            cs = getattr(pp_module, resolve_cstruct(name))
        elif revid == 9:                 # ATOM_Polaris_Fan_Table (v9)
            cs = getattr(pp_module, resolve_cstruct(name, 'Polaris'))
        elif revid == 10:                # ATOM_Vega10_Fan_Table (v10)
            cs = getattr(pp_module, resolve_cstruct(name))
        elif revid == 11:                # ATOM_Vega10_Fan_Table_V2 (v11)
            cs = getattr(pp_module, resolve_cstruct(name) + '_V2')
        else:                            # ATOM_Vega10_Fan_Table_V3 (v12+)
            cs = getattr(pp_module, resolve_cstruct(name) + '_V3')
    elif name == 'PCIETable':
        if revid == 1:                   # ATOM_Polaris10_PCIE_Table (v1)
            cs = getattr(pp_module, resolve_cstruct(name, 'Polaris10'))
        else:                            # ATOM_Vega10_PCIE_Table (v2)
            cs = getattr(pp_module, resolve_cstruct(name))
    elif name in 'PPMTable':             # ATOM_Tonga_PowerTune_Table (v1)
        cs = getattr(pp_module, resolve_cstruct(name))
    elif name in 'PowerTuneTable':
        if revid == 4:                   # ATOM_Polaris_PowerTune_Table (v4)
            cs = getattr(pp_module, resolve_cstruct(name, 'Polaris'))
        elif revid == 5:                 # ATOM_Vega10_PowerTune_Table (v5)
            cs = getattr(pp_module, resolve_cstruct(name))
        elif revid == 6:                 # ATOM_Vega10_PowerTune_Table_V2 (v6)
            cs = getattr(pp_module, resolve_cstruct(name) + '_V2')
        else:                            # ATOM_Vega10_PowerTune_Table_V3 (v7+)
            cs = getattr(pp_module, resolve_cstruct(name) + '_V3')
    else:
        print('ERROR: Unknown data structure {} v{}'.format(name, revid))
        return cs, total_len

    # Here we get the byte-length of the offset-ed C structures
    if 'ucNumEntries' in cs._fields_[1]:
        # Vega10 and older C structures all have number of entries set to 0, we
        # override it with real value that we get from an actual pp_table data
        entry_name, entry_type = cs._fields_[-1]
        entry_count = struct.unpack('B', header_bytes[1:2])[0]

        class FixedEntriesCountArray(ctypes.LittleEndianStructure):
            _pack_ = cs._pack_
            _fields_ = cs._fields_[:-1] + [(entry_name,
                                            entry_type._type_ * entry_count)]

        cs = FixedEntriesCountArray

        # This workarounds the oddity of last field in ATOM_Vega10_State_Array
        # being named 'states', yet all other C structs names it 'entries'
        entries_field_name = cs._fields_[-1][0]
        cs_entries = getattr(cs, entries_field_name)

        entry_len = cs_entries.size
        total_len = cs_entries.offset + cs_entries.size * entry_count

    else:
        total_len = 0
        for field in cs._fields_:
            if field[1] in primitives:
                total_len += struct.calcsize(field[1]._type_)
            else:
                entry_len = struct.calcsize(field[1]._type_._type_)
                array_size = field[1]._length_
                total_len += entry_len * array_size
    if debug:
        print('DEBUG: Detected C structture of', len(cs._fields_),
              'elements, total size of', total_len, 'bytes')

    return cs, total_len


def build_data_tree(data, raw=None, decoded=None, parent_name='/',
                    meta=None, rawdump=False, debug=False):
    """
    Converts ctypes structure into tree-like ordered dictionary

    This relies heavily on ATOM BIOS C structures extracted from Linux kernel,
    where variable names as well as table and array structures are defined.

    Parameters:
    data (ctypes instance): Contains binary data that can be referenced by C
                            variable names that has been decoded using ctypes
                            from_buffer() call
    raw (bytearray): Raw PowerPlay data buffer in bytearray format
    decoded (OrderedDictdict): A special tree-like structure of nested ordered
                               dictionaries that describes binary data
                               structures containing PowerPlay parameters,
                               used as parameter due to recursive nature of
                               this function
    parent_name (string): Reference to a parent of data-structure currently
                          being processed, used for recursion
    meta (dict): Containing 'size' and 'offset' keys, used for calculating
                 offsets & sizes for PowerPlay sub-structure tables
    rawdump (bool): Shows PowerPlay data in a table format showing offsets
                    and hex values on a console instead of returning data dict
    debug (bool): Debugging output enabled

    Returns:
    decoded (dict): A resulting PowerPlay data-structure in a dictionary form

    """

    # Init decoded data dictionary
    if decoded is None:
        decoded = odict()
        if rawdump:
            print(' Offset (dec.) t Raw val. Variable name ' + ' '*24 +
                  'Decoded value\n' + '-'*78)

    # Here we parse data items in C Arrays (all items are same type)
    if issubclass(type(data), ctypes.Array):
        d_size = meta['size'] // len(data)
        d_offset = meta['ofs']
        index = 0

        # Base data types are parsed as is
        if data._type_ in primitives:
            d_symbol = data._type_._type_
            for d_value in data:
                d_bytes = d_value.to_bytes(d_size, 'little')
                if parent_name in float_arrays:
                    d_symbol = 'f'
                    d_value = struct.unpack(d_symbol, d_bytes)[0]
                child_key = index
                decoded[child_key] = {'value':  d_value,
                                      'offset': d_offset,
                                      'type':   d_symbol}
                desc = ''
                if 'desc' in meta and index < len(meta['desc']) - 1:
                    desc = meta['desc'][index]
                    decoded[child_key]['desc'] = desc
                if rawdump:
                    _print_raw_value(d_offset, d_symbol, d_bytes,
                                     parent_name, desc, d_value)
                d_offset += d_size
                index += 1

        # Other types are recursed back into this very same function
        else:
            for item in data:
                if debug:
                    msg = 'DEBUG: Recursive dive into "{}" array, element {}'
                    print(msg.format(parent_name, index))
                child_key = index
                decoded[child_key] = odict()
                r_meta = {'ofs': d_offset, 'size': d_size}
                build_data_tree(item, raw, decoded[child_key], parent_name,
                                r_meta, rawdump, debug)
                if debug:
                    msg = 'DEBUG: End of recursion into "{}"'
                    print(msg.format(parent_name))
                d_offset += d_size
                index += 1

    # Here we parse data items in C Structures
    elif issubclass(type(data), ctypes.Structure):
        for name, ctyp_cls in data._fields_:
            d_value = getattr(data, name)
            d_meta = getattr(type(data), name)
            d_size = d_meta.size
            if name.startswith(('uc', 'us', 'ul')):
                name = name[2:]
            if 'ofs' not in meta:
                d_offset = d_meta.offset
            else:
                d_offset = meta['ofs'] + d_meta.offset

            # Base types parsed as is, exception are floats & offset tables
            if ctyp_cls in primitives:
                d_symbol = ctyp_cls._type_
                d_size = d_meta.size
                if ctyp_cls._type_ in ['b', 'h']:
                    d_bytes = d_value.to_bytes(d_size, 'little', signed=True)
                else:
                    d_bytes = d_value.to_bytes(d_size, 'little')
                if ctyp_cls == ctypes.c_uint and name in float_fields:
                    d_symbol = 'f'
                    d_value = struct.unpack(d_symbol, d_bytes)[0]
                if rawdump:
                    _print_raw_value(d_offset, d_symbol, d_bytes,
                                     name, '', d_value)
                # Check if this is a pointer to an offset-ed table:
                if not name.endswith(('ArrayOffset',
                                      'TableOffset',
                                      'ControllerOffset')):
                    decoded[name] = {'value':  d_value,
                                     'offset': d_offset,
                                     'type':   d_symbol}
                # This part parses legacy offset-ed tables (Polaris, Vega10)
                else:
                    name = name[:-6]
                    ofst = d_value
                    if not ofst:
                        decoded[name] = None
                        if debug:
                            print('DEBUG: Table', name, 'points to 0, ignore')
                    else:
                        c_struct, size = _get_ofst_cstruct(data.__module__,
                                                           name,
                                                           raw[ofst:ofst+2],
                                                           debug)
                        if c_struct:
                            top = ofst + size
                            array_data = c_struct.from_buffer(raw[:top], ofst)
                            r_meta = {'ofs': ofst, 'size': size}
                            if debug:
                                msg = 'DEBUG: Recursive jump at offset ' + \
                                      '{} into "{}"'
                                print(msg.format(ofst, name))
                            decoded[name] = odict()
                            build_data_tree(array_data, raw, decoded[name],
                                            name, r_meta, rawdump, debug)
                            if debug:
                                msg = 'DEBUG: End of recursion into "{}"'
                                print(msg.format(name))

            # Other types are recursed back into this very same function
            else:
                if debug:
                    msg = 'DEBUG: Recursive dive from {} struct into "{}"'
                    print(msg.format(parent_name, name))
                r_meta = {'ofs': d_offset, 'size': d_size}
                if 'enum' in meta:
                    if name in meta['enum']:
                        r_meta['enum'] = {name: meta['enum'][name]}
                    if parent_name in meta['enum'] and name in ['min', 'max']:
                        r_meta['desc'] = meta['enum'][parent_name]['enum']
                    if parent_name in meta['enum'] and name in ['cap']:
                        r_meta['desc'] = meta['enum'][parent_name]['cap']

                decoded[name] = odict()
                build_data_tree(d_value, raw, decoded[name], name, r_meta,
                                rawdump, debug)
                if debug:
                    print('DEBUG: End of recursion into "{}"'.format(name))

    else:
        print('ERROR: Unexpected data structure:', type(data))

    return decoded


def select_pp_struct(rawbytes, rawdump=False, debug=False):
    """
    Selects appropriate variant of ctype data structures for conversion
    """

    pp_header = common_hdr.from_buffer(rawbytes[:4])
    pp_ver = validate_pp(pp_header, rawbytes, rawdump)
    enum_structs = {}

    # Polaris aka RX470/RX480/RX570/RX580/RX590
    if pp_ver == (7, 1):
        gpugen = 'Polaris'
        from upp.atom_gen import pptable_v1_0 as pp_struct
        ctypes_strct = pp_struct.struct__ATOM_Tonga_POWERPLAYTABLE
    # Vega 10 aka Vega 56/64
    elif pp_ver == (8, 1):
        gpugen = 'Vega 10'
        from upp.atom_gen import vega10_pptable as pp_struct
        ctypes_strct = pp_struct.struct__ATOM_Vega10_POWERPLAYTABLE
    # Vega 20 aka Radeon VII
    elif pp_ver == (11, 0):
        gpugen = 'Vega 20'
        from upp.atom_gen import vega20_pptable as pp_struct
        ctypes_strct = pp_struct.struct__ATOM_VEGA20_POWERPLAYTABLE
    # Navi 10 aka RX5700/RX5600(XT,M), Navi 14 aka RX5500/RX5300(XT,M)
    elif pp_ver == (12, 0):
        gpugen = 'Navi 10 or 14'
        from upp.atom_gen import smu_v11_0_navi10 as pp_struct
        ctypes_strct = pp_struct.struct_smu_11_0_powerplay_table
        enum_structs = {
            'power_saving_clock': {
                'prefix': 'SMU_11_0_PPCLOCK_',
                'struct': pp_struct.SMU_11_0_PPCLOCK_ID__enumvalues
            },
            'overdrive_table': {
                'prefix': 'SMU_11_0_ODSETTING_',
                'struct': pp_struct.SMU_11_0_ODSETTING_ID__enumvalues,
                'cappfx': 'SMU_11_0_ODCAP_',
                'capstr': pp_struct.SMU_11_0_ODFEATURE_CAP__enumvalues,
            }
        }
    # Arcturus aka MI100
    elif pp_ver == (13, 0):
        gpugen = 'Arcturus'
        from upp.atom_gen import smu_v11_0_arcturus as pp_struct
        ctypes_strct = pp_struct.struct_smu_11_0_powerplay_table
    # Navi 12 aka PRO V520
    elif pp_ver == (14, 0):
        gpugen = 'Navi 12'
        from upp.atom_gen import smu_v11_0_navi10 as pp_struct
        ctypes_strct = pp_struct.struct_smu_11_0_powerplay_table
    # Navi 21 (Sienna Cichlid) aka RX6900XT/RX6800(XT)
    # Navi 22 (Navy Flounder) aka RX6700(XT)/RX6800M
    # Navi 23 (Dimgrey Cavefish) aka RX6600(XT)/RX6600M
    # Navi 24 (Beige Goby) aka RX6500(XT)/RX6400
    elif ((pp_ver[0] in [15, 16, 18, 19]) and pp_ver[1] == 0):
        gpugen = 'Navi 2x'
        from upp.atom_gen import smu_v11_0_7_navi20 as pp_struct
        ctypes_strct = pp_struct.struct_smu_11_0_7_powerplay_table
        enum_structs = {
            'power_saving_clock': {
                'prefix': 'SMU_11_0_7_PPCLOCK_',
                'struct': pp_struct.SMU_11_0_7_PPCLOCK_ID__enumvalues
            },
            'overdrive_table': {
                'prefix': 'SMU_11_0_7_ODSETTING_',
                'struct': pp_struct.SMU_11_0_7_ODSETTING_ID__enumvalues,
                'cappfx': 'SMU_11_0_7_ODCAP_',
                'capstr': pp_struct.SMU_11_0_7_ODFEATURE_CAP__enumvalues,
            }
        }
    # Navi 31, 32, 33
    elif ((pp_ver[0] in [20, 21, 22]) and pp_ver[1] == 0):
        gpugen = 'Navi 3x'
        from upp.atom_gen import smu_v13_0_7_navi30 as pp_struct
        ctypes_strct = pp_struct.struct_smu_13_0_7_powerplay_table
        enum_structs = {
            'power_saving_clock': {
                'prefix': 'SMU_13_0_7_PPCLOCK_',
                'struct': pp_struct.SMU_13_0_7_PPCLOCK_ID__enumvalues
            },
            'overdrive_table': {
                'prefix': 'SMU_13_0_7_ODSETTING_',
                'struct': pp_struct.SMU_13_0_7_ODSETTING_ID__enumvalues,
                'cappfx': 'SMU_13_0_7_ODCAP_',
                'capstr': pp_struct.SMU_13_0_7_ODFEATURE_CAP__enumvalues,
            }
        }
    elif pp_ver is not None:
        msg = 'Can not decode PowerPlay table version {}.{}'
        print(msg.format(pp_ver[0], pp_ver[1]))
        return None
    else:
        return None

    # Unpack and sanitize enm_structs, if any
    if enum_structs:
        for tbl in enum_structs:
            prefix = enum_structs[tbl].pop('prefix')
            for enum in enum_structs[tbl]['struct']:
                txt = enum_structs[tbl]['struct'][enum]
                enum_structs[tbl]['struct'][enum] = txt.replace(prefix, '')
            enum_structs[tbl]['enum'] = enum_structs[tbl]['struct']
            enum_structs[tbl].pop('struct')
            if 'capstr' in enum_structs[tbl]:
                cappfx = enum_structs[tbl].pop('cappfx')
                for cap in enum_structs[tbl]['capstr']:
                    cpt = enum_structs[tbl]['capstr'][cap]
                    enum_structs[tbl]['capstr'][cap] = cpt.replace(cappfx, '')
                enum_structs[tbl]['cap'] = enum_structs[tbl]['capstr']
                enum_structs[tbl].pop('capstr')
        if debug:
            print('DEBUG: unpacked enumeration data:')
            for table in enum_structs:
                print('  min/max enum in', table, enum_structs[tbl]['enum'])
                if 'cap' in enum_structs[table]:
                    print('  cap enum in', table, enum_structs[tbl]['cap'])

    if debug:
        print('DEBUG: This is a', gpugen,
              'PP table, using', pp_struct.__name__)

    data = decode_pp_table(rawbytes, ctypes_strct)
    data_dict = build_data_tree(data, rawbytes, meta={'enum': enum_structs},
                                rawdump=rawdump, debug=debug)
    return data_dict


def dump_pp_table(pp_bin_file, data_dict=None, indent=0, parent='',
                  rawdump=False, debug=False):
    """
    Prints all decoded PowerPlay parameters and their values to console
    """
    if data_dict is None:
        pp_bytes = _read_binary_file(pp_bin_file)
        data_dict = select_pp_struct(pp_bytes, rawdump, debug)
    # Raw dump is handled at build_data_tree() (via select_pp_struct())
    if not data_dict or rawdump:
        return
    for member in data_dict:
        name = member
        if isinstance(member, int):
            name = str(parent) + ' ' + str(member)
        if data_dict[member] is None:
            print('{}{}: UNUSED'.format(' '*indent, member))
        elif 'value' in data_dict[member]:
            msg = '{}{}: {}'
            if data_dict[member]['type'] == 'f':
                msg = '{}{}:{: n}'
            desc = ''
            if 'desc' in data_dict[member]:
                desc = '(' + data_dict[member]['desc'] + ')'
                msg = '{}{}: {} {}'
            print(msg.format(' '*indent, name,
                             data_dict[member]['value'], desc))
        else:
            print('{}{}:'.format(' '*indent, name))
            dump_pp_table(None, data_dict[member], indent+2, parent=member)


def get_value(pp_bin_file, var_path, data_dict=None, debug=False):
    """
    Returns value of a PowerPlay parameter specified in var_path
    Parameters:
    pp_bin_file (file): a file used for getting raw binary PowerPlay data
    var_path (list): a list containing representing a pp_table key names.
                     for example:
                         ['FanTable', 'TargetTemperature']
                         ['VddGfxLookupTable', 7, 'Vdd']
    data_dict (dict): Reuse existing PowerPlay data-structure dictionary
    debug (bool): Debbuging output enabled
    Returns:
    dict: A descriptor of a parameter, containing decoded 'value', decimal
          'offset' and struct type 'type' keys.
    """
    if data_dict is None:
        pp_bytes = _read_binary_file(pp_bin_file)
        data = select_pp_struct(pp_bytes, debug=debug)
    else:
        data = data_dict.copy()
    for category in var_path:
        if category is not None:
            # helper that allows skipping the 'entries' key name
            if (isinstance(category, int)
               and isinstance(data, dict) and 'entries' in data):
                data = data['entries']
            try:
                data = data[category]
            except KeyError:
                msg = 'ERROR: Invalid parameter "{}", available ones are: {}'
                print(msg.format(category, ', '.join([str(k) for k in data])))
                return None
            except (TypeError, IndexError):
                if isinstance(data, list):
                    indices = [str(i) for i in range(len(data))]
                else:
                    indices = []
                msg = 'ERROR: Invalid parameter "{}", available ones are: {}'
                print(msg.format(category, ', '.join(indices)))
                return None
    if data is None:
        print('ERROR: Table {} does not point anywhere'.format(category))
    if isinstance(data, list):
        print('ERROR: Decoded data does not contain any value, you probably',
              'wanna look deeper into data;',
              ', '.join([str(i) for i in range(len(data))]))
        return None
    if isinstance(data, dict) and 'value' not in data:
        # helper that allows skipping the key name of the element of the array
        if len(data) == 1 and isinstance(data, dict):
            key = list(data.keys())[0]
            if 'value' in data[key]:
                return data[key]
        print('ERROR: Decoded data does not contain any value, you probably',
              'wanna look deeper into data;',
              ', '.join([str(k) for k in data.keys()]))
        return None
    if not isinstance(data, dict):
        print('ERROR: Decoded data does not contain any final values, you',
              'probably wanna go back one step into the data structure')
        return None

    return data


def set_value(pp_bin_file, pp_tbl_bytes, var_path, new_value,
              data_dict=None, write=False, debug=False):
    """
    Sets a PowerPlay parameter specified in var_path to a specified new value
    This will call a get_value(var_path) first, where parameter value will
    get decoded, and then the new value will be set. Finally, the new pp_table
    file with updated value will be written.
    Parameters:
    pp_bin_file (file): a file used for reading & writting raw binary PP data
    pp_tbl_bytes (bytearray): PowerPlay data bytes
    var_path (list): a list containing representing a pp_table key names.
                     for example:
                         ['FanTable', 'TargetTemperature']
                         ['VddGfxLookupTable', 7, 'Vdd']
    new_value (int): New value to be set
    data_dict (dict): Reuse existing PowerPlay data-structure dictionary
    write (bool): Actually writting data to PP-tables binary file
    debug (bool): Debbuging output enabled
    """
    var_pth_str = '.'.join([str(el) for el in var_path])
    current_data = get_value(pp_bin_file, var_path,
                             data_dict=data_dict, debug=debug)
    if current_data:
        curr_val = current_data['value']
        off = current_data['offset']
        d_type = current_data['type']
        d_size = struct.calcsize(d_type)
        msg = 'Changing {} of type {} from {} to {} at 0x{:03x}'
        print(msg.format(var_pth_str, d_type, curr_val, new_value, off))
    else:
        print('Can\'t decode {}'.format(var_path))
    bytes_value = struct.pack(d_type, new_value)
    if debug:
        current_bytes_value = pp_tbl_bytes[off:off+d_size]
        current_d_value = struct.unpack(d_type, current_bytes_value)[0]
        dbg_msg = ' 0x{:04x} ({:04n}) {} {:>8} {:32s}: {:n} {}'
        print(dbg_msg.format(off, off, d_type[-1],
                             _bytes2hex(current_bytes_value), var_pth_str,
                             current_d_value, 'CHANGES TO:'))
        print(dbg_msg.format(off, off, d_type[-1], _bytes2hex(bytes_value),
                             var_pth_str, new_value, ''))
    pp_tbl_bytes[off:off+d_size] = bytes_value
    if write:
        _write_binary_file(pp_bin_file, pp_tbl_bytes)
