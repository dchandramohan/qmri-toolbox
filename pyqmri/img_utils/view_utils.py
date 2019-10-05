__author__ = "Dharshan Chandramohan"

import numpy as np
import matplotlib.pyplot as plt

def norm_mag_slice(cplx_data_3d, slice_num, axis):
    nz, ny, nx = cplx_data_3d.shape

    if axis == 0:
        ipnr, ipnc = (ny,nz)
        cplx_data_slice = cplx_data_3d[:, :, slice_num]
    elif axis == 1:
        ipnr, ipnc = (nx,nz)
        cplx_data_slice = cplx_data_3d[:, slice_num, :]
    elif axis == 2:
        ipnr, ipnc = (nx, ny)
        cplx_data_slice = cplx_data_3d[slice_num, :, :]

    row_axis = np.arange(ipnr)
    col_axis = np.arange(ipnc)
    mag_slice = np.ndarray((ipnr, ipnc), dtype=np.float)
    scl_slice = np.ndarray((ipnr, ipnc), dtype=np.int64)

    for row_i in row_axis:
        for col_i in col_axis:
            mag_slice[row_i, col_i] = np.float(np.abs(np.complex(
                *cplx_data_slice[col_i, row_i]
            )))

    scale = (2**63 - 1)/np.max(mag_slice)
    for row_i in row_axis:
        for col_i in col_axis:
            scl_slice[row_i, col_i] = np.int64(
                scale * mag_slice[row_i, col_i]
            )

    return row_axis, col_axis, scl_slice

def preview_volume_mag_DICOM(vol3d, axis=2):
    pass

def preview_volume_DICOM(vol3d, axis=2, figsize=(20.0,20.0), grid=(5, 4)):
    n_axes = grid[0] * grid[1]
    n_planes = vol3d.shape[axis]

    fig, ax = plt.subplots(grid[0], grid[1], figsize=figsize)
    prev_planes = np.arange(0, n_planes, int(np.ceil(n_planes/n_axes)))

    for pl, sli in enumerate(prev_planes):
        aa = ax[int(pl/4)][int(pl%4)]
        aa.imshow(vol3d[:,:,sli])
        aa.set_title('Sl #{:d}'.format(sli))

    fig.tight_layout()
    fig.patch.set_facecolor('white')

    return fig

def preview_volume_cplx(vol3d, axis=2, figsize=(20.0, 20.0), grid=(5, 4)):
    n_axes = grid[0] * grid[1]
    n_planes = vol3d.shape[2 - axis] # kludge for z, y, x order...
    
    fig, ax = plt.subplots(grid[0], grid[1], figsize=figsize)
    prev_planes = np.arange(0, n_planes, int(np.ceil(n_planes/n_axes)))

    for pl, sli in enumerate(prev_planes):
        rr, cc, imslice = norm_mag_slice(vol3d, sli, axis)
        aa = ax[int(pl/4)][int(pl%4)]
        aa.pcolormesh(rr, cc, imslice)
        aa.set_title('Sl #{:d}'.format(sli))

    fig.tight_layout()
    fig.patch.set_facecolor('white')

    return fig

# Misc: there's nowhere else to put this but I find it useful
from IPython.display import clear_output

class SimpleProgress(object):
    def __init__(self, bar_length=50):
        self.bar_length = bar_length

    def update(self, progress):
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
        if progress < 0:
            progress = 0
        if progress >= 1:
            progress = 1

        block = int(round(self.bar_length * progress))
        clear_output(wait = True)

        text = "Progress: [{0}] {1:.1f}%".format( "#" * block + "-" * (self.bar_length - block),
                                                  progress * 100)
        print(text)

