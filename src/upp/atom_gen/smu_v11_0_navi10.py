# -*- coding: utf-8 -*-
#
# TARGET arch is: ['--include', 'stdint.h', '--include', 'linux/drivers/gpu/drm/amd/include/atom-types.h', '--include', 'linux/drivers/gpu/drm/amd/include/atomfirmware.h', '--include', 'linux/drivers/gpu/drm/amd/pm/swsmu/inc/pmfw_if/smu11_driver_if_navi10.h', '']
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





SMU_11_0_PPTABLE_H = True # macro
SMU_11_0_TABLE_FORMAT_REVISION = 12 # macro
SMU_11_0_PP_PLATFORM_CAP_POWERPLAY = 0x1 # macro
SMU_11_0_PP_PLATFORM_CAP_SBIOSPOWERSOURCE = 0x2 # macro
SMU_11_0_PP_PLATFORM_CAP_HARDWAREDC = 0x4 # macro
SMU_11_0_PP_PLATFORM_CAP_BACO = 0x8 # macro
SMU_11_0_PP_PLATFORM_CAP_MACO = 0x10 # macro
SMU_11_0_PP_PLATFORM_CAP_SHADOWPSTATE = 0x20 # macro
SMU_11_0_PP_THERMALCONTROLLER_NONE = 0 # macro
SMU_11_0_PP_OVERDRIVE_VERSION = 0x0800 # macro
SMU_11_0_PP_POWERSAVINGCLOCK_VERSION = 0x0100 # macro
SMU_11_0_MAX_ODFEATURE = 32 # macro
SMU_11_0_MAX_ODSETTING = 32 # macro
SMU_11_0_MAX_PPCLOCK = 16 # macro

# values for enumeration 'SMU_11_0_ODFEATURE_CAP'
SMU_11_0_ODFEATURE_CAP__enumvalues = {
    0: 'SMU_11_0_ODCAP_GFXCLK_LIMITS',
    1: 'SMU_11_0_ODCAP_GFXCLK_CURVE',
    2: 'SMU_11_0_ODCAP_UCLK_MAX',
    3: 'SMU_11_0_ODCAP_POWER_LIMIT',
    4: 'SMU_11_0_ODCAP_FAN_ACOUSTIC_LIMIT',
    5: 'SMU_11_0_ODCAP_FAN_SPEED_MIN',
    6: 'SMU_11_0_ODCAP_TEMPERATURE_FAN',
    7: 'SMU_11_0_ODCAP_TEMPERATURE_SYSTEM',
    8: 'SMU_11_0_ODCAP_MEMORY_TIMING_TUNE',
    9: 'SMU_11_0_ODCAP_FAN_ZERO_RPM_CONTROL',
    10: 'SMU_11_0_ODCAP_AUTO_UV_ENGINE',
    11: 'SMU_11_0_ODCAP_AUTO_OC_ENGINE',
    12: 'SMU_11_0_ODCAP_AUTO_OC_MEMORY',
    13: 'SMU_11_0_ODCAP_FAN_CURVE',
    14: 'SMU_11_0_ODCAP_COUNT',
}
SMU_11_0_ODCAP_GFXCLK_LIMITS = 0
SMU_11_0_ODCAP_GFXCLK_CURVE = 1
SMU_11_0_ODCAP_UCLK_MAX = 2
SMU_11_0_ODCAP_POWER_LIMIT = 3
SMU_11_0_ODCAP_FAN_ACOUSTIC_LIMIT = 4
SMU_11_0_ODCAP_FAN_SPEED_MIN = 5
SMU_11_0_ODCAP_TEMPERATURE_FAN = 6
SMU_11_0_ODCAP_TEMPERATURE_SYSTEM = 7
SMU_11_0_ODCAP_MEMORY_TIMING_TUNE = 8
SMU_11_0_ODCAP_FAN_ZERO_RPM_CONTROL = 9
SMU_11_0_ODCAP_AUTO_UV_ENGINE = 10
SMU_11_0_ODCAP_AUTO_OC_ENGINE = 11
SMU_11_0_ODCAP_AUTO_OC_MEMORY = 12
SMU_11_0_ODCAP_FAN_CURVE = 13
SMU_11_0_ODCAP_COUNT = 14
SMU_11_0_ODFEATURE_CAP = ctypes.c_uint32 # enum

# values for enumeration 'SMU_11_0_ODFEATURE_ID'
SMU_11_0_ODFEATURE_ID__enumvalues = {
    1: 'SMU_11_0_ODFEATURE_GFXCLK_LIMITS',
    2: 'SMU_11_0_ODFEATURE_GFXCLK_CURVE',
    4: 'SMU_11_0_ODFEATURE_UCLK_MAX',
    8: 'SMU_11_0_ODFEATURE_POWER_LIMIT',
    16: 'SMU_11_0_ODFEATURE_FAN_ACOUSTIC_LIMIT',
    32: 'SMU_11_0_ODFEATURE_FAN_SPEED_MIN',
    64: 'SMU_11_0_ODFEATURE_TEMPERATURE_FAN',
    128: 'SMU_11_0_ODFEATURE_TEMPERATURE_SYSTEM',
    256: 'SMU_11_0_ODFEATURE_MEMORY_TIMING_TUNE',
    512: 'SMU_11_0_ODFEATURE_FAN_ZERO_RPM_CONTROL',
    1024: 'SMU_11_0_ODFEATURE_AUTO_UV_ENGINE',
    2048: 'SMU_11_0_ODFEATURE_AUTO_OC_ENGINE',
    4096: 'SMU_11_0_ODFEATURE_AUTO_OC_MEMORY',
    8192: 'SMU_11_0_ODFEATURE_FAN_CURVE',
    14: 'SMU_11_0_ODFEATURE_COUNT',
}
SMU_11_0_ODFEATURE_GFXCLK_LIMITS = 1
SMU_11_0_ODFEATURE_GFXCLK_CURVE = 2
SMU_11_0_ODFEATURE_UCLK_MAX = 4
SMU_11_0_ODFEATURE_POWER_LIMIT = 8
SMU_11_0_ODFEATURE_FAN_ACOUSTIC_LIMIT = 16
SMU_11_0_ODFEATURE_FAN_SPEED_MIN = 32
SMU_11_0_ODFEATURE_TEMPERATURE_FAN = 64
SMU_11_0_ODFEATURE_TEMPERATURE_SYSTEM = 128
SMU_11_0_ODFEATURE_MEMORY_TIMING_TUNE = 256
SMU_11_0_ODFEATURE_FAN_ZERO_RPM_CONTROL = 512
SMU_11_0_ODFEATURE_AUTO_UV_ENGINE = 1024
SMU_11_0_ODFEATURE_AUTO_OC_ENGINE = 2048
SMU_11_0_ODFEATURE_AUTO_OC_MEMORY = 4096
SMU_11_0_ODFEATURE_FAN_CURVE = 8192
SMU_11_0_ODFEATURE_COUNT = 14
SMU_11_0_ODFEATURE_ID = ctypes.c_uint32 # enum

# values for enumeration 'SMU_11_0_ODSETTING_ID'
SMU_11_0_ODSETTING_ID__enumvalues = {
    0: 'SMU_11_0_ODSETTING_GFXCLKFMAX',
    1: 'SMU_11_0_ODSETTING_GFXCLKFMIN',
    2: 'SMU_11_0_ODSETTING_VDDGFXCURVEFREQ_P1',
    3: 'SMU_11_0_ODSETTING_VDDGFXCURVEVOLTAGE_P1',
    4: 'SMU_11_0_ODSETTING_VDDGFXCURVEFREQ_P2',
    5: 'SMU_11_0_ODSETTING_VDDGFXCURVEVOLTAGE_P2',
    6: 'SMU_11_0_ODSETTING_VDDGFXCURVEFREQ_P3',
    7: 'SMU_11_0_ODSETTING_VDDGFXCURVEVOLTAGE_P3',
    8: 'SMU_11_0_ODSETTING_UCLKFMAX',
    9: 'SMU_11_0_ODSETTING_POWERPERCENTAGE',
    10: 'SMU_11_0_ODSETTING_FANRPMMIN',
    11: 'SMU_11_0_ODSETTING_FANRPMACOUSTICLIMIT',
    12: 'SMU_11_0_ODSETTING_FANTARGETTEMPERATURE',
    13: 'SMU_11_0_ODSETTING_OPERATINGTEMPMAX',
    14: 'SMU_11_0_ODSETTING_ACTIMING',
    15: 'SMU_11_0_ODSETTING_FAN_ZERO_RPM_CONTROL',
    16: 'SMU_11_0_ODSETTING_AUTOUVENGINE',
    17: 'SMU_11_0_ODSETTING_AUTOOCENGINE',
    18: 'SMU_11_0_ODSETTING_AUTOOCMEMORY',
    19: 'SMU_11_0_ODSETTING_COUNT',
}
SMU_11_0_ODSETTING_GFXCLKFMAX = 0
SMU_11_0_ODSETTING_GFXCLKFMIN = 1
SMU_11_0_ODSETTING_VDDGFXCURVEFREQ_P1 = 2
SMU_11_0_ODSETTING_VDDGFXCURVEVOLTAGE_P1 = 3
SMU_11_0_ODSETTING_VDDGFXCURVEFREQ_P2 = 4
SMU_11_0_ODSETTING_VDDGFXCURVEVOLTAGE_P2 = 5
SMU_11_0_ODSETTING_VDDGFXCURVEFREQ_P3 = 6
SMU_11_0_ODSETTING_VDDGFXCURVEVOLTAGE_P3 = 7
SMU_11_0_ODSETTING_UCLKFMAX = 8
SMU_11_0_ODSETTING_POWERPERCENTAGE = 9
SMU_11_0_ODSETTING_FANRPMMIN = 10
SMU_11_0_ODSETTING_FANRPMACOUSTICLIMIT = 11
SMU_11_0_ODSETTING_FANTARGETTEMPERATURE = 12
SMU_11_0_ODSETTING_OPERATINGTEMPMAX = 13
SMU_11_0_ODSETTING_ACTIMING = 14
SMU_11_0_ODSETTING_FAN_ZERO_RPM_CONTROL = 15
SMU_11_0_ODSETTING_AUTOUVENGINE = 16
SMU_11_0_ODSETTING_AUTOOCENGINE = 17
SMU_11_0_ODSETTING_AUTOOCMEMORY = 18
SMU_11_0_ODSETTING_COUNT = 19
SMU_11_0_ODSETTING_ID = ctypes.c_uint32 # enum
class struct_smu_11_0_overdrive_table(Structure):
    pass

struct_smu_11_0_overdrive_table._pack_ = 1 # source:False
struct_smu_11_0_overdrive_table._fields_ = [
    ('revision', ctypes.c_ubyte),
    ('reserve', ctypes.c_ubyte * 3),
    ('feature_count', ctypes.c_uint32),
    ('setting_count', ctypes.c_uint32),
    ('cap', ctypes.c_ubyte * 32),
    ('max', ctypes.c_uint32 * 32),
    ('min', ctypes.c_uint32 * 32),
]


# values for enumeration 'SMU_11_0_PPCLOCK_ID'
SMU_11_0_PPCLOCK_ID__enumvalues = {
    0: 'SMU_11_0_PPCLOCK_GFXCLK',
    1: 'SMU_11_0_PPCLOCK_VCLK',
    2: 'SMU_11_0_PPCLOCK_DCLK',
    3: 'SMU_11_0_PPCLOCK_ECLK',
    4: 'SMU_11_0_PPCLOCK_SOCCLK',
    5: 'SMU_11_0_PPCLOCK_UCLK',
    6: 'SMU_11_0_PPCLOCK_DCEFCLK',
    7: 'SMU_11_0_PPCLOCK_DISPCLK',
    8: 'SMU_11_0_PPCLOCK_PIXCLK',
    9: 'SMU_11_0_PPCLOCK_PHYCLK',
    10: 'SMU_11_0_PPCLOCK_COUNT',
}
SMU_11_0_PPCLOCK_GFXCLK = 0
SMU_11_0_PPCLOCK_VCLK = 1
SMU_11_0_PPCLOCK_DCLK = 2
SMU_11_0_PPCLOCK_ECLK = 3
SMU_11_0_PPCLOCK_SOCCLK = 4
SMU_11_0_PPCLOCK_UCLK = 5
SMU_11_0_PPCLOCK_DCEFCLK = 6
SMU_11_0_PPCLOCK_DISPCLK = 7
SMU_11_0_PPCLOCK_PIXCLK = 8
SMU_11_0_PPCLOCK_PHYCLK = 9
SMU_11_0_PPCLOCK_COUNT = 10
SMU_11_0_PPCLOCK_ID = ctypes.c_uint32 # enum
class struct_smu_11_0_power_saving_clock_table(Structure):
    pass

struct_smu_11_0_power_saving_clock_table._pack_ = 1 # source:False
struct_smu_11_0_power_saving_clock_table._fields_ = [
    ('revision', ctypes.c_ubyte),
    ('reserve', ctypes.c_ubyte * 3),
    ('count', ctypes.c_uint32),
    ('max', ctypes.c_uint32 * 16),
    ('min', ctypes.c_uint32 * 16),
]

class struct_smu_11_0_powerplay_table(Structure):
    pass

class struct_PPTable_t(Structure):
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

class struct_DroopInt_t(Structure):
    pass

struct_DroopInt_t._pack_ = 1 # source:False
struct_DroopInt_t._fields_ = [
    ('a', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
    ('c', ctypes.c_uint32),
]

class struct_DpmDescriptor_t(Structure):
    pass

struct_DpmDescriptor_t._pack_ = 1 # source:False
struct_DpmDescriptor_t._fields_ = [
    ('VoltageMode', ctypes.c_ubyte),
    ('SnapToDiscrete', ctypes.c_ubyte),
    ('NumDiscreteLevels', ctypes.c_ubyte),
    ('Padding', ctypes.c_ubyte),
    ('ConversionToAvfsClk', struct_LinearInt_t),
    ('SsCurve', struct_QuadraticInt_t),
]

class struct_I2cControllerConfig_t(Structure):
    pass

struct_I2cControllerConfig_t._pack_ = 1 # source:False
struct_I2cControllerConfig_t._fields_ = [
    ('Enabled', ctypes.c_ubyte),
    ('Speed', ctypes.c_ubyte),
    ('Padding', ctypes.c_ubyte * 2),
    ('SlaveAddress', ctypes.c_uint32),
    ('ControllerPort', ctypes.c_ubyte),
    ('ControllerName', ctypes.c_ubyte),
    ('ThermalThrotter', ctypes.c_ubyte),
    ('I2cProtocol', ctypes.c_ubyte),
]

struct_PPTable_t._pack_ = 1 # source:False
struct_PPTable_t._fields_ = [
    ('Version', ctypes.c_uint32),
    ('FeaturesToRun', ctypes.c_uint32 * 2),
    ('SocketPowerLimitAc', ctypes.c_uint16 * 4),
    ('SocketPowerLimitAcTau', ctypes.c_uint16 * 4),
    ('SocketPowerLimitDc', ctypes.c_uint16 * 4),
    ('SocketPowerLimitDcTau', ctypes.c_uint16 * 4),
    ('TdcLimitSoc', ctypes.c_uint16),
    ('TdcLimitSocTau', ctypes.c_uint16),
    ('TdcLimitGfx', ctypes.c_uint16),
    ('TdcLimitGfxTau', ctypes.c_uint16),
    ('TedgeLimit', ctypes.c_uint16),
    ('ThotspotLimit', ctypes.c_uint16),
    ('TmemLimit', ctypes.c_uint16),
    ('Tvr_gfxLimit', ctypes.c_uint16),
    ('Tvr_mem0Limit', ctypes.c_uint16),
    ('Tvr_mem1Limit', ctypes.c_uint16),
    ('Tvr_socLimit', ctypes.c_uint16),
    ('Tliquid0Limit', ctypes.c_uint16),
    ('Tliquid1Limit', ctypes.c_uint16),
    ('TplxLimit', ctypes.c_uint16),
    ('FitLimit', ctypes.c_uint32),
    ('PpmPowerLimit', ctypes.c_uint16),
    ('PpmTemperatureThreshold', ctypes.c_uint16),
    ('ThrottlerControlMask', ctypes.c_uint32),
    ('FwDStateMask', ctypes.c_uint32),
    ('UlvVoltageOffsetSoc', ctypes.c_uint16),
    ('UlvVoltageOffsetGfx', ctypes.c_uint16),
    ('GceaLinkMgrIdleThreshold', ctypes.c_ubyte),
    ('paddingRlcUlvParams', ctypes.c_ubyte * 3),
    ('UlvSmnclkDid', ctypes.c_ubyte),
    ('UlvMp1clkDid', ctypes.c_ubyte),
    ('UlvGfxclkBypass', ctypes.c_ubyte),
    ('Padding234', ctypes.c_ubyte),
    ('MinVoltageUlvGfx', ctypes.c_uint16),
    ('MinVoltageUlvSoc', ctypes.c_uint16),
    ('MinVoltageGfx', ctypes.c_uint16),
    ('MinVoltageSoc', ctypes.c_uint16),
    ('MaxVoltageGfx', ctypes.c_uint16),
    ('MaxVoltageSoc', ctypes.c_uint16),
    ('LoadLineResistanceGfx', ctypes.c_uint16),
    ('LoadLineResistanceSoc', ctypes.c_uint16),
    ('DpmDescriptor', struct_DpmDescriptor_t * 9),
    ('FreqTableGfx', ctypes.c_uint16 * 16),
    ('FreqTableVclk', ctypes.c_uint16 * 8),
    ('FreqTableDclk', ctypes.c_uint16 * 8),
    ('FreqTableSocclk', ctypes.c_uint16 * 8),
    ('FreqTableUclk', ctypes.c_uint16 * 4),
    ('FreqTableDcefclk', ctypes.c_uint16 * 8),
    ('FreqTableDispclk', ctypes.c_uint16 * 8),
    ('FreqTablePixclk', ctypes.c_uint16 * 8),
    ('FreqTablePhyclk', ctypes.c_uint16 * 8),
    ('Paddingclks', ctypes.c_uint32 * 16),
    ('DcModeMaxFreq', ctypes.c_uint16 * 9),
    ('Padding8_Clks', ctypes.c_uint16),
    ('FreqTableUclkDiv', ctypes.c_ubyte * 4),
    ('Mp0clkFreq', ctypes.c_uint16 * 2),
    ('Mp0DpmVoltage', ctypes.c_uint16 * 2),
    ('MemVddciVoltage', ctypes.c_uint16 * 4),
    ('MemMvddVoltage', ctypes.c_uint16 * 4),
    ('GfxclkFgfxoffEntry', ctypes.c_uint16),
    ('GfxclkFinit', ctypes.c_uint16),
    ('GfxclkFidle', ctypes.c_uint16),
    ('GfxclkSlewRate', ctypes.c_uint16),
    ('GfxclkFopt', ctypes.c_uint16),
    ('Padding567', ctypes.c_ubyte * 2),
    ('GfxclkDsMaxFreq', ctypes.c_uint16),
    ('GfxclkSource', ctypes.c_ubyte),
    ('Padding456', ctypes.c_ubyte),
    ('LowestUclkReservedForUlv', ctypes.c_ubyte),
    ('paddingUclk', ctypes.c_ubyte * 3),
    ('MemoryType', ctypes.c_ubyte),
    ('MemoryChannels', ctypes.c_ubyte),
    ('PaddingMem', ctypes.c_ubyte * 2),
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
    ('FanGainLiquid0', ctypes.c_uint16),
    ('FanGainLiquid1', ctypes.c_uint16),
    ('FanGainVrGfx', ctypes.c_uint16),
    ('FanGainVrSoc', ctypes.c_uint16),
    ('FanGainVrMem0', ctypes.c_uint16),
    ('FanGainVrMem1', ctypes.c_uint16),
    ('FanGainPlx', ctypes.c_uint16),
    ('FanGainMem', ctypes.c_uint16),
    ('FanPwmMin', ctypes.c_uint16),
    ('FanAcousticLimitRpm', ctypes.c_uint16),
    ('FanThrottlingRpm', ctypes.c_uint16),
    ('FanMaximumRpm', ctypes.c_uint16),
    ('FanTargetTemperature', ctypes.c_uint16),
    ('FanTargetGfxclk', ctypes.c_uint16),
    ('FanTempInputSelect', ctypes.c_ubyte),
    ('FanPadding', ctypes.c_ubyte),
    ('FanZeroRpmEnable', ctypes.c_ubyte),
    ('FanTachEdgePerRev', ctypes.c_ubyte),
    ('FuzzyFan_ErrorSetDelta', ctypes.c_int16),
    ('FuzzyFan_ErrorRateSetDelta', ctypes.c_int16),
    ('FuzzyFan_PwmSetDelta', ctypes.c_int16),
    ('FuzzyFan_Reserved', ctypes.c_uint16),
    ('OverrideAvfsGb', ctypes.c_ubyte * 2),
    ('Padding8_Avfs', ctypes.c_ubyte * 2),
    ('qAvfsGb', struct_QuadraticInt_t * 2),
    ('dBtcGbGfxPll', struct_DroopInt_t),
    ('dBtcGbGfxDfll', struct_DroopInt_t),
    ('dBtcGbSoc', struct_DroopInt_t),
    ('qAgingGb', struct_LinearInt_t * 2),
    ('qStaticVoltageOffset', struct_QuadraticInt_t * 2),
    ('DcTol', ctypes.c_uint16 * 2),
    ('DcBtcEnabled', ctypes.c_ubyte * 2),
    ('Padding8_GfxBtc', ctypes.c_ubyte * 2),
    ('DcBtcMin', ctypes.c_uint16 * 2),
    ('DcBtcMax', ctypes.c_uint16 * 2),
    ('DebugOverrides', ctypes.c_uint32),
    ('ReservedEquation0', struct_QuadraticInt_t),
    ('ReservedEquation1', struct_QuadraticInt_t),
    ('ReservedEquation2', struct_QuadraticInt_t),
    ('ReservedEquation3', struct_QuadraticInt_t),
    ('TotalPowerConfig', ctypes.c_ubyte),
    ('TotalPowerSpare1', ctypes.c_ubyte),
    ('TotalPowerSpare2', ctypes.c_uint16),
    ('PccThresholdLow', ctypes.c_uint16),
    ('PccThresholdHigh', ctypes.c_uint16),
    ('MGpuFanBoostLimitRpm', ctypes.c_uint32),
    ('PaddingAPCC', ctypes.c_uint32 * 5),
    ('VDDGFX_TVmin', ctypes.c_uint16),
    ('VDDSOC_TVmin', ctypes.c_uint16),
    ('VDDGFX_Vmin_HiTemp', ctypes.c_uint16),
    ('VDDGFX_Vmin_LoTemp', ctypes.c_uint16),
    ('VDDSOC_Vmin_HiTemp', ctypes.c_uint16),
    ('VDDSOC_Vmin_LoTemp', ctypes.c_uint16),
    ('VDDGFX_TVminHystersis', ctypes.c_uint16),
    ('VDDSOC_TVminHystersis', ctypes.c_uint16),
    ('BtcConfig', ctypes.c_uint32),
    ('SsFmin', ctypes.c_uint16 * 10),
    ('DcBtcGb', ctypes.c_uint16 * 2),
    ('Reserved', ctypes.c_uint32 * 8),
    ('I2cControllers', struct_I2cControllerConfig_t * 8),
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
    ('GthrGpio', ctypes.c_ubyte),
    ('GthrPolarity', ctypes.c_ubyte),
    ('LedPin0', ctypes.c_ubyte),
    ('LedPin1', ctypes.c_ubyte),
    ('LedPin2', ctypes.c_ubyte),
    ('padding8_4', ctypes.c_ubyte),
    ('PllGfxclkSpreadEnabled', ctypes.c_ubyte),
    ('PllGfxclkSpreadPercent', ctypes.c_ubyte),
    ('PllGfxclkSpreadFreq', ctypes.c_uint16),
    ('DfllGfxclkSpreadEnabled', ctypes.c_ubyte),
    ('DfllGfxclkSpreadPercent', ctypes.c_ubyte),
    ('DfllGfxclkSpreadFreq', ctypes.c_uint16),
    ('UclkSpreadEnabled', ctypes.c_ubyte),
    ('UclkSpreadPercent', ctypes.c_ubyte),
    ('UclkSpreadFreq', ctypes.c_uint16),
    ('SoclkSpreadEnabled', ctypes.c_ubyte),
    ('SocclkSpreadPercent', ctypes.c_ubyte),
    ('SocclkSpreadFreq', ctypes.c_uint16),
    ('TotalBoardPower', ctypes.c_uint16),
    ('BoardPadding', ctypes.c_uint16),
    ('MvddRatio', ctypes.c_uint32),
    ('RenesesLoadLineEnabled', ctypes.c_ubyte),
    ('GfxLoadlineResistance', ctypes.c_ubyte),
    ('SocLoadlineResistance', ctypes.c_ubyte),
    ('Padding8_Loadline', ctypes.c_ubyte),
    ('BoardReserved', ctypes.c_uint32 * 8),
    ('MmHubPadding', ctypes.c_uint32 * 8),
]

class struct_atom_common_table_header(Structure):
    pass

struct_atom_common_table_header._pack_ = 1 # source:False
struct_atom_common_table_header._fields_ = [
    ('structuresize', ctypes.c_uint16),
    ('format_revision', ctypes.c_ubyte),
    ('content_revision', ctypes.c_ubyte),
]

struct_smu_11_0_powerplay_table._pack_ = 1 # source:False
struct_smu_11_0_powerplay_table._fields_ = [
    ('header', struct_atom_common_table_header),
    ('table_revision', ctypes.c_ubyte),
    ('table_size', ctypes.c_uint16),
    ('golden_pp_id', ctypes.c_uint32),
    ('golden_revision', ctypes.c_uint32),
    ('format_id', ctypes.c_uint16),
    ('platform_caps', ctypes.c_uint32),
    ('thermal_controller_type', ctypes.c_ubyte),
    ('small_power_limit1', ctypes.c_uint16),
    ('small_power_limit2', ctypes.c_uint16),
    ('boost_power_limit', ctypes.c_uint16),
    ('od_turbo_power_limit', ctypes.c_uint16),
    ('od_power_save_power_limit', ctypes.c_uint16),
    ('software_shutdown_temp', ctypes.c_uint16),
    ('reserve', ctypes.c_uint16 * 6),
    ('power_saving_clock', struct_smu_11_0_power_saving_clock_table),
    ('overdrive_table', struct_smu_11_0_overdrive_table),
    ('smc_pptable', struct_PPTable_t),
]

__all__ = \
    ['SMU_11_0_MAX_ODFEATURE', 'SMU_11_0_MAX_ODSETTING',
    'SMU_11_0_MAX_PPCLOCK', 'SMU_11_0_ODCAP_AUTO_OC_ENGINE',
    'SMU_11_0_ODCAP_AUTO_OC_MEMORY', 'SMU_11_0_ODCAP_AUTO_UV_ENGINE',
    'SMU_11_0_ODCAP_COUNT', 'SMU_11_0_ODCAP_FAN_ACOUSTIC_LIMIT',
    'SMU_11_0_ODCAP_FAN_CURVE', 'SMU_11_0_ODCAP_FAN_SPEED_MIN',
    'SMU_11_0_ODCAP_FAN_ZERO_RPM_CONTROL',
    'SMU_11_0_ODCAP_GFXCLK_CURVE', 'SMU_11_0_ODCAP_GFXCLK_LIMITS',
    'SMU_11_0_ODCAP_MEMORY_TIMING_TUNE', 'SMU_11_0_ODCAP_POWER_LIMIT',
    'SMU_11_0_ODCAP_TEMPERATURE_FAN',
    'SMU_11_0_ODCAP_TEMPERATURE_SYSTEM', 'SMU_11_0_ODCAP_UCLK_MAX',
    'SMU_11_0_ODFEATURE_AUTO_OC_ENGINE',
    'SMU_11_0_ODFEATURE_AUTO_OC_MEMORY',
    'SMU_11_0_ODFEATURE_AUTO_UV_ENGINE', 'SMU_11_0_ODFEATURE_CAP',
    'SMU_11_0_ODFEATURE_COUNT',
    'SMU_11_0_ODFEATURE_FAN_ACOUSTIC_LIMIT',
    'SMU_11_0_ODFEATURE_FAN_CURVE',
    'SMU_11_0_ODFEATURE_FAN_SPEED_MIN',
    'SMU_11_0_ODFEATURE_FAN_ZERO_RPM_CONTROL',
    'SMU_11_0_ODFEATURE_GFXCLK_CURVE',
    'SMU_11_0_ODFEATURE_GFXCLK_LIMITS', 'SMU_11_0_ODFEATURE_ID',
    'SMU_11_0_ODFEATURE_MEMORY_TIMING_TUNE',
    'SMU_11_0_ODFEATURE_POWER_LIMIT',
    'SMU_11_0_ODFEATURE_TEMPERATURE_FAN',
    'SMU_11_0_ODFEATURE_TEMPERATURE_SYSTEM',
    'SMU_11_0_ODFEATURE_UCLK_MAX', 'SMU_11_0_ODSETTING_ACTIMING',
    'SMU_11_0_ODSETTING_AUTOOCENGINE',
    'SMU_11_0_ODSETTING_AUTOOCMEMORY',
    'SMU_11_0_ODSETTING_AUTOUVENGINE', 'SMU_11_0_ODSETTING_COUNT',
    'SMU_11_0_ODSETTING_FANRPMACOUSTICLIMIT',
    'SMU_11_0_ODSETTING_FANRPMMIN',
    'SMU_11_0_ODSETTING_FANTARGETTEMPERATURE',
    'SMU_11_0_ODSETTING_FAN_ZERO_RPM_CONTROL',
    'SMU_11_0_ODSETTING_GFXCLKFMAX', 'SMU_11_0_ODSETTING_GFXCLKFMIN',
    'SMU_11_0_ODSETTING_ID', 'SMU_11_0_ODSETTING_OPERATINGTEMPMAX',
    'SMU_11_0_ODSETTING_POWERPERCENTAGE',
    'SMU_11_0_ODSETTING_UCLKFMAX',
    'SMU_11_0_ODSETTING_VDDGFXCURVEFREQ_P1',
    'SMU_11_0_ODSETTING_VDDGFXCURVEFREQ_P2',
    'SMU_11_0_ODSETTING_VDDGFXCURVEFREQ_P3',
    'SMU_11_0_ODSETTING_VDDGFXCURVEVOLTAGE_P1',
    'SMU_11_0_ODSETTING_VDDGFXCURVEVOLTAGE_P2',
    'SMU_11_0_ODSETTING_VDDGFXCURVEVOLTAGE_P3',
    'SMU_11_0_PPCLOCK_COUNT', 'SMU_11_0_PPCLOCK_DCEFCLK',
    'SMU_11_0_PPCLOCK_DCLK', 'SMU_11_0_PPCLOCK_DISPCLK',
    'SMU_11_0_PPCLOCK_ECLK', 'SMU_11_0_PPCLOCK_GFXCLK',
    'SMU_11_0_PPCLOCK_ID', 'SMU_11_0_PPCLOCK_PHYCLK',
    'SMU_11_0_PPCLOCK_PIXCLK', 'SMU_11_0_PPCLOCK_SOCCLK',
    'SMU_11_0_PPCLOCK_UCLK', 'SMU_11_0_PPCLOCK_VCLK',
    'SMU_11_0_PPTABLE_H', 'SMU_11_0_PP_OVERDRIVE_VERSION',
    'SMU_11_0_PP_PLATFORM_CAP_BACO',
    'SMU_11_0_PP_PLATFORM_CAP_HARDWAREDC',
    'SMU_11_0_PP_PLATFORM_CAP_MACO',
    'SMU_11_0_PP_PLATFORM_CAP_POWERPLAY',
    'SMU_11_0_PP_PLATFORM_CAP_SBIOSPOWERSOURCE',
    'SMU_11_0_PP_PLATFORM_CAP_SHADOWPSTATE',
    'SMU_11_0_PP_POWERSAVINGCLOCK_VERSION',
    'SMU_11_0_PP_THERMALCONTROLLER_NONE',
    'SMU_11_0_TABLE_FORMAT_REVISION', 'struct_DpmDescriptor_t',
    'struct_DroopInt_t', 'struct_I2cControllerConfig_t',
    'struct_LinearInt_t', 'struct_PPTable_t', 'struct_QuadraticInt_t',
    'struct_atom_common_table_header',
    'struct_smu_11_0_overdrive_table',
    'struct_smu_11_0_power_saving_clock_table',
    'struct_smu_11_0_powerplay_table']
