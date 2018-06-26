__author__ = "Dharshan Chandramohan"

import numpy as np

class CylinderROI(object):
    def __init__(self, cx, cy, cz, ht, rd):
        self.cx = cx # center x-coordinate
        self.cy = cy # center y-coordinate
        self.cz = cz # center z-coordinate

        self.ht = ht # height
        self.rd = rd # radius

    def generate_mask(self, nx, ny, nz, dx, dy, dz, axis=2):
        # xx = np.arange(0.0, nx * dx, dx)
        # yy = np.arange(0.0, ny * dy, dy)
        # zz = np.arange(0.0, nz * dz, dz)

        xx = np.arange(nx) * dx
        yy = np.arange(ny) * dy
        zz = np.arange(nz) * dz

        (xg, yg, zg) = np.meshgrid(xx, yy, zz, indexing='ij')
        if (axis == 2):
            #(xg, yg, zg) = np.meshgrid(xx, yy, zz)
            roi_mask = np.power(xg - self.cx, 2) + np.power(yg - self.cy, 2) <= np.power(self.rd, 2)
            roi_mask = np.logical_and(roi_mask, zg >= self.cz - (self.ht/2))
            roi_mask = np.logical_and(roi_mask, zg <= self.cz + (self.ht/2))
        elif (axis == 1):
            #(yg, xg, zg) = np.meshgrid(xx, yy, zz)
            roi_mask = np.power(xg - self.cx, 2) + np.power(zg - self.cz, 2) <= np.power(self.rd, 2)
            roi_mask = np.logical_and(roi_mask, yg >= self.cy - (self.ht/2))
            roi_mask = np.logical_and(roi_mask, yg <= self.cy + (self.ht/2))
        elif (axis == 0):
            #(yg, xg, zg) = np.meshgrid(xx, yy, zz)
            roi_mask = np.power(yg - self.cy, 2) + np.power(zg - self.cz, 2) <= np.power(self.rd, 2)
            roi_mask = np.logical_and(roi_mask, xg >= self.cx - (self.ht/2))
            roi_mask = np.logical_and(roi_mask, xg <= self.cx + (self.ht/2))

        return np.float32(roi_mask)

