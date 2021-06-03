
# How to generate Python readable ATOM C structures from Linux kernel code

## Reguirements

    sudo apt install clang-6.0
    pip3 install --user ctypeslib2 clang

## Get latest Linux kernel

    git clone --depth=1 git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git

Generated against 324c92e5e (Wed Jun 2 08:53:37 2021 -1000)


## atom.py

    sed -i 's|\tstruct mutex mutex;|//\0|' linux/drivers/gpu/drm/amd/amdgpu/atom.h
    clang2py -k 'm' --clang-args="\
        -Ilinux/include -Ilinux/drivers/gpu/drm/amd/include" \
      linux/drivers/gpu/drm/amd/amdgpu/atom.h > atom.py
    pushd linux && git checkout drivers/gpu/drm/amd/amdgpu/atom.h && popd


## atombios.py

    clang2py -k 's' --clang-args="\
        --include stdint.h \
        --include linux/drivers/gpu/drm/amd/include/atom-types.h \
        " \
      linux/drivers/gpu/drm/amd/include/atombios.h > atombios.py

    clang2py -k 's' --clang-args="\
        --include stdint.h \
        --include linux/drivers/gpu/drm/amd/include/atom-types.h \
        " \
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

    clang2py -k 'mst' \
      --clang-args="--include stdint.h \
                    --include linux/drivers/gpu/drm/amd/include/atom-types.h \
                    --include linux/drivers/gpu/drm/amd/include/atomfirmware.h \
                    --include linux/drivers/gpu/drm/amd/include/atombios.h" \
       linux/drivers/gpu/drm/amd/pm/powerplay/hwmgr/vega10_pptable.h > vega10_pptable.py


## vega20_pptable.py (Vega20 aka Radeon7)

    clang2py -k 'mst' \
      --clang-args="--include stdint.h \
                    --include linux/drivers/gpu/drm/amd/include/atom-types.h \
                    --include linux/drivers/gpu/drm/amd/include/atomfirmware.h \
                    --include linux/drivers/gpu/drm/amd/pm/inc/smu11_driver_if.h " \
       linux/drivers/gpu/drm/amd/pm/powerplay/hwmgr/vega20_pptable.h > vega20_pptable.py


##  smu_v11_0_navi10.py (Navi10/14)

    clang2py -k 'mst' \
      --clang-args="--include stdint.h \
                    --include linux/drivers/gpu/drm/amd/include/atom-types.h \
                    --include linux/drivers/gpu/drm/amd/include/atomfirmware.h \
                    --include linux/drivers/gpu/drm/amd/pm/inc/smu11_driver_if_navi10.h " \
       linux/drivers/gpu/drm/amd/pm/inc/smu_v11_0_pptable.h > smu_v11_0_navi10.py


##  smu_v11_0_navi20.py (Navi21/22)

    clang2py -k 'mst' \
      --clang-args="--include stdint.h \
                    --include linux/drivers/gpu/drm/amd/include/atom-types.h \
                    --include linux/drivers/gpu/drm/amd/include/atomfirmware.h \
                    --include linux/drivers/gpu/drm/amd/pm/inc/smu11_driver_if_sienna_cichlid.h " \
       linux/drivers/gpu/drm/amd/pm/inc/smu_v11_0_7_pptable.h > smu_v11_0_7_navi20.py

