
# How to generate Python readable ATOM C structures from Linux kernel code

## Versions

Generated against kernel commit 80e54e849 (v6.14-rc6) (Sun Mar 9 13:45:25 2025 -1000)
Generated against drm-next kernel commit 5da39dce1 tag drm-xe-next-fixes-2025-03-12

clang version 19.1.7
ctypeslib2 2.4.0


## Python Requirements

    sudo apt install clang
    pip3 install --user clang==19.1.7 ctypeslib2==2.4.0

or

    pacman -S clang
    pipx install --preinstall clang==19.1.7 ctypeslib2


## Get a particular Linux kernel release

    git clone --depth=1 git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
    pushd linux
    # git fetch origin v6.14-rc6 --tags
    # git checkout v6.14-rc6
    # git remote add linux-next https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
    # git fetch --tags linux-next
    git remote add drm-next https://anongit.freedesktop.org/git/drm/drm.git
    git fetch --tags drm-next
    git checkout drm-next
    popd


## Some Linux header hacks, clang2py can't deal with __counted_by()

    sed -i 's| __counted_by(.*);|; //\0|' linux/drivers/gpu/drm/amd/include/pptable.h
    sed -i 's| __counted_by(.*);|; //\0|' linux/drivers/gpu/drm/amd/include/atomfirmware.h
    sed -i 's| __counted_by(.*);|; //\0|' linux/drivers/gpu/drm/amd/pm/powerplay/hwmgr/pptable_v1_0.h
    sed -i 's|#include "hwmgr.h"|//\0|'   linux/drivers/gpu/drm/amd/pm/powerplay/hwmgr/pptable_v1_0.h


## atombios.py

    clang2py -k 's' --clang-args="\
        --include stdint.h \
        --include linux/drivers/gpu/drm/amd/include/atom-types.h \
        " \
      -s struct__ATOM_COMMON_TABLE_HEADER -s struct__ATOM_MASTER_DATA_TABLE \
      -s struct__ATOM_ROM_HEADER -s struct__ATOM_ROM_HEADER_V2_1 \
      linux/drivers/gpu/drm/amd/include/atombios.h > atombios.py


## pptable_v1_0.py (Polaris/Tonga)


    clang2py -k 'mst' \
      --clang-args="\
        --include stdint.h \
        --include linux/drivers/gpu/drm/amd/include/atom-types.h \
        --include linux/drivers/gpu/drm/amd/include/atombios.h
        " \
       linux/drivers/gpu/drm/amd/pm/powerplay/hwmgr/pptable_v1_0.h > pptable_v1_0.py


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


##  smu_v11_0_navi20.py (Navi2x)

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


##  smu_v14_0 (Navi 4x)

    clang2py -k 'mste' \
      --clang-args="--include stdint.h \
                    --include linux/drivers/gpu/drm/amd/include/atom-types.h \
                    --include linux/drivers/gpu/drm/amd/include/atomfirmware.h \
                    --include linux/drivers/gpu/drm/amd/pm/swsmu/inc/pmfw_if/smu14_driver_if_v14_0.h " \
       linux/drivers/gpu/drm/amd/pm/swsmu/inc/smu_v14_0_2_pptable.h > smu_v14_0_2_navi40.py


## Linux source cleanup

    pushd linux
    git checkout \
      drivers/gpu/drm/amd/include/pptable.h      \
      drivers/gpu/drm/amd/include/atomfirmware.h \
      drivers/gpu/drm/amd/pm/powerplay/hwmgr/pptable_v1_0.h
    popd

