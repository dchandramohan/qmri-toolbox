__author__ = "Dharshan Chandramohan"

import abc

import numpy as np
import matplotlib.pyplot as plt
import mongoengine as mg

from . import roi as ru
from . import db
from ..img_utils import view_utils as vu

# connect when module is imported (?)
#  ... is this the most efficient way to do this?
#mg.connect('prelim')

# __19c_hex_geometry
# __6x2_plus_7_config
_MaterialsPhantom_Mk4__6x2_plus_7_placement_order = \
    [10, 4, 12, 3, 15, 17, 5, 8, 13, 0, 7, 14, 2, 11, 9, 6, 18, 1, 16]
_MaterialsPhantom_Mk5__6x2_plus_7_placement_order = \
    [14, 6, 16, 5, 7, 9, 1, 12, 17, 0, 11, 18, 4, 15, 13, 2, 10, 3, 8]


# BasePhantom
class BasePhantom(metaclass=abc.ABCMeta):
    @property
    def designation(self):
        return self._designation

    @property
    def container_spec(self):
        return self._container_spec

    @abc.abstractmethod
    def preview_geometry_2d(self, *args, **kwargs):
        """Plot container centers on a single 2d image (slice)"""
        pass

    @abc.abstractmethod
    def preview_geometry_3d(self, *args, **kwargs):
        """Plot container centers in all 3 planes"""
        pass


# MP-Mk1
class MaterialsPhantom_Mk1(BasePhantom):
    _designation = 'MP-Mk1'
    _container_spec = {
        'nc' : 8,
        'physical' : {
            'material' : 'glass',
            'shape' : 'cylinder',
        },
        'dims' : {
            'rc' : 55.0 / 2.0, # (mm) -> 55.0 mm diameter [measured by ruler]
            'hc' : 50.8 # (mm) [measured by ruler]
        }
    }
    
    def __init__(self):
        pass


# MP-Mk2
class MaterialsPhantom_Mk2(BasePhantom):
    _designation = 'MP-Mk2'
    _container_spec = {
        'nc' : 24,
        'physical' : {
            'material' : 'plastic (unknown)',
            'shape' : 'cylinder'
        },
        'dims' : {
            'rc' : 38.0 / 2.0, # (mm) -> 38.0 mm diameter [measured by calipers]
            'hc' : 20.0 # (mm) [measured by calipers]
        }
    }

    def __init__(self, phantom_uid, container_labels=None, roi_rd_scl=0.25, roi_ht_scl=0.5):
        try:
            self.phantom_info = db.MaterialPhantom.get(phantom_uid=phantom_uid)
        except DoesNotExist:
            if not container_labels:
                raise Exception('Unable to construct phantom record')

            # otherwise build the phantom record
            self.phantom_info = db.MaterialPhantom(phantom_uid=phantom_uid)
            for ci,clabel in enumerate(container_labels):
                sample_rec = db.MaterialSample(label=clabel); sample_rec.save()
                self.phantom_info.containers.append(sample_rec)
            
            self.phantom_info.save()

        self.nc = self._container_spec['nc']
        self.rc = self._container_spec['dims']['rc']
        self.hc = self._container_spec['dims']['hc']

        roi_ht = self.hc * roi_ht_scl
        roi_rd = self.rc * roi_rd_scl
        
        self.roi_info = []
        for cc in self.phantom_info.containers:
            self.roi_info.append({
                'label' : cc.label,
                'ht' : roi_ht,
                'rd' : roi_rd,
            })

        return

    def preview_geometry_2d(self, img_slice):
        pass


# MP-Mk3



# MP-Mk4
class MaterialsPhantom_Mk4(BasePhantom):
    _designation = 'MP-Mk4'
    _container_spec = {
        'nc' : 19,
        'physical' : {
            'material' : 'glass',
            'shape' : 'cylinder'
        },
        'dims' : {
            'rc' : 13.5, # (mm)
            'hc' : 95.25 / 2.0 # (mm) [Approximate!!!]
        }
    }

    def __init__(self, phantom_uid, container_labels=None, roi_rd_scl=0.25, roi_ht_scl=0.5, db=False):
        if db:
            try:
                self.phantom_info = db.MaterialPhantom.get(phantom_uid=phantom_uid)
            except DoesNotExist:
                if not container_labels:
                    raise Exception('Unable to construct phantom record')
                
                # otherwise build the phantom record
                self.phantom_info = db.MaterialPhantom(phantom_uid=phantom_uid)
                for ci,clabel in enumerate(container_labels):
                    sample_rec = db.MaterialSample(label=clabel); sample_rec.save()
                    self.phantom_info.containers.append(sample_rec)
                    
                self.phantom_info.save()
        
        self.nc = self._container_spec['nc']
        self.rc = self._container_spec['dims']['rc']
        self.hc = self._container_spec['dims']['hc']

        roi_ht = self.hc * roi_ht_scl
        roi_rd = self.rc * roi_rd_scl
        
        self.roi_info = []
        if db:
            for cc in self.phantom_info.containers:
                self.roi_info.append({
                    'label' : cc.label,
                    'ht' : roi_ht,
                    'rd' : roi_rd,
                })
        
        for ci, clabel in enumerate(container_labels):
            self.roi_info.append({
                'label' : 'C{:02d}: {:s}'.format(ci, clabel),
                'ht' : roi_ht,
                'rd' : roi_rd,
            })
        
        return

    def compute_roi_centers(self, nx, ny, nz, dx, dy, dz,
                            cz0=None, cx0=None, cy0=None, th0=0.0):

        im_cx = int(nx/2) * dx
        im_cy = int(ny/2) * dy
        im_cz = int(nz/2) * dz

        cz = im_cz if not cz0 else cz0

        roi_ctrs = []
        roi_ctrs.append((cx0, cy0, cz))

        for ci in range(1,7):
            thi = th0 + (np.pi / 2.0) + ((ci - 1) * np.pi / 3.0)
            del_cx = 2 * (2 * self.rc * np.cos(np.pi/6.0)) * np.cos(thi)
            del_cy = 2 * (2 * self.rc * np.cos(np.pi/6.0)) * np.sin(thi)

            roi_ctrs.append((
                cx0 + del_cx,
                cy0 + del_cy,
                cz
            ))

        for ci in range(7,self.nc):
            c1 = ci - 7
            if (c1 % 2 == 0):
                thi = th0 + np.floor(c1/2) * np.pi / 3.0
                del_cx = 2 * self.rc * np.cos(thi)
                del_cy = 2 * self.rc * np.sin(thi)
            else:
                thi = np.pi + th0 + np.floor(c1/2) * np.pi / 3.0
                del_cx = 4 * self.rc * np.cos(thi)
                del_cy = 4 * self.rc * np.sin(thi)

            roi_ctrs.append((
                cx0 + del_cx,
                cy0 + del_cy,
                cz
            ))

        roi_ctrs = [tuple(cc) for cc in np.array(roi_ctrs)[__6x2_plus_7_placement_order]]
        return roi_ctrs
        
    def compute_rois(self, nx, ny, nz, dx, dy, dz,
                     cz0=None, cx0=None, cy0=None, th0=0.0):

        # initialize cx0, cy0, cz0, th0 and/or set defaults
        im_cx = int(nx/2) * dx
        im_cy = int(ny/2) * dy
        im_cz = int(nz/2) * dz

        cz = cz0 if cz0 else im_cz
        cx0 = cx0 if cx0 else im_cx
        cy0 = cy0 if cy0 else im_cy

        th0 = th0

        # compute ROI centers:
        roi_ctrs = self.compute_roi_centers(nx, ny, nz, dx, dy, dz,
                                            cz0=cz, cx0=cx0, cy0=cy0, th0=th0)

        # populate roi_info and generate masks
        for ci, roi in enumerate(self.roi_info):
            cx = roi_ctrs[ci][0]
            cy = roi_ctrs[ci][1]
            cz = roi_ctrs[ci][2]
            
            roi['cx'] = cx
            roi['cy'] = cy
            roi['cz'] = cz

            roi['mask'] = ru.CylinderROI(
                roi['cx'],
                roi['cy'],
                roi['cz'],
                roi['ht'],
                roi['rd'],
            ).generate_mask(nx, ny, nz, dx, dy, dz)

        return
    
    def preview_geometry_2d(self, prvw_slc, dx, dy,
                            dcx0=0.0, # (mm)
                            dcy0=0.0, # (mm)
                            dth=0.0,  # (deg)
                            hide_circles=False,
                            slctype='mag',
                            label_font={
                                'color' : 'red',
                                'fontsize' : 20,
                                'horizontalalignment' : 'center',
                                'verticalalignment' : 'center'
                            }):
        
        cx0 = dx * int(prvw_slc.shape[0] / 2.0) + dcx0
        cy0 = dy * int(prvw_slc.shape[1] / 2.0) + dcy0
        dth0 = dth * np.pi / 180.0

        nx = prvw_slc.shape[0]
        ny = prvw_slc.shape[1]
        
        roi_ctrs = self.compute_roi_centers(nx, ny, 1,
                                            dx, dy, 1,
                                            cz0=0,
                                            cx0=cx0,
                                            cy0=cy0,
                                            th0=dth0)

        fig = plt.figure(figsize=(10.0, 10.0))
        if not (slctype == 'mag'):
            if (slctype == 'cplx'): # ... this needs some work
                rr, cc, prvw_slc = vu.norm_mag_slice(prvw_slc)
            else:
                raise Exception("Slice type (slctype) should be 'mag' or 'cplx'")
        
        plt.imshow(prvw_slc)
        
        th = np.linspace(0.0, 2 * np.pi, 100)
        for ci, cc in enumerate(roi_ctrs):
            cx = cc[0]/dx
            cy = cc[1]/dy
            
            plt.text(cy, cx, 'C{:02d}'.format(ci),
                     fontdict=label_font)

            if not hide_circles:
                xx = (self.rc / dy) * np.cos(th) + cy
                yy = (self.rc / dx) * np.sin(th) + cx
                plt.plot(xx, yy, 'r')

        return fig

    def preview_geometry_3d(self, vol3d, nx, ny, nz, dx, dy, dz,
                            cz0=None,
                            cy0=None,
                            cx0=None,
                            th0=0.0,
                            voltype='cplx',
                            alpha=0.4):
        
        if (voltype not in ('cplx', 'mag')):
            raise Exception("Volume type (voltype) should be 'mag' or 'cplx'")
        
        # get ready for some "one line" magic (if it works!)
        prvw_slc_gen = vu.norm_mag_slice if (voltype=='cplx') else (lambda vol, slc, ax: {
            0: (np.arange(vol.shape[1]),
                np.arange(vol.shape[2]),
                vol[slc, :, :]),
            1: (np.arange(vol.shape[0]),
                np.arange(vol.shape[2]),
                vol[:, slc, :]),
            2: (np.arange(vol.shape[0]),
                np.arange(vol.shape[1]),
                vol[:, :, slc])
        }.get(ax))
        
        try:
            figs = []
            for ci, roi in enumerate(self.roi_info):
                fig, ax = plt.subplots(1, 3, figsize=(40.0, 20.0))
                
                # Plot a slice in each axis through the ROI center
                cx, cy, cz = (
                    int(roi['cx']/dx),
                    int(roi['cy']/dy),
                    int(roi['cz']/dz)
                )
                
                rows, cols, xslice = prvw_slc_gen(vol3d, cx, 0)
                rows, cols, yslice = prvw_slc_gen(vol3d, cy, 1)
                rows, cols, zslice = prvw_slc_gen(vol3d, cz, 2)
                
                roi_data = np.zeros((nx, ny, nz, 4), dtype=np.float)
                roi_data[:,:,:,1] = roi['mask']
                roi_data[:,:,:,3] = alpha * roi['mask']
                
                ax[0].imshow(xslice, cmap=plt.cm.gray)
                ax[0].imshow(roi_data[cx,:,:,:])
                
                ax[1].imshow(yslice, cmap=plt.cm.gray)
                ax[1].imshow(roi_data[:,cy,:,:])
                
                ax[2].imshow(zslice, cmap=plt.cm.gray)
                ax[2].imshow(roi_data[:,:,cz,:])
                
                fig.tight_layout()
                figs.append(fig)
        except KeyError:
            raise Exception("ROI masks not computed")
            
        return figs


# MP-Mk5
class MaterialsPhantom_Mk5(BasePhantom):
    _designation = 'MP-Mk5'
    _container_spec = {
        'nc' : 19,
        'physical' : {
            'material' : 'HDPE',
            'shape' : 'cylinder'
        },
        'dims' : {
            'rc' : 13.5, # (mm)
            'hc' : 95.25 / 2.0 # (mm) [Approximate!!!]
        }
    }

    def __init__(self, phantom_uid, container_labels=None, roi_rd_scl=0.25, roi_ht_scl=0.5, db=False):
        if db:
            try:
                self.phantom_info = db.MaterialPhantom.get(phantom_uid=phantom_uid)
            except DoesNotExist:
                if not container_labels:
                    raise Exception('Unable to construct phantom record')
                
                # otherwise build the phantom record
                self.phantom_info = db.MaterialPhantom(phantom_uid=phantom_uid)
                for ci,clabel in enumerate(container_labels):
                    sample_rec = db.MaterialSample(label=clabel); sample_rec.save()
                    self.phantom_info.containers.append(sample_rec)
                    
                self.phantom_info.save()
        
        self.nc = self._container_spec['nc']
        self.rc = self._container_spec['dims']['rc']
        self.hc = self._container_spec['dims']['hc']

        roi_ht = self.hc * roi_ht_scl
        roi_rd = self.rc * roi_rd_scl
        
        self.roi_info = []
        if db:
            for cc in self.phantom_info.containers:
                self.roi_info.append({
                    'label' : cc.label,
                    'ht' : roi_ht,
                    'rd' : roi_rd,
                })
        
        for ci, clabel in enumerate(container_labels):
            self.roi_info.append({
                'label' : 'C{:02d}: {:s}'.format(ci, clabel),
                'ht' : roi_ht,
                'rd' : roi_rd,
            })
        
        return

    def compute_roi_centers(self, nx, ny, nz, dx, dy, dz,
                            cz0=None, cx0=None, cy0=None, th0=0.0):

        im_cx = int(nx/2) * dx
        im_cy = int(ny/2) * dy
        im_cz = int(nz/2) * dz

        cz = im_cz if not cz0 else cz0

        roi_ctrs = []
        roi_ctrs.append((cx0, cy0, cz))

        for ci in range(1,7):
            thi = th0 + (np.pi / 2.0) + ((ci - 1) * np.pi / 3.0)
            del_cx = 2 * (2 * self.rc * np.cos(np.pi/6.0)) * np.cos(thi)
            del_cy = 2 * (2 * self.rc * np.cos(np.pi/6.0)) * np.sin(thi)

            roi_ctrs.append((
                cx0 + del_cx,
                cy0 + del_cy,
                cz
            ))

        for ci in range(7,self.nc):
            c1 = ci - 7
            if (c1 % 2 == 0):
                thi = th0 + np.floor(c1/2) * np.pi / 3.0
                del_cx = 2 * self.rc * np.cos(thi)
                del_cy = 2 * self.rc * np.sin(thi)
            else:
                thi = np.pi + th0 + np.floor(c1/2) * np.pi / 3.0
                del_cx = 4 * self.rc * np.cos(thi)
                del_cy = 4 * self.rc * np.sin(thi)

            roi_ctrs.append((
                cx0 + del_cx,
                cy0 + del_cy,
                cz
            ))

        roi_ctrs = [tuple(cc) for cc in np.array(roi_ctrs)[__6x2_plus_7_placement_order]]
        return roi_ctrs
        
    def compute_rois(self, nx, ny, nz, dx, dy, dz,
                     cz0=None, cx0=None, cy0=None, th0=0.0):

        # initialize cx0, cy0, cz0, th0 and/or set defaults
        im_cx = int(nx/2) * dx
        im_cy = int(ny/2) * dy
        im_cz = int(nz/2) * dz

        cz = cz0 if cz0 else im_cz
        cx0 = cx0 if cx0 else im_cx
        cy0 = cy0 if cy0 else im_cy

        th0 = th0

        # compute ROI centers:
        roi_ctrs = self.compute_roi_centers(nx, ny, nz, dx, dy, dz,
                                            cz0=cz, cx0=cx0, cy0=cy0, th0=th0)

        # populate roi_info and generate masks
        for ci, roi in enumerate(self.roi_info):
            cx = roi_ctrs[ci][0]
            cy = roi_ctrs[ci][1]
            cz = roi_ctrs[ci][2]
            
            roi['cx'] = cx
            roi['cy'] = cy
            roi['cz'] = cz

            roi['mask'] = ru.CylinderROI(
                roi['cx'],
                roi['cy'],
                roi['cz'],
                roi['ht'],
                roi['rd'],
            ).generate_mask(nx, ny, nz, dx, dy, dz)

        return
    
    def preview_geometry_2d(self, prvw_slc, dx, dy,
                            dcx0=0.0, # (mm)
                            dcy0=0.0, # (mm)
                            dth=0.0,  # (deg)
                            hide_circles=False,
                            slctype='mag',
                            label_font={
                                'color' : 'red',
                                'fontsize' : 20,
                                'horizontalalignment' : 'center',
                                'verticalalignment' : 'center'
                            }):
        
        cx0 = dx * int(prvw_slc.shape[0] / 2.0) + dcx0
        cy0 = dy * int(prvw_slc.shape[1] / 2.0) + dcy0
        dth0 = dth * np.pi / 180.0

        nx = prvw_slc.shape[0]
        ny = prvw_slc.shape[1]
        
        roi_ctrs = self.compute_roi_centers(nx, ny, 1,
                                            dx, dy, 1,
                                            cz0=0,
                                            cx0=cx0,
                                            cy0=cy0,
                                            th0=dth0)

        fig = plt.figure(figsize=(10.0, 10.0))
        if not (slctype == 'mag'):
            if (slctype == 'cplx'): # ... this needs some work
                rr, cc, prvw_slc = vu.norm_mag_slice(prvw_slc)
            else:
                raise Exception("Slice type (slctype) should be 'mag' or 'cplx'")
        
        plt.imshow(prvw_slc)
        
        th = np.linspace(0.0, 2 * np.pi, 100)
        for ci, cc in enumerate(roi_ctrs):
            cx = cc[0]/dx
            cy = cc[1]/dy
            
            plt.text(cy, cx, 'C{:02d}'.format(ci),
                     fontdict=label_font)

            if not hide_circles:
                xx = (self.rc / dy) * np.cos(th) + cy
                yy = (self.rc / dx) * np.sin(th) + cx
                plt.plot(xx, yy, 'r')

        return fig

    def preview_geometry_3d(self, vol3d, nx, ny, nz, dx, dy, dz,
                            cz0=None,
                            cy0=None,
                            cx0=None,
                            th0=0.0,
                            voltype='cplx',
                            alpha=0.4):
        
        if (voltype not in ('cplx', 'mag')):
            raise Exception("Volume type (voltype) should be 'mag' or 'cplx'")
        
        def mag_slc_gen(vol, slc, ax):
            if ax == 0:
                return (np.arange(vol.shape[1]),
                        np.arange(vol.shape[2]),
                        vol[slc, :, :])
            elif ax == 1:
                return (np.arange(vol.shape[0]),
                        np.arange(vol.shape[2]),
                        vol[:, slc, :])
            elif ax == 2:
                return (np.arange(vol.shape[0]),
                        np.arange(vol.shape[1]),
                        vol[:, :, slc])
        
        prvw_slc_gen = vu.norm_mag_slice if (voltype=='cplx') else mag_slc_gen
        
        try:
            figs = []
            for ci, roi in enumerate(self.roi_info):
                fig, ax = plt.subplots(1, 3, figsize=(40.0, 20.0))
                
                # Plot a slice in each axis through the ROI center
                cx, cy, cz = (
                    int(roi['cx']/dx),
                    int(roi['cy']/dy),
                    int(roi['cz']/dz)
                )
                
                rows, cols, xslice = prvw_slc_gen(vol3d, cx, 0)
                rows, cols, yslice = prvw_slc_gen(vol3d, cy, 1)
                rows, cols, zslice = prvw_slc_gen(vol3d, cz, 2)
                
                roi_data = np.zeros((nx, ny, nz, 4), dtype=np.float)
                roi_data[:,:,:,1] = roi['mask']
                roi_data[:,:,:,3] = alpha * roi['mask']
                
                ax[0].imshow(xslice, cmap=plt.cm.gray)
                ax[0].imshow(roi_data[cx,:,:,:])
                
                ax[1].imshow(yslice, cmap=plt.cm.gray)
                ax[1].imshow(roi_data[:,cy,:,:])
                
                ax[2].imshow(zslice, cmap=plt.cm.gray)
                ax[2].imshow(roi_data[:,:,cz,:])
                
                fig.tight_layout()
                figs.append(fig)
        except KeyError:
            raise Exception("ROI masks not computed")
            
        return figs
