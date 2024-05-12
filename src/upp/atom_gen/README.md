
# How to generate Python readable ATOM C structures from Linux kernel code

## Reguirements

    sudo apt install clang
    pip3 install --user ctypeslib2 clang


## Get latest Linux kernel

    git clone --depth=1 git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git

Generated against e8f897f4a (v6.8) (Sun Mar 10 13:38:09 2024 -0700)
clang version 17.0.6
clang2py version 2.3.4


## atombios.py

    clang2py -k 's' --clang-args="\
        --include stdint.h \
        --include linux/drivers/gpu/drm/amd/include/atom-types.h \
        " \
      -s struct__ATOM_COMMON_TABLE_HEADER -s struct__ATOM_MASTER_DATA_TABLE \
      -s struct__ATOM_ROM_HEADER -s struct__ATOM_ROM_HEADER_V2_1 \
      linux/drivers/gpu/drm/amd/include/atombios.h > atombios.py


## pptable_v1_0.py (Polaris/Tonga)

    sed -i 's|#include "hwmgr.h"|//\0|' linux/drivers/gpu/drm/amd/pm/powerplay/hwmgr/pptable_v1_0.h
    clang2py -k 'mst' \
      --clang-args="\
        --include stdint.h \
        --include linux/drivers/gpu/drm/amd/include/atom-types.h \
        --include linux/drivers/gpu/drm/amd/include/atombios.h
        " \
       linux/drivers/gpu/drm/amd/pm/powerplay/hwmgr/pptable_v1_0.h > pptable_v1_0.py
    pushd linux && git checkout drivers/gpu/drm/amd/pm/powerplay/hwmgr/pptable_v1_0.h && popd


## vega10_pptable.py (Vega10 aka Vega 56/64)

    clang2py -k 'mste' \
      --clang-args="--include stdint.h \
                    --include linux/drivers/gpu/drm/amd/include/atom-types.h \
                    --include linux/drivers/gpu/drm/amd/include/atomfirmware.h \
                    --include linux/drivers/gpu/drm/amd/include/atombios.h" \
       linux/drivers/gpu/drm/amd/pm/powerplay/hwmgr/vega10_pptable.h > vega10_pptable.py


## vega20_pptable.py (Vega20 aka Radeon7)

    clang2py -k 'mste' \
      --clang-args="--include stdint.h \
                    --include linux/drivers/gpu/drm/amd/include/atom-types.h \
                    --include linux/drivers/gpu/drm/amd/include/atomfirmware.h \
                    --include linux/drivers/gpu/drm/amd/pm/powerplay/inc/smu11_driver_if.h " \
       linux/drivers/gpu/drm/amd/pm/powerplay/hwmgr/vega20_pptable.h > vega20_pptable.py


##  smu_v11_0_navi10.py (Navi10/14)

    clang2py -k 'mste' \
      --clang-args="--include stdint.h \
                    --include linux/drivers/gpu/drm/amd/include/atom-types.h \
                    --include linux/drivers/gpu/drm/amd/include/atomfirmware.h \
                    --include linux/drivers/gpu/drm/amd/pm/swsmu/inc/pmfw_if/smu11_driver_if_navi10.h " \
       linux/drivers/gpu/drm/amd/pm/swsmu/inc/smu_v11_0_pptable.h > smu_v11_0_navi10.py


##  smu_v11_0_arcturus.py (MI100)

    clang2py -k 'mste' \
      --clang-args="--include stdint.h \
                    --include linux/drivers/gpu/drm/amd/include/atom-types.h \
                    --include linux/drivers/gpu/drm/amd/include/atomfirmware.h \
                    --include linux/drivers/gpu/drm/amd/pm/swsmu/inc/pmfw_if/smu11_driver_if_arcturus.h " \
       linux/drivers/gpu/drm/amd/pm/swsmu/inc/smu_v11_0_pptable.h > smu_v11_0_arcturus.py


##  smu_v11_0_navi20.py (Navi21/22/23)

    clang2py -k 'mste' \
      --clang-args="--include stdint.h \
                    --include linux/drivers/gpu/drm/amd/include/atom-types.h \
                    --include linux/drivers/gpu/drm/amd/include/atomfirmware.h \
                    --include linux/drivers/gpu/drm/amd/pm/swsmu/inc/pmfw_if/smu11_driver_if_sienna_cichlid.h " \
       linux/drivers/gpu/drm/amd/pm/swsmu/inc/smu_v11_0_7_pptable.h > smu_v11_0_7_navi20.py


##  smu_v13_0 (Navi 3x)

    clang2py -k 'mste' \
      --clang-args="--include stdint.h \
                    --include linux/drivers/gpu/drm/amd/include/atom-types.h \
                    --include linux/drivers/gpu/drm/amd/include/atomfirmware.h \
                    --include linux/drivers/gpu/drm/amd/pm/swsmu/inc/pmfw_if/smu13_driver_if_v13_0_7.h " \
       linux/drivers/gpu/drm/amd/pm/swsmu/inc/smu_v13_0_7_pptable.h > smu_v13_0_7_navi30.py

