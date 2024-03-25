# -*- coding: utf-8 -*-
#
# TARGET arch is: ['', '--include', 'stdint.h', '--include', 'linux/drivers/gpu/drm/amd/include/atom-types.h', '']
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes


class AsDictMixin:
    @classmethod
    def as_dict(cls, self):
        result = {}
        if not isinstance(self, AsDictMixin):
            # not a structure, assume it's already a python object
            return self
        if not hasattr(cls, "_fields_"):
            return result
        # sys.version_info >= (3, 5)
        # for (field, *_) in cls._fields_:  # noqa
        for field_tuple in cls._fields_:  # noqa
            field = field_tuple[0]
            if field.startswith('PADDING_'):
                continue
            value = getattr(self, field)
            type_ = type(value)
            if hasattr(value, "_length_") and hasattr(value, "_type_"):
                # array
                if not hasattr(type_, "as_dict"):
                    value = [v for v in value]
                else:
                    type_ = type_._type_
                    value = [type_.as_dict(v) for v in value]
            elif hasattr(value, "contents") and hasattr(value, "_type_"):
                # pointer
                try:
                    if not hasattr(type_, "as_dict"):
                        value = value.contents
                    else:
                        type_ = type_._type_
                        value = type_.as_dict(value.contents)
                except ValueError:
                    # nullptr
                    value = None
            elif isinstance(value, AsDictMixin):
                # other structure
                value = type_.as_dict(value)
            result[field] = value
        return result


class Structure(ctypes.Structure, AsDictMixin):

    def __init__(self, *args, **kwds):
        # We don't want to use positional arguments fill PADDING_* fields

        args = dict(zip(self.__class__._field_names_(), args))
        args.update(kwds)
        super(Structure, self).__init__(**args)

    @classmethod
    def _field_names_(cls):
        if hasattr(cls, '_fields_'):
            return (f[0] for f in cls._fields_ if not f[0].startswith('PADDING'))
        else:
            return ()

    @classmethod
    def get_type(cls, field):
        for f in cls._fields_:
            if f[0] == field:
                return f[1]
        return None

    @classmethod
    def bind(cls, bound_fields):
        fields = {}
        for name, type_ in cls._fields_:
            if hasattr(type_, "restype"):
                if name in bound_fields:
                    if bound_fields[name] is None:
                        fields[name] = type_()
                    else:
                        # use a closure to capture the callback from the loop scope
                        fields[name] = (
                            type_((lambda callback: lambda *args: callback(*args))(
                                bound_fields[name]))
                        )
                    del bound_fields[name]
                else:
                    # default callback implementation (does nothing)
                    try:
                        default_ = type_(0).restype().value
                    except TypeError:
                        default_ = None
                    fields[name] = type_((
                        lambda default_: lambda *args: default_)(default_))
            else:
                # not a callback function, use default initialization
                if name in bound_fields:
                    fields[name] = bound_fields[name]
                    del bound_fields[name]
                else:
                    fields[name] = type_()
        if len(bound_fields) != 0:
            raise ValueError(
                "Cannot bind the following unknown callback(s) {}.{}".format(
                    cls.__name__, bound_fields.keys()
            ))
        return cls(**fields)


class Union(ctypes.Union, AsDictMixin):
    pass





class struct__ATOM_COMMON_TABLE_HEADER(Structure):
    pass

struct__ATOM_COMMON_TABLE_HEADER._pack_ = 1 # source:False
struct__ATOM_COMMON_TABLE_HEADER._fields_ = [
    ('usStructureSize', ctypes.c_uint16),
    ('ucTableFormatRevision', ctypes.c_ubyte),
    ('ucTableContentRevision', ctypes.c_ubyte),
]

class struct__ATOM_ROM_HEADER(Structure):
    pass

ATOM_COMMON_TABLE_HEADER = struct__ATOM_COMMON_TABLE_HEADER
struct__ATOM_ROM_HEADER._pack_ = 1 # source:False
struct__ATOM_ROM_HEADER._fields_ = [
    ('sHeader', ATOM_COMMON_TABLE_HEADER),
    ('uaFirmWareSignature', ctypes.c_ubyte * 4),
    ('usBiosRuntimeSegmentAddress', ctypes.c_uint16),
    ('usProtectedModeInfoOffset', ctypes.c_uint16),
    ('usConfigFilenameOffset', ctypes.c_uint16),
    ('usCRC_BlockOffset', ctypes.c_uint16),
    ('usBIOS_BootupMessageOffset', ctypes.c_uint16),
    ('usInt10Offset', ctypes.c_uint16),
    ('usPciBusDevInitCode', ctypes.c_uint16),
    ('usIoBaseAddress', ctypes.c_uint16),
    ('usSubsystemVendorID', ctypes.c_uint16),
    ('usSubsystemID', ctypes.c_uint16),
    ('usPCI_InfoOffset', ctypes.c_uint16),
    ('usMasterCommandTableOffset', ctypes.c_uint16),
    ('usMasterDataTableOffset', ctypes.c_uint16),
    ('ucExtendedFunctionCode', ctypes.c_ubyte),
    ('ucReserved', ctypes.c_ubyte),
]

class struct__ATOM_ROM_HEADER_V2_1(Structure):
    pass

struct__ATOM_ROM_HEADER_V2_1._pack_ = 1 # source:False
struct__ATOM_ROM_HEADER_V2_1._fields_ = [
    ('sHeader', ATOM_COMMON_TABLE_HEADER),
    ('uaFirmWareSignature', ctypes.c_ubyte * 4),
    ('usBiosRuntimeSegmentAddress', ctypes.c_uint16),
    ('usProtectedModeInfoOffset', ctypes.c_uint16),
    ('usConfigFilenameOffset', ctypes.c_uint16),
    ('usCRC_BlockOffset', ctypes.c_uint16),
    ('usBIOS_BootupMessageOffset', ctypes.c_uint16),
    ('usInt10Offset', ctypes.c_uint16),
    ('usPciBusDevInitCode', ctypes.c_uint16),
    ('usIoBaseAddress', ctypes.c_uint16),
    ('usSubsystemVendorID', ctypes.c_uint16),
    ('usSubsystemID', ctypes.c_uint16),
    ('usPCI_InfoOffset', ctypes.c_uint16),
    ('usMasterCommandTableOffset', ctypes.c_uint16),
    ('usMasterDataTableOffset', ctypes.c_uint16),
    ('ucExtendedFunctionCode', ctypes.c_ubyte),
    ('ucReserved', ctypes.c_ubyte),
    ('ulPSPDirTableOffset', ctypes.c_uint32),
]

class struct__ATOM_MASTER_DATA_TABLE(Structure):
    pass

class struct__ATOM_MASTER_LIST_OF_DATA_TABLES(Structure):
    pass

struct__ATOM_MASTER_LIST_OF_DATA_TABLES._pack_ = 1 # source:False
struct__ATOM_MASTER_LIST_OF_DATA_TABLES._fields_ = [
    ('UtilityPipeLine', ctypes.c_uint16),
    ('MultimediaCapabilityInfo', ctypes.c_uint16),
    ('MultimediaConfigInfo', ctypes.c_uint16),
    ('StandardVESA_Timing', ctypes.c_uint16),
    ('FirmwareInfo', ctypes.c_uint16),
    ('PaletteData', ctypes.c_uint16),
    ('LCD_Info', ctypes.c_uint16),
    ('DIGTransmitterInfo', ctypes.c_uint16),
    ('SMU_Info', ctypes.c_uint16),
    ('SupportedDevicesInfo', ctypes.c_uint16),
    ('GPIO_I2C_Info', ctypes.c_uint16),
    ('VRAM_UsageByFirmware', ctypes.c_uint16),
    ('GPIO_Pin_LUT', ctypes.c_uint16),
    ('VESA_ToInternalModeLUT', ctypes.c_uint16),
    ('GFX_Info', ctypes.c_uint16),
    ('PowerPlayInfo', ctypes.c_uint16),
    ('GPUVirtualizationInfo', ctypes.c_uint16),
    ('SaveRestoreInfo', ctypes.c_uint16),
    ('PPLL_SS_Info', ctypes.c_uint16),
    ('OemInfo', ctypes.c_uint16),
    ('XTMDS_Info', ctypes.c_uint16),
    ('MclkSS_Info', ctypes.c_uint16),
    ('Object_Header', ctypes.c_uint16),
    ('IndirectIOAccess', ctypes.c_uint16),
    ('MC_InitParameter', ctypes.c_uint16),
    ('ASIC_VDDC_Info', ctypes.c_uint16),
    ('ASIC_InternalSS_Info', ctypes.c_uint16),
    ('TV_VideoMode', ctypes.c_uint16),
    ('VRAM_Info', ctypes.c_uint16),
    ('MemoryTrainingInfo', ctypes.c_uint16),
    ('IntegratedSystemInfo', ctypes.c_uint16),
    ('ASIC_ProfilingInfo', ctypes.c_uint16),
    ('VoltageObjectInfo', ctypes.c_uint16),
    ('PowerSourceInfo', ctypes.c_uint16),
    ('ServiceInfo', ctypes.c_uint16),
]

ATOM_MASTER_LIST_OF_DATA_TABLES = struct__ATOM_MASTER_LIST_OF_DATA_TABLES
struct__ATOM_MASTER_DATA_TABLE._pack_ = 1 # source:False
struct__ATOM_MASTER_DATA_TABLE._fields_ = [
    ('sHeader', ATOM_COMMON_TABLE_HEADER),
    ('ListOfDataTables', ATOM_MASTER_LIST_OF_DATA_TABLES),
]

__all__ = \
    ['ATOM_COMMON_TABLE_HEADER', 'ATOM_MASTER_LIST_OF_DATA_TABLES',
    'struct__ATOM_COMMON_TABLE_HEADER',
    'struct__ATOM_MASTER_DATA_TABLE',
    'struct__ATOM_MASTER_LIST_OF_DATA_TABLES',
    'struct__ATOM_ROM_HEADER', 'struct__ATOM_ROM_HEADER_V2_1']
