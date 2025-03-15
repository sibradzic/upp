# -*- coding: utf-8 -*-
#
# TARGET arch is: ['--include', 'stdint.h', '--include', 'linux/drivers/gpu/drm/amd/include/atom-types.h', '--include', 'linux/drivers/gpu/drm/amd/include/atomfirmware.h', '--include', 'linux/drivers/gpu/drm/amd/pm/swsmu/inc/pmfw_if/smu14_driver_if_v14_0.h', '']
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





SMU_14_0_2_PPTABLE_H = True # macro
SMU_14_0_2_TABLE_FORMAT_REVISION = 23 # macro
SMU_14_0_2_CUSTOM_TABLE_FORMAT_REVISION = 1 # macro
SMU_14_0_2_PP_PLATFORM_CAP_POWERPLAY = 0x1 # macro
SMU_14_0_2_PP_PLATFORM_CAP_SBIOSPOWERSOURCE = 0x2 # macro
SMU_14_0_2_PP_PLATFORM_CAP_HARDWAREDC = 0x4 # macro
SMU_14_0_2_PP_PLATFORM_CAP_BACO = 0x8 # macro
SMU_14_0_2_PP_PLATFORM_CAP_MACO = 0x10 # macro
SMU_14_0_2_PP_PLATFORM_CAP_SHADOWPSTATE = 0x20 # macro
SMU_14_0_2_PP_PLATFORM_CAP_LEDSUPPORTED = 0x40 # macro
SMU_14_0_2_PP_PLATFORM_CAP_MOBILEOVERDRIVE = 0x80 # macro
SMU_14_0_2_PP_THERMALCONTROLLER_NONE = 0 # macro
SMU_14_0_2_PP_OVERDRIVE_VERSION = 0x1 # macro
SMU_14_0_2_PP_CUSTOM_OVERDRIVE_VERSION = 0x1 # macro
SMU_14_0_2_PP_POWERSAVINGCLOCK_VERSION = 0x01 # macro
SMU_14_0_2_MAX_ODFEATURE = 32 # macro
SMU_14_0_2_MAX_ODSETTING = 64 # macro
SMU_14_0_2_MAX_PMSETTING = 32 # macro

# values for enumeration 'SMU_14_0_2_OD_SW_FEATURE_CAP'
SMU_14_0_2_OD_SW_FEATURE_CAP__enumvalues = {
    0: 'SMU_14_0_2_ODCAP_AUTO_FAN_ACOUSTIC_LIMIT',
    1: 'SMU_14_0_2_ODCAP_POWER_MODE',
    2: 'SMU_14_0_2_ODCAP_AUTO_UV_ENGINE',
    3: 'SMU_14_0_2_ODCAP_AUTO_OC_ENGINE',
    4: 'SMU_14_0_2_ODCAP_AUTO_OC_MEMORY',
    5: 'SMU_14_0_2_ODCAP_MEMORY_TIMING_TUNE',
    6: 'SMU_14_0_2_ODCAP_MANUAL_AC_TIMING',
    7: 'SMU_14_0_2_ODCAP_AUTO_VF_CURVE_OPTIMIZER',
    8: 'SMU_14_0_2_ODCAP_AUTO_SOC_UV',
    9: 'SMU_14_0_2_ODCAP_COUNT',
}
SMU_14_0_2_ODCAP_AUTO_FAN_ACOUSTIC_LIMIT = 0
SMU_14_0_2_ODCAP_POWER_MODE = 1
SMU_14_0_2_ODCAP_AUTO_UV_ENGINE = 2
SMU_14_0_2_ODCAP_AUTO_OC_ENGINE = 3
SMU_14_0_2_ODCAP_AUTO_OC_MEMORY = 4
SMU_14_0_2_ODCAP_MEMORY_TIMING_TUNE = 5
SMU_14_0_2_ODCAP_MANUAL_AC_TIMING = 6
SMU_14_0_2_ODCAP_AUTO_VF_CURVE_OPTIMIZER = 7
SMU_14_0_2_ODCAP_AUTO_SOC_UV = 8
SMU_14_0_2_ODCAP_COUNT = 9
SMU_14_0_2_OD_SW_FEATURE_CAP = ctypes.c_uint32 # enum

# values for enumeration 'SMU_14_0_2_OD_SW_FEATURE_ID'
SMU_14_0_2_OD_SW_FEATURE_ID__enumvalues = {
    1: 'SMU_14_0_2_ODFEATURE_AUTO_FAN_ACOUSTIC_LIMIT',
    2: 'SMU_14_0_2_ODFEATURE_POWER_MODE',
    4: 'SMU_14_0_2_ODFEATURE_AUTO_UV_ENGINE',
    8: 'SMU_14_0_2_ODFEATURE_AUTO_OC_ENGINE',
    16: 'SMU_14_0_2_ODFEATURE_AUTO_OC_MEMORY',
    32: 'SMU_14_0_2_ODFEATURE_MEMORY_TIMING_TUNE',
    64: 'SMU_14_0_2_ODFEATURE_MANUAL_AC_TIMING',
    128: 'SMU_14_0_2_ODFEATURE_AUTO_VF_CURVE_OPTIMIZER',
    256: 'SMU_14_0_2_ODFEATURE_AUTO_SOC_UV',
}
SMU_14_0_2_ODFEATURE_AUTO_FAN_ACOUSTIC_LIMIT = 1
SMU_14_0_2_ODFEATURE_POWER_MODE = 2
SMU_14_0_2_ODFEATURE_AUTO_UV_ENGINE = 4
SMU_14_0_2_ODFEATURE_AUTO_OC_ENGINE = 8
SMU_14_0_2_ODFEATURE_AUTO_OC_MEMORY = 16
SMU_14_0_2_ODFEATURE_MEMORY_TIMING_TUNE = 32
SMU_14_0_2_ODFEATURE_MANUAL_AC_TIMING = 64
SMU_14_0_2_ODFEATURE_AUTO_VF_CURVE_OPTIMIZER = 128
SMU_14_0_2_ODFEATURE_AUTO_SOC_UV = 256
SMU_14_0_2_OD_SW_FEATURE_ID = ctypes.c_uint32 # enum

# values for enumeration 'SMU_14_0_2_OD_SW_FEATURE_SETTING_ID'
SMU_14_0_2_OD_SW_FEATURE_SETTING_ID__enumvalues = {
    0: 'SMU_14_0_2_ODSETTING_AUTO_FAN_ACOUSTIC_LIMIT',
    1: 'SMU_14_0_2_ODSETTING_POWER_MODE',
    2: 'SMU_14_0_2_ODSETTING_AUTOUVENGINE',
    3: 'SMU_14_0_2_ODSETTING_AUTOOCENGINE',
    4: 'SMU_14_0_2_ODSETTING_AUTOOCMEMORY',
    5: 'SMU_14_0_2_ODSETTING_ACTIMING',
    6: 'SMU_14_0_2_ODSETTING_MANUAL_AC_TIMING',
    7: 'SMU_14_0_2_ODSETTING_AUTO_VF_CURVE_OPTIMIZER',
    8: 'SMU_14_0_2_ODSETTING_AUTO_SOC_UV',
    9: 'SMU_14_0_2_ODSETTING_COUNT',
}
SMU_14_0_2_ODSETTING_AUTO_FAN_ACOUSTIC_LIMIT = 0
SMU_14_0_2_ODSETTING_POWER_MODE = 1
SMU_14_0_2_ODSETTING_AUTOUVENGINE = 2
SMU_14_0_2_ODSETTING_AUTOOCENGINE = 3
SMU_14_0_2_ODSETTING_AUTOOCMEMORY = 4
SMU_14_0_2_ODSETTING_ACTIMING = 5
SMU_14_0_2_ODSETTING_MANUAL_AC_TIMING = 6
SMU_14_0_2_ODSETTING_AUTO_VF_CURVE_OPTIMIZER = 7
SMU_14_0_2_ODSETTING_AUTO_SOC_UV = 8
SMU_14_0_2_ODSETTING_COUNT = 9
SMU_14_0_2_OD_SW_FEATURE_SETTING_ID = ctypes.c_uint32 # enum

# values for enumeration 'SMU_14_0_2_PWRMODE_SETTING'
SMU_14_0_2_PWRMODE_SETTING__enumvalues = {
    0: 'SMU_14_0_2_PMSETTING_POWER_LIMIT_QUIET',
    1: 'SMU_14_0_2_PMSETTING_POWER_LIMIT_BALANCE',
    2: 'SMU_14_0_2_PMSETTING_POWER_LIMIT_TURBO',
    3: 'SMU_14_0_2_PMSETTING_POWER_LIMIT_RAGE',
    4: 'SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_QUIET',
    5: 'SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_BALANCE',
    6: 'SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_TURBO',
    7: 'SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_RAGE',
    8: 'SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_QUIET',
    9: 'SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_BALANCE',
    10: 'SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_TURBO',
    11: 'SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_RAGE',
    12: 'SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_QUIET',
    13: 'SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_BALANCE',
    14: 'SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_TURBO',
    15: 'SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_RAGE',
    16: 'SMU_14_0_2_PMSETTING_COUNT',
}
SMU_14_0_2_PMSETTING_POWER_LIMIT_QUIET = 0
SMU_14_0_2_PMSETTING_POWER_LIMIT_BALANCE = 1
SMU_14_0_2_PMSETTING_POWER_LIMIT_TURBO = 2
SMU_14_0_2_PMSETTING_POWER_LIMIT_RAGE = 3
SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_QUIET = 4
SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_BALANCE = 5
SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_TURBO = 6
SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_RAGE = 7
SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_QUIET = 8
SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_BALANCE = 9
SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_TURBO = 10
SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_RAGE = 11
SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_QUIET = 12
SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_BALANCE = 13
SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_TURBO = 14
SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_RAGE = 15
SMU_14_0_2_PMSETTING_COUNT = 16
SMU_14_0_2_PWRMODE_SETTING = ctypes.c_uint32 # enum

# values for enumeration 'SMU_14_0_2_overdrive_table_id'
SMU_14_0_2_overdrive_table_id__enumvalues = {
    0: 'SMU_14_0_2_OVERDRIVE_TABLE_BASIC',
    1: 'SMU_14_0_2_OVERDRIVE_TABLE_ADVANCED',
    2: 'SMU_14_0_2_OVERDRIVE_TABLE_COUNT',
}
SMU_14_0_2_OVERDRIVE_TABLE_BASIC = 0
SMU_14_0_2_OVERDRIVE_TABLE_ADVANCED = 1
SMU_14_0_2_OVERDRIVE_TABLE_COUNT = 2
SMU_14_0_2_overdrive_table_id = ctypes.c_uint32 # enum
class struct_smu_14_0_2_overdrive_table(Structure):
    pass

struct_smu_14_0_2_overdrive_table._pack_ = 1 # source:False
struct_smu_14_0_2_overdrive_table._fields_ = [
    ('revision', ctypes.c_ubyte),
    ('reserve', ctypes.c_ubyte * 3),
    ('cap', ctypes.c_ubyte * 32 * 2),
    ('max', ctypes.c_int32 * 64 * 2),
    ('min', ctypes.c_int32 * 64 * 2),
    ('pm_setting', ctypes.c_int16 * 32),
]


# values for enumeration 'smu_14_0_3_pptable_source'
smu_14_0_3_pptable_source__enumvalues = {
    0: 'PPTABLE_SOURCE_IFWI',
    1: 'PPTABLE_SOURCE_DRIVER_HARDCODED',
    2: 'PPTABLE_SOURCE_PPGEN_REGISTRY',
    2: 'PPTABLE_SOURCE_MAX',
}
PPTABLE_SOURCE_IFWI = 0
PPTABLE_SOURCE_DRIVER_HARDCODED = 1
PPTABLE_SOURCE_PPGEN_REGISTRY = 2
PPTABLE_SOURCE_MAX = 2
smu_14_0_3_pptable_source = ctypes.c_uint32 # enum
class struct_smu_14_0_2_powerplay_table(Structure):
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

class struct_PFE_Settings_t(Structure):
    pass

struct_PFE_Settings_t._pack_ = 1 # source:False
struct_PFE_Settings_t._fields_ = [
    ('Version', ctypes.c_ubyte),
    ('Spare8', ctypes.c_ubyte * 3),
    ('FeaturesToRun', ctypes.c_uint32 * 2),
    ('FwDStateMask', ctypes.c_uint32),
    ('DebugOverrides', ctypes.c_uint32),
    ('Spare', ctypes.c_uint32 * 2),
]

class struct_SkuTable_t(Structure):
    pass

class struct_QuadraticInt_t(Structure):
    pass

struct_QuadraticInt_t._pack_ = 1 # source:False
struct_QuadraticInt_t._fields_ = [
    ('a', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
    ('c', ctypes.c_uint32),
]

class struct_DpmDescriptor_t(Structure):
    pass

class struct_LinearInt_t(Structure):
    pass

struct_LinearInt_t._pack_ = 1 # source:False
struct_LinearInt_t._fields_ = [
    ('m', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
]

struct_DpmDescriptor_t._pack_ = 1 # source:False
struct_DpmDescriptor_t._fields_ = [
    ('Padding', ctypes.c_ubyte),
    ('SnapToDiscrete', ctypes.c_ubyte),
    ('NumDiscreteLevels', ctypes.c_ubyte),
    ('CalculateFopt', ctypes.c_ubyte),
    ('ConversionToAvfsClk', struct_LinearInt_t),
    ('Padding3', ctypes.c_uint32 * 3),
    ('Padding4', ctypes.c_uint16),
    ('FoptimalDc', ctypes.c_uint16),
    ('FoptimalAc', ctypes.c_uint16),
    ('Padding2', ctypes.c_uint16),
]

class struct_AvfsDcBtcParams_t(Structure):
    pass

struct_AvfsDcBtcParams_t._pack_ = 1 # source:False
struct_AvfsDcBtcParams_t._fields_ = [
    ('DcBtcEnabled', ctypes.c_ubyte),
    ('Padding', ctypes.c_ubyte * 3),
    ('DcTol', ctypes.c_uint16),
    ('DcBtcGb', ctypes.c_uint16),
    ('DcBtcMin', ctypes.c_uint16),
    ('DcBtcMax', ctypes.c_uint16),
    ('DcBtcGbScalar', struct_LinearInt_t),
]

class struct_AvfsFuseOverride_t(Structure):
    pass

struct_AvfsFuseOverride_t._pack_ = 1 # source:False
struct_AvfsFuseOverride_t._fields_ = [
    ('AvfsTemp', ctypes.c_uint16 * 2),
    ('VftFMin', ctypes.c_uint16),
    ('VInversion', ctypes.c_uint16),
    ('qVft', struct_QuadraticInt_t * 2),
    ('qAvfsGb', struct_QuadraticInt_t),
    ('qAvfsGb2', struct_QuadraticInt_t),
]

class struct_DroopInt_t(Structure):
    pass

struct_DroopInt_t._pack_ = 1 # source:False
struct_DroopInt_t._fields_ = [
    ('a', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
    ('c', ctypes.c_uint32),
]

class struct_BootValues_t(Structure):
    pass

struct_BootValues_t._pack_ = 1 # source:False
struct_BootValues_t._fields_ = [
    ('InitImuClk', ctypes.c_uint16),
    ('InitSocclk', ctypes.c_uint16),
    ('InitMpioclk', ctypes.c_uint16),
    ('InitSmnclk', ctypes.c_uint16),
    ('InitDispClk', ctypes.c_uint16),
    ('InitDppClk', ctypes.c_uint16),
    ('InitDprefclk', ctypes.c_uint16),
    ('InitDcfclk', ctypes.c_uint16),
    ('InitDtbclk', ctypes.c_uint16),
    ('InitDbguSocClk', ctypes.c_uint16),
    ('InitGfxclk_bypass', ctypes.c_uint16),
    ('InitMp1clk', ctypes.c_uint16),
    ('InitLclk', ctypes.c_uint16),
    ('InitDbguBacoClk', ctypes.c_uint16),
    ('InitBaco400clk', ctypes.c_uint16),
    ('InitBaco1200clk_bypass', ctypes.c_uint16),
    ('InitBaco700clk_bypass', ctypes.c_uint16),
    ('InitBaco500clk', ctypes.c_uint16),
    ('InitDclk0', ctypes.c_uint16),
    ('InitVclk0', ctypes.c_uint16),
    ('InitFclk', ctypes.c_uint16),
    ('Padding1', ctypes.c_uint16),
    ('InitUclkLevel', ctypes.c_ubyte),
    ('Padding', ctypes.c_ubyte * 3),
    ('InitVcoFreqPll0', ctypes.c_uint32),
    ('InitVcoFreqPll1', ctypes.c_uint32),
    ('InitVcoFreqPll2', ctypes.c_uint32),
    ('InitVcoFreqPll3', ctypes.c_uint32),
    ('InitVcoFreqPll4', ctypes.c_uint32),
    ('InitVcoFreqPll5', ctypes.c_uint32),
    ('InitVcoFreqPll6', ctypes.c_uint32),
    ('InitVcoFreqPll7', ctypes.c_uint32),
    ('InitVcoFreqPll8', ctypes.c_uint32),
    ('InitGfx', ctypes.c_uint16),
    ('InitSoc', ctypes.c_uint16),
    ('InitVddIoMem', ctypes.c_uint16),
    ('InitVddCiMem', ctypes.c_uint16),
    ('Spare', ctypes.c_uint32 * 8),
]

class struct_DriverReportedClocks_t(Structure):
    pass

struct_DriverReportedClocks_t._pack_ = 1 # source:False
struct_DriverReportedClocks_t._fields_ = [
    ('BaseClockAc', ctypes.c_uint16),
    ('GameClockAc', ctypes.c_uint16),
    ('BoostClockAc', ctypes.c_uint16),
    ('BaseClockDc', ctypes.c_uint16),
    ('GameClockDc', ctypes.c_uint16),
    ('BoostClockDc', ctypes.c_uint16),
    ('MaxReportedClock', ctypes.c_uint16),
    ('Padding', ctypes.c_uint16),
    ('Reserved', ctypes.c_uint32 * 3),
]

class struct_MsgLimits_t(Structure):
    pass

struct_MsgLimits_t._pack_ = 1 # source:False
struct_MsgLimits_t._fields_ = [
    ('Power', ctypes.c_uint16 * 2 * 4),
    ('Tdc', ctypes.c_uint16 * 2),
    ('Temperature', ctypes.c_uint16 * 12),
    ('PwmLimitMin', ctypes.c_ubyte),
    ('PwmLimitMax', ctypes.c_ubyte),
    ('FanTargetTemperature', ctypes.c_ubyte),
    ('Spare1', ctypes.c_ubyte * 1),
    ('AcousticTargetRpmThresholdMin', ctypes.c_uint16),
    ('AcousticTargetRpmThresholdMax', ctypes.c_uint16),
    ('AcousticLimitRpmThresholdMin', ctypes.c_uint16),
    ('AcousticLimitRpmThresholdMax', ctypes.c_uint16),
    ('PccLimitMin', ctypes.c_uint16),
    ('PccLimitMax', ctypes.c_uint16),
    ('FanStopTempMin', ctypes.c_uint16),
    ('FanStopTempMax', ctypes.c_uint16),
    ('FanStartTempMin', ctypes.c_uint16),
    ('FanStartTempMax', ctypes.c_uint16),
    ('PowerMinPpt0', ctypes.c_uint16 * 2),
    ('Spare', ctypes.c_uint32 * 11),
]

class struct_OverDriveLimits_t(Structure):
    pass

struct_OverDriveLimits_t._pack_ = 1 # source:False
struct_OverDriveLimits_t._fields_ = [
    ('FeatureCtrlMask', ctypes.c_uint32),
    ('VoltageOffsetPerZoneBoundary', ctypes.c_int16 * 6),
    ('VddGfxVmax', ctypes.c_uint16),
    ('VddSocVmax', ctypes.c_uint16),
    ('GfxclkFoffset', ctypes.c_int16),
    ('Padding', ctypes.c_uint16),
    ('UclkFmin', ctypes.c_uint16),
    ('UclkFmax', ctypes.c_uint16),
    ('FclkFmin', ctypes.c_uint16),
    ('FclkFmax', ctypes.c_uint16),
    ('Ppt', ctypes.c_int16),
    ('Tdc', ctypes.c_int16),
    ('FanLinearPwmPoints', ctypes.c_ubyte * 6),
    ('FanLinearTempPoints', ctypes.c_ubyte * 6),
    ('FanMinimumPwm', ctypes.c_uint16),
    ('AcousticTargetRpmThreshold', ctypes.c_uint16),
    ('AcousticLimitRpmThreshold', ctypes.c_uint16),
    ('FanTargetTemperature', ctypes.c_uint16),
    ('FanZeroRpmEnable', ctypes.c_ubyte),
    ('MaxOpTemp', ctypes.c_ubyte),
    ('Padding1', ctypes.c_ubyte * 2),
    ('GfxVoltageFullCtrlMode', ctypes.c_uint16),
    ('SocVoltageFullCtrlMode', ctypes.c_uint16),
    ('GfxclkFullCtrlMode', ctypes.c_uint16),
    ('UclkFullCtrlMode', ctypes.c_uint16),
    ('FclkFullCtrlMode', ctypes.c_uint16),
    ('GfxEdc', ctypes.c_int16),
    ('GfxPccLimitControl', ctypes.c_int16),
    ('Padding2', ctypes.c_int16),
    ('Spare', ctypes.c_uint32 * 5),
]

struct_SkuTable_t._pack_ = 1 # source:False
struct_SkuTable_t._fields_ = [
    ('Version', ctypes.c_uint32),
    ('TotalPowerConfig', ctypes.c_ubyte),
    ('CustomerVariant', ctypes.c_ubyte),
    ('MemoryTemperatureTypeMask', ctypes.c_ubyte),
    ('SmartShiftVersion', ctypes.c_ubyte),
    ('SocketPowerLimitSpare', ctypes.c_ubyte * 10),
    ('EnableLegacyPptLimit', ctypes.c_ubyte),
    ('UseInputTelemetry', ctypes.c_ubyte),
    ('SmartShiftMinReportedPptinDcs', ctypes.c_ubyte),
    ('PaddingPpt', ctypes.c_ubyte * 7),
    ('HwCtfTempLimit', ctypes.c_uint16),
    ('PaddingInfra', ctypes.c_uint16),
    ('FitControllerFailureRateLimit', ctypes.c_uint32),
    ('FitControllerGfxDutyCycle', ctypes.c_uint32),
    ('FitControllerSocDutyCycle', ctypes.c_uint32),
    ('FitControllerSocOffset', ctypes.c_uint32),
    ('GfxApccPlusResidencyLimit', ctypes.c_uint32),
    ('ThrottlerControlMask', ctypes.c_uint32),
    ('UlvVoltageOffset', ctypes.c_uint16 * 2),
    ('Padding', ctypes.c_ubyte * 2),
    ('DeepUlvVoltageOffsetSoc', ctypes.c_uint16),
    ('DefaultMaxVoltage', ctypes.c_uint16 * 2),
    ('BoostMaxVoltage', ctypes.c_uint16 * 2),
    ('VminTempHystersis', ctypes.c_int16 * 2),
    ('VminTempThreshold', ctypes.c_int16 * 2),
    ('Vmin_Hot_T0', ctypes.c_uint16 * 2),
    ('Vmin_Cold_T0', ctypes.c_uint16 * 2),
    ('Vmin_Hot_Eol', ctypes.c_uint16 * 2),
    ('Vmin_Cold_Eol', ctypes.c_uint16 * 2),
    ('Vmin_Aging_Offset', ctypes.c_uint16 * 2),
    ('Spare_Vmin_Plat_Offset_Hot', ctypes.c_uint16 * 2),
    ('Spare_Vmin_Plat_Offset_Cold', ctypes.c_uint16 * 2),
    ('VcBtcFixedVminAgingOffset', ctypes.c_uint16 * 2),
    ('VcBtcVmin2PsmDegrationGb', ctypes.c_uint16 * 2),
    ('VcBtcPsmA', ctypes.c_uint32 * 2),
    ('VcBtcPsmB', ctypes.c_uint32 * 2),
    ('VcBtcVminA', ctypes.c_uint32 * 2),
    ('VcBtcVminB', ctypes.c_uint32 * 2),
    ('PerPartVminEnabled', ctypes.c_ubyte * 2),
    ('VcBtcEnabled', ctypes.c_ubyte * 2),
    ('SocketPowerLimitAcTau', ctypes.c_uint16 * 4),
    ('SocketPowerLimitDcTau', ctypes.c_uint16 * 4),
    ('Gfx_Vmin_droop', struct_QuadraticInt_t),
    ('Soc_Vmin_droop', struct_QuadraticInt_t),
    ('SpareVmin', ctypes.c_uint32 * 6),
    ('DpmDescriptor', struct_DpmDescriptor_t * 11),
    ('FreqTableGfx', ctypes.c_uint16 * 16),
    ('FreqTableVclk', ctypes.c_uint16 * 8),
    ('FreqTableDclk', ctypes.c_uint16 * 8),
    ('FreqTableSocclk', ctypes.c_uint16 * 8),
    ('FreqTableUclk', ctypes.c_uint16 * 6),
    ('FreqTableShadowUclk', ctypes.c_uint16 * 6),
    ('FreqTableDispclk', ctypes.c_uint16 * 8),
    ('FreqTableDppClk', ctypes.c_uint16 * 8),
    ('FreqTableDprefclk', ctypes.c_uint16 * 8),
    ('FreqTableDcfclk', ctypes.c_uint16 * 8),
    ('FreqTableDtbclk', ctypes.c_uint16 * 8),
    ('FreqTableFclk', ctypes.c_uint16 * 8),
    ('DcModeMaxFreq', ctypes.c_uint32 * 11),
    ('GfxclkAibFmax', ctypes.c_uint16),
    ('GfxDpmPadding', ctypes.c_uint16),
    ('GfxclkFgfxoffEntry', ctypes.c_uint16),
    ('GfxclkFgfxoffExitImu', ctypes.c_uint16),
    ('GfxclkFgfxoffExitRlc', ctypes.c_uint16),
    ('GfxclkThrottleClock', ctypes.c_uint16),
    ('EnableGfxPowerStagesGpio', ctypes.c_ubyte),
    ('GfxIdlePadding', ctypes.c_ubyte),
    ('SmsRepairWRCKClkDivEn', ctypes.c_ubyte),
    ('SmsRepairWRCKClkDivVal', ctypes.c_ubyte),
    ('GfxOffEntryEarlyMGCGEn', ctypes.c_ubyte),
    ('GfxOffEntryForceCGCGEn', ctypes.c_ubyte),
    ('GfxOffEntryForceCGCGDelayEn', ctypes.c_ubyte),
    ('GfxOffEntryForceCGCGDelayVal', ctypes.c_ubyte),
    ('GfxclkFreqGfxUlv', ctypes.c_uint16),
    ('GfxIdlePadding2', ctypes.c_ubyte * 2),
    ('GfxOffEntryHysteresis', ctypes.c_uint32),
    ('GfxoffSpare', ctypes.c_uint32 * 15),
    ('DfllMstrOscConfigA', ctypes.c_uint16),
    ('DfllSlvOscConfigA', ctypes.c_uint16),
    ('DfllBtcMasterScalerM', ctypes.c_uint32),
    ('DfllBtcMasterScalerB', ctypes.c_int32),
    ('DfllBtcSlaveScalerM', ctypes.c_uint32),
    ('DfllBtcSlaveScalerB', ctypes.c_int32),
    ('DfllPccAsWaitCtrl', ctypes.c_uint32),
    ('DfllPccAsStepCtrl', ctypes.c_uint32),
    ('GfxDfllSpare', ctypes.c_uint32 * 9),
    ('DvoPsmDownThresholdVoltage', ctypes.c_uint32),
    ('DvoPsmUpThresholdVoltage', ctypes.c_uint32),
    ('DvoFmaxLowScaler', ctypes.c_uint32),
    ('PaddingDcs', ctypes.c_uint32),
    ('DcsMinGfxOffTime', ctypes.c_uint16),
    ('DcsMaxGfxOffTime', ctypes.c_uint16),
    ('DcsMinCreditAccum', ctypes.c_uint32),
    ('DcsExitHysteresis', ctypes.c_uint16),
    ('DcsTimeout', ctypes.c_uint16),
    ('DcsPfGfxFopt', ctypes.c_uint32),
    ('DcsPfUclkFopt', ctypes.c_uint32),
    ('FoptEnabled', ctypes.c_ubyte),
    ('DcsSpare2', ctypes.c_ubyte * 3),
    ('DcsFoptM', ctypes.c_uint32),
    ('DcsFoptB', ctypes.c_uint32),
    ('DcsSpare', ctypes.c_uint32 * 9),
    ('UseStrobeModeOptimizations', ctypes.c_ubyte),
    ('PaddingMem', ctypes.c_ubyte * 3),
    ('UclkDpmPstates', ctypes.c_ubyte * 6),
    ('UclkDpmShadowPstates', ctypes.c_ubyte * 6),
    ('FreqTableUclkDiv', ctypes.c_ubyte * 6),
    ('FreqTableShadowUclkDiv', ctypes.c_ubyte * 6),
    ('MemVmempVoltage', ctypes.c_uint16 * 6),
    ('MemVddioVoltage', ctypes.c_uint16 * 6),
    ('DalDcModeMaxUclkFreq', ctypes.c_uint16),
    ('PaddingsMem', ctypes.c_ubyte * 2),
    ('PaddingFclk', ctypes.c_uint32),
    ('PcieGenSpeed', ctypes.c_ubyte * 3),
    ('PcieLaneCount', ctypes.c_ubyte * 3),
    ('LclkFreq', ctypes.c_uint16 * 3),
    ('OverrideGfxAvfsFuses', ctypes.c_ubyte),
    ('GfxAvfsPadding', ctypes.c_ubyte * 1),
    ('DroopGBStDev', ctypes.c_uint16),
    ('SocHwRtAvfsFuses', ctypes.c_uint32 * 32),
    ('GfxL2HwRtAvfsFuses', ctypes.c_uint32 * 32),
    ('PsmDidt_Vcross', ctypes.c_uint16 * 2),
    ('PsmDidt_StaticDroop_A', ctypes.c_uint32 * 3),
    ('PsmDidt_StaticDroop_B', ctypes.c_uint32 * 3),
    ('PsmDidt_DynDroop_A', ctypes.c_uint32 * 3),
    ('PsmDidt_DynDroop_B', ctypes.c_uint32 * 3),
    ('spare_HwRtAvfsFuses', ctypes.c_uint32 * 19),
    ('SocCommonRtAvfs', ctypes.c_uint32 * 13),
    ('GfxCommonRtAvfs', ctypes.c_uint32 * 13),
    ('SocFwRtAvfsFuses', ctypes.c_uint32 * 19),
    ('GfxL2FwRtAvfsFuses', ctypes.c_uint32 * 19),
    ('spare_FwRtAvfsFuses', ctypes.c_uint32 * 19),
    ('Soc_Droop_PWL_F', ctypes.c_uint32 * 5),
    ('Soc_Droop_PWL_a', ctypes.c_uint32 * 5),
    ('Soc_Droop_PWL_b', ctypes.c_uint32 * 5),
    ('Soc_Droop_PWL_c', ctypes.c_uint32 * 5),
    ('Gfx_Droop_PWL_F', ctypes.c_uint32 * 5),
    ('Gfx_Droop_PWL_a', ctypes.c_uint32 * 5),
    ('Gfx_Droop_PWL_b', ctypes.c_uint32 * 5),
    ('Gfx_Droop_PWL_c', ctypes.c_uint32 * 5),
    ('Gfx_Static_PWL_Offset', ctypes.c_uint32 * 5),
    ('Soc_Static_PWL_Offset', ctypes.c_uint32 * 5),
    ('dGbV_dT_vmin', ctypes.c_uint32),
    ('dGbV_dT_vmax', ctypes.c_uint32),
    ('PaddingV2F', ctypes.c_uint32 * 4),
    ('DcBtcGfxParams', struct_AvfsDcBtcParams_t),
    ('SSCurve_GFX', struct_QuadraticInt_t),
    ('GfxAvfsSpare', ctypes.c_uint32 * 29),
    ('OverrideSocAvfsFuses', ctypes.c_ubyte),
    ('MinSocAvfsRevision', ctypes.c_ubyte),
    ('SocAvfsPadding', ctypes.c_ubyte * 2),
    ('SocAvfsFuseOverride', struct_AvfsFuseOverride_t * 1),
    ('dBtcGbSoc', struct_DroopInt_t * 1),
    ('qAgingGb', struct_LinearInt_t * 1),
    ('qStaticVoltageOffset', struct_QuadraticInt_t * 1),
    ('DcBtcSocParams', struct_AvfsDcBtcParams_t * 1),
    ('SSCurve_SOC', struct_QuadraticInt_t),
    ('SocAvfsSpare', ctypes.c_uint32 * 29),
    ('BootValues', struct_BootValues_t),
    ('DriverReportedClocks', struct_DriverReportedClocks_t),
    ('MsgLimits', struct_MsgLimits_t),
    ('OverDriveLimitsBasicMin', struct_OverDriveLimits_t),
    ('OverDriveLimitsBasicMax', struct_OverDriveLimits_t),
    ('OverDriveLimitsAdvancedMin', struct_OverDriveLimits_t),
    ('OverDriveLimitsAdvancedMax', struct_OverDriveLimits_t),
    ('TotalBoardPowerSupport', ctypes.c_ubyte),
    ('TotalBoardPowerPadding', ctypes.c_ubyte * 1),
    ('TotalBoardPowerRoc', ctypes.c_uint16),
    ('qFeffCoeffGameClock', struct_QuadraticInt_t * 2),
    ('qFeffCoeffBaseClock', struct_QuadraticInt_t * 2),
    ('qFeffCoeffBoostClock', struct_QuadraticInt_t * 2),
    ('AptUclkGfxclkLookup', ctypes.c_int32 * 6 * 2),
    ('AptUclkGfxclkLookupHyst', ctypes.c_uint32 * 6 * 2),
    ('AptPadding', ctypes.c_uint32),
    ('GfxXvminDidtDroopThresh', struct_QuadraticInt_t),
    ('GfxXvminDidtResetDDWait', ctypes.c_uint32),
    ('GfxXvminDidtClkStopWait', ctypes.c_uint32),
    ('GfxXvminDidtFcsStepCtrl', ctypes.c_uint32),
    ('GfxXvminDidtFcsWaitCtrl', ctypes.c_uint32),
    ('PsmModeEnabled', ctypes.c_uint32),
    ('P2v_a', ctypes.c_uint32),
    ('P2v_b', ctypes.c_uint32),
    ('P2v_c', ctypes.c_uint32),
    ('T2p_a', ctypes.c_uint32),
    ('T2p_b', ctypes.c_uint32),
    ('T2p_c', ctypes.c_uint32),
    ('P2vTemp', ctypes.c_uint32),
    ('PsmDidtStaticSettings', struct_QuadraticInt_t),
    ('PsmDidtDynamicSettings', struct_QuadraticInt_t),
    ('PsmDidtAvgDiv', ctypes.c_ubyte),
    ('PsmDidtForceStall', ctypes.c_ubyte),
    ('PsmDidtReleaseTimer', ctypes.c_uint16),
    ('PsmDidtStallPattern', ctypes.c_uint32),
    ('CacEdcCacLeakageC0', ctypes.c_uint32),
    ('CacEdcCacLeakageC1', ctypes.c_uint32),
    ('CacEdcCacLeakageC2', ctypes.c_uint32),
    ('CacEdcCacLeakageC3', ctypes.c_uint32),
    ('CacEdcCacLeakageC4', ctypes.c_uint32),
    ('CacEdcCacLeakageC5', ctypes.c_uint32),
    ('CacEdcGfxClkScalar', ctypes.c_uint32),
    ('CacEdcGfxClkIntercept', ctypes.c_uint32),
    ('CacEdcCac_m', ctypes.c_uint32),
    ('CacEdcCac_b', ctypes.c_uint32),
    ('CacEdcCurrLimitGuardband', ctypes.c_uint32),
    ('CacEdcDynToTotalCacRatio', ctypes.c_uint32),
    ('XVmin_Gfx_EdcThreshScalar', ctypes.c_uint32),
    ('XVmin_Gfx_EdcEnableFreq', ctypes.c_uint32),
    ('XVmin_Gfx_EdcPccAsStepCtrl', ctypes.c_uint32),
    ('XVmin_Gfx_EdcPccAsWaitCtrl', ctypes.c_uint32),
    ('XVmin_Gfx_EdcThreshold', ctypes.c_uint16),
    ('XVmin_Gfx_EdcFiltHysWaitCtrl', ctypes.c_uint16),
    ('XVmin_Soc_EdcThreshScalar', ctypes.c_uint32),
    ('XVmin_Soc_EdcEnableFreq', ctypes.c_uint32),
    ('XVmin_Soc_EdcThreshold', ctypes.c_uint32),
    ('XVmin_Soc_EdcStepUpTime', ctypes.c_uint16),
    ('XVmin_Soc_EdcStepDownTime', ctypes.c_uint16),
    ('XVmin_Soc_EdcInitPccStep', ctypes.c_ubyte),
    ('PaddingSocEdc', ctypes.c_ubyte * 3),
    ('GfxXvminFuseOverride', ctypes.c_ubyte),
    ('SocXvminFuseOverride', ctypes.c_ubyte),
    ('PaddingXvminFuseOverride', ctypes.c_ubyte * 2),
    ('GfxXvminFddTempLow', ctypes.c_ubyte),
    ('GfxXvminFddTempHigh', ctypes.c_ubyte),
    ('SocXvminFddTempLow', ctypes.c_ubyte),
    ('SocXvminFddTempHigh', ctypes.c_ubyte),
    ('GfxXvminFddVolt0', ctypes.c_uint16),
    ('GfxXvminFddVolt1', ctypes.c_uint16),
    ('GfxXvminFddVolt2', ctypes.c_uint16),
    ('SocXvminFddVolt0', ctypes.c_uint16),
    ('SocXvminFddVolt1', ctypes.c_uint16),
    ('SocXvminFddVolt2', ctypes.c_uint16),
    ('GfxXvminDsFddDsm', ctypes.c_uint16 * 6),
    ('GfxXvminEdcFddDsm', ctypes.c_uint16 * 6),
    ('SocXvminEdcFddDsm', ctypes.c_uint16 * 6),
    ('Spare', ctypes.c_uint32),
    ('MmHubPadding', ctypes.c_uint32 * 8),
]

class struct_CustomSkuTable_t(Structure):
    pass

struct_CustomSkuTable_t._pack_ = 1 # source:False
struct_CustomSkuTable_t._fields_ = [
    ('SocketPowerLimitAc', ctypes.c_uint16 * 4),
    ('VrTdcLimit', ctypes.c_uint16 * 2),
    ('TotalIdleBoardPowerM', ctypes.c_int16),
    ('TotalIdleBoardPowerB', ctypes.c_int16),
    ('TotalBoardPowerM', ctypes.c_int16),
    ('TotalBoardPowerB', ctypes.c_int16),
    ('TemperatureLimit', ctypes.c_uint16 * 12),
    ('FanStopTemp', ctypes.c_uint16 * 12),
    ('FanStartTemp', ctypes.c_uint16 * 12),
    ('FanGain', ctypes.c_uint16 * 12),
    ('FanPwmMin', ctypes.c_uint16),
    ('AcousticTargetRpmThreshold', ctypes.c_uint16),
    ('AcousticLimitRpmThreshold', ctypes.c_uint16),
    ('FanMaximumRpm', ctypes.c_uint16),
    ('MGpuAcousticLimitRpmThreshold', ctypes.c_uint16),
    ('FanTargetGfxclk', ctypes.c_uint16),
    ('TempInputSelectMask', ctypes.c_uint32),
    ('FanZeroRpmEnable', ctypes.c_ubyte),
    ('FanTachEdgePerRev', ctypes.c_ubyte),
    ('FanPadding', ctypes.c_uint16),
    ('FanTargetTemperature', ctypes.c_uint16 * 12),
    ('FuzzyFan_ErrorSetDelta', ctypes.c_int16),
    ('FuzzyFan_ErrorRateSetDelta', ctypes.c_int16),
    ('FuzzyFan_PwmSetDelta', ctypes.c_int16),
    ('FanPadding2', ctypes.c_uint16),
    ('FwCtfLimit', ctypes.c_uint16 * 12),
    ('IntakeTempEnableRPM', ctypes.c_uint16),
    ('IntakeTempOffsetTemp', ctypes.c_int16),
    ('IntakeTempReleaseTemp', ctypes.c_uint16),
    ('IntakeTempHighIntakeAcousticLimit', ctypes.c_uint16),
    ('IntakeTempAcouticLimitReleaseRate', ctypes.c_uint16),
    ('FanAbnormalTempLimitOffset', ctypes.c_int16),
    ('FanStalledTriggerRpm', ctypes.c_uint16),
    ('FanAbnormalTriggerRpmCoeff', ctypes.c_uint16),
    ('FanSpare', ctypes.c_uint16 * 1),
    ('FanIntakeSensorSupport', ctypes.c_ubyte),
    ('FanIntakePadding', ctypes.c_ubyte),
    ('FanSpare2', ctypes.c_uint32 * 12),
    ('ODFeatureCtrlMask', ctypes.c_uint32),
    ('TemperatureLimit_Hynix', ctypes.c_uint16),
    ('TemperatureLimit_Micron', ctypes.c_uint16),
    ('TemperatureFwCtfLimit_Hynix', ctypes.c_uint16),
    ('TemperatureFwCtfLimit_Micron', ctypes.c_uint16),
    ('PlatformTdcLimit', ctypes.c_uint16 * 2),
    ('SocketPowerLimitDc', ctypes.c_uint16 * 4),
    ('SocketPowerLimitSmartShift2', ctypes.c_uint16),
    ('CustomSkuSpare16b', ctypes.c_uint16),
    ('CustomSkuSpare32b', ctypes.c_uint32 * 10),
    ('MmHubPadding', ctypes.c_uint32 * 8),
]

class struct_BoardTable_t(Structure):
    pass

class struct_I2cControllerConfig_t(Structure):
    pass

struct_I2cControllerConfig_t._pack_ = 1 # source:False
struct_I2cControllerConfig_t._fields_ = [
    ('Enabled', ctypes.c_ubyte),
    ('Speed', ctypes.c_ubyte),
    ('SlaveAddress', ctypes.c_ubyte),
    ('ControllerPort', ctypes.c_ubyte),
    ('ControllerName', ctypes.c_ubyte),
    ('ThermalThrotter', ctypes.c_ubyte),
    ('I2cProtocol', ctypes.c_ubyte),
    ('PaddingConfig', ctypes.c_ubyte),
]

class struct_Svi3RegulatorSettings_t(Structure):
    pass

struct_Svi3RegulatorSettings_t._pack_ = 1 # source:False
struct_Svi3RegulatorSettings_t._fields_ = [
    ('SlewRateConditions', ctypes.c_ubyte),
    ('LoadLineAdjust', ctypes.c_ubyte),
    ('VoutOffset', ctypes.c_ubyte),
    ('VidMax', ctypes.c_ubyte),
    ('VidMin', ctypes.c_ubyte),
    ('TenBitTelEn', ctypes.c_ubyte),
    ('SixteenBitTelEn', ctypes.c_ubyte),
    ('OcpThresh', ctypes.c_ubyte),
    ('OcpWarnThresh', ctypes.c_ubyte),
    ('OcpSettings', ctypes.c_ubyte),
    ('VrhotThresh', ctypes.c_ubyte),
    ('OtpThresh', ctypes.c_ubyte),
    ('UvpOvpDeltaRef', ctypes.c_ubyte),
    ('PhaseShed', ctypes.c_ubyte),
    ('Padding', ctypes.c_ubyte * 10),
    ('SettingOverrideMask', ctypes.c_uint32),
]

struct_BoardTable_t._pack_ = 1 # source:False
struct_BoardTable_t._fields_ = [
    ('Version', ctypes.c_uint32),
    ('I2cControllers', struct_I2cControllerConfig_t * 8),
    ('SlaveAddrMapping', ctypes.c_ubyte * 4),
    ('VrPsiSupport', ctypes.c_ubyte * 4),
    ('Svi3SvcSpeed', ctypes.c_uint32),
    ('EnablePsi6', ctypes.c_ubyte * 4),
    ('Svi3RegSettings', struct_Svi3RegulatorSettings_t * 4),
    ('LedOffGpio', ctypes.c_ubyte),
    ('FanOffGpio', ctypes.c_ubyte),
    ('GfxVrPowerStageOffGpio', ctypes.c_ubyte),
    ('AcDcGpio', ctypes.c_ubyte),
    ('AcDcPolarity', ctypes.c_ubyte),
    ('VR0HotGpio', ctypes.c_ubyte),
    ('VR0HotPolarity', ctypes.c_ubyte),
    ('GthrGpio', ctypes.c_ubyte),
    ('GthrPolarity', ctypes.c_ubyte),
    ('LedPin0', ctypes.c_ubyte),
    ('LedPin1', ctypes.c_ubyte),
    ('LedPin2', ctypes.c_ubyte),
    ('LedEnableMask', ctypes.c_ubyte),
    ('LedPcie', ctypes.c_ubyte),
    ('LedError', ctypes.c_ubyte),
    ('PaddingLed', ctypes.c_ubyte),
    ('UclkTrainingModeSpreadPercent', ctypes.c_ubyte),
    ('UclkSpreadPadding', ctypes.c_ubyte),
    ('UclkSpreadFreq', ctypes.c_uint16),
    ('UclkSpreadPercent', ctypes.c_ubyte * 16),
    ('GfxclkSpreadEnable', ctypes.c_ubyte),
    ('FclkSpreadPercent', ctypes.c_ubyte),
    ('FclkSpreadFreq', ctypes.c_uint16),
    ('DramWidth', ctypes.c_ubyte),
    ('PaddingMem1', ctypes.c_ubyte * 7),
    ('HsrEnabled', ctypes.c_ubyte),
    ('VddqOffEnabled', ctypes.c_ubyte),
    ('PaddingUmcFlags', ctypes.c_ubyte * 2),
    ('Paddign1', ctypes.c_uint32),
    ('BacoEntryDelay', ctypes.c_uint32),
    ('FuseWritePowerMuxPresent', ctypes.c_ubyte),
    ('FuseWritePadding', ctypes.c_ubyte * 3),
    ('LoadlineGfx', ctypes.c_uint32),
    ('LoadlineSoc', ctypes.c_uint32),
    ('GfxEdcLimit', ctypes.c_uint32),
    ('SocEdcLimit', ctypes.c_uint32),
    ('RestBoardPower', ctypes.c_uint32),
    ('ConnectorsImpedance', ctypes.c_uint32),
    ('EpcsSens0', ctypes.c_ubyte),
    ('EpcsSens1', ctypes.c_ubyte),
    ('PaddingEpcs', ctypes.c_ubyte * 2),
    ('BoardSpare', ctypes.c_uint32 * 52),
    ('MmHubPadding', ctypes.c_uint32 * 8),
]

struct_PPTable_t._pack_ = 1 # source:False
struct_PPTable_t._fields_ = [
    ('PFE_Settings', struct_PFE_Settings_t),
    ('SkuTable', struct_SkuTable_t),
    ('CustomSkuTable', struct_CustomSkuTable_t),
    ('BoardTable', struct_BoardTable_t),
]

struct_smu_14_0_2_powerplay_table._pack_ = 1 # source:False
struct_smu_14_0_2_powerplay_table._fields_ = [
    ('header', struct_atom_common_table_header),
    ('table_revision', ctypes.c_ubyte),
    ('pptable_source', ctypes.c_ubyte),
    ('pmfw_pptable_start_offset', ctypes.c_uint16),
    ('pmfw_pptable_size', ctypes.c_uint16),
    ('pmfw_sku_table_start_offset', ctypes.c_uint16),
    ('pmfw_sku_table_size', ctypes.c_uint16),
    ('pmfw_board_table_start_offset', ctypes.c_uint16),
    ('pmfw_board_table_size', ctypes.c_uint16),
    ('pmfw_custom_sku_table_start_offset', ctypes.c_uint16),
    ('pmfw_custom_sku_table_size', ctypes.c_uint16),
    ('golden_pp_id', ctypes.c_uint32),
    ('golden_revision', ctypes.c_uint32),
    ('format_id', ctypes.c_uint16),
    ('platform_caps', ctypes.c_uint32),
    ('thermal_controller_type', ctypes.c_ubyte),
    ('small_power_limit1', ctypes.c_uint16),
    ('small_power_limit2', ctypes.c_uint16),
    ('boost_power_limit', ctypes.c_uint16),
    ('software_shutdown_temp', ctypes.c_uint16),
    ('reserve', ctypes.c_ubyte * 143),
    ('overdrive_table', struct_smu_14_0_2_overdrive_table),
    ('smc_pptable', struct_PPTable_t),
]


# values for enumeration 'SMU_14_0_2_CUSTOM_OD_SW_FEATURE_CAP'
SMU_14_0_2_CUSTOM_OD_SW_FEATURE_CAP__enumvalues = {
    0: 'SMU_14_0_2_CUSTOM_ODCAP_POWER_MODE',
    1: 'SMU_14_0_2_CUSTOM_ODCAP_COUNT',
}
SMU_14_0_2_CUSTOM_ODCAP_POWER_MODE = 0
SMU_14_0_2_CUSTOM_ODCAP_COUNT = 1
SMU_14_0_2_CUSTOM_OD_SW_FEATURE_CAP = ctypes.c_uint32 # enum

# values for enumeration 'SMU_14_0_2_CUSTOM_OD_FEATURE_SETTING_ID'
SMU_14_0_2_CUSTOM_OD_FEATURE_SETTING_ID__enumvalues = {
    0: 'SMU_14_0_2_CUSTOM_ODSETTING_POWER_MODE',
    1: 'SMU_14_0_2_CUSTOM_ODSETTING_COUNT',
}
SMU_14_0_2_CUSTOM_ODSETTING_POWER_MODE = 0
SMU_14_0_2_CUSTOM_ODSETTING_COUNT = 1
SMU_14_0_2_CUSTOM_OD_FEATURE_SETTING_ID = ctypes.c_uint32 # enum
class struct_smu_14_0_2_custom_overdrive_table(Structure):
    pass

struct_smu_14_0_2_custom_overdrive_table._pack_ = 1 # source:False
struct_smu_14_0_2_custom_overdrive_table._fields_ = [
    ('revision', ctypes.c_ubyte),
    ('reserve', ctypes.c_ubyte * 3),
    ('cap', ctypes.c_ubyte * 1),
    ('max', ctypes.c_int32 * 1),
    ('min', ctypes.c_int32 * 1),
    ('pm_setting', ctypes.c_int16 * 16),
]

class struct_smu_14_0_3_custom_powerplay_table(Structure):
    pass

struct_smu_14_0_3_custom_powerplay_table._pack_ = 1 # source:False
struct_smu_14_0_3_custom_powerplay_table._fields_ = [
    ('custom_table_revision', ctypes.c_ubyte),
    ('custom_table_size', ctypes.c_uint16),
    ('custom_sku_table_offset', ctypes.c_uint16),
    ('custom_platform_caps', ctypes.c_uint32),
    ('software_shutdown_temp', ctypes.c_uint16),
    ('custom_overdrive_table', struct_smu_14_0_2_custom_overdrive_table),
    ('reserve', ctypes.c_uint32 * 8),
    ('custom_sku_table_pmfw', struct_CustomSkuTable_t),
]

__all__ = \
    ['PPTABLE_SOURCE_DRIVER_HARDCODED', 'PPTABLE_SOURCE_IFWI',
    'PPTABLE_SOURCE_MAX', 'PPTABLE_SOURCE_PPGEN_REGISTRY',
    'SMU_14_0_2_CUSTOM_ODCAP_COUNT',
    'SMU_14_0_2_CUSTOM_ODCAP_POWER_MODE',
    'SMU_14_0_2_CUSTOM_ODSETTING_COUNT',
    'SMU_14_0_2_CUSTOM_ODSETTING_POWER_MODE',
    'SMU_14_0_2_CUSTOM_OD_FEATURE_SETTING_ID',
    'SMU_14_0_2_CUSTOM_OD_SW_FEATURE_CAP',
    'SMU_14_0_2_CUSTOM_TABLE_FORMAT_REVISION',
    'SMU_14_0_2_MAX_ODFEATURE', 'SMU_14_0_2_MAX_ODSETTING',
    'SMU_14_0_2_MAX_PMSETTING',
    'SMU_14_0_2_ODCAP_AUTO_FAN_ACOUSTIC_LIMIT',
    'SMU_14_0_2_ODCAP_AUTO_OC_ENGINE',
    'SMU_14_0_2_ODCAP_AUTO_OC_MEMORY', 'SMU_14_0_2_ODCAP_AUTO_SOC_UV',
    'SMU_14_0_2_ODCAP_AUTO_UV_ENGINE',
    'SMU_14_0_2_ODCAP_AUTO_VF_CURVE_OPTIMIZER',
    'SMU_14_0_2_ODCAP_COUNT', 'SMU_14_0_2_ODCAP_MANUAL_AC_TIMING',
    'SMU_14_0_2_ODCAP_MEMORY_TIMING_TUNE',
    'SMU_14_0_2_ODCAP_POWER_MODE',
    'SMU_14_0_2_ODFEATURE_AUTO_FAN_ACOUSTIC_LIMIT',
    'SMU_14_0_2_ODFEATURE_AUTO_OC_ENGINE',
    'SMU_14_0_2_ODFEATURE_AUTO_OC_MEMORY',
    'SMU_14_0_2_ODFEATURE_AUTO_SOC_UV',
    'SMU_14_0_2_ODFEATURE_AUTO_UV_ENGINE',
    'SMU_14_0_2_ODFEATURE_AUTO_VF_CURVE_OPTIMIZER',
    'SMU_14_0_2_ODFEATURE_MANUAL_AC_TIMING',
    'SMU_14_0_2_ODFEATURE_MEMORY_TIMING_TUNE',
    'SMU_14_0_2_ODFEATURE_POWER_MODE',
    'SMU_14_0_2_ODSETTING_ACTIMING',
    'SMU_14_0_2_ODSETTING_AUTOOCENGINE',
    'SMU_14_0_2_ODSETTING_AUTOOCMEMORY',
    'SMU_14_0_2_ODSETTING_AUTOUVENGINE',
    'SMU_14_0_2_ODSETTING_AUTO_FAN_ACOUSTIC_LIMIT',
    'SMU_14_0_2_ODSETTING_AUTO_SOC_UV',
    'SMU_14_0_2_ODSETTING_AUTO_VF_CURVE_OPTIMIZER',
    'SMU_14_0_2_ODSETTING_COUNT',
    'SMU_14_0_2_ODSETTING_MANUAL_AC_TIMING',
    'SMU_14_0_2_ODSETTING_POWER_MODE', 'SMU_14_0_2_OD_SW_FEATURE_CAP',
    'SMU_14_0_2_OD_SW_FEATURE_ID',
    'SMU_14_0_2_OD_SW_FEATURE_SETTING_ID',
    'SMU_14_0_2_OVERDRIVE_TABLE_ADVANCED',
    'SMU_14_0_2_OVERDRIVE_TABLE_BASIC',
    'SMU_14_0_2_OVERDRIVE_TABLE_COUNT',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_BALANCE',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_QUIET',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_RAGE',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_LIMIT_RPM_TURBO',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_BALANCE',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_QUIET',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_RAGE',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_TARGET_RPM_TURBO',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_BALANCE',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_QUIET',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_RAGE',
    'SMU_14_0_2_PMSETTING_ACOUSTIC_TEMP_TURBO',
    'SMU_14_0_2_PMSETTING_COUNT',
    'SMU_14_0_2_PMSETTING_POWER_LIMIT_BALANCE',
    'SMU_14_0_2_PMSETTING_POWER_LIMIT_QUIET',
    'SMU_14_0_2_PMSETTING_POWER_LIMIT_RAGE',
    'SMU_14_0_2_PMSETTING_POWER_LIMIT_TURBO', 'SMU_14_0_2_PPTABLE_H',
    'SMU_14_0_2_PP_CUSTOM_OVERDRIVE_VERSION',
    'SMU_14_0_2_PP_OVERDRIVE_VERSION',
    'SMU_14_0_2_PP_PLATFORM_CAP_BACO',
    'SMU_14_0_2_PP_PLATFORM_CAP_HARDWAREDC',
    'SMU_14_0_2_PP_PLATFORM_CAP_LEDSUPPORTED',
    'SMU_14_0_2_PP_PLATFORM_CAP_MACO',
    'SMU_14_0_2_PP_PLATFORM_CAP_MOBILEOVERDRIVE',
    'SMU_14_0_2_PP_PLATFORM_CAP_POWERPLAY',
    'SMU_14_0_2_PP_PLATFORM_CAP_SBIOSPOWERSOURCE',
    'SMU_14_0_2_PP_PLATFORM_CAP_SHADOWPSTATE',
    'SMU_14_0_2_PP_POWERSAVINGCLOCK_VERSION',
    'SMU_14_0_2_PP_THERMALCONTROLLER_NONE',
    'SMU_14_0_2_PWRMODE_SETTING', 'SMU_14_0_2_TABLE_FORMAT_REVISION',
    'SMU_14_0_2_overdrive_table_id', 'smu_14_0_3_pptable_source',
    'struct_AvfsDcBtcParams_t', 'struct_AvfsFuseOverride_t',
    'struct_BoardTable_t', 'struct_BootValues_t',
    'struct_CustomSkuTable_t', 'struct_DpmDescriptor_t',
    'struct_DriverReportedClocks_t', 'struct_DroopInt_t',
    'struct_I2cControllerConfig_t', 'struct_LinearInt_t',
    'struct_MsgLimits_t', 'struct_OverDriveLimits_t',
    'struct_PFE_Settings_t', 'struct_PPTable_t',
    'struct_QuadraticInt_t', 'struct_SkuTable_t',
    'struct_Svi3RegulatorSettings_t',
    'struct_atom_common_table_header',
    'struct_smu_14_0_2_custom_overdrive_table',
    'struct_smu_14_0_2_overdrive_table',
    'struct_smu_14_0_2_powerplay_table',
    'struct_smu_14_0_3_custom_powerplay_table']
