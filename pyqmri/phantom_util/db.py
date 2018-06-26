__author__ = "Dharshan Chandramohan"

from mongoengine import *

class Phantom(Document):
    phantom_uid = StringField(required=True, unique=True)
    creation_date = DateTimeField()

    meta = {'allow_inheritance' : True}


class Doping(DynamicEmbeddedDocument):
    compound = StringField()
    concentration = FloatField()


class MaterialSample(Document):
    label = StringField(required=True)
    filled_date = DateTimeField()
    base_material = StringField()
    doping = EmbeddedDocumentListField(Doping)


class MaterialPhantom(Phantom):
    containers = ListField(ReferenceField(MaterialSample))


class ImageSeries(EmbeddedDocument):
    series_description = StringField()
    series_number = IntField()
    scanner_dicom_reconned = BooleanField()
    pfile_stored = BooleanField()
    pfile_numbers = ListField(StringField())


class Experiment(Document):
    session_date = DateTimeField()
    facility = StringField()
    scanner = StringField()

    meta = {'allow_inheritance' : True}


class CT_Experiment(Experiment):
    pass


class MR_Experiment(Experiment):
    scanner_software_version = StringField()
    exam_number = IntField()
    rf_coil = StringField()
    protocol = StringField()
    acquisition_list = EmbeddedDocumentListField(ImageSeries)


class Measurement(Document):
    parameter = StringField() # OR CHOICE [?]
    value = FloatField()
    quantification_details = DictField() # basically a notes field...
