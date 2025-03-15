# -*- coding: utf-8 -*-
#
# TARGET arch is: ['--include', 'stdint.h', '--include', 'linux/drivers/gpu/drm/amd/include/atom-types.h', '--include', 'linux/drivers/gpu/drm/amd/include/atomfirmware.h', '--include', 'linux/drivers/gpu/drm/amd/pm/powerplay/inc/smu11_driver_if.h', '']
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
                type_ = type_._type_
                if hasattr(type_, 'as_dict'):
                    value = [type_.as_dict(v) for v in value]
                else:
                    value = [i for i in value]
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





_VEGA20_PPTABLE_H_ = True # macro
ATOM_VEGA20_PP_THERMALCONTROLLER_NONE = 0 # macro
ATOM_VEGA20_PP_THERMALCONTROLLER_VEGA20 = 26 # macro
ATOM_VEGA20_PP_PLATFORM_CAP_POWERPLAY = 0x1 # macro
ATOM_VEGA20_PP_PLATFORM_CAP_SBIOSPOWERSOURCE = 0x2 # macro
ATOM_VEGA20_PP_PLATFORM_CAP_HARDWAREDC = 0x4 # macro
ATOM_VEGA20_PP_PLATFORM_CAP_BACO = 0x8 # macro
ATOM_VEGA20_PP_PLATFORM_CAP_BAMACO = 0x10 # macro
ATOM_VEGA20_PP_PLATFORM_CAP_ENABLESHADOWPSTATE = 0x20 # macro
ATOM_VEGA20_TABLE_REVISION_VEGA20 = 11 # macro
ATOM_VEGA20_ODFEATURE_MAX_COUNT = 32 # macro
ATOM_VEGA20_ODSETTING_MAX_COUNT = 32 # macro
ATOM_VEGA20_PPCLOCK_MAX_COUNT = 16 # macro

# values for enumeration 'ATOM_VEGA20_ODFEATURE_ID'
ATOM_VEGA20_ODFEATURE_ID__enumvalues = {
    0: 'ATOM_VEGA20_ODFEATURE_GFXCLK_LIMITS',
    1: 'ATOM_VEGA20_ODFEATURE_GFXCLK_CURVE',
    2: 'ATOM_VEGA20_ODFEATURE_UCLK_MAX',
    3: 'ATOM_VEGA20_ODFEATURE_POWER_LIMIT',
    4: 'ATOM_VEGA20_ODFEATURE_FAN_ACOUSTIC_LIMIT',
    5: 'ATOM_VEGA20_ODFEATURE_FAN_SPEED_MIN',
    6: 'ATOM_VEGA20_ODFEATURE_TEMPERATURE_FAN',
    7: 'ATOM_VEGA20_ODFEATURE_TEMPERATURE_SYSTEM',
    8: 'ATOM_VEGA20_ODFEATURE_MEMORY_TIMING_TUNE',
    9: 'ATOM_VEGA20_ODFEATURE_FAN_ZERO_RPM_CONTROL',
    10: 'ATOM_VEGA20_ODFEATURE_COUNT',
}
ATOM_VEGA20_ODFEATURE_GFXCLK_LIMITS = 0
ATOM_VEGA20_ODFEATURE_GFXCLK_CURVE = 1
ATOM_VEGA20_ODFEATURE_UCLK_MAX = 2
ATOM_VEGA20_ODFEATURE_POWER_LIMIT = 3
ATOM_VEGA20_ODFEATURE_FAN_ACOUSTIC_LIMIT = 4
ATOM_VEGA20_ODFEATURE_FAN_SPEED_MIN = 5
ATOM_VEGA20_ODFEATURE_TEMPERATURE_FAN = 6
ATOM_VEGA20_ODFEATURE_TEMPERATURE_SYSTEM = 7
ATOM_VEGA20_ODFEATURE_MEMORY_TIMING_TUNE = 8
ATOM_VEGA20_ODFEATURE_FAN_ZERO_RPM_CONTROL = 9
ATOM_VEGA20_ODFEATURE_COUNT = 10
ATOM_VEGA20_ODFEATURE_ID = ctypes.c_uint32 # enum

# values for enumeration 'ATOM_VEGA20_ODSETTING_ID'
ATOM_VEGA20_ODSETTING_ID__enumvalues = {
    0: 'ATOM_VEGA20_ODSETTING_GFXCLKFMAX',
    1: 'ATOM_VEGA20_ODSETTING_GFXCLKFMIN',
    2: 'ATOM_VEGA20_ODSETTING_VDDGFXCURVEFREQ_P1',
    3: 'ATOM_VEGA20_ODSETTING_VDDGFXCURVEVOLTAGEOFFSET_P1',
    4: 'ATOM_VEGA20_ODSETTING_VDDGFXCURVEFREQ_P2',
    5: 'ATOM_VEGA20_ODSETTING_VDDGFXCURVEVOLTAGEOFFSET_P2',
    6: 'ATOM_VEGA20_ODSETTING_VDDGFXCURVEFREQ_P3',
    7: 'ATOM_VEGA20_ODSETTING_VDDGFXCURVEVOLTAGEOFFSET_P3',
    8: 'ATOM_VEGA20_ODSETTING_UCLKFMAX',
    9: 'ATOM_VEGA20_ODSETTING_POWERPERCENTAGE',
    10: 'ATOM_VEGA20_ODSETTING_FANRPMMIN',
    11: 'ATOM_VEGA20_ODSETTING_FANRPMACOUSTICLIMIT',
    12: 'ATOM_VEGA20_ODSETTING_FANTARGETTEMPERATURE',
    13: 'ATOM_VEGA20_ODSETTING_OPERATINGTEMPMAX',
    14: 'ATOM_VEGA20_ODSETTING_COUNT',
}
ATOM_VEGA20_ODSETTING_GFXCLKFMAX = 0
ATOM_VEGA20_ODSETTING_GFXCLKFMIN = 1
ATOM_VEGA20_ODSETTING_VDDGFXCURVEFREQ_P1 = 2
ATOM_VEGA20_ODSETTING_VDDGFXCURVEVOLTAGEOFFSET_P1 = 3
ATOM_VEGA20_ODSETTING_VDDGFXCURVEFREQ_P2 = 4
ATOM_VEGA20_ODSETTING_VDDGFXCURVEVOLTAGEOFFSET_P2 = 5
ATOM_VEGA20_ODSETTING_VDDGFXCURVEFREQ_P3 = 6
ATOM_VEGA20_ODSETTING_VDDGFXCURVEVOLTAGEOFFSET_P3 = 7
ATOM_VEGA20_ODSETTING_UCLKFMAX = 8
ATOM_VEGA20_ODSETTING_POWERPERCENTAGE = 9
ATOM_VEGA20_ODSETTING_FANRPMMIN = 10
ATOM_VEGA20_ODSETTING_FANRPMACOUSTICLIMIT = 11
ATOM_VEGA20_ODSETTING_FANTARGETTEMPERATURE = 12
ATOM_VEGA20_ODSETTING_OPERATINGTEMPMAX = 13
ATOM_VEGA20_ODSETTING_COUNT = 14
ATOM_VEGA20_ODSETTING_ID = ctypes.c_uint32 # enum
class struct__ATOM_VEGA20_OVERDRIVE8_RECORD(Structure):
    pass

struct__ATOM_VEGA20_OVERDRIVE8_RECORD._pack_ = 1 # source:False
struct__ATOM_VEGA20_OVERDRIVE8_RECORD._fields_ = [
    ('ucODTableRevision', ctypes.c_ubyte),
    ('ODFeatureCount', ctypes.c_uint32),
    ('ODFeatureCapabilities', ctypes.c_ubyte * 32),
    ('ODSettingCount', ctypes.c_uint32),
    ('ODSettingsMax', ctypes.c_uint32 * 32),
    ('ODSettingsMin', ctypes.c_uint32 * 32),
]

ATOM_VEGA20_OVERDRIVE8_RECORD = struct__ATOM_VEGA20_OVERDRIVE8_RECORD

# values for enumeration 'ATOM_VEGA20_PPCLOCK_ID'
ATOM_VEGA20_PPCLOCK_ID__enumvalues = {
    0: 'ATOM_VEGA20_PPCLOCK_GFXCLK',
    1: 'ATOM_VEGA20_PPCLOCK_VCLK',
    2: 'ATOM_VEGA20_PPCLOCK_DCLK',
    3: 'ATOM_VEGA20_PPCLOCK_ECLK',
    4: 'ATOM_VEGA20_PPCLOCK_SOCCLK',
    5: 'ATOM_VEGA20_PPCLOCK_UCLK',
    6: 'ATOM_VEGA20_PPCLOCK_FCLK',
    7: 'ATOM_VEGA20_PPCLOCK_DCEFCLK',
    8: 'ATOM_VEGA20_PPCLOCK_DISPCLK',
    9: 'ATOM_VEGA20_PPCLOCK_PIXCLK',
    10: 'ATOM_VEGA20_PPCLOCK_PHYCLK',
    11: 'ATOM_VEGA20_PPCLOCK_COUNT',
}
ATOM_VEGA20_PPCLOCK_GFXCLK = 0
ATOM_VEGA20_PPCLOCK_VCLK = 1
ATOM_VEGA20_PPCLOCK_DCLK = 2
ATOM_VEGA20_PPCLOCK_ECLK = 3
ATOM_VEGA20_PPCLOCK_SOCCLK = 4
ATOM_VEGA20_PPCLOCK_UCLK = 5
ATOM_VEGA20_PPCLOCK_FCLK = 6
ATOM_VEGA20_PPCLOCK_DCEFCLK = 7
ATOM_VEGA20_PPCLOCK_DISPCLK = 8
ATOM_VEGA20_PPCLOCK_PIXCLK = 9
ATOM_VEGA20_PPCLOCK_PHYCLK = 10
ATOM_VEGA20_PPCLOCK_COUNT = 11
ATOM_VEGA20_PPCLOCK_ID = ctypes.c_uint32 # enum
class struct__ATOM_VEGA20_POWER_SAVING_CLOCK_RECORD(Structure):
    pass

struct__ATOM_VEGA20_POWER_SAVING_CLOCK_RECORD._pack_ = 1 # source:False
struct__ATOM_VEGA20_POWER_SAVING_CLOCK_RECORD._fields_ = [
    ('ucTableRevision', ctypes.c_ubyte),
    ('PowerSavingClockCount', ctypes.c_uint32),
    ('PowerSavingClockMax', ctypes.c_uint32 * 16),
    ('PowerSavingClockMin', ctypes.c_uint32 * 16),
]

ATOM_VEGA20_POWER_SAVING_CLOCK_RECORD = struct__ATOM_VEGA20_POWER_SAVING_CLOCK_RECORD
class struct__ATOM_VEGA20_POWERPLAYTABLE(Structure):
    pass

class struct_atom_common_table_header(Structure):
    pass

struct_atom_common_table_header._pack_ = 1 # source:False
struct_atom_common_table_header._fields_ = [
    ('structuresize', ctypes.c_uint16),
    ('format_revision', ctypes.c_ubyte),
    ('content_revision', ctypes.c_ubyte),
]

class struct_PPTable_t(Structure):
    pass

class struct_DpmDescriptor_t(Structure):
    pass

class struct_LinearInt_t(Structure):
    pass

struct_LinearInt_t._pack_ = 1 # source:False
struct_LinearInt_t._fields_ = [
    ('m', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
]

class struct_QuadraticInt_t(Structure):
    pass

struct_QuadraticInt_t._pack_ = 1 # source:False
struct_QuadraticInt_t._fields_ = [
    ('a', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
    ('c', ctypes.c_uint32),
]

struct_DpmDescriptor_t._pack_ = 1 # source:False
struct_DpmDescriptor_t._fields_ = [
    ('VoltageMode', ctypes.c_ubyte),
    ('SnapToDiscrete', ctypes.c_ubyte),
    ('NumDiscreteLevels', ctypes.c_ubyte),
    ('padding', ctypes.c_ubyte),
    ('ConversionToAvfsClk', struct_LinearInt_t),
    ('SsCurve', struct_QuadraticInt_t),
]

class struct_DroopInt_t(Structure):
    pass

struct_DroopInt_t._pack_ = 1 # source:False
struct_DroopInt_t._fields_ = [
    ('a', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
    ('c', ctypes.c_uint32),
]

class struct_I2cControllerConfig_t(Structure):
    pass

struct_I2cControllerConfig_t._pack_ = 1 # source:False
struct_I2cControllerConfig_t._fields_ = [
    ('Enabled', ctypes.c_uint32),
    ('SlaveAddress', ctypes.c_uint32),
    ('ControllerPort', ctypes.c_uint32),
    ('ControllerName', ctypes.c_uint32),
    ('ThermalThrottler', ctypes.c_uint32),
    ('I2cProtocol', ctypes.c_uint32),
    ('I2cSpeed', ctypes.c_uint32),
]

struct_PPTable_t._pack_ = 1 # source:False
struct_PPTable_t._fields_ = [
    ('Version', ctypes.c_uint32),
    ('FeaturesToRun', ctypes.c_uint32 * 2),
    ('SocketPowerLimitAc0', ctypes.c_uint16),
    ('SocketPowerLimitAc0Tau', ctypes.c_uint16),
    ('SocketPowerLimitAc1', ctypes.c_uint16),
    ('SocketPowerLimitAc1Tau', ctypes.c_uint16),
    ('SocketPowerLimitAc2', ctypes.c_uint16),
    ('SocketPowerLimitAc2Tau', ctypes.c_uint16),
    ('SocketPowerLimitAc3', ctypes.c_uint16),
    ('SocketPowerLimitAc3Tau', ctypes.c_uint16),
    ('SocketPowerLimitDc', ctypes.c_uint16),
    ('SocketPowerLimitDcTau', ctypes.c_uint16),
    ('TdcLimitSoc', ctypes.c_uint16),
    ('TdcLimitSocTau', ctypes.c_uint16),
    ('TdcLimitGfx', ctypes.c_uint16),
    ('TdcLimitGfxTau', ctypes.c_uint16),
    ('TedgeLimit', ctypes.c_uint16),
    ('ThotspotLimit', ctypes.c_uint16),
    ('ThbmLimit', ctypes.c_uint16),
    ('Tvr_gfxLimit', ctypes.c_uint16),
    ('Tvr_memLimit', ctypes.c_uint16),
    ('Tliquid1Limit', ctypes.c_uint16),
    ('Tliquid2Limit', ctypes.c_uint16),
    ('TplxLimit', ctypes.c_uint16),
    ('FitLimit', ctypes.c_uint32),
    ('PpmPowerLimit', ctypes.c_uint16),
    ('PpmTemperatureThreshold', ctypes.c_uint16),
    ('MemoryOnPackage', ctypes.c_ubyte),
    ('padding8_limits', ctypes.c_ubyte),
    ('Tvr_SocLimit', ctypes.c_uint16),
    ('UlvVoltageOffsetSoc', ctypes.c_uint16),
    ('UlvVoltageOffsetGfx', ctypes.c_uint16),
    ('UlvSmnclkDid', ctypes.c_ubyte),
    ('UlvMp1clkDid', ctypes.c_ubyte),
    ('UlvGfxclkBypass', ctypes.c_ubyte),
    ('Padding234', ctypes.c_ubyte),
    ('MinVoltageGfx', ctypes.c_uint16),
    ('MinVoltageSoc', ctypes.c_uint16),
    ('MaxVoltageGfx', ctypes.c_uint16),
    ('MaxVoltageSoc', ctypes.c_uint16),
    ('LoadLineResistanceGfx', ctypes.c_uint16),
    ('LoadLineResistanceSoc', ctypes.c_uint16),
    ('DpmDescriptor', struct_DpmDescriptor_t * 11),
    ('FreqTableGfx', ctypes.c_uint16 * 16),
    ('FreqTableVclk', ctypes.c_uint16 * 8),
    ('FreqTableDclk', ctypes.c_uint16 * 8),
    ('FreqTableEclk', ctypes.c_uint16 * 8),
    ('FreqTableSocclk', ctypes.c_uint16 * 8),
    ('FreqTableUclk', ctypes.c_uint16 * 4),
    ('FreqTableFclk', ctypes.c_uint16 * 8),
    ('FreqTableDcefclk', ctypes.c_uint16 * 8),
    ('FreqTableDispclk', ctypes.c_uint16 * 8),
    ('FreqTablePixclk', ctypes.c_uint16 * 8),
    ('FreqTablePhyclk', ctypes.c_uint16 * 8),
    ('DcModeMaxFreq', ctypes.c_uint16 * 11),
    ('Padding8_Clks', ctypes.c_uint16),
    ('Mp0clkFreq', ctypes.c_uint16 * 2),
    ('Mp0DpmVoltage', ctypes.c_uint16 * 2),
    ('GfxclkFidle', ctypes.c_uint16),
    ('GfxclkSlewRate', ctypes.c_uint16),
    ('CksEnableFreq', ctypes.c_uint16),
    ('Padding789', ctypes.c_uint16),
    ('CksVoltageOffset', struct_QuadraticInt_t),
    ('Padding567', ctypes.c_ubyte * 4),
    ('GfxclkDsMaxFreq', ctypes.c_uint16),
    ('GfxclkSource', ctypes.c_ubyte),
    ('Padding456', ctypes.c_ubyte),
    ('LowestUclkReservedForUlv', ctypes.c_ubyte),
    ('Padding8_Uclk', ctypes.c_ubyte * 3),
    ('PcieGenSpeed', ctypes.c_ubyte * 2),
    ('PcieLaneCount', ctypes.c_ubyte * 2),
    ('LclkFreq', ctypes.c_uint16 * 2),
    ('EnableTdpm', ctypes.c_uint16),
    ('TdpmHighHystTemperature', ctypes.c_uint16),
    ('TdpmLowHystTemperature', ctypes.c_uint16),
    ('GfxclkFreqHighTempLimit', ctypes.c_uint16),
    ('FanStopTemp', ctypes.c_uint16),
    ('FanStartTemp', ctypes.c_uint16),
    ('FanGainEdge', ctypes.c_uint16),
    ('FanGainHotspot', ctypes.c_uint16),
    ('FanGainLiquid', ctypes.c_uint16),
    ('FanGainVrGfx', ctypes.c_uint16),
    ('FanGainVrSoc', ctypes.c_uint16),
    ('FanGainPlx', ctypes.c_uint16),
    ('FanGainHbm', ctypes.c_uint16),
    ('FanPwmMin', ctypes.c_uint16),
    ('FanAcousticLimitRpm', ctypes.c_uint16),
    ('FanThrottlingRpm', ctypes.c_uint16),
    ('FanMaximumRpm', ctypes.c_uint16),
    ('FanTargetTemperature', ctypes.c_uint16),
    ('FanTargetGfxclk', ctypes.c_uint16),
    ('FanZeroRpmEnable', ctypes.c_ubyte),
    ('FanTachEdgePerRev', ctypes.c_ubyte),
    ('FuzzyFan_ErrorSetDelta', ctypes.c_int16),
    ('FuzzyFan_ErrorRateSetDelta', ctypes.c_int16),
    ('FuzzyFan_PwmSetDelta', ctypes.c_int16),
    ('FuzzyFan_Reserved', ctypes.c_uint16),
    ('OverrideAvfsGb', ctypes.c_ubyte * 2),
    ('Padding8_Avfs', ctypes.c_ubyte * 2),
    ('qAvfsGb', struct_QuadraticInt_t * 2),
    ('dBtcGbGfxCksOn', struct_DroopInt_t),
    ('dBtcGbGfxCksOff', struct_DroopInt_t),
    ('dBtcGbGfxAfll', struct_DroopInt_t),
    ('dBtcGbSoc', struct_DroopInt_t),
    ('qAgingGb', struct_LinearInt_t * 2),
    ('qStaticVoltageOffset', struct_QuadraticInt_t * 2),
    ('DcTol', ctypes.c_uint16 * 2),
    ('DcBtcEnabled', ctypes.c_ubyte * 2),
    ('Padding8_GfxBtc', ctypes.c_ubyte * 2),
    ('DcBtcMin', ctypes.c_int16 * 2),
    ('DcBtcMax', ctypes.c_uint16 * 2),
    ('XgmiLinkSpeed', ctypes.c_ubyte * 2),
    ('XgmiLinkWidth', ctypes.c_ubyte * 2),
    ('XgmiFclkFreq', ctypes.c_uint16 * 2),
    ('XgmiUclkFreq', ctypes.c_uint16 * 2),
    ('XgmiSocclkFreq', ctypes.c_uint16 * 2),
    ('XgmiSocVoltage', ctypes.c_uint16 * 2),
    ('DebugOverrides', ctypes.c_uint32),
    ('ReservedEquation0', struct_QuadraticInt_t),
    ('ReservedEquation1', struct_QuadraticInt_t),
    ('ReservedEquation2', struct_QuadraticInt_t),
    ('ReservedEquation3', struct_QuadraticInt_t),
    ('MinVoltageUlvGfx', ctypes.c_uint16),
    ('MinVoltageUlvSoc', ctypes.c_uint16),
    ('MGpuFanBoostLimitRpm', ctypes.c_uint16),
    ('padding16_Fan', ctypes.c_uint16),
    ('FanGainVrMem0', ctypes.c_uint16),
    ('FanGainVrMem1', ctypes.c_uint16),
    ('DcBtcGb', ctypes.c_uint16 * 2),
    ('Reserved', ctypes.c_uint32 * 11),
    ('Padding32', ctypes.c_uint32 * 3),
    ('MaxVoltageStepGfx', ctypes.c_uint16),
    ('MaxVoltageStepSoc', ctypes.c_uint16),
    ('VddGfxVrMapping', ctypes.c_ubyte),
    ('VddSocVrMapping', ctypes.c_ubyte),
    ('VddMem0VrMapping', ctypes.c_ubyte),
    ('VddMem1VrMapping', ctypes.c_ubyte),
    ('GfxUlvPhaseSheddingMask', ctypes.c_ubyte),
    ('SocUlvPhaseSheddingMask', ctypes.c_ubyte),
    ('ExternalSensorPresent', ctypes.c_ubyte),
    ('Padding8_V', ctypes.c_ubyte),
    ('GfxMaxCurrent', ctypes.c_uint16),
    ('GfxOffset', ctypes.c_byte),
    ('Padding_TelemetryGfx', ctypes.c_ubyte),
    ('SocMaxCurrent', ctypes.c_uint16),
    ('SocOffset', ctypes.c_byte),
    ('Padding_TelemetrySoc', ctypes.c_ubyte),
    ('Mem0MaxCurrent', ctypes.c_uint16),
    ('Mem0Offset', ctypes.c_byte),
    ('Padding_TelemetryMem0', ctypes.c_ubyte),
    ('Mem1MaxCurrent', ctypes.c_uint16),
    ('Mem1Offset', ctypes.c_byte),
    ('Padding_TelemetryMem1', ctypes.c_ubyte),
    ('AcDcGpio', ctypes.c_ubyte),
    ('AcDcPolarity', ctypes.c_ubyte),
    ('VR0HotGpio', ctypes.c_ubyte),
    ('VR0HotPolarity', ctypes.c_ubyte),
    ('VR1HotGpio', ctypes.c_ubyte),
    ('VR1HotPolarity', ctypes.c_ubyte),
    ('Padding1', ctypes.c_ubyte),
    ('Padding2', ctypes.c_ubyte),
    ('LedPin0', ctypes.c_ubyte),
    ('LedPin1', ctypes.c_ubyte),
    ('LedPin2', ctypes.c_ubyte),
    ('padding8_4', ctypes.c_ubyte),
    ('PllGfxclkSpreadEnabled', ctypes.c_ubyte),
    ('PllGfxclkSpreadPercent', ctypes.c_ubyte),
    ('PllGfxclkSpreadFreq', ctypes.c_uint16),
    ('UclkSpreadEnabled', ctypes.c_ubyte),
    ('UclkSpreadPercent', ctypes.c_ubyte),
    ('UclkSpreadFreq', ctypes.c_uint16),
    ('FclkSpreadEnabled', ctypes.c_ubyte),
    ('FclkSpreadPercent', ctypes.c_ubyte),
    ('FclkSpreadFreq', ctypes.c_uint16),
    ('FllGfxclkSpreadEnabled', ctypes.c_ubyte),
    ('FllGfxclkSpreadPercent', ctypes.c_ubyte),
    ('FllGfxclkSpreadFreq', ctypes.c_uint16),
    ('I2cControllers', struct_I2cControllerConfig_t * 7),
    ('BoardReserved', ctypes.c_uint32 * 10),
    ('MmHubPadding', ctypes.c_uint32 * 8),
]

struct__ATOM_VEGA20_POWERPLAYTABLE._pack_ = 1 # source:False
struct__ATOM_VEGA20_POWERPLAYTABLE._fields_ = [
    ('sHeader', struct_atom_common_table_header),
    ('ucTableRevision', ctypes.c_ubyte),
    ('usTableSize', ctypes.c_uint16),
    ('ulGoldenPPID', ctypes.c_uint32),
    ('ulGoldenRevision', ctypes.c_uint32),
    ('usFormatID', ctypes.c_uint16),
    ('ulPlatformCaps', ctypes.c_uint32),
    ('ucThermalControllerType', ctypes.c_ubyte),
    ('usSmallPowerLimit1', ctypes.c_uint16),
    ('usSmallPowerLimit2', ctypes.c_uint16),
    ('usBoostPowerLimit', ctypes.c_uint16),
    ('usODTurboPowerLimit', ctypes.c_uint16),
    ('usODPowerSavePowerLimit', ctypes.c_uint16),
    ('usSoftwareShutdownTemp', ctypes.c_uint16),
    ('PowerSavingClockTable', ATOM_VEGA20_POWER_SAVING_CLOCK_RECORD),
    ('OverDrive8Table', ATOM_VEGA20_OVERDRIVE8_RECORD),
    ('usReserve', ctypes.c_uint16 * 5),
    ('smcPPTable', struct_PPTable_t),
]

ATOM_Vega20_POWERPLAYTABLE = struct__ATOM_VEGA20_POWERPLAYTABLE
__all__ = \
    ['ATOM_VEGA20_ODFEATURE_COUNT',
    'ATOM_VEGA20_ODFEATURE_FAN_ACOUSTIC_LIMIT',
    'ATOM_VEGA20_ODFEATURE_FAN_SPEED_MIN',
    'ATOM_VEGA20_ODFEATURE_FAN_ZERO_RPM_CONTROL',
    'ATOM_VEGA20_ODFEATURE_GFXCLK_CURVE',
    'ATOM_VEGA20_ODFEATURE_GFXCLK_LIMITS', 'ATOM_VEGA20_ODFEATURE_ID',
    'ATOM_VEGA20_ODFEATURE_MAX_COUNT',
    'ATOM_VEGA20_ODFEATURE_MEMORY_TIMING_TUNE',
    'ATOM_VEGA20_ODFEATURE_POWER_LIMIT',
    'ATOM_VEGA20_ODFEATURE_TEMPERATURE_FAN',
    'ATOM_VEGA20_ODFEATURE_TEMPERATURE_SYSTEM',
    'ATOM_VEGA20_ODFEATURE_UCLK_MAX', 'ATOM_VEGA20_ODSETTING_COUNT',
    'ATOM_VEGA20_ODSETTING_FANRPMACOUSTICLIMIT',
    'ATOM_VEGA20_ODSETTING_FANRPMMIN',
    'ATOM_VEGA20_ODSETTING_FANTARGETTEMPERATURE',
    'ATOM_VEGA20_ODSETTING_GFXCLKFMAX',
    'ATOM_VEGA20_ODSETTING_GFXCLKFMIN', 'ATOM_VEGA20_ODSETTING_ID',
    'ATOM_VEGA20_ODSETTING_MAX_COUNT',
    'ATOM_VEGA20_ODSETTING_OPERATINGTEMPMAX',
    'ATOM_VEGA20_ODSETTING_POWERPERCENTAGE',
    'ATOM_VEGA20_ODSETTING_UCLKFMAX',
    'ATOM_VEGA20_ODSETTING_VDDGFXCURVEFREQ_P1',
    'ATOM_VEGA20_ODSETTING_VDDGFXCURVEFREQ_P2',
    'ATOM_VEGA20_ODSETTING_VDDGFXCURVEFREQ_P3',
    'ATOM_VEGA20_ODSETTING_VDDGFXCURVEVOLTAGEOFFSET_P1',
    'ATOM_VEGA20_ODSETTING_VDDGFXCURVEVOLTAGEOFFSET_P2',
    'ATOM_VEGA20_ODSETTING_VDDGFXCURVEVOLTAGEOFFSET_P3',
    'ATOM_VEGA20_OVERDRIVE8_RECORD',
    'ATOM_VEGA20_POWER_SAVING_CLOCK_RECORD',
    'ATOM_VEGA20_PPCLOCK_COUNT', 'ATOM_VEGA20_PPCLOCK_DCEFCLK',
    'ATOM_VEGA20_PPCLOCK_DCLK', 'ATOM_VEGA20_PPCLOCK_DISPCLK',
    'ATOM_VEGA20_PPCLOCK_ECLK', 'ATOM_VEGA20_PPCLOCK_FCLK',
    'ATOM_VEGA20_PPCLOCK_GFXCLK', 'ATOM_VEGA20_PPCLOCK_ID',
    'ATOM_VEGA20_PPCLOCK_MAX_COUNT', 'ATOM_VEGA20_PPCLOCK_PHYCLK',
    'ATOM_VEGA20_PPCLOCK_PIXCLK', 'ATOM_VEGA20_PPCLOCK_SOCCLK',
    'ATOM_VEGA20_PPCLOCK_UCLK', 'ATOM_VEGA20_PPCLOCK_VCLK',
    'ATOM_VEGA20_PP_PLATFORM_CAP_BACO',
    'ATOM_VEGA20_PP_PLATFORM_CAP_BAMACO',
    'ATOM_VEGA20_PP_PLATFORM_CAP_ENABLESHADOWPSTATE',
    'ATOM_VEGA20_PP_PLATFORM_CAP_HARDWAREDC',
    'ATOM_VEGA20_PP_PLATFORM_CAP_POWERPLAY',
    'ATOM_VEGA20_PP_PLATFORM_CAP_SBIOSPOWERSOURCE',
    'ATOM_VEGA20_PP_THERMALCONTROLLER_NONE',
    'ATOM_VEGA20_PP_THERMALCONTROLLER_VEGA20',
    'ATOM_VEGA20_TABLE_REVISION_VEGA20', 'ATOM_Vega20_POWERPLAYTABLE',
    '_VEGA20_PPTABLE_H_', 'struct_DpmDescriptor_t',
    'struct_DroopInt_t', 'struct_I2cControllerConfig_t',
    'struct_LinearInt_t', 'struct_PPTable_t', 'struct_QuadraticInt_t',
    'struct__ATOM_VEGA20_OVERDRIVE8_RECORD',
    'struct__ATOM_VEGA20_POWERPLAYTABLE',
    'struct__ATOM_VEGA20_POWER_SAVING_CLOCK_RECORD',
    'struct_atom_common_table_header']
