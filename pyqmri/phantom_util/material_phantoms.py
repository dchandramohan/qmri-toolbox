__author__ = "Dharshan Chandramohan"

import abc

import numpy as np
import mongoengine as mg

import .roi
import .db

# connect when module is imported (?)
#  ... is this the most efficient way to do this?
mg.connect('prelim')

# __19c_hex_geometry
# __6x2_plus_7_config

# BasePhantom
class BasePhantom(abc.ABC):
    @property
    def designation(self):
        return self._designation

    @property
    def container_spec(self):
        return self._container_spec

    @abstractmethod
    def preview_geometry_2d(self, *args, **kwargs):
        """Plot container centers on a single 2d image (slice)"""
        pass

    @abstractmethod
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

# MP-Mk3



# MP-Mk4



# MP-Mk5
