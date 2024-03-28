""" snomed: a collection of static SNOMED-CT codes.

Used whenever a code is necessary, for various implementations.

"""
from . import Code

class NAMESPACES:
    snomedct = "http://snomed.info/sct"

dental_chair = Code(
    system=NAMESPACES.snomedct,
    code='706356006',
    display='Dental examination/treatment chair')

orthod_treatment_perm_class1 = Code(
    system=NAMESPACES.snomedct,
    code='3891000',
    display='Comprehensive orthodontic treatment, permanent dentition, for class I malocclusion')

ortho_treatment = Code(
    system=NAMESPACES.snomedct,
    code='122452007',
    display='Comprehensive orthodontic treatment')

orthodontist = Code(
    system=NAMESPACES.snomedct,
    code='37504001',
    display='Orthodontist')

clinical_staff = Code(
    system=NAMESPACES.snomedct,
    code='4162009',
    display='Dental assistant')

admin_staff = Code(
    system=NAMESPACES.snomedct,
    code='224608005',
    display='Administrative healthcare staff')

tech_support = Code(
    system=NAMESPACES.snomedct,
    code='159324001',
    display='Technical assistant')
