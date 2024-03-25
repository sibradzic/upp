# -*- coding: utf-8 -*-
#
# TARGET arch is: ['', '--include', 'stdint.h', '--include', 'linux/drivers/gpu/drm/amd/include/atom-types.h', '--include', 'linux/drivers/gpu/drm/amd/include/atombios.h', '']
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





TONGA_PPTABLE_H = True # macro
ATOM_TONGA_PP_FANPARAMETERS_TACHOMETER_PULSES_PER_REVOLUTION_MASK = 0x0f # macro
ATOM_TONGA_PP_FANPARAMETERS_NOFAN = 0x80 # macro
ATOM_TONGA_PP_THERMALCONTROLLER_NONE = 0 # macro
ATOM_TONGA_PP_THERMALCONTROLLER_LM96163 = 17 # macro
ATOM_TONGA_PP_THERMALCONTROLLER_TONGA = 21 # macro
ATOM_TONGA_PP_THERMALCONTROLLER_FIJI = 22 # macro
ATOM_TONGA_PP_THERMALCONTROLLER_ADT7473_WITH_INTERNAL = 0x89 # macro
ATOM_TONGA_PP_THERMALCONTROLLER_EMC2103_WITH_INTERNAL = 0x8D # macro
ATOM_TONGA_PP_PLATFORM_CAP_VDDGFX_CONTROL = 0x1 # macro
ATOM_TONGA_PP_PLATFORM_CAP_POWERPLAY = 0x2 # macro
ATOM_TONGA_PP_PLATFORM_CAP_SBIOSPOWERSOURCE = 0x4 # macro
ATOM_TONGA_PP_PLATFORM_CAP_DISABLE_VOLTAGE_ISLAND = 0x8 # macro
____RETIRE16____ = 0x10 # macro
ATOM_TONGA_PP_PLATFORM_CAP_HARDWAREDC = 0x20 # macro
____RETIRE64____ = 0x40 # macro
____RETIRE128____ = 0x80 # macro
____RETIRE256____ = 0x100 # macro
____RETIRE512____ = 0x200 # macro
____RETIRE1024____ = 0x400 # macro
____RETIRE2048____ = 0x800 # macro
ATOM_TONGA_PP_PLATFORM_CAP_MVDD_CONTROL = 0x1000 # macro
____RETIRE2000____ = 0x2000 # macro
____RETIRE4000____ = 0x4000 # macro
ATOM_TONGA_PP_PLATFORM_CAP_VDDCI_CONTROL = 0x8000 # macro
____RETIRE10000____ = 0x10000 # macro
ATOM_TONGA_PP_PLATFORM_CAP_BACO = 0x20000 # macro
ATOM_TONGA_PP_PLATFORM_CAP_OUTPUT_THERMAL2GPIO17 = 0x100000 # macro
ATOM_TONGA_PP_PLATFORM_COMBINE_PCC_WITH_THERMAL_SIGNAL = 0x1000000 # macro
ATOM_TONGA_PLATFORM_LOAD_POST_PRODUCTION_FIRMWARE = 0x2000000 # macro
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
ATOM_Tonga_DISALLOW_ON_DC = 0x00004000 # macro
ATOM_Tonga_ENABLE_VARIBRIGHT = 0x00008000 # macro
ATOM_Tonga_TABLE_REVISION_TONGA = 7 # macro
ATOM_PPM_A_A = 1 # macro
ATOM_PPM_A_I = 2 # macro
class struct__ATOM_Tonga_POWERPLAYTABLE(Structure):
    pass

class struct__ATOM_COMMON_TABLE_HEADER(Structure):
    pass

struct__ATOM_COMMON_TABLE_HEADER._pack_ = 1 # source:False
struct__ATOM_COMMON_TABLE_HEADER._fields_ = [
    ('usStructureSize', ctypes.c_uint16),
    ('ucTableFormatRevision', ctypes.c_ubyte),
    ('ucTableContentRevision', ctypes.c_ubyte),
]

struct__ATOM_Tonga_POWERPLAYTABLE._pack_ = 1 # source:False
struct__ATOM_Tonga_POWERPLAYTABLE._fields_ = [
    ('sHeader', struct__ATOM_COMMON_TABLE_HEADER),
    ('ucTableRevision', ctypes.c_ubyte),
    ('usTableSize', ctypes.c_uint16),
    ('ulGoldenPPID', ctypes.c_uint32),
    ('ulGoldenRevision', ctypes.c_uint32),
    ('usFormatID', ctypes.c_uint16),
    ('usVoltageTime', ctypes.c_uint16),
    ('ulPlatformCaps', ctypes.c_uint32),
    ('ulMaxODEngineClock', ctypes.c_uint32),
    ('ulMaxODMemoryClock', ctypes.c_uint32),
    ('usPowerControlLimit', ctypes.c_uint16),
    ('usUlvVoltageOffset', ctypes.c_uint16),
    ('usStateArrayOffset', ctypes.c_uint16),
    ('usFanTableOffset', ctypes.c_uint16),
    ('usThermalControllerOffset', ctypes.c_uint16),
    ('usReserv', ctypes.c_uint16),
    ('usMclkDependencyTableOffset', ctypes.c_uint16),
    ('usSclkDependencyTableOffset', ctypes.c_uint16),
    ('usVddcLookupTableOffset', ctypes.c_uint16),
    ('usVddgfxLookupTableOffset', ctypes.c_uint16),
    ('usMMDependencyTableOffset', ctypes.c_uint16),
    ('usVCEStateTableOffset', ctypes.c_uint16),
    ('usPPMTableOffset', ctypes.c_uint16),
    ('usPowerTuneTableOffset', ctypes.c_uint16),
    ('usHardLimitTableOffset', ctypes.c_uint16),
    ('usPCIETableOffset', ctypes.c_uint16),
    ('usGPIOTableOffset', ctypes.c_uint16),
    ('usReserved', ctypes.c_uint16 * 6),
]

ATOM_Tonga_POWERPLAYTABLE = struct__ATOM_Tonga_POWERPLAYTABLE
class struct__ATOM_Tonga_State(Structure):
    pass

struct__ATOM_Tonga_State._pack_ = 1 # source:False
struct__ATOM_Tonga_State._fields_ = [
    ('ucEngineClockIndexHigh', ctypes.c_ubyte),
    ('ucEngineClockIndexLow', ctypes.c_ubyte),
    ('ucMemoryClockIndexHigh', ctypes.c_ubyte),
    ('ucMemoryClockIndexLow', ctypes.c_ubyte),
    ('ucPCIEGenLow', ctypes.c_ubyte),
    ('ucPCIEGenHigh', ctypes.c_ubyte),
    ('ucPCIELaneLow', ctypes.c_ubyte),
    ('ucPCIELaneHigh', ctypes.c_ubyte),
    ('usClassification', ctypes.c_uint16),
    ('ulCapsAndSettings', ctypes.c_uint32),
    ('usClassification2', ctypes.c_uint16),
    ('ucUnused', ctypes.c_ubyte * 4),
]

ATOM_Tonga_State = struct__ATOM_Tonga_State
class struct__ATOM_Tonga_State_Array(Structure):
    pass

struct__ATOM_Tonga_State_Array._pack_ = 1 # source:False
struct__ATOM_Tonga_State_Array._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Tonga_State * 0),
]

ATOM_Tonga_State_Array = struct__ATOM_Tonga_State_Array
class struct__ATOM_Tonga_MCLK_Dependency_Record(Structure):
    pass

struct__ATOM_Tonga_MCLK_Dependency_Record._pack_ = 1 # source:False
struct__ATOM_Tonga_MCLK_Dependency_Record._fields_ = [
    ('ucVddcInd', ctypes.c_ubyte),
    ('usVddci', ctypes.c_uint16),
    ('usVddgfxOffset', ctypes.c_uint16),
    ('usMvdd', ctypes.c_uint16),
    ('ulMclk', ctypes.c_uint32),
    ('usReserved', ctypes.c_uint16),
]

ATOM_Tonga_MCLK_Dependency_Record = struct__ATOM_Tonga_MCLK_Dependency_Record
class struct__ATOM_Tonga_MCLK_Dependency_Table(Structure):
    pass

struct__ATOM_Tonga_MCLK_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Tonga_MCLK_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Tonga_MCLK_Dependency_Record * 0),
]

ATOM_Tonga_MCLK_Dependency_Table = struct__ATOM_Tonga_MCLK_Dependency_Table
class struct__ATOM_Tonga_SCLK_Dependency_Record(Structure):
    pass

struct__ATOM_Tonga_SCLK_Dependency_Record._pack_ = 1 # source:False
struct__ATOM_Tonga_SCLK_Dependency_Record._fields_ = [
    ('ucVddInd', ctypes.c_ubyte),
    ('usVddcOffset', ctypes.c_uint16),
    ('ulSclk', ctypes.c_uint32),
    ('usEdcCurrent', ctypes.c_uint16),
    ('ucReliabilityTemperature', ctypes.c_ubyte),
    ('ucCKSVOffsetandDisable', ctypes.c_ubyte),
]

ATOM_Tonga_SCLK_Dependency_Record = struct__ATOM_Tonga_SCLK_Dependency_Record
class struct__ATOM_Tonga_SCLK_Dependency_Table(Structure):
    pass

struct__ATOM_Tonga_SCLK_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Tonga_SCLK_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Tonga_SCLK_Dependency_Record * 0),
]

ATOM_Tonga_SCLK_Dependency_Table = struct__ATOM_Tonga_SCLK_Dependency_Table
class struct__ATOM_Polaris_SCLK_Dependency_Record(Structure):
    pass

struct__ATOM_Polaris_SCLK_Dependency_Record._pack_ = 1 # source:False
struct__ATOM_Polaris_SCLK_Dependency_Record._fields_ = [
    ('ucVddInd', ctypes.c_ubyte),
    ('usVddcOffset', ctypes.c_uint16),
    ('ulSclk', ctypes.c_uint32),
    ('usEdcCurrent', ctypes.c_uint16),
    ('ucReliabilityTemperature', ctypes.c_ubyte),
    ('ucCKSVOffsetandDisable', ctypes.c_ubyte),
    ('ulSclkOffset', ctypes.c_uint32),
]

ATOM_Polaris_SCLK_Dependency_Record = struct__ATOM_Polaris_SCLK_Dependency_Record
class struct__ATOM_Polaris_SCLK_Dependency_Table(Structure):
    pass

struct__ATOM_Polaris_SCLK_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Polaris_SCLK_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Polaris_SCLK_Dependency_Record * 0),
]

ATOM_Polaris_SCLK_Dependency_Table = struct__ATOM_Polaris_SCLK_Dependency_Table
class struct__ATOM_Tonga_PCIE_Record(Structure):
    pass

struct__ATOM_Tonga_PCIE_Record._pack_ = 1 # source:False
struct__ATOM_Tonga_PCIE_Record._fields_ = [
    ('ucPCIEGenSpeed', ctypes.c_ubyte),
    ('usPCIELaneWidth', ctypes.c_ubyte),
    ('ucReserved', ctypes.c_ubyte * 2),
]

ATOM_Tonga_PCIE_Record = struct__ATOM_Tonga_PCIE_Record
class struct__ATOM_Tonga_PCIE_Table(Structure):
    pass

struct__ATOM_Tonga_PCIE_Table._pack_ = 1 # source:False
struct__ATOM_Tonga_PCIE_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Tonga_PCIE_Record * 0),
]

ATOM_Tonga_PCIE_Table = struct__ATOM_Tonga_PCIE_Table
class struct__ATOM_Polaris10_PCIE_Record(Structure):
    pass

struct__ATOM_Polaris10_PCIE_Record._pack_ = 1 # source:False
struct__ATOM_Polaris10_PCIE_Record._fields_ = [
    ('ucPCIEGenSpeed', ctypes.c_ubyte),
    ('usPCIELaneWidth', ctypes.c_ubyte),
    ('ucReserved', ctypes.c_ubyte * 2),
    ('ulPCIE_Sclk', ctypes.c_uint32),
]

ATOM_Polaris10_PCIE_Record = struct__ATOM_Polaris10_PCIE_Record
class struct__ATOM_Polaris10_PCIE_Table(Structure):
    pass

struct__ATOM_Polaris10_PCIE_Table._pack_ = 1 # source:False
struct__ATOM_Polaris10_PCIE_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Polaris10_PCIE_Record * 0),
]

ATOM_Polaris10_PCIE_Table = struct__ATOM_Polaris10_PCIE_Table
class struct__ATOM_Tonga_MM_Dependency_Record(Structure):
    pass

struct__ATOM_Tonga_MM_Dependency_Record._pack_ = 1 # source:False
struct__ATOM_Tonga_MM_Dependency_Record._fields_ = [
    ('ucVddcInd', ctypes.c_ubyte),
    ('usVddgfxOffset', ctypes.c_uint16),
    ('ulDClk', ctypes.c_uint32),
    ('ulVClk', ctypes.c_uint32),
    ('ulEClk', ctypes.c_uint32),
    ('ulAClk', ctypes.c_uint32),
    ('ulSAMUClk', ctypes.c_uint32),
]

ATOM_Tonga_MM_Dependency_Record = struct__ATOM_Tonga_MM_Dependency_Record
class struct__ATOM_Tonga_MM_Dependency_Table(Structure):
    pass

struct__ATOM_Tonga_MM_Dependency_Table._pack_ = 1 # source:False
struct__ATOM_Tonga_MM_Dependency_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Tonga_MM_Dependency_Record * 0),
]

ATOM_Tonga_MM_Dependency_Table = struct__ATOM_Tonga_MM_Dependency_Table
class struct__ATOM_Tonga_Voltage_Lookup_Record(Structure):
    pass

struct__ATOM_Tonga_Voltage_Lookup_Record._pack_ = 1 # source:False
struct__ATOM_Tonga_Voltage_Lookup_Record._fields_ = [
    ('usVdd', ctypes.c_uint16),
    ('usCACLow', ctypes.c_uint16),
    ('usCACMid', ctypes.c_uint16),
    ('usCACHigh', ctypes.c_uint16),
]

ATOM_Tonga_Voltage_Lookup_Record = struct__ATOM_Tonga_Voltage_Lookup_Record
class struct__ATOM_Tonga_Voltage_Lookup_Table(Structure):
    pass

struct__ATOM_Tonga_Voltage_Lookup_Table._pack_ = 1 # source:False
struct__ATOM_Tonga_Voltage_Lookup_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Tonga_Voltage_Lookup_Record * 0),
]

ATOM_Tonga_Voltage_Lookup_Table = struct__ATOM_Tonga_Voltage_Lookup_Table
class struct__ATOM_Tonga_Fan_Table(Structure):
    pass

struct__ATOM_Tonga_Fan_Table._pack_ = 1 # source:False
struct__ATOM_Tonga_Fan_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucTHyst', ctypes.c_ubyte),
    ('usTMin', ctypes.c_uint16),
    ('usTMed', ctypes.c_uint16),
    ('usTHigh', ctypes.c_uint16),
    ('usPWMMin', ctypes.c_uint16),
    ('usPWMMed', ctypes.c_uint16),
    ('usPWMHigh', ctypes.c_uint16),
    ('usTMax', ctypes.c_uint16),
    ('ucFanControlMode', ctypes.c_ubyte),
    ('usFanPWMMax', ctypes.c_uint16),
    ('usFanOutputSensitivity', ctypes.c_uint16),
    ('usFanRPMMax', ctypes.c_uint16),
    ('ulMinFanSCLKAcousticLimit', ctypes.c_uint32),
    ('ucTargetTemperature', ctypes.c_ubyte),
    ('ucMinimumPWMLimit', ctypes.c_ubyte),
    ('usReserved', ctypes.c_uint16),
]

ATOM_Tonga_Fan_Table = struct__ATOM_Tonga_Fan_Table
class struct__ATOM_Fiji_Fan_Table(Structure):
    pass

struct__ATOM_Fiji_Fan_Table._pack_ = 1 # source:False
struct__ATOM_Fiji_Fan_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucTHyst', ctypes.c_ubyte),
    ('usTMin', ctypes.c_uint16),
    ('usTMed', ctypes.c_uint16),
    ('usTHigh', ctypes.c_uint16),
    ('usPWMMin', ctypes.c_uint16),
    ('usPWMMed', ctypes.c_uint16),
    ('usPWMHigh', ctypes.c_uint16),
    ('usTMax', ctypes.c_uint16),
    ('ucFanControlMode', ctypes.c_ubyte),
    ('usFanPWMMax', ctypes.c_uint16),
    ('usFanOutputSensitivity', ctypes.c_uint16),
    ('usFanRPMMax', ctypes.c_uint16),
    ('ulMinFanSCLKAcousticLimit', ctypes.c_uint32),
    ('ucTargetTemperature', ctypes.c_ubyte),
    ('ucMinimumPWMLimit', ctypes.c_ubyte),
    ('usFanGainEdge', ctypes.c_uint16),
    ('usFanGainHotspot', ctypes.c_uint16),
    ('usFanGainLiquid', ctypes.c_uint16),
    ('usFanGainVrVddc', ctypes.c_uint16),
    ('usFanGainVrMvdd', ctypes.c_uint16),
    ('usFanGainPlx', ctypes.c_uint16),
    ('usFanGainHbm', ctypes.c_uint16),
    ('usReserved', ctypes.c_uint16),
]

ATOM_Fiji_Fan_Table = struct__ATOM_Fiji_Fan_Table
class struct__ATOM_Polaris_Fan_Table(Structure):
    pass

struct__ATOM_Polaris_Fan_Table._pack_ = 1 # source:False
struct__ATOM_Polaris_Fan_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucTHyst', ctypes.c_ubyte),
    ('usTMin', ctypes.c_uint16),
    ('usTMed', ctypes.c_uint16),
    ('usTHigh', ctypes.c_uint16),
    ('usPWMMin', ctypes.c_uint16),
    ('usPWMMed', ctypes.c_uint16),
    ('usPWMHigh', ctypes.c_uint16),
    ('usTMax', ctypes.c_uint16),
    ('ucFanControlMode', ctypes.c_ubyte),
    ('usFanPWMMax', ctypes.c_uint16),
    ('usFanOutputSensitivity', ctypes.c_uint16),
    ('usFanRPMMax', ctypes.c_uint16),
    ('ulMinFanSCLKAcousticLimit', ctypes.c_uint32),
    ('ucTargetTemperature', ctypes.c_ubyte),
    ('ucMinimumPWMLimit', ctypes.c_ubyte),
    ('usFanGainEdge', ctypes.c_uint16),
    ('usFanGainHotspot', ctypes.c_uint16),
    ('usFanGainLiquid', ctypes.c_uint16),
    ('usFanGainVrVddc', ctypes.c_uint16),
    ('usFanGainVrMvdd', ctypes.c_uint16),
    ('usFanGainPlx', ctypes.c_uint16),
    ('usFanGainHbm', ctypes.c_uint16),
    ('ucEnableZeroRPM', ctypes.c_ubyte),
    ('ucFanStopTemperature', ctypes.c_ubyte),
    ('ucFanStartTemperature', ctypes.c_ubyte),
    ('usReserved', ctypes.c_uint16),
]

ATOM_Polaris_Fan_Table = struct__ATOM_Polaris_Fan_Table
class struct__ATOM_Tonga_Thermal_Controller(Structure):
    pass

struct__ATOM_Tonga_Thermal_Controller._pack_ = 1 # source:False
struct__ATOM_Tonga_Thermal_Controller._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucType', ctypes.c_ubyte),
    ('ucI2cLine', ctypes.c_ubyte),
    ('ucI2cAddress', ctypes.c_ubyte),
    ('ucFanParameters', ctypes.c_ubyte),
    ('ucFanMinRPM', ctypes.c_ubyte),
    ('ucFanMaxRPM', ctypes.c_ubyte),
    ('ucReserved', ctypes.c_ubyte),
    ('ucFlags', ctypes.c_ubyte),
]

ATOM_Tonga_Thermal_Controller = struct__ATOM_Tonga_Thermal_Controller
class struct__ATOM_Tonga_VCE_State_Record(Structure):
    pass

struct__ATOM_Tonga_VCE_State_Record._pack_ = 1 # source:False
struct__ATOM_Tonga_VCE_State_Record._fields_ = [
    ('ucVCEClockIndex', ctypes.c_ubyte),
    ('ucFlag', ctypes.c_ubyte),
    ('ucSCLKIndex', ctypes.c_ubyte),
    ('ucMCLKIndex', ctypes.c_ubyte),
]

ATOM_Tonga_VCE_State_Record = struct__ATOM_Tonga_VCE_State_Record
class struct__ATOM_Tonga_VCE_State_Table(Structure):
    pass

struct__ATOM_Tonga_VCE_State_Table._pack_ = 1 # source:False
struct__ATOM_Tonga_VCE_State_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Tonga_VCE_State_Record * 0),
]

ATOM_Tonga_VCE_State_Table = struct__ATOM_Tonga_VCE_State_Table
class struct__ATOM_Tonga_PowerTune_Table(Structure):
    pass

struct__ATOM_Tonga_PowerTune_Table._pack_ = 1 # source:False
struct__ATOM_Tonga_PowerTune_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('usTDP', ctypes.c_uint16),
    ('usConfigurableTDP', ctypes.c_uint16),
    ('usTDC', ctypes.c_uint16),
    ('usBatteryPowerLimit', ctypes.c_uint16),
    ('usSmallPowerLimit', ctypes.c_uint16),
    ('usLowCACLeakage', ctypes.c_uint16),
    ('usHighCACLeakage', ctypes.c_uint16),
    ('usMaximumPowerDeliveryLimit', ctypes.c_uint16),
    ('usTjMax', ctypes.c_uint16),
    ('usPowerTuneDataSetID', ctypes.c_uint16),
    ('usEDCLimit', ctypes.c_uint16),
    ('usSoftwareShutdownTemp', ctypes.c_uint16),
    ('usClockStretchAmount', ctypes.c_uint16),
    ('usReserve', ctypes.c_uint16 * 2),
]

ATOM_Tonga_PowerTune_Table = struct__ATOM_Tonga_PowerTune_Table
class struct__ATOM_Fiji_PowerTune_Table(Structure):
    pass

struct__ATOM_Fiji_PowerTune_Table._pack_ = 1 # source:False
struct__ATOM_Fiji_PowerTune_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('usTDP', ctypes.c_uint16),
    ('usConfigurableTDP', ctypes.c_uint16),
    ('usTDC', ctypes.c_uint16),
    ('usBatteryPowerLimit', ctypes.c_uint16),
    ('usSmallPowerLimit', ctypes.c_uint16),
    ('usLowCACLeakage', ctypes.c_uint16),
    ('usHighCACLeakage', ctypes.c_uint16),
    ('usMaximumPowerDeliveryLimit', ctypes.c_uint16),
    ('usTjMax', ctypes.c_uint16),
    ('usPowerTuneDataSetID', ctypes.c_uint16),
    ('usEDCLimit', ctypes.c_uint16),
    ('usSoftwareShutdownTemp', ctypes.c_uint16),
    ('usClockStretchAmount', ctypes.c_uint16),
    ('usTemperatureLimitHotspot', ctypes.c_uint16),
    ('usTemperatureLimitLiquid1', ctypes.c_uint16),
    ('usTemperatureLimitLiquid2', ctypes.c_uint16),
    ('usTemperatureLimitVrVddc', ctypes.c_uint16),
    ('usTemperatureLimitVrMvdd', ctypes.c_uint16),
    ('usTemperatureLimitPlx', ctypes.c_uint16),
    ('ucLiquid1_I2C_address', ctypes.c_ubyte),
    ('ucLiquid2_I2C_address', ctypes.c_ubyte),
    ('ucLiquid_I2C_Line', ctypes.c_ubyte),
    ('ucVr_I2C_address', ctypes.c_ubyte),
    ('ucVr_I2C_Line', ctypes.c_ubyte),
    ('ucPlx_I2C_address', ctypes.c_ubyte),
    ('ucPlx_I2C_Line', ctypes.c_ubyte),
    ('usReserved', ctypes.c_uint16),
]

ATOM_Fiji_PowerTune_Table = struct__ATOM_Fiji_PowerTune_Table
class struct__ATOM_Polaris_PowerTune_Table(Structure):
    pass

struct__ATOM_Polaris_PowerTune_Table._pack_ = 1 # source:False
struct__ATOM_Polaris_PowerTune_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('usTDP', ctypes.c_uint16),
    ('usConfigurableTDP', ctypes.c_uint16),
    ('usTDC', ctypes.c_uint16),
    ('usBatteryPowerLimit', ctypes.c_uint16),
    ('usSmallPowerLimit', ctypes.c_uint16),
    ('usLowCACLeakage', ctypes.c_uint16),
    ('usHighCACLeakage', ctypes.c_uint16),
    ('usMaximumPowerDeliveryLimit', ctypes.c_uint16),
    ('usTjMax', ctypes.c_uint16),
    ('usPowerTuneDataSetID', ctypes.c_uint16),
    ('usEDCLimit', ctypes.c_uint16),
    ('usSoftwareShutdownTemp', ctypes.c_uint16),
    ('usClockStretchAmount', ctypes.c_uint16),
    ('usTemperatureLimitHotspot', ctypes.c_uint16),
    ('usTemperatureLimitLiquid1', ctypes.c_uint16),
    ('usTemperatureLimitLiquid2', ctypes.c_uint16),
    ('usTemperatureLimitVrVddc', ctypes.c_uint16),
    ('usTemperatureLimitVrMvdd', ctypes.c_uint16),
    ('usTemperatureLimitPlx', ctypes.c_uint16),
    ('ucLiquid1_I2C_address', ctypes.c_ubyte),
    ('ucLiquid2_I2C_address', ctypes.c_ubyte),
    ('ucLiquid_I2C_Line', ctypes.c_ubyte),
    ('ucVr_I2C_address', ctypes.c_ubyte),
    ('ucVr_I2C_Line', ctypes.c_ubyte),
    ('ucPlx_I2C_address', ctypes.c_ubyte),
    ('ucPlx_I2C_Line', ctypes.c_ubyte),
    ('usBoostPowerLimit', ctypes.c_uint16),
    ('ucCKS_LDO_REFSEL', ctypes.c_ubyte),
    ('ucHotSpotOnly', ctypes.c_ubyte),
    ('ucReserve', ctypes.c_ubyte),
    ('usReserve', ctypes.c_uint16),
]

ATOM_Polaris_PowerTune_Table = struct__ATOM_Polaris_PowerTune_Table
class struct__ATOM_Tonga_PPM_Table(Structure):
    pass

struct__ATOM_Tonga_PPM_Table._pack_ = 1 # source:False
struct__ATOM_Tonga_PPM_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucPpmDesign', ctypes.c_ubyte),
    ('usCpuCoreNumber', ctypes.c_uint16),
    ('ulPlatformTDP', ctypes.c_uint32),
    ('ulSmallACPlatformTDP', ctypes.c_uint32),
    ('ulPlatformTDC', ctypes.c_uint32),
    ('ulSmallACPlatformTDC', ctypes.c_uint32),
    ('ulApuTDP', ctypes.c_uint32),
    ('ulDGpuTDP', ctypes.c_uint32),
    ('ulDGpuUlvPower', ctypes.c_uint32),
    ('ulTjmax', ctypes.c_uint32),
]

ATOM_Tonga_PPM_Table = struct__ATOM_Tonga_PPM_Table
class struct__ATOM_Tonga_Hard_Limit_Record(Structure):
    pass

struct__ATOM_Tonga_Hard_Limit_Record._pack_ = 1 # source:False
struct__ATOM_Tonga_Hard_Limit_Record._fields_ = [
    ('ulSCLKLimit', ctypes.c_uint32),
    ('ulMCLKLimit', ctypes.c_uint32),
    ('usVddcLimit', ctypes.c_uint16),
    ('usVddciLimit', ctypes.c_uint16),
    ('usVddgfxLimit', ctypes.c_uint16),
]

ATOM_Tonga_Hard_Limit_Record = struct__ATOM_Tonga_Hard_Limit_Record
class struct__ATOM_Tonga_Hard_Limit_Table(Structure):
    pass

struct__ATOM_Tonga_Hard_Limit_Table._pack_ = 1 # source:False
struct__ATOM_Tonga_Hard_Limit_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucNumEntries', ctypes.c_ubyte),
    ('entries', struct__ATOM_Tonga_Hard_Limit_Record * 0),
]

ATOM_Tonga_Hard_Limit_Table = struct__ATOM_Tonga_Hard_Limit_Table
class struct__ATOM_Tonga_GPIO_Table(Structure):
    pass

struct__ATOM_Tonga_GPIO_Table._pack_ = 1 # source:False
struct__ATOM_Tonga_GPIO_Table._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
    ('ucVRHotTriggeredSclkDpmIndex', ctypes.c_ubyte),
    ('ucReserve', ctypes.c_ubyte * 5),
]

ATOM_Tonga_GPIO_Table = struct__ATOM_Tonga_GPIO_Table
class struct__PPTable_Generic_SubTable_Header(Structure):
    pass

struct__PPTable_Generic_SubTable_Header._pack_ = 1 # source:False
struct__PPTable_Generic_SubTable_Header._fields_ = [
    ('ucRevId', ctypes.c_ubyte),
]

PPTable_Generic_SubTable_Header = struct__PPTable_Generic_SubTable_Header
__all__ = \
    ['ATOM_Fiji_Fan_Table', 'ATOM_Fiji_PowerTune_Table',
    'ATOM_PPLIB_CLASSIFICATION2_LIMITEDPOWERSOURCE_2',
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
    'ATOM_PPLIB_CLASSIFICATION_UI_SHIFT', 'ATOM_PPM_A_A',
    'ATOM_PPM_A_I', 'ATOM_Polaris10_PCIE_Record',
    'ATOM_Polaris10_PCIE_Table', 'ATOM_Polaris_Fan_Table',
    'ATOM_Polaris_PowerTune_Table',
    'ATOM_Polaris_SCLK_Dependency_Record',
    'ATOM_Polaris_SCLK_Dependency_Table',
    'ATOM_TONGA_PLATFORM_LOAD_POST_PRODUCTION_FIRMWARE',
    'ATOM_TONGA_PP_FANPARAMETERS_NOFAN',
    'ATOM_TONGA_PP_FANPARAMETERS_TACHOMETER_PULSES_PER_REVOLUTION_MASK',
    'ATOM_TONGA_PP_PLATFORM_CAP_BACO',
    'ATOM_TONGA_PP_PLATFORM_CAP_DISABLE_VOLTAGE_ISLAND',
    'ATOM_TONGA_PP_PLATFORM_CAP_HARDWAREDC',
    'ATOM_TONGA_PP_PLATFORM_CAP_MVDD_CONTROL',
    'ATOM_TONGA_PP_PLATFORM_CAP_OUTPUT_THERMAL2GPIO17',
    'ATOM_TONGA_PP_PLATFORM_CAP_POWERPLAY',
    'ATOM_TONGA_PP_PLATFORM_CAP_SBIOSPOWERSOURCE',
    'ATOM_TONGA_PP_PLATFORM_CAP_VDDCI_CONTROL',
    'ATOM_TONGA_PP_PLATFORM_CAP_VDDGFX_CONTROL',
    'ATOM_TONGA_PP_PLATFORM_COMBINE_PCC_WITH_THERMAL_SIGNAL',
    'ATOM_TONGA_PP_THERMALCONTROLLER_ADT7473_WITH_INTERNAL',
    'ATOM_TONGA_PP_THERMALCONTROLLER_EMC2103_WITH_INTERNAL',
    'ATOM_TONGA_PP_THERMALCONTROLLER_FIJI',
    'ATOM_TONGA_PP_THERMALCONTROLLER_LM96163',
    'ATOM_TONGA_PP_THERMALCONTROLLER_NONE',
    'ATOM_TONGA_PP_THERMALCONTROLLER_TONGA',
    'ATOM_Tonga_DISALLOW_ON_DC', 'ATOM_Tonga_ENABLE_VARIBRIGHT',
    'ATOM_Tonga_Fan_Table', 'ATOM_Tonga_GPIO_Table',
    'ATOM_Tonga_Hard_Limit_Record', 'ATOM_Tonga_Hard_Limit_Table',
    'ATOM_Tonga_MCLK_Dependency_Record',
    'ATOM_Tonga_MCLK_Dependency_Table',
    'ATOM_Tonga_MM_Dependency_Record',
    'ATOM_Tonga_MM_Dependency_Table', 'ATOM_Tonga_PCIE_Record',
    'ATOM_Tonga_PCIE_Table', 'ATOM_Tonga_POWERPLAYTABLE',
    'ATOM_Tonga_PPM_Table', 'ATOM_Tonga_PowerTune_Table',
    'ATOM_Tonga_SCLK_Dependency_Record',
    'ATOM_Tonga_SCLK_Dependency_Table', 'ATOM_Tonga_State',
    'ATOM_Tonga_State_Array', 'ATOM_Tonga_TABLE_REVISION_TONGA',
    'ATOM_Tonga_Thermal_Controller', 'ATOM_Tonga_VCE_State_Record',
    'ATOM_Tonga_VCE_State_Table', 'ATOM_Tonga_Voltage_Lookup_Record',
    'ATOM_Tonga_Voltage_Lookup_Table',
    'PPTable_Generic_SubTable_Header', 'TONGA_PPTABLE_H',
    '____RETIRE10000____', '____RETIRE1024____', '____RETIRE128____',
    '____RETIRE16____', '____RETIRE2000____', '____RETIRE2048____',
    '____RETIRE256____', '____RETIRE4000____', '____RETIRE512____',
    '____RETIRE64____', 'struct__ATOM_COMMON_TABLE_HEADER',
    'struct__ATOM_Fiji_Fan_Table',
    'struct__ATOM_Fiji_PowerTune_Table',
    'struct__ATOM_Polaris10_PCIE_Record',
    'struct__ATOM_Polaris10_PCIE_Table',
    'struct__ATOM_Polaris_Fan_Table',
    'struct__ATOM_Polaris_PowerTune_Table',
    'struct__ATOM_Polaris_SCLK_Dependency_Record',
    'struct__ATOM_Polaris_SCLK_Dependency_Table',
    'struct__ATOM_Tonga_Fan_Table', 'struct__ATOM_Tonga_GPIO_Table',
    'struct__ATOM_Tonga_Hard_Limit_Record',
    'struct__ATOM_Tonga_Hard_Limit_Table',
    'struct__ATOM_Tonga_MCLK_Dependency_Record',
    'struct__ATOM_Tonga_MCLK_Dependency_Table',
    'struct__ATOM_Tonga_MM_Dependency_Record',
    'struct__ATOM_Tonga_MM_Dependency_Table',
    'struct__ATOM_Tonga_PCIE_Record', 'struct__ATOM_Tonga_PCIE_Table',
    'struct__ATOM_Tonga_POWERPLAYTABLE',
    'struct__ATOM_Tonga_PPM_Table',
    'struct__ATOM_Tonga_PowerTune_Table',
    'struct__ATOM_Tonga_SCLK_Dependency_Record',
    'struct__ATOM_Tonga_SCLK_Dependency_Table',
    'struct__ATOM_Tonga_State', 'struct__ATOM_Tonga_State_Array',
    'struct__ATOM_Tonga_Thermal_Controller',
    'struct__ATOM_Tonga_VCE_State_Record',
    'struct__ATOM_Tonga_VCE_State_Table',
    'struct__ATOM_Tonga_Voltage_Lookup_Record',
    'struct__ATOM_Tonga_Voltage_Lookup_Table',
    'struct__PPTable_Generic_SubTable_Header']
