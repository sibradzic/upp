# -*- coding: utf-8 -*-
#
# TARGET arch is: ['--include', 'stdint.h', '--include', 'linux/drivers/gpu/drm/amd/include/atom-types.h', '--include', 'linux/drivers/gpu/drm/amd/include/atomfirmware.h', '--include', 'linux/drivers/gpu/drm/amd/include/atombios.h']
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





_VEGA10_PPTABLE_H_ = True # macro
ATOM_VEGA10_PP_FANPARAMETERS_TACHOMETER_PULSES_PER_REVOLUTION_MASK = 0x0f # macro
ATOM_VEGA10_PP_FANPARAMETERS_NOFAN = 0x80 # macro
ATOM_VEGA10_PP_THERMALCONTROLLER_NONE = 0 # macro
ATOM_VEGA10_PP_THERMALCONTROLLER_LM96163 = 17 # macro
ATOM_VEGA10_PP_THERMALCONTROLLER_VEGA10 = 24 # macro
ATOM_VEGA10_PP_THERMALCONTROLLER_ADT7473_WITH_INTERNAL = 0x89 # macro
ATOM_VEGA10_PP_THERMALCONTROLLER_EMC2103_WITH_INTERNAL = 0x8D # macro
ATOM_VEGA10_PP_PLATFORM_CAP_POWERPLAY = 0x1 # macro
ATOM_VEGA10_PP_PLATFORM_CAP_SBIOSPOWERSOURCE = 0x2 # macro
ATOM_VEGA10_PP_PLATFORM_CAP_HARDWAREDC = 0x4 # macro
ATOM_VEGA10_PP_PLATFORM_CAP_BACO = 0x8 # macro
ATOM_VEGA10_PP_PLATFORM_COMBINE_PCC_WITH_THERMAL_SIGNAL = 0x10 # macro
ATOM_PPLIB_CLASSIFICATION_UI_MASK = 0x0007 # macro
ATOM_PPLIB_CLASSIFICATION_UI_SHIFT = 0 # macro
ATOM_PPLIB_CLASSIFICATION_UI_NONE = 0 # macro
ATOM_PPLIB_CLASSIFICATION_UI_BATTERY = 1 # macro
ATOM_PPLIB_CLASSIFICATION_UI_BALANCED = 3 # macro
ATOM_PPLIB_CLASSIFICATION_UI_PERFORMANCE = 5 # macro
ATOM_PPLIB_CLASSIFICATION_BOOT = 0x0008 # macro
ATOM_PPLIB_CLASSIFICATION_THERMAL = 0x0010 # macro
ATOM_PPLIB_CLASSIFICATION_LIMITEDPOWERSOURCE = 0x0020 # macro
ATOM_PPLIB_CLASSIFICATION_REST = 0x0040 # macro
ATOM_PPLIB_CLASSIFICATION_FORCED = 0x0080 # macro
ATOM_PPLIB_CLASSIFICATION_ACPI = 0x1000 # macro
ATOM_PPLIB_CLASSIFICATION2_LIMITEDPOWERSOURCE_2 = 0x0001 # macro
ATOM_Vega10_DISALLOW_ON_DC = 0x00004000 # macro
ATOM_Vega10_ENABLE_VARIBRIGHT = 0x00008000 # macro
ATOM_Vega10_TABLE_REVISION_VEGA10 = 8 # macro
ATOM_Vega10_VoltageMode_AVFS_Interpolate = 0 # macro
ATOM_Vega10_VoltageMode_AVFS_WorstCase = 1 # macro
ATOM_Vega10_VoltageMode_Static = 2 # macro
class struct__ATOM_Vega10_POWERPLAYTABLE(Structure):
    pass

class struct_atom_common_table_header(Structure):
    pass

struct_atom_common_table_header._pack_ = 1 # source:False
struct_atom_common_table_header._fields_ = [
    ('structuresize', ctypes.c_uint16),
    ('format_revision', ctypes.c_ubyte),
    ('content_revision', ctypes.c_ubyte),
]

struct__ATOM_Vega10_POWERPLAYTABLE._pack_ = 1 # source:False
struct__ATOM_Vega10_POWERPLAYTABLE._fields_ = [
    ('sHeader', struct_atom_common_table_header),
    ('ucTableRevision', ctypes.c_ubyte),
    ('usTableSize', ctypes.c_uint16),
    ('ulGoldenPPID', ctypes.c_uint32),
    ('ulGoldenRevision', ctypes.c_uint32),
    ('usFormatID', ctypes.c_uint16),
    ('ulPlatformCaps', ctypes.c_uint32),
    ('ulMaxODEngineClock', ctypes.c_uint32),
    ('ulMaxODMemoryClock', ctypes.c_uint32),
    ('usPowerControlLimit', ctypes.c_uint16),
    ('usUlvVoltageOffset', ctypes.c_uint16),
    ('usUlvSmnclkDid', ctypes.c_uint16),
    ('usUlvMp1clkDid', ctypes.c_uint16),
    ('usUlvGfxclkBypass', ctypes.c_uint16),
    ('usGfxclkSlewRate', ctypes.c_uint16),
    ('ucGfxVoltageMode', ctypes.c_ubyte),
    ('ucSocVoltageMode', ctypes.c_ubyte),
    ('ucUclkVoltageMode', ctypes.c_ubyte),
    ('ucUvdVoltageMode', ctypes.c_ubyte),
    ('ucVceVoltageMode', ctypes.c_ubyte),
    ('ucMp0VoltageMode', ctypes.c_ubyte),
    ('ucDcefVoltageMode', ctypes.c_ubyte),
    ('usStateArrayOffset', ctypes.c_uint16),
    ('usFanTableOffset', ctypes.c_uint16),
    ('usThermalControllerOffset', ctypes.c_uint16),
    ('usSocclkDependencyTableOffset', ctypes.c_uint16),
    ('usMclkDependencyTableOffset', ctypes.c_uint16),
    ('usGfxclkDependencyTableOffset', ctypes.c_uint16),
    ('usDcefclkDependencyTableOffset', ctypes.c_uint16),
    ('usVddcLookupTableOffset', ctypes.c_uint16),
    ('usVddmemLookupTableOffset', ctypes.c_uint16),
    ('usMMDependencyTableOffset', ctypes.c_uint16),
    ('usVCEStateTableOffset', ctypes.c_uint16),
    ('usReserve', ctypes.c_uint16),
    ('usPowerTuneTableOffset', ctypes.c_uint16),
    ('usHardLimitTableOffset', ctypes.c_uint16),
    ('usVddciLookupTableOffset', ctypes.c_uint16),
    ('usPCIETableOffset', ctypes.c_uint16),
    ('usPixclkDependencyTableOffset', ctypes.c_uint16),
    ('usDispClkDependencyTableOffset', ctypes.c_uint16),
    ('usPhyClkDependencyTableOffset', ctypes.c_uint16),
]

ATOM_Vega10_POWERPLAYTABLE = struct__ATOM_Vega10_POWERPLAYTABLE
class struct__ATOM_Vega10_State(Structure):
    pass

struct__ATOM_Vega10_State._pack_ = 1 # source:False
struct__ATOM_Vega10_State._fields_ = [
    ('ucSocClockIndexHigh', ctypes.c_ubyte),
    ('ucSocClockIndexLow', ctypes.c_ubyte),
    ('ucGfxClockIndexHigh', ctypes.c_ubyte),
    ('ucGfxClockIndexLow', ctypes.c_ubyte),
    ('ucMemClockIndexHigh', ctypes.c_ubyte),
    ('ucMemClockIndexLow', ctypes.c_ubyte),
    ('usClassification', ctypes.c_uint16),
    ('ulCapsAndSettings', ctypes.c_uint32),
    ('usClassification2', ctypes.c_uint16),
]

ATOM_Vega10_State = struct__ATOM_Vega10_State
class struct__ATOM_Vega10_State_Array(Structure):
    pass

struct__ATOM_Vega10_State_Array._pack_ = 1 # source:False
struct__ATOM_Vega10_State_Array._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('states', struct__ATOM_Vega10_State * 0),
]

ATOM_Vega10_State_Array = struct__ATOM_Vega10_State_Array
class struct__ATOM_Vega10_CLK_Dependency_Record(Structure):
    pass

struct__ATOM_Vega10_CLK_Dependency_Record._pack_ = 1 # source:False
struct__ATOM_Vega10_CLK_Dependency_Record._fields_ = [
    ('ulClk', ctypes.c_uint32),
    ('ucVddInd', ctypes.c_ubyte),
]

ATOM_Vega10_CLK_Dependency_Record = struct__ATOM_Vega10_CLK_Dependency_Record
class struct__ATOM_Vega10_GFXCLK_Dependency_Record(Structure):
    pass

struct__ATOM_Vega10_GFXCLK_Dependency_Record._pack_ = 1 # source:False
struct__ATOM_Vega10_GFXCLK_Dependency_Record._fields_ = [
    ('ulClk', ctypes.c_uint32),
    ('ucVddInd', ctypes.c_ubyte),
    ('usCKSVOffsetandDisable', ctypes.c_uint16),
    ('usAVFSOffset', ctypes.c_uint16),
]

ATOM_Vega10_GFXCLK_Dependency_Record = struct__ATOM_Vega10_GFXCLK_Dependency_Record
class struct__ATOM_Vega10_GFXCLK_Dependency_Record_V2(Structure):
    pass

struct__ATOM_Vega10_GFXCLK_Dependency_Record_V2._pack_ = 1 # source:False
struct__ATOM_Vega10_GFXCLK_Dependency_Record_V2._fields_ = [
    ('ulClk', ctypes.c_uint32),
    ('ucVddInd', ctypes.c_ubyte),
    ('usCKSVOffsetandDisable', ctypes.c_uint16),
    ('usAVFSOffset', ctypes.c_uint16),
    ('ucACGEnable', ctypes.c_ubyte),
    ('ucReserved', ctypes.c_ubyte * 3),
]

ATOM_Vega10_GFXCLK_Dependency_Record_V2 = struct__ATOM_Vega10_GFXCLK_Dependency_Record_V2
class struct__ATOM_Vega10_MCLK_Dependency_Record(Structure):
    pass

struct__ATOM_Vega10_MCLK_Dependency_Record._pack_ = 1 # source:False
struct__ATOM_Vega10_MCLK_Dependency_Record._fields_ = [
    ('ulMemClk', ctypes.c_uint32),
    ('ucVddInd', ctypes.c_ubyte),
    ('ucVddMemInd', ctypes.c_ubyte),
    ('ucVddciInd', ctypes.c_ubyte),
]

ATOM_Vega10_MCLK_Dependency_Record = struct__ATOM_Vega10_MCLK_Dependency_Record
class struct__ATOM_Vega10_GFXCLK_Dependency_Table(Structure):
    pass

struct__ATOM_Vega10_GFXCLK_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_GFXCLK_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_GFXCLK_Dependency_Record * 0),
]

ATOM_Vega10_GFXCLK_Dependency_Table = struct__ATOM_Vega10_GFXCLK_Dependency_Table
class struct__ATOM_Vega10_MCLK_Dependency_Table(Structure):
    pass

struct__ATOM_Vega10_MCLK_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_MCLK_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_MCLK_Dependency_Record * 0),
]

ATOM_Vega10_MCLK_Dependency_Table = struct__ATOM_Vega10_MCLK_Dependency_Table
class struct__ATOM_Vega10_SOCCLK_Dependency_Table(Structure):
    pass

struct__ATOM_Vega10_SOCCLK_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_SOCCLK_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_CLK_Dependency_Record * 0),
]

ATOM_Vega10_SOCCLK_Dependency_Table = struct__ATOM_Vega10_SOCCLK_Dependency_Table
class struct__ATOM_Vega10_DCEFCLK_Dependency_Table(Structure):
    pass

struct__ATOM_Vega10_DCEFCLK_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_DCEFCLK_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_CLK_Dependency_Record * 0),
]

ATOM_Vega10_DCEFCLK_Dependency_Table = struct__ATOM_Vega10_DCEFCLK_Dependency_Table
class struct__ATOM_Vega10_PIXCLK_Dependency_Table(Structure):
    pass

struct__ATOM_Vega10_PIXCLK_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_PIXCLK_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_CLK_Dependency_Record * 0),
]

ATOM_Vega10_PIXCLK_Dependency_Table = struct__ATOM_Vega10_PIXCLK_Dependency_Table
class struct__ATOM_Vega10_DISPCLK_Dependency_Table(Structure):
    pass

struct__ATOM_Vega10_DISPCLK_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_DISPCLK_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_CLK_Dependency_Record * 0),
]

ATOM_Vega10_DISPCLK_Dependency_Table = struct__ATOM_Vega10_DISPCLK_Dependency_Table
class struct__ATOM_Vega10_PHYCLK_Dependency_Table(Structure):
    pass

struct__ATOM_Vega10_PHYCLK_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_PHYCLK_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_CLK_Dependency_Record * 0),
]

ATOM_Vega10_PHYCLK_Dependency_Table = struct__ATOM_Vega10_PHYCLK_Dependency_Table
class struct__ATOM_Vega10_MM_Dependency_Record(Structure):
    pass

struct__ATOM_Vega10_MM_Dependency_Record._pack_ = 1 # source:False
struct__ATOM_Vega10_MM_Dependency_Record._fields_ = [
    ('ucVddcInd', ctypes.c_ubyte),
    ('ulDClk', ctypes.c_uint32),
    ('ulVClk', ctypes.c_uint32),
    ('ulEClk', ctypes.c_uint32),
    ('ulPSPClk', ctypes.c_uint32),
]

ATOM_Vega10_MM_Dependency_Record = struct__ATOM_Vega10_MM_Dependency_Record
class struct__ATOM_Vega10_MM_Dependency_Table(Structure):
    pass

struct__ATOM_Vega10_MM_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_MM_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_MM_Dependency_Record * 0),
]

ATOM_Vega10_MM_Dependency_Table = struct__ATOM_Vega10_MM_Dependency_Table
class struct__ATOM_Vega10_PCIE_Record(Structure):
    pass

struct__ATOM_Vega10_PCIE_Record._pack_ = 1 # source:False
struct__ATOM_Vega10_PCIE_Record._fields_ = [
    ('ulLCLK', ctypes.c_uint32),
    ('ucPCIEGenSpeed', ctypes.c_ubyte),
    ('ucPCIELaneWidth', ctypes.c_ubyte),
]

ATOM_Vega10_PCIE_Record = struct__ATOM_Vega10_PCIE_Record
class struct__ATOM_Vega10_PCIE_Table(Structure):
    pass

struct__ATOM_Vega10_PCIE_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_PCIE_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_PCIE_Record * 0),
]

ATOM_Vega10_PCIE_Table = struct__ATOM_Vega10_PCIE_Table
class struct__ATOM_Vega10_Voltage_Lookup_Record(Structure):
    pass

struct__ATOM_Vega10_Voltage_Lookup_Record._pack_ = 1 # source:False
struct__ATOM_Vega10_Voltage_Lookup_Record._fields_ = [
    ('usVdd', ctypes.c_uint16),
]

ATOM_Vega10_Voltage_Lookup_Record = struct__ATOM_Vega10_Voltage_Lookup_Record
class struct__ATOM_Vega10_Voltage_Lookup_Table(Structure):
    pass

struct__ATOM_Vega10_Voltage_Lookup_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_Voltage_Lookup_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_Voltage_Lookup_Record * 0),
]

ATOM_Vega10_Voltage_Lookup_Table = struct__ATOM_Vega10_Voltage_Lookup_Table
class struct__ATOM_Vega10_Fan_Table(Structure):
    pass

struct__ATOM_Vega10_Fan_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_Fan_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('usFanOutputSensitivity', ctypes.c_uint16),
    ('usFanRPMMax', ctypes.c_uint16),
    ('usThrottlingRPM', ctypes.c_uint16),
    ('usFanAcousticLimit', ctypes.c_uint16),
    ('usTargetTemperature', ctypes.c_uint16),
    ('usMinimumPWMLimit', ctypes.c_uint16),
    ('usTargetGfxClk', ctypes.c_uint16),
    ('usFanGainEdge', ctypes.c_uint16),
    ('usFanGainHotspot', ctypes.c_uint16),
    ('usFanGainLiquid', ctypes.c_uint16),
    ('usFanGainVrVddc', ctypes.c_uint16),
    ('usFanGainVrMvdd', ctypes.c_uint16),
    ('usFanGainPlx', ctypes.c_uint16),
    ('usFanGainHbm', ctypes.c_uint16),
    ('ucEnableZeroRPM', ctypes.c_ubyte),
    ('usFanStopTemperature', ctypes.c_uint16),
    ('usFanStartTemperature', ctypes.c_uint16),
]

ATOM_Vega10_Fan_Table = struct__ATOM_Vega10_Fan_Table
class struct__ATOM_Vega10_Fan_Table_V2(Structure):
    pass

struct__ATOM_Vega10_Fan_Table_V2._pack_ = 1 # source:False
struct__ATOM_Vega10_Fan_Table_V2._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('usFanOutputSensitivity', ctypes.c_uint16),
    ('usFanAcousticLimitRpm', ctypes.c_uint16),
    ('usThrottlingRPM', ctypes.c_uint16),
    ('usTargetTemperature', ctypes.c_uint16),
    ('usMinimumPWMLimit', ctypes.c_uint16),
    ('usTargetGfxClk', ctypes.c_uint16),
    ('usFanGainEdge', ctypes.c_uint16),
    ('usFanGainHotspot', ctypes.c_uint16),
    ('usFanGainLiquid', ctypes.c_uint16),
    ('usFanGainVrVddc', ctypes.c_uint16),
    ('usFanGainVrMvdd', ctypes.c_uint16),
    ('usFanGainPlx', ctypes.c_uint16),
    ('usFanGainHbm', ctypes.c_uint16),
    ('ucEnableZeroRPM', ctypes.c_ubyte),
    ('usFanStopTemperature', ctypes.c_uint16),
    ('usFanStartTemperature', ctypes.c_uint16),
    ('ucFanParameters', ctypes.c_ubyte),
    ('ucFanMinRPM', ctypes.c_ubyte),
    ('ucFanMaxRPM', ctypes.c_ubyte),
]

ATOM_Vega10_Fan_Table_V2 = struct__ATOM_Vega10_Fan_Table_V2
class struct__ATOM_Vega10_Fan_Table_V3(Structure):
    pass

struct__ATOM_Vega10_Fan_Table_V3._pack_ = 1 # source:False
struct__ATOM_Vega10_Fan_Table_V3._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('usFanOutputSensitivity', ctypes.c_uint16),
    ('usFanAcousticLimitRpm', ctypes.c_uint16),
    ('usThrottlingRPM', ctypes.c_uint16),
    ('usTargetTemperature', ctypes.c_uint16),
    ('usMinimumPWMLimit', ctypes.c_uint16),
    ('usTargetGfxClk', ctypes.c_uint16),
    ('usFanGainEdge', ctypes.c_uint16),
    ('usFanGainHotspot', ctypes.c_uint16),
    ('usFanGainLiquid', ctypes.c_uint16),
    ('usFanGainVrVddc', ctypes.c_uint16),
    ('usFanGainVrMvdd', ctypes.c_uint16),
    ('usFanGainPlx', ctypes.c_uint16),
    ('usFanGainHbm', ctypes.c_uint16),
    ('ucEnableZeroRPM', ctypes.c_ubyte),
    ('usFanStopTemperature', ctypes.c_uint16),
    ('usFanStartTemperature', ctypes.c_uint16),
    ('ucFanParameters', ctypes.c_ubyte),
    ('ucFanMinRPM', ctypes.c_ubyte),
    ('ucFanMaxRPM', ctypes.c_ubyte),
    ('usMGpuThrottlingRPM', ctypes.c_uint16),
]

ATOM_Vega10_Fan_Table_V3 = struct__ATOM_Vega10_Fan_Table_V3
class struct__ATOM_Vega10_Thermal_Controller(Structure):
    pass

struct__ATOM_Vega10_Thermal_Controller._pack_ = 1 # source:False
struct__ATOM_Vega10_Thermal_Controller._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucType', ctypes.c_ubyte),
    ('ucI2cLine', ctypes.c_ubyte),
    ('ucI2cAddress', ctypes.c_ubyte),
    ('ucFanParameters', ctypes.c_ubyte),
    ('ucFanMinRPM', ctypes.c_ubyte),
    ('ucFanMaxRPM', ctypes.c_ubyte),
    ('ucFlags', ctypes.c_ubyte),
]

ATOM_Vega10_Thermal_Controller = struct__ATOM_Vega10_Thermal_Controller
class struct__ATOM_Vega10_VCE_State_Record(Structure):
    pass

struct__ATOM_Vega10_VCE_State_Record._pack_ = 1 # source:False
struct__ATOM_Vega10_VCE_State_Record._fields_ = [
    ('ucVCEClockIndex', ctypes.c_ubyte),
    ('ucFlag', ctypes.c_ubyte),
    ('ucSCLKIndex', ctypes.c_ubyte),
    ('ucMCLKIndex', ctypes.c_ubyte),
]

ATOM_Vega10_VCE_State_Record = struct__ATOM_Vega10_VCE_State_Record
class struct__ATOM_Vega10_VCE_State_Table(Structure):
    pass

struct__ATOM_Vega10_VCE_State_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_VCE_State_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_VCE_State_Record * 0),
]

ATOM_Vega10_VCE_State_Table = struct__ATOM_Vega10_VCE_State_Table
class struct__ATOM_Vega10_PowerTune_Table(Structure):
    pass

struct__ATOM_Vega10_PowerTune_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_PowerTune_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('usSocketPowerLimit', ctypes.c_uint16),
    ('usBatteryPowerLimit', ctypes.c_uint16),
    ('usSmallPowerLimit', ctypes.c_uint16),
    ('usTdcLimit', ctypes.c_uint16),
    ('usEdcLimit', ctypes.c_uint16),
    ('usSoftwareShutdownTemp', ctypes.c_uint16),
    ('usTemperatureLimitHotSpot', ctypes.c_uint16),
    ('usTemperatureLimitLiquid1', ctypes.c_uint16),
    ('usTemperatureLimitLiquid2', ctypes.c_uint16),
    ('usTemperatureLimitHBM', ctypes.c_uint16),
    ('usTemperatureLimitVrSoc', ctypes.c_uint16),
    ('usTemperatureLimitVrMem', ctypes.c_uint16),
    ('usTemperatureLimitPlx', ctypes.c_uint16),
    ('usLoadLineResistance', ctypes.c_uint16),
    ('ucLiquid1_I2C_address', ctypes.c_ubyte),
    ('ucLiquid2_I2C_address', ctypes.c_ubyte),
    ('ucVr_I2C_address', ctypes.c_ubyte),
    ('ucPlx_I2C_address', ctypes.c_ubyte),
    ('ucLiquid_I2C_LineSCL', ctypes.c_ubyte),
    ('ucLiquid_I2C_LineSDA', ctypes.c_ubyte),
    ('ucVr_I2C_LineSCL', ctypes.c_ubyte),
    ('ucVr_I2C_LineSDA', ctypes.c_ubyte),
    ('ucPlx_I2C_LineSCL', ctypes.c_ubyte),
    ('ucPlx_I2C_LineSDA', ctypes.c_ubyte),
    ('usTemperatureLimitTedge', ctypes.c_uint16),
]

ATOM_Vega10_PowerTune_Table = struct__ATOM_Vega10_PowerTune_Table
class struct__ATOM_Vega10_PowerTune_Table_V2(Structure):
    pass

struct__ATOM_Vega10_PowerTune_Table_V2._pack_ = 1 # source:False
struct__ATOM_Vega10_PowerTune_Table_V2._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('usSocketPowerLimit', ctypes.c_uint16),
    ('usBatteryPowerLimit', ctypes.c_uint16),
    ('usSmallPowerLimit', ctypes.c_uint16),
    ('usTdcLimit', ctypes.c_uint16),
    ('usEdcLimit', ctypes.c_uint16),
    ('usSoftwareShutdownTemp', ctypes.c_uint16),
    ('usTemperatureLimitHotSpot', ctypes.c_uint16),
    ('usTemperatureLimitLiquid1', ctypes.c_uint16),
    ('usTemperatureLimitLiquid2', ctypes.c_uint16),
    ('usTemperatureLimitHBM', ctypes.c_uint16),
    ('usTemperatureLimitVrSoc', ctypes.c_uint16),
    ('usTemperatureLimitVrMem', ctypes.c_uint16),
    ('usTemperatureLimitPlx', ctypes.c_uint16),
    ('usLoadLineResistance', ctypes.c_uint16),
    ('ucLiquid1_I2C_address', ctypes.c_ubyte),
    ('ucLiquid2_I2C_address', ctypes.c_ubyte),
    ('ucLiquid_I2C_Line', ctypes.c_ubyte),
    ('ucVr_I2C_address', ctypes.c_ubyte),
    ('ucVr_I2C_Line', ctypes.c_ubyte),
    ('ucPlx_I2C_address', ctypes.c_ubyte),
    ('ucPlx_I2C_Line', ctypes.c_ubyte),
    ('usTemperatureLimitTedge', ctypes.c_uint16),
]

ATOM_Vega10_PowerTune_Table_V2 = struct__ATOM_Vega10_PowerTune_Table_V2
class struct__ATOM_Vega10_PowerTune_Table_V3(Structure):
    pass

struct__ATOM_Vega10_PowerTune_Table_V3._pack_ = 1 # source:False
struct__ATOM_Vega10_PowerTune_Table_V3._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('usSocketPowerLimit', ctypes.c_uint16),
    ('usBatteryPowerLimit', ctypes.c_uint16),
    ('usSmallPowerLimit', ctypes.c_uint16),
    ('usTdcLimit', ctypes.c_uint16),
    ('usEdcLimit', ctypes.c_uint16),
    ('usSoftwareShutdownTemp', ctypes.c_uint16),
    ('usTemperatureLimitHotSpot', ctypes.c_uint16),
    ('usTemperatureLimitLiquid1', ctypes.c_uint16),
    ('usTemperatureLimitLiquid2', ctypes.c_uint16),
    ('usTemperatureLimitHBM', ctypes.c_uint16),
    ('usTemperatureLimitVrSoc', ctypes.c_uint16),
    ('usTemperatureLimitVrMem', ctypes.c_uint16),
    ('usTemperatureLimitPlx', ctypes.c_uint16),
    ('usLoadLineResistance', ctypes.c_uint16),
    ('ucLiquid1_I2C_address', ctypes.c_ubyte),
    ('ucLiquid2_I2C_address', ctypes.c_ubyte),
    ('ucLiquid_I2C_Line', ctypes.c_ubyte),
    ('ucVr_I2C_address', ctypes.c_ubyte),
    ('ucVr_I2C_Line', ctypes.c_ubyte),
    ('ucPlx_I2C_address', ctypes.c_ubyte),
    ('ucPlx_I2C_Line', ctypes.c_ubyte),
    ('usTemperatureLimitTedge', ctypes.c_uint16),
    ('usBoostStartTemperature', ctypes.c_uint16),
    ('usBoostStopTemperature', ctypes.c_uint16),
    ('ulBoostClock', ctypes.c_uint32),
    ('Reserved', ctypes.c_uint32 * 2),
]

ATOM_Vega10_PowerTune_Table_V3 = struct__ATOM_Vega10_PowerTune_Table_V3
class struct__ATOM_Vega10_Hard_Limit_Record(Structure):
    pass

struct__ATOM_Vega10_Hard_Limit_Record._pack_ = 1 # source:False
struct__ATOM_Vega10_Hard_Limit_Record._fields_ = [
    ('ulSOCCLKLimit', ctypes.c_uint32),
    ('ulGFXCLKLimit', ctypes.c_uint32),
    ('ulMCLKLimit', ctypes.c_uint32),
    ('usVddcLimit', ctypes.c_uint16),
    ('usVddciLimit', ctypes.c_uint16),
    ('usVddMemLimit', ctypes.c_uint16),
]

ATOM_Vega10_Hard_Limit_Record = struct__ATOM_Vega10_Hard_Limit_Record
class struct__ATOM_Vega10_Hard_Limit_Table(Structure):
    pass

struct__ATOM_Vega10_Hard_Limit_Table._pack_ = 1 # source:False
struct__ATOM_Vega10_Hard_Limit_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Vega10_Hard_Limit_Record * 0),
]

ATOM_Vega10_Hard_Limit_Table = struct__ATOM_Vega10_Hard_Limit_Table
class struct__Vega10_PPTable_Generic_SubTable_Header(Structure):
    pass

struct__Vega10_PPTable_Generic_SubTable_Header._pack_ = 1 # source:False
struct__Vega10_PPTable_Generic_SubTable_Header._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
]

Vega10_PPTable_Generic_SubTable_Header = struct__Vega10_PPTable_Generic_SubTable_Header
__all__ = \
    ['ATOM_PPLIB_CLASSIFICATION2_LIMITEDPOWERSOURCE_2',
    'ATOM_PPLIB_CLASSIFICATION_ACPI',
    'ATOM_PPLIB_CLASSIFICATION_BOOT',
    'ATOM_PPLIB_CLASSIFICATION_FORCED',
    'ATOM_PPLIB_CLASSIFICATION_LIMITEDPOWERSOURCE',
    'ATOM_PPLIB_CLASSIFICATION_REST',
    'ATOM_PPLIB_CLASSIFICATION_THERMAL',
    'ATOM_PPLIB_CLASSIFICATION_UI_BALANCED',
    'ATOM_PPLIB_CLASSIFICATION_UI_BATTERY',
    'ATOM_PPLIB_CLASSIFICATION_UI_MASK',
    'ATOM_PPLIB_CLASSIFICATION_UI_NONE',
    'ATOM_PPLIB_CLASSIFICATION_UI_PERFORMANCE',
    'ATOM_PPLIB_CLASSIFICATION_UI_SHIFT',
    'ATOM_VEGA10_PP_FANPARAMETERS_NOFAN',
    'ATOM_VEGA10_PP_FANPARAMETERS_TACHOMETER_PULSES_PER_REVOLUTION_MASK',
    'ATOM_VEGA10_PP_PLATFORM_CAP_BACO',
    'ATOM_VEGA10_PP_PLATFORM_CAP_HARDWAREDC',
    'ATOM_VEGA10_PP_PLATFORM_CAP_POWERPLAY',
    'ATOM_VEGA10_PP_PLATFORM_CAP_SBIOSPOWERSOURCE',
    'ATOM_VEGA10_PP_PLATFORM_COMBINE_PCC_WITH_THERMAL_SIGNAL',
    'ATOM_VEGA10_PP_THERMALCONTROLLER_ADT7473_WITH_INTERNAL',
    'ATOM_VEGA10_PP_THERMALCONTROLLER_EMC2103_WITH_INTERNAL',
    'ATOM_VEGA10_PP_THERMALCONTROLLER_LM96163',
    'ATOM_VEGA10_PP_THERMALCONTROLLER_NONE',
    'ATOM_VEGA10_PP_THERMALCONTROLLER_VEGA10',
    'ATOM_Vega10_CLK_Dependency_Record',
    'ATOM_Vega10_DCEFCLK_Dependency_Table',
    'ATOM_Vega10_DISALLOW_ON_DC',
    'ATOM_Vega10_DISPCLK_Dependency_Table',
    'ATOM_Vega10_ENABLE_VARIBRIGHT', 'ATOM_Vega10_Fan_Table',
    'ATOM_Vega10_Fan_Table_V2', 'ATOM_Vega10_Fan_Table_V3',
    'ATOM_Vega10_GFXCLK_Dependency_Record',
    'ATOM_Vega10_GFXCLK_Dependency_Record_V2',
    'ATOM_Vega10_GFXCLK_Dependency_Table',
    'ATOM_Vega10_Hard_Limit_Record', 'ATOM_Vega10_Hard_Limit_Table',
    'ATOM_Vega10_MCLK_Dependency_Record',
    'ATOM_Vega10_MCLK_Dependency_Table',
    'ATOM_Vega10_MM_Dependency_Record',
    'ATOM_Vega10_MM_Dependency_Table', 'ATOM_Vega10_PCIE_Record',
    'ATOM_Vega10_PCIE_Table', 'ATOM_Vega10_PHYCLK_Dependency_Table',
    'ATOM_Vega10_PIXCLK_Dependency_Table',
    'ATOM_Vega10_POWERPLAYTABLE', 'ATOM_Vega10_PowerTune_Table',
    'ATOM_Vega10_PowerTune_Table_V2',
    'ATOM_Vega10_PowerTune_Table_V3',
    'ATOM_Vega10_SOCCLK_Dependency_Table', 'ATOM_Vega10_State',
    'ATOM_Vega10_State_Array', 'ATOM_Vega10_TABLE_REVISION_VEGA10',
    'ATOM_Vega10_Thermal_Controller', 'ATOM_Vega10_VCE_State_Record',
    'ATOM_Vega10_VCE_State_Table',
    'ATOM_Vega10_VoltageMode_AVFS_Interpolate',
    'ATOM_Vega10_VoltageMode_AVFS_WorstCase',
    'ATOM_Vega10_VoltageMode_Static',
    'ATOM_Vega10_Voltage_Lookup_Record',
    'ATOM_Vega10_Voltage_Lookup_Table',
    'Vega10_PPTable_Generic_SubTable_Header', '_VEGA10_PPTABLE_H_',
    'struct__ATOM_Vega10_CLK_Dependency_Record',
    'struct__ATOM_Vega10_DCEFCLK_Dependency_Table',
    'struct__ATOM_Vega10_DISPCLK_Dependency_Table',
    'struct__ATOM_Vega10_Fan_Table',
    'struct__ATOM_Vega10_Fan_Table_V2',
    'struct__ATOM_Vega10_Fan_Table_V3',
    'struct__ATOM_Vega10_GFXCLK_Dependency_Record',
    'struct__ATOM_Vega10_GFXCLK_Dependency_Record_V2',
    'struct__ATOM_Vega10_GFXCLK_Dependency_Table',
    'struct__ATOM_Vega10_Hard_Limit_Record',
    'struct__ATOM_Vega10_Hard_Limit_Table',
    'struct__ATOM_Vega10_MCLK_Dependency_Record',
    'struct__ATOM_Vega10_MCLK_Dependency_Table',
    'struct__ATOM_Vega10_MM_Dependency_Record',
    'struct__ATOM_Vega10_MM_Dependency_Table',
    'struct__ATOM_Vega10_PCIE_Record',
    'struct__ATOM_Vega10_PCIE_Table',
    'struct__ATOM_Vega10_PHYCLK_Dependency_Table',
    'struct__ATOM_Vega10_PIXCLK_Dependency_Table',
    'struct__ATOM_Vega10_POWERPLAYTABLE',
    'struct__ATOM_Vega10_PowerTune_Table',
    'struct__ATOM_Vega10_PowerTune_Table_V2',
    'struct__ATOM_Vega10_PowerTune_Table_V3',
    'struct__ATOM_Vega10_SOCCLK_Dependency_Table',
    'struct__ATOM_Vega10_State', 'struct__ATOM_Vega10_State_Array',
    'struct__ATOM_Vega10_Thermal_Controller',
    'struct__ATOM_Vega10_VCE_State_Record',
    'struct__ATOM_Vega10_VCE_State_Table',
    'struct__ATOM_Vega10_Voltage_Lookup_Record',
    'struct__ATOM_Vega10_Voltage_Lookup_Table',
    'struct__Vega10_PPTable_Generic_SubTable_Header',
    'struct_atom_common_table_header']
