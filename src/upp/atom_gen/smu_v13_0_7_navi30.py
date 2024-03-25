# -*- coding: utf-8 -*-
#
# TARGET arch is: ['--include', 'stdint.h', '--include', 'linux/drivers/gpu/drm/amd/include/atom-types.h', '--include', 'linux/drivers/gpu/drm/amd/include/atomfirmware.h', '--include', 'linux/drivers/gpu/drm/amd/pm/swsmu/inc/pmfw_if/smu13_driver_if_v13_0_7.h', '']
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





SMU_13_0_7_PPTABLE_H = True # macro
SMU_13_0_7_TABLE_FORMAT_REVISION = 15 # macro
SMU_13_0_7_PP_PLATFORM_CAP_POWERPLAY = 0x1 # macro
SMU_13_0_7_PP_PLATFORM_CAP_SBIOSPOWERSOURCE = 0x2 # macro
SMU_13_0_7_PP_PLATFORM_CAP_HARDWAREDC = 0x4 # macro
SMU_13_0_7_PP_PLATFORM_CAP_BACO = 0x8 # macro
SMU_13_0_7_PP_PLATFORM_CAP_MACO = 0x10 # macro
SMU_13_0_7_PP_PLATFORM_CAP_SHADOWPSTATE = 0x20 # macro
SMU_13_0_7_PP_THERMALCONTROLLER_NONE = 0 # macro
SMU_13_0_7_PP_THERMALCONTROLLER_NAVI21 = 28 # macro
SMU_13_0_7_PP_OVERDRIVE_VERSION = 0x83 # macro
SMU_13_0_7_PP_POWERSAVINGCLOCK_VERSION = 0x01 # macro
SMU_13_0_7_MAX_ODFEATURE = 32 # macro
SMU_13_0_7_MAX_ODSETTING = 64 # macro
SMU_13_0_7_MAX_PMSETTING = 32 # macro
SMU_13_0_7_MAX_PPCLOCK = 16 # macro

# values for enumeration 'SMU_13_0_7_ODFEATURE_CAP'
SMU_13_0_7_ODFEATURE_CAP__enumvalues = {
    0: 'SMU_13_0_7_ODCAP_GFXCLK_LIMITS',
    1: 'SMU_13_0_7_ODCAP_UCLK_LIMITS',
    2: 'SMU_13_0_7_ODCAP_POWER_LIMIT',
    3: 'SMU_13_0_7_ODCAP_FAN_ACOUSTIC_LIMIT',
    4: 'SMU_13_0_7_ODCAP_FAN_SPEED_MIN',
    5: 'SMU_13_0_7_ODCAP_TEMPERATURE_FAN',
    6: 'SMU_13_0_7_ODCAP_TEMPERATURE_SYSTEM',
    7: 'SMU_13_0_7_ODCAP_MEMORY_TIMING_TUNE',
    8: 'SMU_13_0_7_ODCAP_FAN_ZERO_RPM_CONTROL',
    9: 'SMU_13_0_7_ODCAP_AUTO_UV_ENGINE',
    10: 'SMU_13_0_7_ODCAP_AUTO_OC_ENGINE',
    11: 'SMU_13_0_7_ODCAP_AUTO_OC_MEMORY',
    12: 'SMU_13_0_7_ODCAP_FAN_CURVE',
    13: 'SMU_13_0_7_ODCAP_AUTO_FAN_ACOUSTIC_LIMIT',
    14: 'SMU_13_0_7_ODCAP_POWER_MODE',
    15: 'SMU_13_0_7_ODCAP_PER_ZONE_GFX_VOLTAGE_OFFSET',
    16: 'SMU_13_0_7_ODCAP_COUNT',
}
SMU_13_0_7_ODCAP_GFXCLK_LIMITS = 0
SMU_13_0_7_ODCAP_UCLK_LIMITS = 1
SMU_13_0_7_ODCAP_POWER_LIMIT = 2
SMU_13_0_7_ODCAP_FAN_ACOUSTIC_LIMIT = 3
SMU_13_0_7_ODCAP_FAN_SPEED_MIN = 4
SMU_13_0_7_ODCAP_TEMPERATURE_FAN = 5
SMU_13_0_7_ODCAP_TEMPERATURE_SYSTEM = 6
SMU_13_0_7_ODCAP_MEMORY_TIMING_TUNE = 7
SMU_13_0_7_ODCAP_FAN_ZERO_RPM_CONTROL = 8
SMU_13_0_7_ODCAP_AUTO_UV_ENGINE = 9
SMU_13_0_7_ODCAP_AUTO_OC_ENGINE = 10
SMU_13_0_7_ODCAP_AUTO_OC_MEMORY = 11
SMU_13_0_7_ODCAP_FAN_CURVE = 12
SMU_13_0_7_ODCAP_AUTO_FAN_ACOUSTIC_LIMIT = 13
SMU_13_0_7_ODCAP_POWER_MODE = 14
SMU_13_0_7_ODCAP_PER_ZONE_GFX_VOLTAGE_OFFSET = 15
SMU_13_0_7_ODCAP_COUNT = 16
SMU_13_0_7_ODFEATURE_CAP = ctypes.c_uint32 # enum

# values for enumeration 'SMU_13_0_7_ODFEATURE_ID'
SMU_13_0_7_ODFEATURE_ID__enumvalues = {
    1: 'SMU_13_0_7_ODFEATURE_GFXCLK_LIMITS',
    2: 'SMU_13_0_7_ODFEATURE_UCLK_LIMITS',
    4: 'SMU_13_0_7_ODFEATURE_POWER_LIMIT',
    8: 'SMU_13_0_7_ODFEATURE_FAN_ACOUSTIC_LIMIT',
    16: 'SMU_13_0_7_ODFEATURE_FAN_SPEED_MIN',
    32: 'SMU_13_0_7_ODFEATURE_TEMPERATURE_FAN',
    64: 'SMU_13_0_7_ODFEATURE_TEMPERATURE_SYSTEM',
    128: 'SMU_13_0_7_ODFEATURE_MEMORY_TIMING_TUNE',
    256: 'SMU_13_0_7_ODFEATURE_FAN_ZERO_RPM_CONTROL',
    512: 'SMU_13_0_7_ODFEATURE_AUTO_UV_ENGINE',
    1024: 'SMU_13_0_7_ODFEATURE_AUTO_OC_ENGINE',
    2048: 'SMU_13_0_7_ODFEATURE_AUTO_OC_MEMORY',
    4096: 'SMU_13_0_7_ODFEATURE_FAN_CURVE',
    8192: 'SMU_13_0_7_ODFEATURE_AUTO_FAN_ACOUSTIC_LIMIT',
    16384: 'SMU_13_0_7_ODFEATURE_POWER_MODE',
    32768: 'SMU_13_0_7_ODFEATURE_PER_ZONE_GFX_VOLTAGE_OFFSET',
    16: 'SMU_13_0_7_ODFEATURE_COUNT',
}
SMU_13_0_7_ODFEATURE_GFXCLK_LIMITS = 1
SMU_13_0_7_ODFEATURE_UCLK_LIMITS = 2
SMU_13_0_7_ODFEATURE_POWER_LIMIT = 4
SMU_13_0_7_ODFEATURE_FAN_ACOUSTIC_LIMIT = 8
SMU_13_0_7_ODFEATURE_FAN_SPEED_MIN = 16
SMU_13_0_7_ODFEATURE_TEMPERATURE_FAN = 32
SMU_13_0_7_ODFEATURE_TEMPERATURE_SYSTEM = 64
SMU_13_0_7_ODFEATURE_MEMORY_TIMING_TUNE = 128
SMU_13_0_7_ODFEATURE_FAN_ZERO_RPM_CONTROL = 256
SMU_13_0_7_ODFEATURE_AUTO_UV_ENGINE = 512
SMU_13_0_7_ODFEATURE_AUTO_OC_ENGINE = 1024
SMU_13_0_7_ODFEATURE_AUTO_OC_MEMORY = 2048
SMU_13_0_7_ODFEATURE_FAN_CURVE = 4096
SMU_13_0_7_ODFEATURE_AUTO_FAN_ACOUSTIC_LIMIT = 8192
SMU_13_0_7_ODFEATURE_POWER_MODE = 16384
SMU_13_0_7_ODFEATURE_PER_ZONE_GFX_VOLTAGE_OFFSET = 32768
SMU_13_0_7_ODFEATURE_COUNT = 16
SMU_13_0_7_ODFEATURE_ID = ctypes.c_uint32 # enum

# values for enumeration 'SMU_13_0_7_ODSETTING_ID'
SMU_13_0_7_ODSETTING_ID__enumvalues = {
    0: 'SMU_13_0_7_ODSETTING_GFXCLKFMAX',
    1: 'SMU_13_0_7_ODSETTING_GFXCLKFMIN',
    2: 'SMU_13_0_7_ODSETTING_UCLKFMIN',
    3: 'SMU_13_0_7_ODSETTING_UCLKFMAX',
    4: 'SMU_13_0_7_ODSETTING_POWERPERCENTAGE',
    5: 'SMU_13_0_7_ODSETTING_FANRPMMIN',
    6: 'SMU_13_0_7_ODSETTING_FANRPMACOUSTICLIMIT',
    7: 'SMU_13_0_7_ODSETTING_FANTARGETTEMPERATURE',
    8: 'SMU_13_0_7_ODSETTING_OPERATINGTEMPMAX',
    9: 'SMU_13_0_7_ODSETTING_ACTIMING',
    10: 'SMU_13_0_7_ODSETTING_FAN_ZERO_RPM_CONTROL',
    11: 'SMU_13_0_7_ODSETTING_AUTOUVENGINE',
    12: 'SMU_13_0_7_ODSETTING_AUTOOCENGINE',
    13: 'SMU_13_0_7_ODSETTING_AUTOOCMEMORY',
    14: 'SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_1',
    15: 'SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_1',
    16: 'SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_2',
    17: 'SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_2',
    18: 'SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_3',
    19: 'SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_3',
    20: 'SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_4',
    21: 'SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_4',
    22: 'SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_5',
    23: 'SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_5',
    24: 'SMU_13_0_7_ODSETTING_AUTO_FAN_ACOUSTIC_LIMIT',
    25: 'SMU_13_0_7_ODSETTING_POWER_MODE',
    26: 'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_1',
    27: 'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_2',
    28: 'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_3',
    29: 'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_4',
    30: 'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_5',
    31: 'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_6',
    32: 'SMU_13_0_7_ODSETTING_COUNT',
}
SMU_13_0_7_ODSETTING_GFXCLKFMAX = 0
SMU_13_0_7_ODSETTING_GFXCLKFMIN = 1
SMU_13_0_7_ODSETTING_UCLKFMIN = 2
SMU_13_0_7_ODSETTING_UCLKFMAX = 3
SMU_13_0_7_ODSETTING_POWERPERCENTAGE = 4
SMU_13_0_7_ODSETTING_FANRPMMIN = 5
SMU_13_0_7_ODSETTING_FANRPMACOUSTICLIMIT = 6
SMU_13_0_7_ODSETTING_FANTARGETTEMPERATURE = 7
SMU_13_0_7_ODSETTING_OPERATINGTEMPMAX = 8
SMU_13_0_7_ODSETTING_ACTIMING = 9
SMU_13_0_7_ODSETTING_FAN_ZERO_RPM_CONTROL = 10
SMU_13_0_7_ODSETTING_AUTOUVENGINE = 11
SMU_13_0_7_ODSETTING_AUTOOCENGINE = 12
SMU_13_0_7_ODSETTING_AUTOOCMEMORY = 13
SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_1 = 14
SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_1 = 15
SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_2 = 16
SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_2 = 17
SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_3 = 18
SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_3 = 19
SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_4 = 20
SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_4 = 21
SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_5 = 22
SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_5 = 23
SMU_13_0_7_ODSETTING_AUTO_FAN_ACOUSTIC_LIMIT = 24
SMU_13_0_7_ODSETTING_POWER_MODE = 25
SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_1 = 26
SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_2 = 27
SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_3 = 28
SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_4 = 29
SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_5 = 30
SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_6 = 31
SMU_13_0_7_ODSETTING_COUNT = 32
SMU_13_0_7_ODSETTING_ID = ctypes.c_uint32 # enum

# values for enumeration 'SMU_13_0_7_PWRMODE_SETTING'
SMU_13_0_7_PWRMODE_SETTING__enumvalues = {
    0: 'SMU_13_0_7_PMSETTING_POWER_LIMIT_QUIET',
    1: 'SMU_13_0_7_PMSETTING_POWER_LIMIT_BALANCE',
    2: 'SMU_13_0_7_PMSETTING_POWER_LIMIT_TURBO',
    3: 'SMU_13_0_7_PMSETTING_POWER_LIMIT_RAGE',
    4: 'SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_QUIET',
    5: 'SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_BALANCE',
    6: 'SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_TURBO',
    7: 'SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_RAGE',
    8: 'SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_QUIET',
    9: 'SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_BALANCE',
    10: 'SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_TURBO',
    11: 'SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_RAGE',
    12: 'SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_QUIET',
    13: 'SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_BALANCE',
    14: 'SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_TURBO',
    15: 'SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_RAGE',
}
SMU_13_0_7_PMSETTING_POWER_LIMIT_QUIET = 0
SMU_13_0_7_PMSETTING_POWER_LIMIT_BALANCE = 1
SMU_13_0_7_PMSETTING_POWER_LIMIT_TURBO = 2
SMU_13_0_7_PMSETTING_POWER_LIMIT_RAGE = 3
SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_QUIET = 4
SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_BALANCE = 5
SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_TURBO = 6
SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_RAGE = 7
SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_QUIET = 8
SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_BALANCE = 9
SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_TURBO = 10
SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_RAGE = 11
SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_QUIET = 12
SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_BALANCE = 13
SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_TURBO = 14
SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_RAGE = 15
SMU_13_0_7_PWRMODE_SETTING = ctypes.c_uint32 # enum
class struct_smu_13_0_7_overdrive_table(Structure):
    pass

struct_smu_13_0_7_overdrive_table._pack_ = 1 # source:False
struct_smu_13_0_7_overdrive_table._fields_ = [
    ('revision', ctypes.c_ubyte),
    ('reserve', ctypes.c_ubyte * 3),
    ('feature_count', ctypes.c_uint32),
    ('setting_count', ctypes.c_uint32),
    ('cap', ctypes.c_ubyte * 32),
    ('max', ctypes.c_uint32 * 64),
    ('min', ctypes.c_uint32 * 64),
    ('pm_setting', ctypes.c_int16 * 32),
]


# values for enumeration 'SMU_13_0_7_PPCLOCK_ID'
SMU_13_0_7_PPCLOCK_ID__enumvalues = {
    0: 'SMU_13_0_7_PPCLOCK_GFXCLK',
    1: 'SMU_13_0_7_PPCLOCK_SOCCLK',
    2: 'SMU_13_0_7_PPCLOCK_UCLK',
    3: 'SMU_13_0_7_PPCLOCK_FCLK',
    4: 'SMU_13_0_7_PPCLOCK_DCLK_0',
    5: 'SMU_13_0_7_PPCLOCK_VCLK_0',
    6: 'SMU_13_0_7_PPCLOCK_DCLK_1',
    7: 'SMU_13_0_7_PPCLOCK_VCLK_1',
    8: 'SMU_13_0_7_PPCLOCK_DCEFCLK',
    9: 'SMU_13_0_7_PPCLOCK_DISPCLK',
    10: 'SMU_13_0_7_PPCLOCK_PIXCLK',
    11: 'SMU_13_0_7_PPCLOCK_PHYCLK',
    12: 'SMU_13_0_7_PPCLOCK_DTBCLK',
    13: 'SMU_13_0_7_PPCLOCK_COUNT',
}
SMU_13_0_7_PPCLOCK_GFXCLK = 0
SMU_13_0_7_PPCLOCK_SOCCLK = 1
SMU_13_0_7_PPCLOCK_UCLK = 2
SMU_13_0_7_PPCLOCK_FCLK = 3
SMU_13_0_7_PPCLOCK_DCLK_0 = 4
SMU_13_0_7_PPCLOCK_VCLK_0 = 5
SMU_13_0_7_PPCLOCK_DCLK_1 = 6
SMU_13_0_7_PPCLOCK_VCLK_1 = 7
SMU_13_0_7_PPCLOCK_DCEFCLK = 8
SMU_13_0_7_PPCLOCK_DISPCLK = 9
SMU_13_0_7_PPCLOCK_PIXCLK = 10
SMU_13_0_7_PPCLOCK_PHYCLK = 11
SMU_13_0_7_PPCLOCK_DTBCLK = 12
SMU_13_0_7_PPCLOCK_COUNT = 13
SMU_13_0_7_PPCLOCK_ID = ctypes.c_uint32 # enum
class struct_smu_13_0_7_powerplay_table(Structure):
    pass

class struct_PPTable_t(Structure):
    pass

class struct_SkuTable_t(Structure):
    pass

class struct_DroopInt_t(Structure):
    pass

struct_DroopInt_t._pack_ = 1 # source:False
struct_DroopInt_t._fields_ = [
    ('a', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
    ('c', ctypes.c_uint32),
]

class struct_LinearInt_t(Structure):
    pass

struct_LinearInt_t._pack_ = 1 # source:False
struct_LinearInt_t._fields_ = [
    ('m', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
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

class struct_QuadraticInt_t(Structure):
    pass

struct_QuadraticInt_t._pack_ = 1 # source:False
struct_QuadraticInt_t._fields_ = [
    ('a', ctypes.c_uint32),
    ('b', ctypes.c_uint32),
    ('c', ctypes.c_uint32),
]

struct_AvfsFuseOverride_t._pack_ = 1 # source:False
struct_AvfsFuseOverride_t._fields_ = [
    ('AvfsTemp', ctypes.c_uint16 * 2),
    ('VftFMin', ctypes.c_uint16),
    ('VInversion', ctypes.c_uint16),
    ('qVft', struct_QuadraticInt_t * 2),
    ('qAvfsGb', struct_QuadraticInt_t),
    ('qAvfsGb2', struct_QuadraticInt_t),
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
    ('Reserved', ctypes.c_uint32 * 4),
]

class struct_OverDriveLimits_t(Structure):
    pass

struct_OverDriveLimits_t._pack_ = 1 # source:False
struct_OverDriveLimits_t._fields_ = [
    ('FeatureCtrlMask', ctypes.c_uint32),
    ('VoltageOffsetPerZoneBoundary', ctypes.c_int16),
    ('Reserved1', ctypes.c_uint16),
    ('Reserved2', ctypes.c_uint16),
    ('GfxclkFmin', ctypes.c_int16),
    ('GfxclkFmax', ctypes.c_int16),
    ('UclkFmin', ctypes.c_uint16),
    ('UclkFmax', ctypes.c_uint16),
    ('Ppt', ctypes.c_int16),
    ('Tdc', ctypes.c_int16),
    ('FanLinearPwmPoints', ctypes.c_ubyte),
    ('FanLinearTempPoints', ctypes.c_ubyte),
    ('FanMinimumPwm', ctypes.c_uint16),
    ('AcousticTargetRpmThreshold', ctypes.c_uint16),
    ('AcousticLimitRpmThreshold', ctypes.c_uint16),
    ('FanTargetTemperature', ctypes.c_uint16),
    ('FanZeroRpmEnable', ctypes.c_ubyte),
    ('FanZeroRpmStopTemp', ctypes.c_ubyte),
    ('FanMode', ctypes.c_ubyte),
    ('MaxOpTemp', ctypes.c_ubyte),
    ('Padding', ctypes.c_ubyte * 4),
    ('Spare', ctypes.c_uint32 * 12),
]

class struct_BootValues_t(Structure):
    pass

struct_BootValues_t._pack_ = 1 # source:False
struct_BootValues_t._fields_ = [
    ('InitGfxclk_bypass', ctypes.c_uint16),
    ('InitSocclk', ctypes.c_uint16),
    ('InitMp0clk', ctypes.c_uint16),
    ('InitMpioclk', ctypes.c_uint16),
    ('InitSmnclk', ctypes.c_uint16),
    ('InitUcpclk', ctypes.c_uint16),
    ('InitCsrclk', ctypes.c_uint16),
    ('InitDprefclk', ctypes.c_uint16),
    ('InitDcfclk', ctypes.c_uint16),
    ('InitDtbclk', ctypes.c_uint16),
    ('InitDclk', ctypes.c_uint16),
    ('InitVclk', ctypes.c_uint16),
    ('InitUsbdfsclk', ctypes.c_uint16),
    ('InitMp1clk', ctypes.c_uint16),
    ('InitLclk', ctypes.c_uint16),
    ('InitBaco400clk_bypass', ctypes.c_uint16),
    ('InitBaco1200clk_bypass', ctypes.c_uint16),
    ('InitBaco700clk_bypass', ctypes.c_uint16),
    ('InitFclk', ctypes.c_uint16),
    ('InitGfxclk_clkb', ctypes.c_uint16),
    ('InitUclkDPMState', ctypes.c_ubyte),
    ('Padding', ctypes.c_ubyte * 3),
    ('InitVcoFreqPll0', ctypes.c_uint32),
    ('InitVcoFreqPll1', ctypes.c_uint32),
    ('InitVcoFreqPll2', ctypes.c_uint32),
    ('InitVcoFreqPll3', ctypes.c_uint32),
    ('InitVcoFreqPll4', ctypes.c_uint32),
    ('InitVcoFreqPll5', ctypes.c_uint32),
    ('InitVcoFreqPll6', ctypes.c_uint32),
    ('InitGfx', ctypes.c_uint16),
    ('InitSoc', ctypes.c_uint16),
    ('InitU', ctypes.c_uint16),
    ('Padding2', ctypes.c_uint16),
    ('Spare', ctypes.c_uint32 * 8),
]

class struct_MsgLimits_t(Structure):
    pass

struct_MsgLimits_t._pack_ = 1 # source:False
struct_MsgLimits_t._fields_ = [
    ('Power', ctypes.c_uint16 * 2 * 4),
    ('Tdc', ctypes.c_uint16 * 3),
    ('Temperature', ctypes.c_uint16 * 13),
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

class struct_DpmDescriptor_t(Structure):
    pass

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

struct_SkuTable_t._pack_ = 1 # source:False
struct_SkuTable_t._fields_ = [
    ('Version', ctypes.c_uint32),
    ('FeaturesToRun', ctypes.c_uint32 * 2),
    ('TotalPowerConfig', ctypes.c_ubyte),
    ('CustomerVariant', ctypes.c_ubyte),
    ('MemoryTemperatureTypeMask', ctypes.c_ubyte),
    ('SmartShiftVersion', ctypes.c_ubyte),
    ('SocketPowerLimitAc', ctypes.c_uint16 * 4),
    ('SocketPowerLimitDc', ctypes.c_uint16 * 4),
    ('SocketPowerLimitSmartShift2', ctypes.c_uint16),
    ('EnableLegacyPptLimit', ctypes.c_ubyte),
    ('UseInputTelemetry', ctypes.c_ubyte),
    ('SmartShiftMinReportedPptinDcs', ctypes.c_ubyte),
    ('PaddingPpt', ctypes.c_ubyte * 1),
    ('VrTdcLimit', ctypes.c_uint16 * 3),
    ('PlatformTdcLimit', ctypes.c_uint16 * 3),
    ('TemperatureLimit', ctypes.c_uint16 * 13),
    ('HwCtfTempLimit', ctypes.c_uint16),
    ('PaddingInfra', ctypes.c_uint16),
    ('FitControllerFailureRateLimit', ctypes.c_uint32),
    ('FitControllerGfxDutyCycle', ctypes.c_uint32),
    ('FitControllerSocDutyCycle', ctypes.c_uint32),
    ('FitControllerSocOffset', ctypes.c_uint32),
    ('GfxApccPlusResidencyLimit', ctypes.c_uint32),
    ('ThrottlerControlMask', ctypes.c_uint32),
    ('FwDStateMask', ctypes.c_uint32),
    ('UlvVoltageOffset', ctypes.c_uint16 * 2),
    ('UlvVoltageOffsetU', ctypes.c_uint16),
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
    ('Vmin_droop', struct_QuadraticInt_t),
    ('SpareVmin', ctypes.c_uint32 * 9),
    ('DpmDescriptor', struct_DpmDescriptor_t * 13),
    ('FreqTableGfx', ctypes.c_uint16 * 16),
    ('FreqTableVclk', ctypes.c_uint16 * 8),
    ('FreqTableDclk', ctypes.c_uint16 * 8),
    ('FreqTableSocclk', ctypes.c_uint16 * 8),
    ('FreqTableUclk', ctypes.c_uint16 * 4),
    ('FreqTableDispclk', ctypes.c_uint16 * 8),
    ('FreqTableDppClk', ctypes.c_uint16 * 8),
    ('FreqTableDprefclk', ctypes.c_uint16 * 8),
    ('FreqTableDcfclk', ctypes.c_uint16 * 8),
    ('FreqTableDtbclk', ctypes.c_uint16 * 8),
    ('FreqTableFclk', ctypes.c_uint16 * 8),
    ('DcModeMaxFreq', ctypes.c_uint32 * 13),
    ('Mp0clkFreq', ctypes.c_uint16 * 2),
    ('Mp0DpmVoltage', ctypes.c_uint16 * 2),
    ('GfxclkSpare', ctypes.c_ubyte * 2),
    ('GfxclkFreqCap', ctypes.c_uint16),
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
    ('DfllBtcMasterScalerM', ctypes.c_uint32),
    ('DfllBtcMasterScalerB', ctypes.c_int32),
    ('DfllBtcSlaveScalerM', ctypes.c_uint32),
    ('DfllBtcSlaveScalerB', ctypes.c_int32),
    ('DfllPccAsWaitCtrl', ctypes.c_uint32),
    ('DfllPccAsStepCtrl', ctypes.c_uint32),
    ('GfxGpoSpare', ctypes.c_uint32 * 10),
    ('DcsGfxOffVoltage', ctypes.c_uint16),
    ('PaddingDcs', ctypes.c_uint16),
    ('DcsMinGfxOffTime', ctypes.c_uint16),
    ('DcsMaxGfxOffTime', ctypes.c_uint16),
    ('DcsMinCreditAccum', ctypes.c_uint32),
    ('DcsExitHysteresis', ctypes.c_uint16),
    ('DcsTimeout', ctypes.c_uint16),
    ('DcsSpare', ctypes.c_uint32 * 14),
    ('ShadowFreqTableUclk', ctypes.c_uint16 * 4),
    ('UseStrobeModeOptimizations', ctypes.c_ubyte),
    ('PaddingMem', ctypes.c_ubyte * 3),
    ('UclkDpmPstates', ctypes.c_ubyte * 4),
    ('FreqTableUclkDiv', ctypes.c_ubyte * 4),
    ('MemVmempVoltage', ctypes.c_uint16 * 4),
    ('MemVddioVoltage', ctypes.c_uint16 * 4),
    ('FclkDpmUPstates', ctypes.c_ubyte * 8),
    ('FclkDpmVddU', ctypes.c_uint16 * 8),
    ('FclkDpmUSpeed', ctypes.c_uint16 * 8),
    ('FclkDpmDisallowPstateFreq', ctypes.c_uint16),
    ('PaddingFclk', ctypes.c_uint16),
    ('PcieGenSpeed', ctypes.c_ubyte * 3),
    ('PcieLaneCount', ctypes.c_ubyte * 3),
    ('LclkFreq', ctypes.c_uint16 * 3),
    ('FanStopTemp', ctypes.c_uint16 * 13),
    ('FanStartTemp', ctypes.c_uint16 * 13),
    ('FanGain', ctypes.c_uint16 * 13),
    ('FanGainPadding', ctypes.c_uint16),
    ('FanPwmMin', ctypes.c_uint16),
    ('AcousticTargetRpmThreshold', ctypes.c_uint16),
    ('AcousticLimitRpmThreshold', ctypes.c_uint16),
    ('FanMaximumRpm', ctypes.c_uint16),
    ('MGpuAcousticLimitRpmThreshold', ctypes.c_uint16),
    ('FanTargetGfxclk', ctypes.c_uint16),
    ('TempInputSelectMask', ctypes.c_uint32),
    ('FanZeroRpmEnable', ctypes.c_ubyte),
    ('FanTachEdgePerRev', ctypes.c_ubyte),
    ('FanTargetTemperature', ctypes.c_uint16 * 13),
    ('FuzzyFan_ErrorSetDelta', ctypes.c_int16),
    ('FuzzyFan_ErrorRateSetDelta', ctypes.c_int16),
    ('FuzzyFan_PwmSetDelta', ctypes.c_int16),
    ('FuzzyFan_Reserved', ctypes.c_uint16),
    ('FwCtfLimit', ctypes.c_uint16 * 13),
    ('IntakeTempEnableRPM', ctypes.c_uint16),
    ('IntakeTempOffsetTemp', ctypes.c_int16),
    ('IntakeTempReleaseTemp', ctypes.c_uint16),
    ('IntakeTempHighIntakeAcousticLimit', ctypes.c_uint16),
    ('IntakeTempAcouticLimitReleaseRate', ctypes.c_uint16),
    ('FanAbnormalTempLimitOffset', ctypes.c_int16),
    ('FanStalledTriggerRpm', ctypes.c_uint16),
    ('FanAbnormalTriggerRpmCoeff', ctypes.c_uint16),
    ('FanAbnormalDetectionEnable', ctypes.c_uint16),
    ('FanIntakeSensorSupport', ctypes.c_ubyte),
    ('FanIntakePadding', ctypes.c_ubyte * 3),
    ('FanSpare', ctypes.c_uint32 * 13),
    ('OverrideGfxAvfsFuses', ctypes.c_ubyte),
    ('GfxAvfsPadding', ctypes.c_ubyte * 3),
    ('L2HwRtAvfsFuses', ctypes.c_uint32 * 32),
    ('SeHwRtAvfsFuses', ctypes.c_uint32 * 32),
    ('CommonRtAvfs', ctypes.c_uint32 * 13),
    ('L2FwRtAvfsFuses', ctypes.c_uint32 * 19),
    ('SeFwRtAvfsFuses', ctypes.c_uint32 * 19),
    ('Droop_PWL_F', ctypes.c_uint32 * 5),
    ('Droop_PWL_a', ctypes.c_uint32 * 5),
    ('Droop_PWL_b', ctypes.c_uint32 * 5),
    ('Droop_PWL_c', ctypes.c_uint32 * 5),
    ('Static_PWL_Offset', ctypes.c_uint32 * 5),
    ('dGbV_dT_vmin', ctypes.c_uint32),
    ('dGbV_dT_vmax', ctypes.c_uint32),
    ('V2F_vmin_range_low', ctypes.c_uint32),
    ('V2F_vmin_range_high', ctypes.c_uint32),
    ('V2F_vmax_range_low', ctypes.c_uint32),
    ('V2F_vmax_range_high', ctypes.c_uint32),
    ('DcBtcGfxParams', struct_AvfsDcBtcParams_t),
    ('GfxAvfsSpare', ctypes.c_uint32 * 32),
    ('OverrideSocAvfsFuses', ctypes.c_ubyte),
    ('MinSocAvfsRevision', ctypes.c_ubyte),
    ('SocAvfsPadding', ctypes.c_ubyte * 2),
    ('SocAvfsFuseOverride', struct_AvfsFuseOverride_t * 3),
    ('dBtcGbSoc', struct_DroopInt_t * 3),
    ('qAgingGb', struct_LinearInt_t * 3),
    ('qStaticVoltageOffset', struct_QuadraticInt_t * 3),
    ('DcBtcSocParams', struct_AvfsDcBtcParams_t * 3),
    ('SocAvfsSpare', ctypes.c_uint32 * 32),
    ('BootValues', struct_BootValues_t),
    ('DriverReportedClocks', struct_DriverReportedClocks_t),
    ('MsgLimits', struct_MsgLimits_t),
    ('OverDriveLimitsMin', struct_OverDriveLimits_t),
    ('OverDriveLimitsBasicMax', struct_OverDriveLimits_t),
    ('OverDriveLimitsAdvancedMax', struct_OverDriveLimits_t),
    ('DebugOverrides', ctypes.c_uint32),
    ('TotalBoardPowerSupport', ctypes.c_ubyte),
    ('TotalBoardPowerPadding', ctypes.c_ubyte * 3),
    ('TotalIdleBoardPowerM', ctypes.c_int16),
    ('TotalIdleBoardPowerB', ctypes.c_int16),
    ('TotalBoardPowerM', ctypes.c_int16),
    ('TotalBoardPowerB', ctypes.c_int16),
    ('qFeffCoeffGameClock', struct_QuadraticInt_t * 2),
    ('qFeffCoeffBaseClock', struct_QuadraticInt_t * 2),
    ('qFeffCoeffBoostClock', struct_QuadraticInt_t * 2),
    ('Spare', ctypes.c_uint32 * 43),
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

class struct_SviTelemetryScale_t(Structure):
    pass

struct_SviTelemetryScale_t._pack_ = 1 # source:False
struct_SviTelemetryScale_t._fields_ = [
    ('Offset', ctypes.c_byte),
    ('Padding', ctypes.c_ubyte),
    ('MaxCurrent', ctypes.c_uint16),
]

struct_BoardTable_t._pack_ = 1 # source:False
struct_BoardTable_t._fields_ = [
    ('Version', ctypes.c_uint32),
    ('I2cControllers', struct_I2cControllerConfig_t * 8),
    ('VddGfxVrMapping', ctypes.c_ubyte),
    ('VddSocVrMapping', ctypes.c_ubyte),
    ('VddMem0VrMapping', ctypes.c_ubyte),
    ('VddMem1VrMapping', ctypes.c_ubyte),
    ('GfxUlvPhaseSheddingMask', ctypes.c_ubyte),
    ('SocUlvPhaseSheddingMask', ctypes.c_ubyte),
    ('VmempUlvPhaseSheddingMask', ctypes.c_ubyte),
    ('VddioUlvPhaseSheddingMask', ctypes.c_ubyte),
    ('SlaveAddrMapping', ctypes.c_ubyte * 5),
    ('VrPsiSupport', ctypes.c_ubyte * 5),
    ('PaddingPsi', ctypes.c_ubyte * 5),
    ('EnablePsi6', ctypes.c_ubyte * 5),
    ('SviTelemetryScale', struct_SviTelemetryScale_t * 5),
    ('VoltageTelemetryRatio', ctypes.c_uint32 * 5),
    ('DownSlewRateVr', ctypes.c_ubyte * 5),
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
    ('UclkTrainingModeSpreadPercent', ctypes.c_ubyte),
    ('UclkSpreadPadding', ctypes.c_ubyte),
    ('UclkSpreadFreq', ctypes.c_uint16),
    ('UclkSpreadPercent', ctypes.c_ubyte * 16),
    ('FclkSpreadPadding', ctypes.c_ubyte),
    ('FclkSpreadPercent', ctypes.c_ubyte),
    ('FclkSpreadFreq', ctypes.c_uint16),
    ('DramWidth', ctypes.c_ubyte),
    ('PaddingMem1', ctypes.c_ubyte * 7),
    ('HsrEnabled', ctypes.c_ubyte),
    ('VddqOffEnabled', ctypes.c_ubyte),
    ('PaddingUmcFlags', ctypes.c_ubyte * 2),
    ('PostVoltageSetBacoDelay', ctypes.c_uint32),
    ('BacoEntryDelay', ctypes.c_uint32),
    ('FuseWritePowerMuxPresent', ctypes.c_ubyte),
    ('FuseWritePadding', ctypes.c_ubyte * 3),
    ('BoardSpare', ctypes.c_uint32 * 63),
    ('MmHubPadding', ctypes.c_uint32 * 8),
]

struct_PPTable_t._pack_ = 1 # source:False
struct_PPTable_t._fields_ = [
    ('SkuTable', struct_SkuTable_t),
    ('BoardTable', struct_BoardTable_t),
]

class struct_atom_common_table_header(Structure):
    pass

struct_atom_common_table_header._pack_ = 1 # source:False
struct_atom_common_table_header._fields_ = [
    ('structuresize', ctypes.c_uint16),
    ('format_revision', ctypes.c_ubyte),
    ('content_revision', ctypes.c_ubyte),
]

struct_smu_13_0_7_powerplay_table._pack_ = 1 # source:False
struct_smu_13_0_7_powerplay_table._fields_ = [
    ('header', struct_atom_common_table_header),
    ('table_revision', ctypes.c_ubyte),
    ('padding', ctypes.c_ubyte),
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
    ('reserve', ctypes.c_uint32 * 45),
    ('overdrive_table', struct_smu_13_0_7_overdrive_table),
    ('padding1', ctypes.c_ubyte),
    ('smc_pptable', struct_PPTable_t),
]

__all__ = \
    ['SMU_13_0_7_MAX_ODFEATURE', 'SMU_13_0_7_MAX_ODSETTING',
    'SMU_13_0_7_MAX_PMSETTING', 'SMU_13_0_7_MAX_PPCLOCK',
    'SMU_13_0_7_ODCAP_AUTO_FAN_ACOUSTIC_LIMIT',
    'SMU_13_0_7_ODCAP_AUTO_OC_ENGINE',
    'SMU_13_0_7_ODCAP_AUTO_OC_MEMORY',
    'SMU_13_0_7_ODCAP_AUTO_UV_ENGINE', 'SMU_13_0_7_ODCAP_COUNT',
    'SMU_13_0_7_ODCAP_FAN_ACOUSTIC_LIMIT',
    'SMU_13_0_7_ODCAP_FAN_CURVE', 'SMU_13_0_7_ODCAP_FAN_SPEED_MIN',
    'SMU_13_0_7_ODCAP_FAN_ZERO_RPM_CONTROL',
    'SMU_13_0_7_ODCAP_GFXCLK_LIMITS',
    'SMU_13_0_7_ODCAP_MEMORY_TIMING_TUNE',
    'SMU_13_0_7_ODCAP_PER_ZONE_GFX_VOLTAGE_OFFSET',
    'SMU_13_0_7_ODCAP_POWER_LIMIT', 'SMU_13_0_7_ODCAP_POWER_MODE',
    'SMU_13_0_7_ODCAP_TEMPERATURE_FAN',
    'SMU_13_0_7_ODCAP_TEMPERATURE_SYSTEM',
    'SMU_13_0_7_ODCAP_UCLK_LIMITS',
    'SMU_13_0_7_ODFEATURE_AUTO_FAN_ACOUSTIC_LIMIT',
    'SMU_13_0_7_ODFEATURE_AUTO_OC_ENGINE',
    'SMU_13_0_7_ODFEATURE_AUTO_OC_MEMORY',
    'SMU_13_0_7_ODFEATURE_AUTO_UV_ENGINE', 'SMU_13_0_7_ODFEATURE_CAP',
    'SMU_13_0_7_ODFEATURE_COUNT',
    'SMU_13_0_7_ODFEATURE_FAN_ACOUSTIC_LIMIT',
    'SMU_13_0_7_ODFEATURE_FAN_CURVE',
    'SMU_13_0_7_ODFEATURE_FAN_SPEED_MIN',
    'SMU_13_0_7_ODFEATURE_FAN_ZERO_RPM_CONTROL',
    'SMU_13_0_7_ODFEATURE_GFXCLK_LIMITS', 'SMU_13_0_7_ODFEATURE_ID',
    'SMU_13_0_7_ODFEATURE_MEMORY_TIMING_TUNE',
    'SMU_13_0_7_ODFEATURE_PER_ZONE_GFX_VOLTAGE_OFFSET',
    'SMU_13_0_7_ODFEATURE_POWER_LIMIT',
    'SMU_13_0_7_ODFEATURE_POWER_MODE',
    'SMU_13_0_7_ODFEATURE_TEMPERATURE_FAN',
    'SMU_13_0_7_ODFEATURE_TEMPERATURE_SYSTEM',
    'SMU_13_0_7_ODFEATURE_UCLK_LIMITS',
    'SMU_13_0_7_ODSETTING_ACTIMING',
    'SMU_13_0_7_ODSETTING_AUTOOCENGINE',
    'SMU_13_0_7_ODSETTING_AUTOOCMEMORY',
    'SMU_13_0_7_ODSETTING_AUTOUVENGINE',
    'SMU_13_0_7_ODSETTING_AUTO_FAN_ACOUSTIC_LIMIT',
    'SMU_13_0_7_ODSETTING_COUNT',
    'SMU_13_0_7_ODSETTING_FANRPMACOUSTICLIMIT',
    'SMU_13_0_7_ODSETTING_FANRPMMIN',
    'SMU_13_0_7_ODSETTING_FANTARGETTEMPERATURE',
    'SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_1',
    'SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_2',
    'SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_3',
    'SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_4',
    'SMU_13_0_7_ODSETTING_FAN_CURVE_SPEED_5',
    'SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_1',
    'SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_2',
    'SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_3',
    'SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_4',
    'SMU_13_0_7_ODSETTING_FAN_CURVE_TEMPERATURE_5',
    'SMU_13_0_7_ODSETTING_FAN_ZERO_RPM_CONTROL',
    'SMU_13_0_7_ODSETTING_GFXCLKFMAX',
    'SMU_13_0_7_ODSETTING_GFXCLKFMIN', 'SMU_13_0_7_ODSETTING_ID',
    'SMU_13_0_7_ODSETTING_OPERATINGTEMPMAX',
    'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_1',
    'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_2',
    'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_3',
    'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_4',
    'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_5',
    'SMU_13_0_7_ODSETTING_PER_ZONE_GFX_VOLTAGE_OFFSET_POINT_6',
    'SMU_13_0_7_ODSETTING_POWERPERCENTAGE',
    'SMU_13_0_7_ODSETTING_POWER_MODE',
    'SMU_13_0_7_ODSETTING_UCLKFMAX', 'SMU_13_0_7_ODSETTING_UCLKFMIN',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_BALANCE',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_QUIET',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_RAGE',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_LIMIT_RPM_TURBO',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_BALANCE',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_QUIET',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_RAGE',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_TARGET_RPM_TURBO',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_BALANCE',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_QUIET',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_RAGE',
    'SMU_13_0_7_PMSETTING_ACOUSTIC_TEMP_TURBO',
    'SMU_13_0_7_PMSETTING_POWER_LIMIT_BALANCE',
    'SMU_13_0_7_PMSETTING_POWER_LIMIT_QUIET',
    'SMU_13_0_7_PMSETTING_POWER_LIMIT_RAGE',
    'SMU_13_0_7_PMSETTING_POWER_LIMIT_TURBO',
    'SMU_13_0_7_PPCLOCK_COUNT', 'SMU_13_0_7_PPCLOCK_DCEFCLK',
    'SMU_13_0_7_PPCLOCK_DCLK_0', 'SMU_13_0_7_PPCLOCK_DCLK_1',
    'SMU_13_0_7_PPCLOCK_DISPCLK', 'SMU_13_0_7_PPCLOCK_DTBCLK',
    'SMU_13_0_7_PPCLOCK_FCLK', 'SMU_13_0_7_PPCLOCK_GFXCLK',
    'SMU_13_0_7_PPCLOCK_ID', 'SMU_13_0_7_PPCLOCK_PHYCLK',
    'SMU_13_0_7_PPCLOCK_PIXCLK', 'SMU_13_0_7_PPCLOCK_SOCCLK',
    'SMU_13_0_7_PPCLOCK_UCLK', 'SMU_13_0_7_PPCLOCK_VCLK_0',
    'SMU_13_0_7_PPCLOCK_VCLK_1', 'SMU_13_0_7_PPTABLE_H',
    'SMU_13_0_7_PP_OVERDRIVE_VERSION',
    'SMU_13_0_7_PP_PLATFORM_CAP_BACO',
    'SMU_13_0_7_PP_PLATFORM_CAP_HARDWAREDC',
    'SMU_13_0_7_PP_PLATFORM_CAP_MACO',
    'SMU_13_0_7_PP_PLATFORM_CAP_POWERPLAY',
    'SMU_13_0_7_PP_PLATFORM_CAP_SBIOSPOWERSOURCE',
    'SMU_13_0_7_PP_PLATFORM_CAP_SHADOWPSTATE',
    'SMU_13_0_7_PP_POWERSAVINGCLOCK_VERSION',
    'SMU_13_0_7_PP_THERMALCONTROLLER_NAVI21',
    'SMU_13_0_7_PP_THERMALCONTROLLER_NONE',
    'SMU_13_0_7_PWRMODE_SETTING', 'SMU_13_0_7_TABLE_FORMAT_REVISION',
    'struct_AvfsDcBtcParams_t', 'struct_AvfsFuseOverride_t',
    'struct_BoardTable_t', 'struct_BootValues_t',
    'struct_DpmDescriptor_t', 'struct_DriverReportedClocks_t',
    'struct_DroopInt_t', 'struct_I2cControllerConfig_t',
    'struct_LinearInt_t', 'struct_MsgLimits_t',
    'struct_OverDriveLimits_t', 'struct_PPTable_t',
    'struct_QuadraticInt_t', 'struct_SkuTable_t',
    'struct_SviTelemetryScale_t', 'struct_atom_common_table_header',
    'struct_smu_13_0_7_overdrive_table',
    'struct_smu_13_0_7_powerplay_table']
