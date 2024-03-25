# -*- coding: utf-8 -*-
#
# TARGET arch is: ['--include', 'stdint.h', '--include', 'linux/drivers/gpu/drm/amd/include/atom-types.h', '--include', 'linux/drivers/gpu/drm/amd/include/atomfirmware.h', '--include', 'linux/drivers/gpu/drm/amd/pm/swsmu/inc/pmfw_if/smu11_driver_if_sienna_cichlid.h', '']
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





SMU_11_0_7_PPTABLE_H = True # macro
SMU_11_0_7_TABLE_FORMAT_REVISION = 15 # macro
SMU_11_0_7_PP_PLATFORM_CAP_POWERPLAY = 0x1 # macro
SMU_11_0_7_PP_PLATFORM_CAP_SBIOSPOWERSOURCE = 0x2 # macro
SMU_11_0_7_PP_PLATFORM_CAP_HARDWAREDC = 0x4 # macro
SMU_11_0_7_PP_PLATFORM_CAP_BACO = 0x8 # macro
SMU_11_0_7_PP_PLATFORM_CAP_MACO = 0x10 # macro
SMU_11_0_7_PP_PLATFORM_CAP_SHADOWPSTATE = 0x20 # macro
SMU_11_0_7_PP_THERMALCONTROLLER_NONE = 0 # macro
SMU_11_0_7_PP_THERMALCONTROLLER_SIENNA_CICHLID = 28 # macro
SMU_11_0_7_PP_OVERDRIVE_VERSION = 0x81 # macro
SMU_11_0_7_PP_POWERSAVINGCLOCK_VERSION = 0x01 # macro
SMU_11_0_7_MAX_ODFEATURE = 32 # macro
SMU_11_0_7_MAX_ODSETTING = 64 # macro
SMU_11_0_7_MAX_PMSETTING = 32 # macro
SMU_11_0_7_MAX_PPCLOCK = 16 # macro

# values for enumeration 'SMU_11_0_7_ODFEATURE_CAP'
SMU_11_0_7_ODFEATURE_CAP__enumvalues = {
    0: 'SMU_11_0_7_ODCAP_GFXCLK_LIMITS',
    1: 'SMU_11_0_7_ODCAP_GFXCLK_CURVE',
    2: 'SMU_11_0_7_ODCAP_UCLK_LIMITS',
    3: 'SMU_11_0_7_ODCAP_POWER_LIMIT',
    4: 'SMU_11_0_7_ODCAP_FAN_ACOUSTIC_LIMIT',
    5: 'SMU_11_0_7_ODCAP_FAN_SPEED_MIN',
    6: 'SMU_11_0_7_ODCAP_TEMPERATURE_FAN',
    7: 'SMU_11_0_7_ODCAP_TEMPERATURE_SYSTEM',
    8: 'SMU_11_0_7_ODCAP_MEMORY_TIMING_TUNE',
    9: 'SMU_11_0_7_ODCAP_FAN_ZERO_RPM_CONTROL',
    10: 'SMU_11_0_7_ODCAP_AUTO_UV_ENGINE',
    11: 'SMU_11_0_7_ODCAP_AUTO_OC_ENGINE',
    12: 'SMU_11_0_7_ODCAP_AUTO_OC_MEMORY',
    13: 'SMU_11_0_7_ODCAP_FAN_CURVE',
    14: 'SMU_11_0_ODCAP_AUTO_FAN_ACOUSTIC_LIMIT',
    15: 'SMU_11_0_7_ODCAP_POWER_MODE',
    16: 'SMU_11_0_7_ODCAP_COUNT',
}
SMU_11_0_7_ODCAP_GFXCLK_LIMITS = 0
SMU_11_0_7_ODCAP_GFXCLK_CURVE = 1
SMU_11_0_7_ODCAP_UCLK_LIMITS = 2
SMU_11_0_7_ODCAP_POWER_LIMIT = 3
SMU_11_0_7_ODCAP_FAN_ACOUSTIC_LIMIT = 4
SMU_11_0_7_ODCAP_FAN_SPEED_MIN = 5
SMU_11_0_7_ODCAP_TEMPERATURE_FAN = 6
SMU_11_0_7_ODCAP_TEMPERATURE_SYSTEM = 7
SMU_11_0_7_ODCAP_MEMORY_TIMING_TUNE = 8
SMU_11_0_7_ODCAP_FAN_ZERO_RPM_CONTROL = 9
SMU_11_0_7_ODCAP_AUTO_UV_ENGINE = 10
SMU_11_0_7_ODCAP_AUTO_OC_ENGINE = 11
SMU_11_0_7_ODCAP_AUTO_OC_MEMORY = 12
SMU_11_0_7_ODCAP_FAN_CURVE = 13
SMU_11_0_ODCAP_AUTO_FAN_ACOUSTIC_LIMIT = 14
SMU_11_0_7_ODCAP_POWER_MODE = 15
SMU_11_0_7_ODCAP_COUNT = 16
SMU_11_0_7_ODFEATURE_CAP = ctypes.c_uint32 # enum

# values for enumeration 'SMU_11_0_7_ODFEATURE_ID'
SMU_11_0_7_ODFEATURE_ID__enumvalues = {
    1: 'SMU_11_0_7_ODFEATURE_GFXCLK_LIMITS',
    2: 'SMU_11_0_7_ODFEATURE_GFXCLK_CURVE',
    4: 'SMU_11_0_7_ODFEATURE_UCLK_LIMITS',
    8: 'SMU_11_0_7_ODFEATURE_POWER_LIMIT',
    16: 'SMU_11_0_7_ODFEATURE_FAN_ACOUSTIC_LIMIT',
    32: 'SMU_11_0_7_ODFEATURE_FAN_SPEED_MIN',
    64: 'SMU_11_0_7_ODFEATURE_TEMPERATURE_FAN',
    128: 'SMU_11_0_7_ODFEATURE_TEMPERATURE_SYSTEM',
    256: 'SMU_11_0_7_ODFEATURE_MEMORY_TIMING_TUNE',
    512: 'SMU_11_0_7_ODFEATURE_FAN_ZERO_RPM_CONTROL',
    1024: 'SMU_11_0_7_ODFEATURE_AUTO_UV_ENGINE',
    2048: 'SMU_11_0_7_ODFEATURE_AUTO_OC_ENGINE',
    4096: 'SMU_11_0_7_ODFEATURE_AUTO_OC_MEMORY',
    8192: 'SMU_11_0_7_ODFEATURE_FAN_CURVE',
    16384: 'SMU_11_0_ODFEATURE_AUTO_FAN_ACOUSTIC_LIMIT',
    32768: 'SMU_11_0_7_ODFEATURE_POWER_MODE',
    16: 'SMU_11_0_7_ODFEATURE_COUNT',
}
SMU_11_0_7_ODFEATURE_GFXCLK_LIMITS = 1
SMU_11_0_7_ODFEATURE_GFXCLK_CURVE = 2
SMU_11_0_7_ODFEATURE_UCLK_LIMITS = 4
SMU_11_0_7_ODFEATURE_POWER_LIMIT = 8
SMU_11_0_7_ODFEATURE_FAN_ACOUSTIC_LIMIT = 16
SMU_11_0_7_ODFEATURE_FAN_SPEED_MIN = 32
SMU_11_0_7_ODFEATURE_TEMPERATURE_FAN = 64
SMU_11_0_7_ODFEATURE_TEMPERATURE_SYSTEM = 128
SMU_11_0_7_ODFEATURE_MEMORY_TIMING_TUNE = 256
SMU_11_0_7_ODFEATURE_FAN_ZERO_RPM_CONTROL = 512
SMU_11_0_7_ODFEATURE_AUTO_UV_ENGINE = 1024
SMU_11_0_7_ODFEATURE_AUTO_OC_ENGINE = 2048
SMU_11_0_7_ODFEATURE_AUTO_OC_MEMORY = 4096
SMU_11_0_7_ODFEATURE_FAN_CURVE = 8192
SMU_11_0_ODFEATURE_AUTO_FAN_ACOUSTIC_LIMIT = 16384
SMU_11_0_7_ODFEATURE_POWER_MODE = 32768
SMU_11_0_7_ODFEATURE_COUNT = 16
SMU_11_0_7_ODFEATURE_ID = ctypes.c_uint32 # enum

# values for enumeration 'SMU_11_0_7_ODSETTING_ID'
SMU_11_0_7_ODSETTING_ID__enumvalues = {
    0: 'SMU_11_0_7_ODSETTING_GFXCLKFMAX',
    1: 'SMU_11_0_7_ODSETTING_GFXCLKFMIN',
    2: 'SMU_11_0_7_ODSETTING_CUSTOM_GFX_VF_CURVE_A',
    3: 'SMU_11_0_7_ODSETTING_CUSTOM_GFX_VF_CURVE_B',
    4: 'SMU_11_0_7_ODSETTING_CUSTOM_GFX_VF_CURVE_C',
    5: 'SMU_11_0_7_ODSETTING_CUSTOM_CURVE_VFT_FMIN',
    6: 'SMU_11_0_7_ODSETTING_UCLKFMIN',
    7: 'SMU_11_0_7_ODSETTING_UCLKFMAX',
    8: 'SMU_11_0_7_ODSETTING_POWERPERCENTAGE',
    9: 'SMU_11_0_7_ODSETTING_FANRPMMIN',
    10: 'SMU_11_0_7_ODSETTING_FANRPMACOUSTICLIMIT',
    11: 'SMU_11_0_7_ODSETTING_FANTARGETTEMPERATURE',
    12: 'SMU_11_0_7_ODSETTING_OPERATINGTEMPMAX',
    13: 'SMU_11_0_7_ODSETTING_ACTIMING',
    14: 'SMU_11_0_7_ODSETTING_FAN_ZERO_RPM_CONTROL',
    15: 'SMU_11_0_7_ODSETTING_AUTOUVENGINE',
    16: 'SMU_11_0_7_ODSETTING_AUTOOCENGINE',
    17: 'SMU_11_0_7_ODSETTING_AUTOOCMEMORY',
    18: 'SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_1',
    19: 'SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_1',
    20: 'SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_2',
    21: 'SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_2',
    22: 'SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_3',
    23: 'SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_3',
    24: 'SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_4',
    25: 'SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_4',
    26: 'SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_5',
    27: 'SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_5',
    28: 'SMU_11_0_7_ODSETTING_AUTO_FAN_ACOUSTIC_LIMIT',
    29: 'SMU_11_0_7_ODSETTING_POWER_MODE',
    30: 'SMU_11_0_7_ODSETTING_COUNT',
}
SMU_11_0_7_ODSETTING_GFXCLKFMAX = 0
SMU_11_0_7_ODSETTING_GFXCLKFMIN = 1
SMU_11_0_7_ODSETTING_CUSTOM_GFX_VF_CURVE_A = 2
SMU_11_0_7_ODSETTING_CUSTOM_GFX_VF_CURVE_B = 3
SMU_11_0_7_ODSETTING_CUSTOM_GFX_VF_CURVE_C = 4
SMU_11_0_7_ODSETTING_CUSTOM_CURVE_VFT_FMIN = 5
SMU_11_0_7_ODSETTING_UCLKFMIN = 6
SMU_11_0_7_ODSETTING_UCLKFMAX = 7
SMU_11_0_7_ODSETTING_POWERPERCENTAGE = 8
SMU_11_0_7_ODSETTING_FANRPMMIN = 9
SMU_11_0_7_ODSETTING_FANRPMACOUSTICLIMIT = 10
SMU_11_0_7_ODSETTING_FANTARGETTEMPERATURE = 11
SMU_11_0_7_ODSETTING_OPERATINGTEMPMAX = 12
SMU_11_0_7_ODSETTING_ACTIMING = 13
SMU_11_0_7_ODSETTING_FAN_ZERO_RPM_CONTROL = 14
SMU_11_0_7_ODSETTING_AUTOUVENGINE = 15
SMU_11_0_7_ODSETTING_AUTOOCENGINE = 16
SMU_11_0_7_ODSETTING_AUTOOCMEMORY = 17
SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_1 = 18
SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_1 = 19
SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_2 = 20
SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_2 = 21
SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_3 = 22
SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_3 = 23
SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_4 = 24
SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_4 = 25
SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_5 = 26
SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_5 = 27
SMU_11_0_7_ODSETTING_AUTO_FAN_ACOUSTIC_LIMIT = 28
SMU_11_0_7_ODSETTING_POWER_MODE = 29
SMU_11_0_7_ODSETTING_COUNT = 30
SMU_11_0_7_ODSETTING_ID = ctypes.c_uint32 # enum

# values for enumeration 'SMU_11_0_7_PWRMODE_SETTING'
SMU_11_0_7_PWRMODE_SETTING__enumvalues = {
    0: 'SMU_11_0_7_PMSETTING_POWER_LIMIT_QUIET',
    1: 'SMU_11_0_7_PMSETTING_POWER_LIMIT_BALANCE',
    2: 'SMU_11_0_7_PMSETTING_POWER_LIMIT_TURBO',
    3: 'SMU_11_0_7_PMSETTING_POWER_LIMIT_RAGE',
    4: 'SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_QUIET',
    5: 'SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_BALANCE',
    6: 'SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_TURBO',
    7: 'SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_RAGE',
}
SMU_11_0_7_PMSETTING_POWER_LIMIT_QUIET = 0
SMU_11_0_7_PMSETTING_POWER_LIMIT_BALANCE = 1
SMU_11_0_7_PMSETTING_POWER_LIMIT_TURBO = 2
SMU_11_0_7_PMSETTING_POWER_LIMIT_RAGE = 3
SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_QUIET = 4
SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_BALANCE = 5
SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_TURBO = 6
SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_RAGE = 7
SMU_11_0_7_PWRMODE_SETTING = ctypes.c_uint32 # enum
class struct_smu_11_0_7_overdrive_table(Structure):
    pass

struct_smu_11_0_7_overdrive_table._pack_ = 1 # source:False
struct_smu_11_0_7_overdrive_table._fields_ = [
    ('revision', ctypes.c_ubyte),
    ('reserve', ctypes.c_ubyte * 3),
    ('feature_count', ctypes.c_uint32),
    ('setting_count', ctypes.c_uint32),
    ('cap', ctypes.c_ubyte * 32),
    ('max', ctypes.c_uint32 * 64),
    ('min', ctypes.c_uint32 * 64),
    ('pm_setting', ctypes.c_int16 * 32),
]


# values for enumeration 'SMU_11_0_7_PPCLOCK_ID'
SMU_11_0_7_PPCLOCK_ID__enumvalues = {
    0: 'SMU_11_0_7_PPCLOCK_GFXCLK',
    1: 'SMU_11_0_7_PPCLOCK_SOCCLK',
    2: 'SMU_11_0_7_PPCLOCK_UCLK',
    3: 'SMU_11_0_7_PPCLOCK_FCLK',
    4: 'SMU_11_0_7_PPCLOCK_DCLK_0',
    5: 'SMU_11_0_7_PPCLOCK_VCLK_0',
    6: 'SMU_11_0_7_PPCLOCK_DCLK_1',
    7: 'SMU_11_0_7_PPCLOCK_VCLK_1',
    8: 'SMU_11_0_7_PPCLOCK_DCEFCLK',
    9: 'SMU_11_0_7_PPCLOCK_DISPCLK',
    10: 'SMU_11_0_7_PPCLOCK_PIXCLK',
    11: 'SMU_11_0_7_PPCLOCK_PHYCLK',
    12: 'SMU_11_0_7_PPCLOCK_DTBCLK',
    13: 'SMU_11_0_7_PPCLOCK_COUNT',
}
SMU_11_0_7_PPCLOCK_GFXCLK = 0
SMU_11_0_7_PPCLOCK_SOCCLK = 1
SMU_11_0_7_PPCLOCK_UCLK = 2
SMU_11_0_7_PPCLOCK_FCLK = 3
SMU_11_0_7_PPCLOCK_DCLK_0 = 4
SMU_11_0_7_PPCLOCK_VCLK_0 = 5
SMU_11_0_7_PPCLOCK_DCLK_1 = 6
SMU_11_0_7_PPCLOCK_VCLK_1 = 7
SMU_11_0_7_PPCLOCK_DCEFCLK = 8
SMU_11_0_7_PPCLOCK_DISPCLK = 9
SMU_11_0_7_PPCLOCK_PIXCLK = 10
SMU_11_0_7_PPCLOCK_PHYCLK = 11
SMU_11_0_7_PPCLOCK_DTBCLK = 12
SMU_11_0_7_PPCLOCK_COUNT = 13
SMU_11_0_7_PPCLOCK_ID = ctypes.c_uint32 # enum
class struct_smu_11_0_7_power_saving_clock_table(Structure):
    pass

struct_smu_11_0_7_power_saving_clock_table._pack_ = 1 # source:False
struct_smu_11_0_7_power_saving_clock_table._fields_ = [
    ('revision', ctypes.c_ubyte),
    ('reserve', ctypes.c_ubyte * 3),
    ('count', ctypes.c_uint32),
    ('max', ctypes.c_uint32 * 16),
    ('min', ctypes.c_uint32 * 16),
]

class struct_smu_11_0_7_powerplay_table(Structure):
    pass

class struct_PPTable_t(Structure):
    pass

class struct_PiecewiseLinearDroopInt_t(Structure):
    pass

struct_PiecewiseLinearDroopInt_t._pack_ = 1 # source:False
struct_PiecewiseLinearDroopInt_t._fields_ = [
    ('Fset', ctypes.c_uint32 * 5),
    ('Vdroop', ctypes.c_uint32 * 5),
]

class struct_LinearInt_t(Structure):
    pass

struct_LinearInt_t._pack_ = 1 # source:False
struct_LinearInt_t._fields_ = [
    ('m', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
]

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

struct_DpmDescriptor_t._pack_ = 1 # source:False
struct_DpmDescriptor_t._fields_ = [
    ('VoltageMode', ctypes.c_ubyte),
    ('SnapToDiscrete', ctypes.c_ubyte),
    ('NumDiscreteLevels', ctypes.c_ubyte),
    ('Padding', ctypes.c_ubyte),
    ('ConversionToAvfsClk', struct_LinearInt_t),
    ('SsCurve', struct_QuadraticInt_t),
    ('SsFmin', ctypes.c_uint16),
    ('Padding16', ctypes.c_uint16),
]

class struct_UclkDpmChangeRange_t(Structure):
    pass

struct_UclkDpmChangeRange_t._pack_ = 1 # source:False
struct_UclkDpmChangeRange_t._fields_ = [
    ('Fmin', ctypes.c_uint16),
    ('Fmax', ctypes.c_uint16),
]

class struct_DroopInt_t(Structure):
    pass

struct_DroopInt_t._pack_ = 1 # source:False
struct_DroopInt_t._fields_ = [
    ('a', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
    ('c', ctypes.c_uint32),
]

struct_PPTable_t._pack_ = 1 # source:False
struct_PPTable_t._fields_ = [
    ('Version', ctypes.c_uint32),
    ('FeaturesToRun', ctypes.c_uint32 * 2),
    ('SocketPowerLimitAc', ctypes.c_uint16 * 4),
    ('SocketPowerLimitAcTau', ctypes.c_uint16 * 4),
    ('SocketPowerLimitDc', ctypes.c_uint16 * 4),
    ('SocketPowerLimitDcTau', ctypes.c_uint16 * 4),
    ('TdcLimit', ctypes.c_uint16 * 2),
    ('TdcLimitTau', ctypes.c_uint16 * 2),
    ('TemperatureLimit', ctypes.c_uint16 * 10),
    ('FitLimit', ctypes.c_uint32),
    ('TotalPowerConfig', ctypes.c_ubyte),
    ('TotalPowerPadding', ctypes.c_ubyte * 3),
    ('ApccPlusResidencyLimit', ctypes.c_uint32),
    ('SmnclkDpmFreq', ctypes.c_uint16 * 2),
    ('SmnclkDpmVoltage', ctypes.c_uint16 * 2),
    ('PaddingAPCC', ctypes.c_uint32),
    ('PerPartDroopVsetGfxDfll', ctypes.c_uint16 * 5),
    ('PaddingPerPartDroop', ctypes.c_uint16),
    ('ThrottlerControlMask', ctypes.c_uint32),
    ('FwDStateMask', ctypes.c_uint32),
    ('UlvVoltageOffsetSoc', ctypes.c_uint16),
    ('UlvVoltageOffsetGfx', ctypes.c_uint16),
    ('MinVoltageUlvGfx', ctypes.c_uint16),
    ('MinVoltageUlvSoc', ctypes.c_uint16),
    ('SocLIVmin', ctypes.c_uint16),
    ('PaddingLIVmin', ctypes.c_uint16),
    ('GceaLinkMgrIdleThreshold', ctypes.c_ubyte),
    ('paddingRlcUlvParams', ctypes.c_ubyte * 3),
    ('MinVoltageGfx', ctypes.c_uint16),
    ('MinVoltageSoc', ctypes.c_uint16),
    ('MaxVoltageGfx', ctypes.c_uint16),
    ('MaxVoltageSoc', ctypes.c_uint16),
    ('LoadLineResistanceGfx', ctypes.c_uint16),
    ('LoadLineResistanceSoc', ctypes.c_uint16),
    ('VDDGFX_TVmin', ctypes.c_uint16),
    ('VDDSOC_TVmin', ctypes.c_uint16),
    ('VDDGFX_Vmin_HiTemp', ctypes.c_uint16),
    ('VDDGFX_Vmin_LoTemp', ctypes.c_uint16),
    ('VDDSOC_Vmin_HiTemp', ctypes.c_uint16),
    ('VDDSOC_Vmin_LoTemp', ctypes.c_uint16),
    ('VDDGFX_TVminHystersis', ctypes.c_uint16),
    ('VDDSOC_TVminHystersis', ctypes.c_uint16),
    ('DpmDescriptor', struct_DpmDescriptor_t * 13),
    ('FreqTableGfx', ctypes.c_uint16 * 16),
    ('FreqTableVclk', ctypes.c_uint16 * 8),
    ('FreqTableDclk', ctypes.c_uint16 * 8),
    ('FreqTableSocclk', ctypes.c_uint16 * 8),
    ('FreqTableUclk', ctypes.c_uint16 * 4),
    ('FreqTableDcefclk', ctypes.c_uint16 * 8),
    ('FreqTableDispclk', ctypes.c_uint16 * 8),
    ('FreqTablePixclk', ctypes.c_uint16 * 8),
    ('FreqTablePhyclk', ctypes.c_uint16 * 8),
    ('FreqTableDtbclk', ctypes.c_uint16 * 8),
    ('FreqTableFclk', ctypes.c_uint16 * 8),
    ('Paddingclks', ctypes.c_uint32),
    ('PerPartDroopModelGfxDfll', struct_DroopInt_t * 5),
    ('DcModeMaxFreq', ctypes.c_uint32 * 13),
    ('FreqTableUclkDiv', ctypes.c_ubyte * 4),
    ('FclkBoostFreq', ctypes.c_uint16),
    ('FclkParamPadding', ctypes.c_uint16),
    ('Mp0clkFreq', ctypes.c_uint16 * 2),
    ('Mp0DpmVoltage', ctypes.c_uint16 * 2),
    ('MemVddciVoltage', ctypes.c_uint16 * 4),
    ('MemMvddVoltage', ctypes.c_uint16 * 4),
    ('GfxclkFgfxoffEntry', ctypes.c_uint16),
    ('GfxclkFinit', ctypes.c_uint16),
    ('GfxclkFidle', ctypes.c_uint16),
    ('GfxclkSource', ctypes.c_ubyte),
    ('GfxclkPadding', ctypes.c_ubyte),
    ('GfxGpoSubFeatureMask', ctypes.c_ubyte),
    ('GfxGpoEnabledWorkPolicyMask', ctypes.c_ubyte),
    ('GfxGpoDisabledWorkPolicyMask', ctypes.c_ubyte),
    ('GfxGpoPadding', ctypes.c_ubyte * 1),
    ('GfxGpoVotingAllow', ctypes.c_uint32),
    ('GfxGpoPadding32', ctypes.c_uint32 * 4),
    ('GfxDcsFopt', ctypes.c_uint16),
    ('GfxDcsFclkFopt', ctypes.c_uint16),
    ('GfxDcsUclkFopt', ctypes.c_uint16),
    ('DcsGfxOffVoltage', ctypes.c_uint16),
    ('DcsMinGfxOffTime', ctypes.c_uint16),
    ('DcsMaxGfxOffTime', ctypes.c_uint16),
    ('DcsMinCreditAccum', ctypes.c_uint32),
    ('DcsExitHysteresis', ctypes.c_uint16),
    ('DcsTimeout', ctypes.c_uint16),
    ('DcsParamPadding', ctypes.c_uint32 * 5),
    ('FlopsPerByteTable', ctypes.c_uint16 * 16),
    ('LowestUclkReservedForUlv', ctypes.c_ubyte),
    ('PaddingMem', ctypes.c_ubyte * 3),
    ('UclkDpmPstates', ctypes.c_ubyte * 4),
    ('UclkDpmSrcFreqRange', struct_UclkDpmChangeRange_t),
    ('UclkDpmTargFreqRange', struct_UclkDpmChangeRange_t),
    ('UclkDpmMidstepFreq', ctypes.c_uint16),
    ('UclkMidstepPadding', ctypes.c_uint16),
    ('PcieGenSpeed', ctypes.c_ubyte * 2),
    ('PcieLaneCount', ctypes.c_ubyte * 2),
    ('LclkFreq', ctypes.c_uint16 * 2),
    ('FanStopTemp', ctypes.c_uint16),
    ('FanStartTemp', ctypes.c_uint16),
    ('FanGain', ctypes.c_uint16 * 10),
    ('FanPwmMin', ctypes.c_uint16),
    ('FanAcousticLimitRpm', ctypes.c_uint16),
    ('FanThrottlingRpm', ctypes.c_uint16),
    ('FanMaximumRpm', ctypes.c_uint16),
    ('MGpuFanBoostLimitRpm', ctypes.c_uint16),
    ('FanTargetTemperature', ctypes.c_uint16),
    ('FanTargetGfxclk', ctypes.c_uint16),
    ('FanPadding16', ctypes.c_uint16),
    ('FanTempInputSelect', ctypes.c_ubyte),
    ('FanPadding', ctypes.c_ubyte),
    ('FanZeroRpmEnable', ctypes.c_ubyte),
    ('FanTachEdgePerRev', ctypes.c_ubyte),
    ('FuzzyFan_ErrorSetDelta', ctypes.c_int16),
    ('FuzzyFan_ErrorRateSetDelta', ctypes.c_int16),
    ('FuzzyFan_PwmSetDelta', ctypes.c_int16),
    ('FuzzyFan_Reserved', ctypes.c_uint16),
    ('OverrideAvfsGb', ctypes.c_ubyte * 2),
    ('dBtcGbGfxDfllModelSelect', ctypes.c_ubyte),
    ('Padding8_Avfs', ctypes.c_ubyte),
    ('qAvfsGb', struct_QuadraticInt_t * 2),
    ('dBtcGbGfxPll', struct_DroopInt_t),
    ('dBtcGbGfxDfll', struct_DroopInt_t),
    ('dBtcGbSoc', struct_DroopInt_t),
    ('qAgingGb', struct_LinearInt_t * 2),
    ('PiecewiseLinearDroopIntGfxDfll', struct_PiecewiseLinearDroopInt_t),
    ('qStaticVoltageOffset', struct_QuadraticInt_t * 2),
    ('DcTol', ctypes.c_uint16 * 2),
    ('DcBtcEnabled', ctypes.c_ubyte * 2),
    ('Padding8_GfxBtc', ctypes.c_ubyte * 2),
    ('DcBtcMin', ctypes.c_uint16 * 2),
    ('DcBtcMax', ctypes.c_uint16 * 2),
    ('DcBtcGb', ctypes.c_uint16 * 2),
    ('XgmiDpmPstates', ctypes.c_ubyte * 2),
    ('XgmiDpmSpare', ctypes.c_ubyte * 2),
    ('DebugOverrides', ctypes.c_uint32),
    ('ReservedEquation0', struct_QuadraticInt_t),
    ('ReservedEquation1', struct_QuadraticInt_t),
    ('ReservedEquation2', struct_QuadraticInt_t),
    ('ReservedEquation3', struct_QuadraticInt_t),
    ('CustomerVariant', ctypes.c_ubyte),
    ('VcBtcEnabled', ctypes.c_ubyte),
    ('VcBtcVminT0', ctypes.c_uint16),
    ('VcBtcFixedVminAgingOffset', ctypes.c_uint16),
    ('VcBtcVmin2PsmDegrationGb', ctypes.c_uint16),
    ('VcBtcPsmA', ctypes.c_uint32),
    ('VcBtcPsmB', ctypes.c_uint32),
    ('VcBtcVminA', ctypes.c_uint32),
    ('VcBtcVminB', ctypes.c_uint32),
    ('LedGpio', ctypes.c_uint16),
    ('GfxPowerStagesGpio', ctypes.c_uint16),
    ('SkuReserved', ctypes.c_uint32 * 8),
    ('GamingClk', ctypes.c_uint32 * 6),
    ('I2cControllers', struct_I2cControllerConfig_t * 16),
    ('GpioScl', ctypes.c_ubyte),
    ('GpioSda', ctypes.c_ubyte),
    ('FchUsbPdSlaveAddr', ctypes.c_ubyte),
    ('I2cSpare', ctypes.c_ubyte * 1),
    ('VddGfxVrMapping', ctypes.c_ubyte),
    ('VddSocVrMapping', ctypes.c_ubyte),
    ('VddMem0VrMapping', ctypes.c_ubyte),
    ('VddMem1VrMapping', ctypes.c_ubyte),
    ('GfxUlvPhaseSheddingMask', ctypes.c_ubyte),
    ('SocUlvPhaseSheddingMask', ctypes.c_ubyte),
    ('VddciUlvPhaseSheddingMask', ctypes.c_ubyte),
    ('MvddUlvPhaseSheddingMask', ctypes.c_ubyte),
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
    ('MvddRatio', ctypes.c_uint32),
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
    ('LedEnableMask', ctypes.c_ubyte),
    ('LedPcie', ctypes.c_ubyte),
    ('LedError', ctypes.c_ubyte),
    ('LedSpare1', ctypes.c_ubyte * 2),
    ('PllGfxclkSpreadEnabled', ctypes.c_ubyte),
    ('PllGfxclkSpreadPercent', ctypes.c_ubyte),
    ('PllGfxclkSpreadFreq', ctypes.c_uint16),
    ('DfllGfxclkSpreadEnabled', ctypes.c_ubyte),
    ('DfllGfxclkSpreadPercent', ctypes.c_ubyte),
    ('DfllGfxclkSpreadFreq', ctypes.c_uint16),
    ('UclkSpreadPadding', ctypes.c_uint16),
    ('UclkSpreadFreq', ctypes.c_uint16),
    ('FclkSpreadEnabled', ctypes.c_ubyte),
    ('FclkSpreadPercent', ctypes.c_ubyte),
    ('FclkSpreadFreq', ctypes.c_uint16),
    ('MemoryChannelEnabled', ctypes.c_uint32),
    ('DramBitWidth', ctypes.c_ubyte),
    ('PaddingMem1', ctypes.c_ubyte * 3),
    ('TotalBoardPower', ctypes.c_uint16),
    ('BoardPowerPadding', ctypes.c_uint16),
    ('XgmiLinkSpeed', ctypes.c_ubyte * 4),
    ('XgmiLinkWidth', ctypes.c_ubyte * 4),
    ('XgmiFclkFreq', ctypes.c_uint16 * 4),
    ('XgmiSocVoltage', ctypes.c_uint16 * 4),
    ('HsrEnabled', ctypes.c_ubyte),
    ('VddqOffEnabled', ctypes.c_ubyte),
    ('PaddingUmcFlags', ctypes.c_ubyte * 2),
    ('UclkSpreadPercent', ctypes.c_ubyte * 16),
    ('BoardReserved', ctypes.c_uint32 * 11),
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

struct_smu_11_0_7_powerplay_table._pack_ = 1 # source:False
struct_smu_11_0_7_powerplay_table._fields_ = [
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
    ('software_shutdown_temp', ctypes.c_uint16),
    ('reserve', ctypes.c_uint16 * 8),
    ('power_saving_clock', struct_smu_11_0_7_power_saving_clock_table),
    ('overdrive_table', struct_smu_11_0_7_overdrive_table),
    ('smc_pptable', struct_PPTable_t),
]

__all__ = \
    ['SMU_11_0_7_MAX_ODFEATURE', 'SMU_11_0_7_MAX_ODSETTING',
    'SMU_11_0_7_MAX_PMSETTING', 'SMU_11_0_7_MAX_PPCLOCK',
    'SMU_11_0_7_ODCAP_AUTO_OC_ENGINE',
    'SMU_11_0_7_ODCAP_AUTO_OC_MEMORY',
    'SMU_11_0_7_ODCAP_AUTO_UV_ENGINE', 'SMU_11_0_7_ODCAP_COUNT',
    'SMU_11_0_7_ODCAP_FAN_ACOUSTIC_LIMIT',
    'SMU_11_0_7_ODCAP_FAN_CURVE', 'SMU_11_0_7_ODCAP_FAN_SPEED_MIN',
    'SMU_11_0_7_ODCAP_FAN_ZERO_RPM_CONTROL',
    'SMU_11_0_7_ODCAP_GFXCLK_CURVE', 'SMU_11_0_7_ODCAP_GFXCLK_LIMITS',
    'SMU_11_0_7_ODCAP_MEMORY_TIMING_TUNE',
    'SMU_11_0_7_ODCAP_POWER_LIMIT', 'SMU_11_0_7_ODCAP_POWER_MODE',
    'SMU_11_0_7_ODCAP_TEMPERATURE_FAN',
    'SMU_11_0_7_ODCAP_TEMPERATURE_SYSTEM',
    'SMU_11_0_7_ODCAP_UCLK_LIMITS',
    'SMU_11_0_7_ODFEATURE_AUTO_OC_ENGINE',
    'SMU_11_0_7_ODFEATURE_AUTO_OC_MEMORY',
    'SMU_11_0_7_ODFEATURE_AUTO_UV_ENGINE', 'SMU_11_0_7_ODFEATURE_CAP',
    'SMU_11_0_7_ODFEATURE_COUNT',
    'SMU_11_0_7_ODFEATURE_FAN_ACOUSTIC_LIMIT',
    'SMU_11_0_7_ODFEATURE_FAN_CURVE',
    'SMU_11_0_7_ODFEATURE_FAN_SPEED_MIN',
    'SMU_11_0_7_ODFEATURE_FAN_ZERO_RPM_CONTROL',
    'SMU_11_0_7_ODFEATURE_GFXCLK_CURVE',
    'SMU_11_0_7_ODFEATURE_GFXCLK_LIMITS', 'SMU_11_0_7_ODFEATURE_ID',
    'SMU_11_0_7_ODFEATURE_MEMORY_TIMING_TUNE',
    'SMU_11_0_7_ODFEATURE_POWER_LIMIT',
    'SMU_11_0_7_ODFEATURE_POWER_MODE',
    'SMU_11_0_7_ODFEATURE_TEMPERATURE_FAN',
    'SMU_11_0_7_ODFEATURE_TEMPERATURE_SYSTEM',
    'SMU_11_0_7_ODFEATURE_UCLK_LIMITS',
    'SMU_11_0_7_ODSETTING_ACTIMING',
    'SMU_11_0_7_ODSETTING_AUTOOCENGINE',
    'SMU_11_0_7_ODSETTING_AUTOOCMEMORY',
    'SMU_11_0_7_ODSETTING_AUTOUVENGINE',
    'SMU_11_0_7_ODSETTING_AUTO_FAN_ACOUSTIC_LIMIT',
    'SMU_11_0_7_ODSETTING_COUNT',
    'SMU_11_0_7_ODSETTING_CUSTOM_CURVE_VFT_FMIN',
    'SMU_11_0_7_ODSETTING_CUSTOM_GFX_VF_CURVE_A',
    'SMU_11_0_7_ODSETTING_CUSTOM_GFX_VF_CURVE_B',
    'SMU_11_0_7_ODSETTING_CUSTOM_GFX_VF_CURVE_C',
    'SMU_11_0_7_ODSETTING_FANRPMACOUSTICLIMIT',
    'SMU_11_0_7_ODSETTING_FANRPMMIN',
    'SMU_11_0_7_ODSETTING_FANTARGETTEMPERATURE',
    'SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_1',
    'SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_2',
    'SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_3',
    'SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_4',
    'SMU_11_0_7_ODSETTING_FAN_CURVE_SPEED_5',
    'SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_1',
    'SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_2',
    'SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_3',
    'SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_4',
    'SMU_11_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_5',
    'SMU_11_0_7_ODSETTING_FAN_ZERO_RPM_CONTROL',
    'SMU_11_0_7_ODSETTING_GFXCLKFMAX',
    'SMU_11_0_7_ODSETTING_GFXCLKFMIN', 'SMU_11_0_7_ODSETTING_ID',
    'SMU_11_0_7_ODSETTING_OPERATINGTEMPMAX',
    'SMU_11_0_7_ODSETTING_POWERPERCENTAGE',
    'SMU_11_0_7_ODSETTING_POWER_MODE',
    'SMU_11_0_7_ODSETTING_UCLKFMAX', 'SMU_11_0_7_ODSETTING_UCLKFMIN',
    'SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_BALANCE',
    'SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_QUIET',
    'SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_RAGE',
    'SMU_11_0_7_PMSETTING_ACOUSTIC_TEMP_TURBO',
    'SMU_11_0_7_PMSETTING_POWER_LIMIT_BALANCE',
    'SMU_11_0_7_PMSETTING_POWER_LIMIT_QUIET',
    'SMU_11_0_7_PMSETTING_POWER_LIMIT_RAGE',
    'SMU_11_0_7_PMSETTING_POWER_LIMIT_TURBO',
    'SMU_11_0_7_PPCLOCK_COUNT', 'SMU_11_0_7_PPCLOCK_DCEFCLK',
    'SMU_11_0_7_PPCLOCK_DCLK_0', 'SMU_11_0_7_PPCLOCK_DCLK_1',
    'SMU_11_0_7_PPCLOCK_DISPCLK', 'SMU_11_0_7_PPCLOCK_DTBCLK',
    'SMU_11_0_7_PPCLOCK_FCLK', 'SMU_11_0_7_PPCLOCK_GFXCLK',
    'SMU_11_0_7_PPCLOCK_ID', 'SMU_11_0_7_PPCLOCK_PHYCLK',
    'SMU_11_0_7_PPCLOCK_PIXCLK', 'SMU_11_0_7_PPCLOCK_SOCCLK',
    'SMU_11_0_7_PPCLOCK_UCLK', 'SMU_11_0_7_PPCLOCK_VCLK_0',
    'SMU_11_0_7_PPCLOCK_VCLK_1', 'SMU_11_0_7_PPTABLE_H',
    'SMU_11_0_7_PP_OVERDRIVE_VERSION',
    'SMU_11_0_7_PP_PLATFORM_CAP_BACO',
    'SMU_11_0_7_PP_PLATFORM_CAP_HARDWAREDC',
    'SMU_11_0_7_PP_PLATFORM_CAP_MACO',
    'SMU_11_0_7_PP_PLATFORM_CAP_POWERPLAY',
    'SMU_11_0_7_PP_PLATFORM_CAP_SBIOSPOWERSOURCE',
    'SMU_11_0_7_PP_PLATFORM_CAP_SHADOWPSTATE',
    'SMU_11_0_7_PP_POWERSAVINGCLOCK_VERSION',
    'SMU_11_0_7_PP_THERMALCONTROLLER_NONE',
    'SMU_11_0_7_PP_THERMALCONTROLLER_SIENNA_CICHLID',
    'SMU_11_0_7_PWRMODE_SETTING', 'SMU_11_0_7_TABLE_FORMAT_REVISION',
    'SMU_11_0_ODCAP_AUTO_FAN_ACOUSTIC_LIMIT',
    'SMU_11_0_ODFEATURE_AUTO_FAN_ACOUSTIC_LIMIT',
    'struct_DpmDescriptor_t', 'struct_DroopInt_t',
    'struct_I2cControllerConfig_t', 'struct_LinearInt_t',
    'struct_PPTable_t', 'struct_PiecewiseLinearDroopInt_t',
    'struct_QuadraticInt_t', 'struct_UclkDpmChangeRange_t',
    'struct_atom_common_table_header',
    'struct_smu_11_0_7_overdrive_table',
    'struct_smu_11_0_7_power_saving_clock_table',
    'struct_smu_11_0_7_powerplay_table']
