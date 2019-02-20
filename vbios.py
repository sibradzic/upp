# Inspired by:
#   https://github.com/kobalicek/amdtweak/blob/master/lib/vbios.js
#   https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/amd/powerplay

# Don't expect this to be anywhere close to PEP8 standards

# Mapping between base C types and Python struct types, '<' indicates little-endian
base_types = [ 'B', 'b', '<H', '<h', '<I', '<i', 'f']
uint8_t  =  'B'
int8_t   =  'b'
uint16_t = '<H'
int16_t  = '<h'
uint32_t = '<I'
int32_t  = '<i'
float32  =  'f'

# Common PowerPlay header for all GCN Radeon GPUs
PowerPlay_header = [
    { 'name': 'StructureSize'                  , 'type': 'uint16_t' },
    { 'name': 'TableFormatRevision'            , 'type': 'uint8_t', 'ref': 'PowerPlayTable' },
    { 'name': 'TableContentRevision'           , 'type': 'uint8_t'  }
]

# Polaris, Tonga
PowerPlayTable_v7 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "TableSize"                      , 'type': 'uint16_t' },
    { 'name': "GoldenPPId"                     , 'type': 'uint32_t' }, # PPGen use only
    { 'name': "GoldenRevision"                 , 'type': 'uint32_t' }, # PPGen use only
    { 'name': "FormatId"                       , 'type': 'uint16_t' }, # PPGen use only
    { 'name': "VoltageTime"                    , 'type': 'uint16_t' }, # In [ms]
    { 'name': "PlatformCaps"                   , 'type': 'uint32_t' },
    { 'name': "SocClockMaxOD"                  , 'type': 'uint32_t' },
    { 'name': "MemClockMaxOD"                  , 'type': 'uint32_t' },
    { 'name': "PowerControlLimit"              , 'type': 'uint16_t' },
    { 'name': "UlvVoltageOffset"               , 'type': 'uint16_t' }, # In [mV] unit
    { 'name': "StateTable"                     , 'type': 'uint16_t' , 'ref': 'StateTable'               },
    { 'name': "FanTable"                       , 'type': 'uint16_t' , 'ref': 'FanTable'                 },
    { 'name': "ThermalController"              , 'type': 'uint16_t' , 'ref': 'ThermalController'        },
    { 'name': "Reserved1"                      , 'type': 'uint16_t' },
    { 'name': "MemClockDependencyTable"        , 'type': 'uint16_t' , 'ref': 'MemClockDependencyTable'  },
    { 'name': "SocClockDependencyTable"        , 'type': 'uint16_t' , 'ref': 'SocClockDependencyTable'  },
    { 'name': "VddcLookupTable"                , 'type': 'uint16_t' , 'ref': 'VoltageLookupTable'       },
    { 'name': "VddGfxLookupTable"              , 'type': 'uint16_t' , 'ref': 'VoltageLookupTable'       },
    { 'name': "MMDependencyTable"              , 'type': 'uint16_t' , 'ref': 'MMDependencyTable'        },
    { 'name': "VCEStateTable"                  , 'type': 'uint16_t' , 'ref': 'VCEStateTable'            },
    { 'name': "PPMTable"                       , 'type': 'uint16_t' , 'ref': 'PPMTable'                 },
    { 'name': "PowerTuneTable"                 , 'type': 'uint16_t' , 'ref': 'PowerTuneTable'           },
    { 'name': "HardLimitTable"                 , 'type': 'uint16_t' , 'ref': 'HardLimitTable'           },
    { 'name': "PCIETable"                      , 'type': 'uint16_t' , 'ref': 'PCIETable'                },
    { 'name': "GPIOTable"                      , 'type': 'uint16_t' , 'ref': 'GPIOTable'                },
    { 'name': "Reserved2"                      , 'type': 'uint16_t' },
    { 'name': "Reserved3"                      , 'type': 'uint16_t' },
    { 'name': "Reserved4"                      , 'type': 'uint16_t' },
    { 'name': "Reserved5"                      , 'type': 'uint16_t' },
    { 'name': "Reserved6"                      , 'type': 'uint16_t' },
    { 'name': "Reserved7"                      , 'type': 'uint16_t' }
]
# Vega 10
PowerPlayTable_v8 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "TableSize"                      , 'type': 'uint16_t' },
    { 'name': "GoldenPPId"                     , 'type': 'uint32_t' },
    { 'name': "GoldenRevision"                 , 'type': 'uint32_t' },
    { 'name': "FormatId"                       , 'type': 'uint16_t' },
    { 'name': "PlatformCaps"                   , 'type': 'uint32_t' },
    { 'name': "SocClockMaxOD"                  , 'type': 'uint32_t' },
    { 'name': "MemClockMaxOD"                  , 'type': 'uint32_t' },
    { 'name': "PowerControlLimit"              , 'type': 'uint16_t' },
    { 'name': "UlvVoltageOffset"               , 'type': 'uint16_t' }, # In [mV] unit.
    { 'name': "UlvSmnClockDid"                 , 'type': 'uint16_t' },
    { 'name': "UlvMp1ClockDid"                 , 'type': 'uint16_t' },
    { 'name': "UlvGfxClockBypass"              , 'type': 'uint16_t' },
    { 'name': "GfxClockSlewRate"               , 'type': 'uint16_t' },
    { 'name': "GfxVoltageMode"                 , 'type': 'uint8_t'  },
    { 'name': "SocVoltageMode"                 , 'type': 'uint8_t'  },
    { 'name': "UCLKVoltageMode"                , 'type': 'uint8_t'  },
    { 'name': "UVDVoltageMode"                 , 'type': 'uint8_t'  },
    { 'name': "VCEVoltageMode"                 , 'type': 'uint8_t'  },
    { 'name': "Mp0VoltageMode"                 , 'type': 'uint8_t'  },
    { 'name': "DCEFVoltageMode"                , 'type': 'uint8_t'  },
    { 'name': "StateTable"                     , 'type': 'uint16_t' , 'ref': 'StateTable'               },
    { 'name': "FanTable"                       , 'type': 'uint16_t' , 'ref': 'FanTable'                 },
    { 'name': "ThermalController"              , 'type': 'uint16_t' , 'ref': 'ThermalController'        },
    { 'name': "SocClockDependencyTable"        , 'type': 'uint16_t' , 'ref': 'SocClockDependencyTable'  },
    { 'name': "MemClockDependencyTable"        , 'type': 'uint16_t' , 'ref': 'MemClockDependencyTable'  },
    { 'name': "GfxClockDependencyTable"        , 'type': 'uint16_t' , 'ref': 'GfxClockDependencyTable'  },
    { 'name': "DcefClockDependencyTable"       , 'type': 'uint16_t' , 'ref': 'DcefClockDependencyTable' },
    { 'name': "VddcLookupTable"                , 'type': 'uint16_t' , 'ref': 'VoltageLookupTable'       },
    { 'name': "VddGfxLookupTable"              , 'type': 'uint16_t' , 'ref': 'VoltageLookupTable'       },
    { 'name': "MMDependencyTable"              , 'type': 'uint16_t' , 'ref': 'MMDependencyTable'        },
    { 'name': "VCEStateTable"                  , 'type': 'uint16_t' , 'ref': 'VCEStateTable'            },
    { 'name': "Reserved"                       , 'type': 'uint16_t' },
    { 'name': "PowerTuneTable"                 , 'type': 'uint16_t' , 'ref': 'PowerTuneTable'           },
    { 'name': "HardLimitTable"                 , 'type': 'uint16_t' , 'ref': 'HardLimitTable'           },
    { 'name': "VddciLookupTable"               , 'type': 'uint16_t' , 'ref': 'VoltageLookupTable'       },
    { 'name': "PCIETable"                      , 'type': 'uint16_t' , 'ref': 'PCIETable'                },
    { 'name': "PixClockDependencyTable"        , 'type': 'uint16_t' , 'ref': 'PixClockDependencyTable'  },
    { 'name': "DispClockDependencyTable"       , 'type': 'uint16_t' , 'ref': 'DispClockDependencyTable' },
    { 'name': "PhyClockDependencyTable"        , 'type': 'uint16_t' , 'ref': 'PhyClockDependencyTable'  }
]

# Vega VII, totally flat table without any offsets and sub-table revision info?!
# drivers/gpu/drm/amd/powerplay/hwmgr/vega20_pptable.h
PowerPlayTable_v11 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "TableSize"                      , 'type': 'uint16_t' },
    { 'name': "GoldenPPId"                     , 'type': 'uint32_t' },
    { 'name': "GoldenRevision"                 , 'type': 'uint32_t' },
    { 'name': "FormatId"                       , 'type': 'uint16_t' },
    { 'name': "PlatformCaps"                   , 'type': 'uint32_t' },
    { 'name': "ThermalControllerType"          , 'type': 'uint8_t'  },
    { 'name': "SmallPowerLimit1"               , 'type': 'uint16_t' },
    { 'name': "SmallPowerLimit2"               , 'type': 'uint16_t' },
    { 'name': "BoostPowerLimit"                , 'type': 'uint16_t' },
    { 'name': "ODTurboPowerLimit"              , 'type': 'uint16_t' },
    { 'name': "ODPowerSavePowerLimit"          , 'type': 'uint16_t' },
    { 'name': "SoftwareShutdownTemp"           , 'type': 'uint16_t' },
    { 'name': "PowerSavingClockTable"          , 'type': 'ATOM_VEGA20_POWER_SAVING_CLOCK_RECORD' }, # PowerSavingClock Mode Clock Min/Max array
    { 'name': "OverDrive8Table"                , 'type': 'ATOM_VEGA20_OVERDRIVE8_RECORD' },         # OverDrive8 Feature capabilities and Settings Range (Max and Min)
    { 'name': "Reserved"                       , 'type': 'uint16_t'  , 'max_count': 5 },
    { 'name': "smcPPTable"                     , 'type': 'PPTable_t' }
]

ATOM_VEGA20_PPCLOCK_MAX_COUNT = 16
ATOM_VEGA20_POWER_SAVING_CLOCK_RECORD = [
    { 'name': "ucTableRevision"                , 'type': 'uint8_t'  },
    { 'name': "PowerSavingClockCount"          , 'type': 'uint32_t' },
    { 'name': "PowerSavingClockMax"            , 'type': 'PowerSavingClockMax', 'max_count': ATOM_VEGA20_PPCLOCK_MAX_COUNT },
    { 'name': "PowerSavingClockMin"            , 'type': 'PowerSavingClockMin', 'max_count': ATOM_VEGA20_PPCLOCK_MAX_COUNT }
]
PowerSavingClockMax = PowerSavingClockMin = [
    { 'name': "Frequency"                      , 'type': 'uint32_t' }
]

ATOM_VEGA20_ODFEATURE_MAX_COUNT = ATOM_VEGA20_ODSETTING_MAX_COUNT = 32
ATOM_VEGA20_OVERDRIVE8_RECORD = [
    { 'name': "ucODTableRevision"              , 'type': 'uint8_t'  },
    { 'name': "ODFeatureCount"                 , 'type': 'uint32_t' },
    { 'name': "ODFeatureCapabilities"          , 'type': 'ODFeatureCapabilities', 'max_count': ATOM_VEGA20_ODFEATURE_MAX_COUNT },
    { 'name': "ODSettingCount"                 , 'type': 'uint32_t' },
    { 'name': "ODSettingsMax"                  , 'type': 'ODSettingsMax', 'max_count': ATOM_VEGA20_ODSETTING_MAX_COUNT },
    { 'name': "ODSettingsMin"                  , 'type': 'ODSettingsMin', 'max_count': ATOM_VEGA20_ODSETTING_MAX_COUNT }
]
ODFeatureCapabilities = [
    { 'name': "Capability"                     , 'type': 'uint8_t'  }
]
ODSettingsMax = ODSettingsMin = [
    { 'name': "Setting"                        , 'type': 'uint32_t' }
]

StateTable_v1 = StateTable_v2 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t', 'ref': 'StateEntry' },
]
StateEntry_v1 = StateEntry_v2 = [
    { 'name': "SocClockIndexHigh"              , 'type': 'uint8_t'  },
    { 'name': "SocClockIndexLow"               , 'type': 'uint8_t'  },
    { 'name': "MemClockIndexHigh"              , 'type': 'uint8_t'  },
    { 'name': "MemClockIndexLow"               , 'type': 'uint8_t'  },
    { 'name': "PCIEGenLow"                     , 'type': 'uint8_t'  },
    { 'name': "PCIEGenHigh"                    , 'type': 'uint8_t'  },
    { 'name': "PCIELaneLow"                    , 'type': 'uint8_t'  },
    { 'name': "PCIELaneHigh"                   , 'type': 'uint8_t'  },
    { 'name': "Classification"                 , 'type': 'uint16_t' },
    { 'name': "CapsAndSettings"                , 'type': 'uint32_t' },
    { 'name': "Classification2"                , 'type': 'uint16_t' },
    { 'name': "Reserved1"                      , 'type': 'uint32_t' }
]

DcefClockDependencyTable_v0 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t', 'ref': 'DcefClockDependencyEntry' },
]
DcefClockDependencyEntry_v0 = [
    { 'name': "Clock"                          , 'type': 'uint32_t' },
    { 'name': "VddIndex"                       , 'type': 'uint8_t'  }  # Base voltage.
]

FanTable_v9 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "THyst"                          , 'type': 'uint8_t'  }, # Temperature hysteresis.
    { 'name': "TMin"                           , 'type': 'uint16_t' }, # The temperature, in 0.01 centigrades, below which we just run at a minimal PWM.
    { 'name': "TMed"                           , 'type': 'uint16_t' }, # The middle temperature where we change slopes.
    { 'name': "THigh"                          , 'type': 'uint16_t' }, # The high point above TMed for adjusting the second slope.
    { 'name': "PWMMin"                         , 'type': 'uint16_t' }, # The minimum PWM value in percent (0.01% increments).
    { 'name': "PWMMed"                         , 'type': 'uint16_t' }, # The PWM value (in percent) at TMed.
    { 'name': "PWMHigh"                        , 'type': 'uint16_t' }, # The PWM value at THigh.
    { 'name': "TMax"                           , 'type': 'uint16_t' }, # The max temperature.
    { 'name': "FanControlMode"                 , 'type': 'uint8_t'  }, # Legacy or Fuzzy Fan mode.
    { 'name': "FanPWMMax"                      , 'type': 'uint16_t' }, # Maximum allowed fan power in percent.
    { 'name': "FanOutputSensitivity"           , 'type': 'uint16_t' }, # Sensitivity of fan reaction to temepature changes.
    { 'name': "FanRPMMax"                      , 'type': 'uint16_t' }, # The default value in RPM.
    { 'name': "MinFanSocClockAcousticLimit"    , 'type': 'uint32_t' }, # Minimum fan controller SOC clock frequency acoustic limit.
    { 'name': "TargetTemperature"              , 'type': 'uint8_t'  }, # Advanced fan controller target temperature.
    { 'name': "MinimumPWMLimit"                , 'type': 'uint8_t'  }, # The minimum PWM that the advanced fan controller can set.  This should be set to the highest PWM that will run the fan at its lowest RPM.
    { 'name': "Reserved1"                      , 'type': 'uint16_t' }
]
FanTable_v11 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "FanOutputSensitivity"           , 'type': 'uint16_t' },
    { 'name': "FanAcousticLimitRPM"            , 'type': 'uint16_t' },
    { 'name': "ThrottlingRPM"                  , 'type': 'uint16_t' },
    { 'name': "TargetTemperature"              , 'type': 'uint16_t' },
    { 'name': "MinimumPWMLimit"                , 'type': 'uint16_t' },
    { 'name': "TargetGfxClock"                 , 'type': 'uint16_t' },
    { 'name': "FanGainEdge"                    , 'type': 'uint16_t' },
    { 'name': "FanGainHotspot"                 , 'type': 'uint16_t' },
    { 'name': "FanGainLiquid"                  , 'type': 'uint16_t' },
    { 'name': "FanGainVrVddc"                  , 'type': 'uint16_t' },
    { 'name': "FanGainVrMvdd"                  , 'type': 'uint16_t' },
    { 'name': "FanGainPPX"                     , 'type': 'uint16_t' },
    { 'name': "FanGainHBM"                     , 'type': 'uint16_t' },
    { 'name': "EnableZeroRPM"                  , 'type': 'uint8_t'  },
    { 'name': "FanStopTemperature"             , 'type': 'uint16_t' },
    { 'name': "FanStartTemperature"            , 'type': 'uint16_t' },
    { 'name': "FanParameters"                  , 'type': 'uint8_t'  },
    { 'name': "FanMinRPM"                      , 'type': 'uint8_t'  },
    { 'name': "FanMaxRPM"                      , 'type': 'uint8_t'  }
]

ThermalController_v1 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "ControlType"                    , 'type': 'uint8_t'  },
    { 'name': "I2CLine"                        , 'type': 'uint8_t'  }, # As interpreted by DAL I2C.
    { 'name': "I2CAddress"                     , 'type': 'uint8_t'  },
    { 'name': "FanParameters"                  , 'type': 'uint8_t'  },
    { 'name': "FanMinRPM"                      , 'type': 'uint8_t'  }, # Minimum RPM (hundreds), for display purposes only.
    { 'name': "FanMaxRPM"                      , 'type': 'uint8_t'  }, # Maximum RPM (hundreds), for display purposes only.
    { 'name': "Reserved1"                      , 'type': 'uint8_t'  },
    { 'name': "Flags"                          , 'type': 'uint8_t'  }
]

MemClockDependencyTable_v0 = MemClockDependencyTable_v1 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t', 'ref': 'MemClockDependencyEntry' }
]
MemClockDependencyEntry_v0 = [
    { 'name': "Vddc"                           , 'type': 'uint8_t'  },
    { 'name': "Vddci"                          , 'type': 'uint16_t' },
    { 'name': "VddcGfxOffset"                  , 'type': 'int16_t'  }, # Offset relative to Vddc voltage.
    { 'name': "Mvdd"                           , 'type': 'uint16_t' },
    { 'name': "MemClock"                       , 'type': 'uint32_t' },
    { 'name': "Reserved1"                      , 'type': 'uint16_t' }
]
MemClockDependencyEntry_v1 = [
    { 'name': "MemClock"                       , 'type': 'uint32_t' },
    { 'name': "VddIndex"                       , 'type': 'uint8_t'  },
    { 'name': "VddMemIndex"                    , 'type': 'uint8_t'  },
    { 'name': "VddciIndex"                     , 'type': 'uint8_t'  }
]

SocClockDependencyTable_v0 = SocClockDependencyTable_v1 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t'  , 'ref': 'SocClockDependencyEntry' }
]
SocClockDependencyEntry_v0 = [
    { 'name': "VddIndex"                       , 'type': 'uint8_t'  }, # Base voltage.
    { 'name': "VddcOffset"                     , 'type': 'int16_t'  }, # Offset relative to base voltage.
    { 'name': "SocClock"                       , 'type': 'uint32_t' },
    { 'name': "EDCCurrent"                     , 'type': 'uint16_t' },
    { 'name': "ReliabilityTemperature"         , 'type': 'uint8_t'  },
    { 'name': "CKSOffsetAndDisable"            , 'type': 'uint8_t'  }  # Bits 0~6: Voltage offset for CKS, Bit 7: Disable/enable for the SOC clock level.
]
SocClockDependencyEntry_v1 = [
    { 'name': "Vddc"                           , 'type': 'uint8_t'  }, # Base voltage.
    { 'name': "VddcOffset"                     , 'type': 'int16_t'  }, # Offset relative to base voltage.
    { 'name': "SocClock"                       , 'type': 'uint32_t' },
    { 'name': "EDCCurrent"                     , 'type': 'uint16_t' },
    { 'name': "ReliabilityTemperature"         , 'type': 'uint8_t'  },
    { 'name': "CKSOffsetAndDisable"            , 'type': 'uint8_t'  }, # Bits 0~6: Voltage offset for CKS, Bit 7: Disable/enable for the SOC clock level.
    { 'name': "SocClockOffset"                 , 'type': 'int32_t'  }
]

VoltageLookupTable_v0 = VoltageLookupTable_v1 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t'  , 'ref': 'VoltageLookupEntry' }
]
VoltageLookupEntry_v0 = [
    { 'name': "Vdd"                            , 'type': 'uint16_t' }, # Base voltage.
    { 'name': "CACLow"                         , 'type': 'uint16_t' },
    { 'name': "CACMid"                         , 'type': 'uint16_t' },
    { 'name': "CACHigh"                        , 'type': 'uint16_t' }
]
VoltageLookupEntry_v1 = [
    { 'name': "Vdd"                            , 'type': 'uint16_t' } # Base voltage only?
]

MMDependencyTable_v0 = MMDependencyTable_v1 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t'  , 'ref': 'MMDependencyEntry' }
]
MMDependencyEntry_v0 = [
    { 'name': "Vddc"                           , 'type': 'uint8_t'  }, # Vddc voltage.
    { 'name': "VddcGfxOffset"                  , 'type': 'int16_t'  }, # Offset relative to Vddc voltage.
    { 'name': "DCLK"                           , 'type': 'uint32_t' }, # UVD D-clock.
    { 'name': "VCLK"                           , 'type': 'uint32_t' }, # UVD V-clock.
    { 'name': "ECLK"                           , 'type': 'uint32_t' }, # VCE clock.
    { 'name': "ACLK"                           , 'type': 'uint32_t' }, # ACP clock.
    { 'name': "SAMUCLK"                        , 'type': 'uint32_t' }  # SAMU clock.
]
MMDependencyEntry_v1 = [
    { 'name': "VddcInd"                        , 'type': 'uint8_t'  }, # SOC_VDD voltage index
    { 'name': "DCLK"                           , 'type': 'uint32_t' }, # UVD D-clock
    { 'name': "VCLK"                           , 'type': 'uint32_t' }, # UVD V-clock
    { 'name': "ECLK"                           , 'type': 'uint32_t' }, # VCE clock
    { 'name': "PSPClk"                         , 'type': 'uint32_t' }  # PSP clock
]

VCEStateTable_v1 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t'  , 'ref': 'VCEStateEntry' }
]
VCEStateEntry_v1 = [
    { 'name': "VCEClockIndex"                  , 'type': 'uint8_t'  }, # Index into 'VCEDependencyTableOffset' of 'MMDependencyTable'.
    { 'name': "Flag"                           , 'type': 'uint8_t'  }, # 2 bits indicates memory p-states.
    { 'name': "SocClockIndex"                  , 'type': 'uint8_t'  }, # Index into 'SocClockDependencyTable'.
    { 'name': "MemClockIndex"                  , 'type': 'uint8_t'  }  # Index into 'MemClockDependencyTable'.
]

PPMTable_v52 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "PPMDesign"                      , 'type': 'uint8_t'  },
    { 'name': "CPUCoreNumber"                  , 'type': 'uint16_t' },
    { 'name': "PlatformTDP"                    , 'type': 'uint32_t' },
    { 'name': "SmallACPPlatformTDP"            , 'type': 'uint32_t' },
    { 'name': "PlatformTDC"                    , 'type': 'uint32_t' },
    { 'name': "SmallACPPlatformTDC"            , 'type': 'uint32_t' },
    { 'name': "APUTDP"                         , 'type': 'uint32_t' },
    { 'name': "DGPUTDP"                        , 'type': 'uint32_t' },
    { 'name': "DGPUULVPower"                   , 'type': 'uint32_t' },
    { 'name': "TjMax"                          , 'type': 'uint32_t' }
]

PowerTuneTable_v4 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "TDP"                            , 'type': 'uint16_t' },
    { 'name': "ConfigurableTDP"                , 'type': 'uint16_t' },
    { 'name': "TDC"                            , 'type': 'uint16_t' },
    { 'name': "BatteryPowerLimit"              , 'type': 'uint16_t' },
    { 'name': "SmallPowerLimit"                , 'type': 'uint16_t' },
    { 'name': "LowCACLeakage"                  , 'type': 'uint16_t' },
    { 'name': "HighCACLeakage"                 , 'type': 'uint16_t' },
    { 'name': "MaximumPowerDeliveryLimit"      , 'type': 'uint16_t' },
    { 'name': "TjMax"                          , 'type': 'uint16_t' },
    { 'name': "PowerTuneDataSetId"             , 'type': 'uint16_t' },
    { 'name': "EDCLimit"                       , 'type': 'uint16_t' },
    { 'name': "SoftwareShutdownTemp"           , 'type': 'uint16_t' },
    { 'name': "ClockStretchAmount"             , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitHotspot"        , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitLiquid1"        , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitLiquid2"        , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitVrVddc"         , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitVrMvdd"         , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitPlx"            , 'type': 'uint16_t' },
    { 'name': "Liquid1I2CAddress"              , 'type': 'uint8_t'  },
    { 'name': "Liquid2I2CAddress"              , 'type': 'uint8_t'  },
    { 'name': "LiquidI2CLine"                  , 'type': 'uint8_t'  },
    { 'name': "VrI2CAddress"                   , 'type': 'uint8_t'  },
    { 'name': "VrI2CLine"                      , 'type': 'uint8_t'  },
    { 'name': "PlxI2CAddress"                  , 'type': 'uint8_t'  },
    { 'name': "PlxI2CLine"                     , 'type': 'uint8_t'  },
    { 'name': "Reserved1"                      , 'type': 'uint16_t' }
]
PowerTuneTable_v6 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "SocketPowerLimit"               , 'type': 'uint16_t' },
    { 'name': "BatteryPowerLimit"              , 'type': 'uint16_t' },
    { 'name': "SmallPowerLimit"                , 'type': 'uint16_t' },
    { 'name': "TDCLimit"                       , 'type': 'uint16_t' },
    { 'name': "EDCLimit"                       , 'type': 'uint16_t' },
    { 'name': "SoftwareShutdownTemp"           , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitHotSpot"        , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitLiquid1"        , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitLiquid2"        , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitHBM"            , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitVrSoc"          , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitVrMem"          , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitPlx"            , 'type': 'uint16_t' },
    { 'name': "LoadLineResistance"             , 'type': 'uint16_t' },
    { 'name': "Liquid1I2CAddress"              , 'type': 'uint8_t'  },
    { 'name': "Liquid2I2CAddress"              , 'type': 'uint8_t'  },
    { 'name': "LiquidI2CLine"                  , 'type': 'uint8_t'  },
    { 'name': "VrI2CAddress"                   , 'type': 'uint8_t'  },
    { 'name': "VrI2CLine"                      , 'type': 'uint8_t'  },
    { 'name': "PlxI2CAddress"                  , 'type': 'uint8_t'  },
    { 'name': "PlxI2CLine"                     , 'type': 'uint8_t'  },
    { 'name': "TemperatureLimitTedge"          , 'type': 'uint16_t' }
]
PowerTuneTable_v7 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "SocketPowerLimit"               , 'type': 'uint16_t' },
    { 'name': "BatteryPowerLimit"              , 'type': 'uint16_t' },
    { 'name': "SmallPowerLimit"                , 'type': 'uint16_t' },
    { 'name': "TDCLimit"                       , 'type': 'uint16_t' },
    { 'name': "EDCLimit"                       , 'type': 'uint16_t' },
    { 'name': "SoftwareShutdownTemp"           , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitHotSpot"        , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitLiquid1"        , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitLiquid2"        , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitHBM"            , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitVrSoc"          , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitVrMem"          , 'type': 'uint16_t' },
    { 'name': "TemperatureLimitPlx"            , 'type': 'uint16_t' },
    { 'name': "LoadLineResistance"             , 'type': 'uint16_t' },
    { 'name': "Liquid1I2CAddress"              , 'type': 'uint8_t'  },
    { 'name': "Liquid2I2CAddress"              , 'type': 'uint8_t'  },
    { 'name': "LiquidI2CLine"                  , 'type': 'uint8_t'  },
    { 'name': "VrI2CAddress"                   , 'type': 'uint8_t'  },
    { 'name': "VrI2CLine"                      , 'type': 'uint8_t'  },
    { 'name': "PlxI2CAddress"                  , 'type': 'uint8_t'  },
    { 'name': "PlxI2CLine"                     , 'type': 'uint8_t'  },
    { 'name': "TemperatureLimitTedge"          , 'type': 'uint16_t' },
    { 'name': "BoostStartTemperature"          , 'type': 'uint16_t' },
    { 'name': "BoostStopTemperature"           , 'type': 'uint16_t' },
    { 'name': "BoostClock"                     , 'type': 'uint32_t' },
    { 'name': "Reserved1"                      , 'type': 'uint32_t' },
    { 'name': "Reserved2"                      , 'type': 'uint32_t' }
]

HardLimitTable_v52 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t'  , 'ref': 'HardLimitEntry' }
]
HardLimitEntry_v52 = [
    { 'name': "SocClockLimit"                  , 'type': 'uint32_t' },
    { 'name': "MemClockLimit"                  , 'type': 'uint32_t' },
    { 'name': "VddcLimit"                      , 'type': 'uint16_t' },
    { 'name': "VddciLimit"                     , 'type': 'uint16_t' },
    { 'name': "VddGfxLimit"                    , 'type': 'uint16_t' }
]

PCIETable_v1 = PCIETable_v2 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t'  , 'ref': 'PCIEEntry' }
]
PCIEEntry_v1 = [
    { 'name': "PCIEGenSpeed"                   , 'type': 'uint8_t'  },
    { 'name': "PCIELaneWidth"                  , 'type': 'uint8_t'  },
    { 'name': "Reserved1"                      , 'type': 'uint16_t' },
    { 'name': "PCIEClock"                      , 'type': 'uint32_t' }
]
PCIEEntry_v2 = [
    { 'name': "LCLK"                           , 'type': 'uint32_t' }, # L Clock
    { 'name': "PCIEGenSpeed"                   , 'type': 'uint8_t'  }, # PCIE Gen
    { 'name': "PCIELaneWidth"                  , 'type': 'uint8_t'  }  # PCIE Lane Width
]

GPIOTable_v0 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "VRHotTriggeredSocClockDPMIndex" , 'type': 'uint8_t'  }, # If VRHot signal is triggered SOC clock will be limited to this DPM level.
    { 'name': "Reserved1"                      , 'type': 'uint8_t'  },
    { 'name': "Reserved2"                      , 'type': 'uint8_t'  },
    { 'name': "Reserved3"                      , 'type': 'uint8_t'  },
    { 'name': "Reserved4"                      , 'type': 'uint8_t'  },
    { 'name': "Reserved5"                      , 'type': 'uint8_t'  }
]

GfxClockDependencyTable_v0 = GfxClockDependencyTable_v1 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t'  , 'ref': 'GfxClockDependencyEntry' },
]
GfxClockDependencyEntry_v0 = [
    { 'name': "Clock"                          , 'type': 'uint32_t' },
    { 'name': "VddIndex"                       , 'type': 'uint8_t'  }
]
GfxClockDependencyEntry_v1 = [
    { 'name': "Clock"                          , 'type': 'uint32_t' },
    { 'name': "VddIndex"                       , 'type': 'uint8_t'  },
    { 'name': "CKSVOffsetAndDisable"           , 'type': 'uint16_t' },
    { 'name': "AVFSOffset"                     , 'type': 'uint16_t' },
    { 'name': "ACGEnable"                      , 'type': 'uint8_t'  },
    { 'name': "Reserved1"                      , 'type': 'uint16_t' },
    { 'name': "Reserved2"                      , 'type': 'uint8_t'  }
]

PixClockDependencyTable_v0 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t'  , 'ref': 'PixClockDependencyEntry' },
]
PixClockDependencyEntry_v0 = [
    { 'name': "Clock"                          , 'type': 'uint32_t' },
    { 'name': "VddIndex"                       , 'type': 'uint8_t'  }  # Base voltage.
]

DispClockDependencyTable_v0 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t'  , 'ref': 'DispClockDependencyEntry' },
]
DispClockDependencyEntry_v0 = [
    { 'name': "Clock"                          , 'type': 'uint32_t' },
    { 'name': "VddIndex"                       , 'type': 'uint8_t'  }  # Base voltage.
]

PhyClockDependencyTable_v0 = [
    { 'name': "RevisionId"                     , 'type': 'uint8_t'  },
    { 'name': "NumEntries"                     , 'type': 'uint8_t'  , 'ref': 'PhyClockDependencyEntry' },
]
PhyClockDependencyEntry_v0 = [
    { 'name': "Clock"                          , 'type': 'uint32_t' },
    { 'name': "VddIndex"                       , 'type': 'uint8_t'  }  # Base voltage.
]

# drivers/gpu/drm/amd/powerplay/inc/smu11_driver_if.h
PPCLK_COUNT = 11
NUM_GFXCLK_DPM_LEVELS = 16
NUM_VCLK_DPM_LEVELS = NUM_DCLK_DPM_LEVELS = NUM_ECLK_DPM_LEVELS = \
NUM_SOCCLK_DPM_LEVELS = NUM_FCLK_DPM_LEVELS = NUM_DCEFCLK_DPM_LEVELS = \
NUM_DISPCLK_DPM_LEVELS = NUM_PIXCLK_DPM_LEVELS = NUM_PHYCLK_DPM_LEVELS = 8
NUM_UCLK_DPM_LEVELS = 4
NUM_MP0CLK_DPM_LEVELS = 2
NUM_LINK_LEVELS = 2
AVFS_VOLTAGE_COUNT = 2
NUM_XGMI_LEVELS = 2
I2C_CONTROLLER_NAME_COUNT = 7

FeaturesToRun = [
    { 'name': "Features"                       , 'type': 'uint32_t' }
]

DpmDescriptor_t = [
    { 'name': "VoltageMode"                    , 'type': 'uint8_t'  },
    { 'name': "SnapToDiscrete"                 , 'type': 'uint8_t'  },
    { 'name': "NumDiscreteLevels"              , 'type': 'uint8_t'  },
    { 'name': "padding"                        , 'type': 'uint8_t'  },
    { 'name': "ConversionToAvfsClk"            , 'type': 'LinearInt_t' },
    { 'name': "SsCurve"                        , 'type': 'QuadraticInt_t' }
]
LinearInt_t = [
    { 'name': "m"                              , 'type': 'float32'  },
    { 'name': "b"                              , 'type': 'float32'  }
]
QuadraticInt_t = DroopInt_t = [
    { 'name': "a"                              , 'type': 'float32'  },
    { 'name': "b"                              , 'type': 'float32'  },
    { 'name': "c"                              , 'type': 'float32'  }
]

FreqTableGfx = FreqTableVclk = FreqTableDclk = FreqTableEclk = \
FreqTableSocclk = FreqTableUclk = FreqTableFclk = FreqTableDcefclk = \
FreqTableDispclk = FreqTablePixclk = FreqTablePhyclk = DcModeMaxFreq = \
Mp0clkFreq = LclkFreq = XgmiFclkFreq = XgmiUclkFreq = XgmiSocclkFreq = \
[
    { 'name': "Frequency"                      , 'type': 'uint16_t' }
]

Mp0DpmVoltage = XgmiSocVoltage = DcTol = DcBtcMin = DcBtcMax = DcBtcGb = \
[
    { 'name': "Voltage"                        , 'type': 'uint16_t' }
]

Padding567 = Padding8_Uclk = Padding8_Avfs = OverrideAvfsGb = \
Padding8_GfxBtc = DcBtcEnabled = XgmiLinkWidth = \
[
    { 'name': "Byte"                           , 'type': 'uint8_t'  }
]
Padding32 = [
    { 'name': "Padding32"                      , 'type': 'uint32_t' }
]

PcieGenSpeed  = XgmiLinkSpeed = [
    { 'name': "Speed"                          , 'type': 'uint8_t'  }
]
PcieLaneCount  = [
    { 'name': "Count"                          , 'type': 'uint8_t'  }
]

I2cControllerConfig_t = [
    { 'name': "Enabled"                        , 'type': 'uint32_t' },
    { 'name': "SlaveAddress"                   , 'type': 'uint32_t' },
    { 'name': "ControllerPort"                 , 'type': 'uint32_t' },
    { 'name': "ControllerName"                 , 'type': 'uint32_t' },
    { 'name': "ThermalThrottler"               , 'type': 'uint32_t' },
    { 'name': "I2cProtocol"                    , 'type': 'uint32_t' },
    { 'name': "I2cSpeed"                       , 'type': 'uint32_t' },
]

# Megalomaniac Vega VII PP table
PPTable_t = [
    { 'name': "TableVersion"                   , 'type': 'uint32_t' },

    { 'name': "FeaturesToRun"                  , 'type': 'FeaturesToRun', 'max_count': 2 },

    { 'name': "SocketPowerLimitAc0"            , 'type': 'uint16_t' },
    { 'name': "SocketPowerLimitAc0Tau"         , 'type': 'uint16_t' },
    { 'name': "SocketPowerLimitAc1"            , 'type': 'uint16_t' },
    { 'name': "SocketPowerLimitAc1Tau"         , 'type': 'uint16_t' },
    { 'name': "SocketPowerLimitAc2"            , 'type': 'uint16_t' },
    { 'name': "SocketPowerLimitAc2Tau"         , 'type': 'uint16_t' },
    { 'name': "SocketPowerLimitAc3"            , 'type': 'uint16_t' },
    { 'name': "SocketPowerLimitAc3Tau"         , 'type': 'uint16_t' },
    { 'name': "SocketPowerLimitDc"             , 'type': 'uint16_t' },
    { 'name': "SocketPowerLimitDcTau"          , 'type': 'uint16_t' },
    { 'name': "TdcLimitSoc"                    , 'type': 'uint16_t' },
    { 'name': "TdcLimitSocTau"                 , 'type': 'uint16_t' },
    { 'name': "TdcLimitGfx"                    , 'type': 'uint16_t' },
    { 'name': "TdcLimitGfxTau"                 , 'type': 'uint16_t' },

    { 'name': "TedgeLimit"                     , 'type': 'uint16_t' },
    { 'name': "ThotspotLimit"                  , 'type': 'uint16_t' },
    { 'name': "ThbmLimit"                      , 'type': 'uint16_t' },
    { 'name': "Tvr_gfxLimit"                   , 'type': 'uint16_t' },
    { 'name': "Tvr_memLimit"                   , 'type': 'uint16_t' },
    { 'name': "Tliquid1Limit"                  , 'type': 'uint16_t' },
    { 'name': "Tliquid2Limit"                  , 'type': 'uint16_t' },
    { 'name': "TplxLimit"                      , 'type': 'uint16_t' },
    { 'name': "FitLimit"                       , 'type': 'uint32_t' },
    { 'name': "PpmPowerLimit"                  , 'type': 'uint16_t' },
    { 'name': "PpmTemperatureThreshold"        , 'type': 'uint16_t' },
    { 'name': "MemoryOnPackage"                , 'type': 'uint8_t'  },
    { 'name': "padding8_limits"                , 'type': 'uint8_t'  },
    { 'name': "Tvr_socLimit"                   , 'type': 'uint16_t' },
    { 'name': "UlvVoltageOffsetSoc"            , 'type': 'uint16_t' },
    { 'name': "UlvVoltageOffsetGfx"            , 'type': 'uint16_t' },
    { 'name': "UlvSmnclkDid"                   , 'type': 'uint8_t'  },
    { 'name': "UlvMp1clkDid"                   , 'type': 'uint8_t'  },
    { 'name': "UlvGfxclkBypass"                , 'type': 'uint8_t'  },
    { 'name': "Padding234"                     , 'type': 'uint8_t'  },

    { 'name': "MinVoltageGfx"                  , 'type': 'uint16_t' },
    { 'name': "MinVoltageSoc"                  , 'type': 'uint16_t' },
    { 'name': "MaxVoltageGfx"                  , 'type': 'uint16_t' },
    { 'name': "MaxVoltageSoc"                  , 'type': 'uint16_t' },

    { 'name': "LoadLineResistanceGfx"          , 'type': 'uint16_t' },
    { 'name': "LoadLineResistanceSoc"          , 'type': 'uint16_t' },

    { 'name': "DpmDescriptor"                  , 'type': 'DpmDescriptor_t'  , 'max_count': PPCLK_COUNT            },

    { 'name': "FreqTableGfx"                   , 'type': 'FreqTableGfx'     , 'max_count': NUM_GFXCLK_DPM_LEVELS  },
    { 'name': "FreqTableVclk"                  , 'type': 'FreqTableVclk'    , 'max_count': NUM_VCLK_DPM_LEVELS    },
    { 'name': "FreqTableDclk"                  , 'type': 'FreqTableDclk'    , 'max_count': NUM_DCLK_DPM_LEVELS    },
    { 'name': "FreqTableEclk"                  , 'type': 'FreqTableEclk'    , 'max_count': NUM_ECLK_DPM_LEVELS    },
    { 'name': "FreqTableSocclk"                , 'type': 'FreqTableSocclk'  , 'max_count': NUM_SOCCLK_DPM_LEVELS  },
    { 'name': "FreqTableUclk"                  , 'type': 'FreqTableUclk'    , 'max_count': NUM_UCLK_DPM_LEVELS    },
    { 'name': "FreqTableFclk"                  , 'type': 'FreqTableFclk'    , 'max_count': NUM_FCLK_DPM_LEVELS    },
    { 'name': "FreqTableDcefclk"               , 'type': 'FreqTableDcefclk' , 'max_count': NUM_DCEFCLK_DPM_LEVELS },
    { 'name': "FreqTableDispclk"               , 'type': 'FreqTableDispclk' , 'max_count': NUM_DISPCLK_DPM_LEVELS },
    { 'name': "FreqTablePixclk"                , 'type': 'FreqTablePixclk'  , 'max_count': NUM_PIXCLK_DPM_LEVELS  },
    { 'name': "FreqTablePhyclk"                , 'type': 'FreqTablePhyclk'  , 'max_count': NUM_PHYCLK_DPM_LEVELS  },

    { 'name': "DcModeMaxFreq"                  , 'type': 'DcModeMaxFreq'    , 'max_count': PPCLK_COUNT            },
    { 'name': "Padding8_Clks"                  , 'type': 'uint16_t' },

    { 'name': "Mp0clkFreq"                     , 'type': 'Mp0clkFreq'       , 'max_count': NUM_MP0CLK_DPM_LEVELS  },
    { 'name': "Mp0DpmVoltage"                  , 'type': 'Mp0DpmVoltage'    , 'max_count': NUM_MP0CLK_DPM_LEVELS  },

    { 'name': "GfxclkFidle"                    , 'type': 'uint16_t' },
    { 'name': "GfxclkSlewRate"                 , 'type': 'uint16_t' },
    { 'name': "CksEnableFreq"                  , 'type': 'uint16_t' },
    { 'name': "Padding789"                     , 'type': 'uint16_t' },
    { 'name': "CksVoltageOffset"               , 'type': 'QuadraticInt_t' },
    { 'name': "Padding567"                     , 'type': 'Padding567'          , 'max_count': 4},
    { 'name': "GfxclkDsMaxFreq"                , 'type': 'uint16_t' },
    { 'name': "GfxclkSource"                   , 'type': 'uint8_t'  },
    { 'name': "Padding456"                     , 'type': 'uint8_t'  },

    { 'name': "LowestUclkReservedForUlv"       , 'type': 'uint8_t'  },
    { 'name': "Padding8_Uclk"                  , 'type': 'Padding8_Uclk'       , 'max_count': 3},

    { 'name': "PcieGenSpeed"                   , 'type': 'PcieGenSpeed'        , 'max_count': NUM_LINK_LEVELS        },
    { 'name': "PcieLaneCount"                  , 'type': 'PcieLaneCount'       , 'max_count': NUM_LINK_LEVELS        },
    { 'name': "LclkFreq"                       , 'type': 'LclkFreq'            , 'max_count': NUM_LINK_LEVELS        },

    { 'name': "EnableTdpm"                     , 'type': 'uint16_t' },
    { 'name': "TdpmHighHystTemperature"        , 'type': 'uint16_t' },
    { 'name': "TdpmLowHystTemperature"         , 'type': 'uint16_t' },
    { 'name': "GfxclkFreqHighTempLimit"        , 'type': 'uint16_t' },

    { 'name': "FanStopTemp"                    , 'type': 'uint16_t' },
    { 'name': "FanStartTemp"                   , 'type': 'uint16_t' },

    { 'name': "FanGainEdge"                    , 'type': 'uint16_t' },
    { 'name': "FanGainHotspot"                 , 'type': 'uint16_t' },
    { 'name': "FanGainLiquid"                  , 'type': 'uint16_t' },
    { 'name': "FanGainVrGfx"                   , 'type': 'uint16_t' },
    { 'name': "FanGainVrSoc"                   , 'type': 'uint16_t' },
    { 'name': "FanGainPlx"                     , 'type': 'uint16_t' },
    { 'name': "FanGainHbm"                     , 'type': 'uint16_t' },
    { 'name': "FanPwmMin"                      , 'type': 'uint16_t' },
    { 'name': "FanAcousticLimitRpm"            , 'type': 'uint16_t' },
    { 'name': "FanThrottlingRpm"               , 'type': 'uint16_t' },
    { 'name': "FanMaximumRpm"                  , 'type': 'uint16_t' },
    { 'name': "FanTargetTemperature"           , 'type': 'uint16_t' },
    { 'name': "FanTargetGfxclk"                , 'type': 'uint16_t' },
    { 'name': "FanZeroRpmEnable"               , 'type': 'uint8_t'  },
    { 'name': "FanTachEdgePerRev"              , 'type': 'uint8_t'  },

    { 'name': "FuzzyFan_ErrorSetDelta"         , 'type': 'int16_t'  },
    { 'name': "FuzzyFan_ErrorRateSetDelta"     , 'type': 'int16_t'  },
    { 'name': "FuzzyFan_PwmSetDelta"           , 'type': 'int16_t'  },
    { 'name': "FuzzyFan_Reserved"              , 'type': 'uint16_t' },

    { 'name': "OverrideAvfsGb"                 , 'type': 'OverrideAvfsGb'      , 'max_count': AVFS_VOLTAGE_COUNT     },
    { 'name': "Padding8_Avfs"                  , 'type': 'Padding8_Avfs'       , 'max_count': 2                      },

    { 'name': "qAvfsGb"                        , 'type': 'QuadraticInt_t'      , 'max_count': AVFS_VOLTAGE_COUNT     },
    { 'name': "dBtcGbGfxCksOn"                 , 'type': 'DroopInt_t' },
    { 'name': "dBtcGbGfxCksOff"                , 'type': 'DroopInt_t' },
    { 'name': "dBtcGbGfxAfll"                  , 'type': 'DroopInt_t' },
    { 'name': "dBtcGbSoc"                      , 'type': 'DroopInt_t' },
    { 'name': "qAgingGb"                       , 'type': 'LinearInt_t'         , 'max_count': AVFS_VOLTAGE_COUNT     },

    { 'name': "qStaticVoltageOffset"           , 'type': 'QuadraticInt_t'      , 'max_count': AVFS_VOLTAGE_COUNT     },

    { 'name': "DcTol"                          , 'type': 'DcTol'               , 'max_count': AVFS_VOLTAGE_COUNT     },

    { 'name': "DcBtcEnabled"                   , 'type': 'DcBtcEnabled'        , 'max_count': AVFS_VOLTAGE_COUNT     },
    { 'name': "Padding8_GfxBtc"                , 'type': 'Padding8_GfxBtc'     , 'max_count': 2                      },

    { 'name': "DcBtcMin"                       , 'type': 'DcBtcMin'            , 'max_count': AVFS_VOLTAGE_COUNT     },
    { 'name': "DcBtcMax"                       , 'type': 'DcBtcMax'            , 'max_count': AVFS_VOLTAGE_COUNT     },

    { 'name': "XgmiLinkSpeed"                  , 'type': 'XgmiLinkSpeed'       , 'max_count': NUM_XGMI_LEVELS        },
    { 'name': "XgmiLinkWidth"                  , 'type': 'XgmiLinkWidth'       , 'max_count': NUM_XGMI_LEVELS        },
    { 'name': "XgmiFclkFreq"                   , 'type': 'XgmiFclkFreq'        , 'max_count': NUM_XGMI_LEVELS        },
    { 'name': "XgmiUclkFreq"                   , 'type': 'XgmiUclkFreq'        , 'max_count': NUM_XGMI_LEVELS        },
    { 'name': "XgmiSocclkFreq"                 , 'type': 'XgmiSocclkFreq'      , 'max_count': NUM_XGMI_LEVELS        },
    { 'name': "XgmiSocVoltage"                 , 'type': 'XgmiSocVoltage'      , 'max_count': NUM_XGMI_LEVELS        },

    { 'name': "DebugOverrides"                 , 'type': 'uint32_t' },
    { 'name': "ReservedEquation0"              , 'type': 'QuadraticInt_t' },
    { 'name': "ReservedEquation1"              , 'type': 'QuadraticInt_t' },
    { 'name': "ReservedEquation2"              , 'type': 'QuadraticInt_t' },
    { 'name': "ReservedEquation3"              , 'type': 'QuadraticInt_t' },

    { 'name': "MinVoltageUlvGfx"               , 'type': 'uint16_t' },
    { 'name': "MinVoltageUlvSoc"               , 'type': 'uint16_t' },

    { 'name': "MGpuFanBoostLimitRpm"           , 'type': 'uint16_t' },
    { 'name': "padding16_Fan"                  , 'type': 'uint16_t' },

    { 'name': "FanGainVrMem0"                  , 'type': 'uint16_t' },
    { 'name': "FanGainVrMem1"                  , 'type': 'uint16_t' },

    { 'name': "DcBtcGb"                        , 'type': 'DcBtcGb'             , 'max_count': AVFS_VOLTAGE_COUNT     },

    { 'name': "Reserved"                       , 'type': 'Padding32'           , 'max_count': 11 },
    { 'name': "Padding32"                      , 'type': 'Padding32'           , 'max_count': 3 },

    { 'name': "MaxVoltageStepGfx"              , 'type': 'uint16_t' },
    { 'name': "MaxVoltageStepSoc"              , 'type': 'uint16_t' },

    { 'name': "VddGfxVrMapping"                , 'type': 'uint8_t'  },
    { 'name': "VddSocVrMapping"                , 'type': 'uint8_t'  },
    { 'name': "VddMem0VrMapping"               , 'type': 'uint8_t'  },
    { 'name': "VddMem1VrMapping"               , 'type': 'uint8_t'  },

    { 'name': "GfxUlvPhaseSheddingMask"        , 'type': 'uint8_t'  },
    { 'name': "SocUlvPhaseSheddingMask"        , 'type': 'uint8_t'  },
    { 'name': "ExternalSensorPresent"          , 'type': 'uint8_t'  },
    { 'name': "Padding8_V"                     , 'type': 'uint8_t'  },

    { 'name': "GfxMaxCurrent"                  , 'type': 'uint16_t' },
    { 'name': "GfxOffset"                      , 'type': 'int8_t'   },
    { 'name': "Padding_TelemetryGfx"           , 'type': 'uint8_t'  },

    { 'name': "SocMaxCurrent"                  , 'type': 'uint16_t' },
    { 'name': "SocOffset"                      , 'type': 'int8_t'   },
    { 'name': "Padding_TelemetrySoc"           , 'type': 'uint8_t'  },

    { 'name': "Mem0MaxCurrent"                 , 'type': 'uint16_t' },
    { 'name': "Mem0Offset"                     , 'type': 'int8_t'  },
    { 'name': "Padding_TelemetryMem0"          , 'type': 'uint8_t'  },

    { 'name': "Mem1MaxCurrent"                 , 'type': 'uint16_t' },
    { 'name': "Mem1Offset"                     , 'type': 'int8_t'  },
    { 'name': "Padding_TelemetryMem1"          , 'type': 'uint8_t'  },

    { 'name': "AcDcGpio"                       , 'type': 'uint8_t'  },
    { 'name': "AcDcPolarity"                   , 'type': 'uint8_t'  },
    { 'name': "VR0HotGpio"                     , 'type': 'uint8_t'  },
    { 'name': "VR0HotPolarity"                 , 'type': 'uint8_t'  },

    { 'name': "VR1HotGpio"                     , 'type': 'uint8_t'  },
    { 'name': "VR1HotPolarity"                 , 'type': 'uint8_t'  },
    { 'name': "Padding1"                       , 'type': 'uint8_t'  },
    { 'name': "Padding2"                       , 'type': 'uint8_t'  },

    { 'name': "LedPin0"                        , 'type': 'uint8_t'  },
    { 'name': "LedPin1"                        , 'type': 'uint8_t'  },
    { 'name': "LedPin2"                        , 'type': 'uint8_t'  },
    { 'name': "padding8_4"                     , 'type': 'uint8_t'  },

    { 'name': "PllGfxclkSpreadEnabled"         , 'type': 'uint8_t'  },
    { 'name': "PllGfxclkSpreadPercent"         , 'type': 'uint8_t'  },
    { 'name': "PllGfxclkSpreadFreq"            , 'type': 'uint16_t' },

    { 'name': "UclkSpreadEnabled"              , 'type': 'uint8_t'  },
    { 'name': "UclkSpreadPercent"              , 'type': 'uint8_t'  },
    { 'name': "UclkSpreadFreq"                 , 'type': 'uint16_t' },

    { 'name': "FclkSpreadEnabled"              , 'type': 'uint8_t'  },
    { 'name': "FclkSpreadPercent"              , 'type': 'uint8_t'  },
    { 'name': "FclkSpreadFreq"                 , 'type': 'uint16_t' },

    { 'name': "FllGfxclkSpreadEnabled"         , 'type': 'uint8_t'  },
    { 'name': "FllGfxclkSpreadPercent"         , 'type': 'uint8_t'  },
    { 'name': "FllGfxclkSpreadFreq"            , 'type': 'uint16_t' },

    { 'name': "I2cControllers"                 , 'type': 'I2cControllerConfig_t', 'max_count': I2C_CONTROLLER_NAME_COUNT },

    { 'name': "BoardReserved"                  , 'type': 'Padding32'           , 'max_count': 10 },

    { 'name': "MmHubPadding"                   , 'type': 'Padding32'           , 'max_count': 8 }
]

