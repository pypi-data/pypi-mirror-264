""" codes: a collection of static codes from various codesets.

Used across the package, whenever a code is necessary.

"""
NAMESPACE = {
    'fhir_root': "http://hl7.org/fhir",
    'fhir_version_root': "http://hl7.org/fhir/5.0",
    'fhir_created_datetime_url': "http://ortocomputer.com/tops-server-db/fhir/StructureDefinition/created-datetime",
    'snomedct': "http://snomed.info/sct",
    'topsortho': "http://topsortho.com/topsdb",
    'fhir_codesystem': "http://terminology.hl7.org/CodeSystem",
    'fhir_valueset': "http://hl7.org/fhir/ValueSet",
    'fhir_structured_definition': "http://hl7.org/fhir/StructureDefinition"
}


NAMESPACE['fhir_version_root'] = f"{NAMESPACE['fhir_root']}/5.0"
NAMESPACE['EncounterReasonUse'] = f"{NAMESPACE['fhir_root']}/encounter-reason-use"
NAMESPACE['EncounterReasonCodes'] = f"{NAMESPACE['fhir_valueset']}/encounter-reason"
NAMESPACE['ParticipationType'] = f"{NAMESPACE['fhir_codesystem']}/v3-ParticipationType"
NAMESPACE['LocationType'] = f"{NAMESPACE['fhir_codesystem']}/location-physical-type"
NAMESPACE['EncounterType'] = f"{NAMESPACE['fhir_codesystem']}/encounter-type"
NAMESPACE['EncounterClass'] = f"{NAMESPACE['fhir_codesystem']}/v3-ActCode"
NAMESPACE['ProvenanceParticipantType'] = f"{NAMESPACE['fhir_codesystem']}/provenance-participant-type"
NAMESPACE['ProvenanceParticipationType'] = f"{NAMESPACE['fhir_codesystem']}/provenance-participant-type"
NAMESPACE['ServiceType'] = f"{NAMESPACE['fhir_codesystem']}/service-type"
NAMESPACE['ServiceCategory'] = f"{NAMESPACE['fhir_codesystem']}/service-category"
NAMESPACE['Iso_21089_2017_Health_Record_Lifecycle_Events'] = f"{NAMESPACE['fhir_codesystem']}/iso-21089-lifecycle"
NAMESPACE['AppointmentCancellationReason'] = f"{NAMESPACE['fhir_codesystem']}/appointment-cancellation-reason"
NAMESPACE['Practitioner'] = f"{NAMESPACE['fhir_structured_definition']}/Practitioner"
NAMESPACE['Location'] = f"{NAMESPACE['fhir_structured_definition']}/Location"
NAMESPACE['Patient'] = f"{NAMESPACE['fhir_structured_definition']}/Patient"
NAMESPACE['Appointment'] = f"{NAMESPACE['fhir_structured_definition']}/Appointment"
NAMESPACE['Encounter'] = f"{NAMESPACE['fhir_structured_definition']}/Encounter"

Codes = {
    # Used for chairs
    "bed": {
        'system': NAMESPACE['LocationType'],
        'code': "bd",
        'display': "Bed"
    },

    "dental_chair": {
        'system': NAMESPACE['snomedct'],
        'code': "706356006",
        'display': "Dental examination/treatment chair"
    },

    # Used for appointing_staff_member.
    "enterer": {
        'system': NAMESPACE['ProvenanceParticipantType'],
        'code': "enterer",
        'display': "Enterer"
    },

    "originate": {
        "system": NAMESPACE['Iso_21089_2017_Health_Record_Lifecycle_Events'],
        "code": "originate",
        "display": "Originate/Retain Record Lifecycle Event",
    },

    "amend": {
        "system": NAMESPACE['Iso_21089_2017_Health_Record_Lifecycle_Events'],
        "code": "amend",
        "display": "Amend (Update) Record Lifecycle Event",
    },

    # Used for Encounter Class.
    "IMP": {
        'system': NAMESPACE['EncounterClass'],
        'code': "IMP",
        'display': "inpatient encounter"
    },

    "HH": {
        'system': NAMESPACE['EncounterClass'],
        'code': "HH",
        'display': "home health"
    },

    "VR": {
        'system': NAMESPACE['EncounterClass'],
        'code': "VR",
        'display': "virtual"
    },

    # Used for Encounter Reason Use.
    "RV": {
        'system': NAMESPACE['EncounterReasonUse'],
        'code': "RV",
        'display': "Reason for Visit"
    },

    # Used for seating_staff.
    "ADM": {
        'system': NAMESPACE['ParticipationType'],
        'code': "ADM",
        'display': "admitter"
    },

    # Used for orthodontist_id.
    "ATND": {
        'system': NAMESPACE['ParticipationType'],
        'code': "ATND",
        'display': "attender"
    },

    # Used for Appointment reasons
    "orthod_treatment_perm_class1": {
        "code": "3891000",
        "display": "Comprehensive orthodontic treatment, permanent dentition, for class I malocclusion",
        'system': NAMESPACE['snomedct'],
    },

    "ortho_treatment": {
        "code": "122452007",
        "display": "Comprehensive orthodontic treatment",
        'system': NAMESPACE['snomedct'],
    },

    # Used for cancellation_reason
    "prov": {
        "code": "prov",
        "display": "Provider",
        'system': NAMESPACE['AppointmentCancellationReason'],
    },
    "pat": {
        "code": "pat",
        "display": "Patient",
        'system': NAMESPACE['AppointmentCancellationReason'],
    },
    
    # Used for appointment service category
    "10_Dental": {
            'system' : NAMESPACE['ServiceCategory'],
            'code' : "10",
            'display' : "Dental"
    },

    # Used for appointment service type
    "orthodontic": {
        'system': NAMESPACE['ServiceType'],
        'code': "91",
        'display': "Orthodontic"
    },

    "general_dental": {
        'system': NAMESPACE['ServiceType'],
        'code': "88",
        'display': "General Dental"
    },

    "endodontic": {
        'system': NAMESPACE['ServiceType'],
        'code': "87",
        'display': "Endodontic"
    },

    "Orthodontist": {
            'system' : NAMESPACE['snomedct'],
            'code' : "37504001",
            'display' : "Orthodontist"
    },

    "Clinical Staff": {
            'system' : NAMESPACE['snomedct'],
            'code' : "4162009",
            'display' : "Dental assistant"
    },

    "Admin Staff": {
            'system' : NAMESPACE['snomedct'],
            'code' : "224608005",
            'display' : "Administrative healthcare staff"
    },

    "Tech Support": {
            'system' : NAMESPACE['snomedct'],
            'code' : "159324001",
            'display' : "Technical assistant"
    },
}

