from props.paramsAxon import facetPageLimit
from props.utils import json, os

true = True

# Dictionary list of facets body POST request
facets = [
    # Business Area Facet
    {
        "mainFacet": "BUSINESS_AREA",
        "searchGroups": [
            {
                "operator": "START",
                "active": true,
                "searches": [{"operator": "START", "facetId": "BUSINESS_AREA", "filterGroups": []}],
            }
        ],
        "searchScopes": {
            "mainFacet": {
                "facetId": "BUSINESS_AREA",
                "fields": [
                    "id",
                    "name",
                    "parentId",
                    "parentName",
                    "description",
                    "lifecycle",
                    "axonStatus",
                    "level",
                    "accessControl",
                    "segments",
                    "segmentsName",
                    "LongDescription",
                    "DocumentLink",
                    "Type",
                    "OwnershipLink",
                ],
                "orderList": [{"field": "id", "type": "ASC"}],
                "properties": {"offset": "0", "limit": str(facetPageLimit)},
            }
        },
    },
    # System Facet
    {
        "mainFacet": "SYSTEM",
        "searchGroups": [
            {
                "operator": "START",
                "active": true,
                "searches": [
                    {
                        "operator": "START",
                        "facetId": "SYSTEM",
                        "filterGroups": [
                            {
                                "operator": "START",
                                "filters": [
                                    {
                                        "operator": "START",
                                        "type": "FROM",
                                        "properties": {"field": "lastUpdatedDate", "from": "2020-11-29 00:00:00"},
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
        "searchScopes": {
            "mainFacet": {
                "facetId": "SYSTEM",
                "fields": [
                    "id",
                    "name",
                    "description",
                    "parentId",
                    "parentName",
                    "type",
                    "Url",
                    "external",
                    "axonStatus",
                    "longName",
                    "lifecycle",
                    "classification",
                    "createdBy",
                    "createdById",
                    "createdDate",
                    "lastUpdatedDate",
                    "accessControl",
                    "crating",
                    "irating",
                    "arating",
                    "ciarating",
                    "assetId",
                    "segments",
                    "segmentsName",
                    "lastApprovedDate",
                    "Frequency",
                    "CompilingDate",
                    "ReferenceDate",
                    "UpdatingDate",
                    "ExecutionType",
                    "ProcessPerimeter",
                    "TechnologicalTransformation",
                ],
                "orderList": [{"field": "id", "type": "ASC"}],
                "properties": {"offset": "0", "limit": str(facetPageLimit)},
            }
        },
    },
    # Dataset Facet
    {
        "mainFacet": "DATASET",
        "searchGroups": [
            {
                "operator": "START",
                "active": true,
                "searches": [
                    {
                        "operator": "START",
                        "facetId": "DATASET",
                        "filterGroups": [
                            {
                                "operator": "START",
                                "filters": [
                                    {
                                        "operator": "START",
                                        "type": "FROM",
                                        "properties": {"field": "lastUpdatedDate", "from": "2020-11-29 00:00:00"},
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
        "searchScopes": {
            "mainFacet": {
                "facetId": "DATASET",
                "fields": [
                    "id",
                    "name",
                    "definition",
                    "refNumber",
                    "type",
                    "axonStatus",
                    "lifecycle",
                    "systemId",
                    "systemName",
                    "glossaryId",
                    "glossaryName",
                    "collectionIds",
                    "collectionNames",
                    "collectionCategoryNames",
                    "datasetPublishStatus",
                    "createdBy",
                    "createdById",
                    "createdDate",
                    "lastUpdatedDate",
                    "accessControl",
                    "ciUsage",
                    "segments",
                    "segmentsName",
                    "lastApprovedDate",
                    "dqScore",
                    "dqGreenTarget",
                    "dqAmberTarget",
                    "PhaseType",
                    "ExecutionType",
                ],
                "orderList": [{"field": "id", "type": "ASC"}],
                "properties": {"offset": "0", "limit": str(facetPageLimit)},
            }
        },
    },
    # Attribute Facet
    {
        "mainFacet": "ATTRIBUTE",
        "searchGroups": [
            {
                "operator": "START",
                "active": true,
                "searches": [
                    {
                        "operator": "START",
                        "facetId": "ATTRIBUTE",
                        "filterGroups": [
                            {
                                "operator": "START",
                                "filters": [
                                    {
                                        "operator": "START",
                                        "type": "FROM",
                                        "properties": {"field": "lastUpdatedDate", "from": "2020-11-29 00:00:00"},
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
        "searchScopes": {
            "mainFacet": {
                "facetId": "ATTRIBUTE",
                "fields": [
                    "id",
                    "name",
                    "definition",
                    "refNumber",
                    "dataSetId",
                    "dataSetName",
                    "dbName",
                    "dbFormat",
                    "systemId",
                    "systemName",
                    "origination",
                    "discoveryReviewStatus",
                    "confidenceScore",
                    "editabilityRole",
                    "editability",
                    "glossaryId",
                    "glossaryName",
                    "mandatory",
                    "createdBy",
                    "createdById",
                    "createdDate",
                    "lastUpdatedDate",
                    "segments",
                    "segmentsName",
                    "ShortDescription",
                    "DocumentLink",
                    "DomainFlag",
                    "AliasNames",
                    "Frequency",
                    "Granularity",
                    "ManualityFlag",
                    "ManualityType",
                    "KDE",
                    "GlossaryClassification",
                ],
                "orderList": [{"field": "id", "type": "ASC"}],
                "properties": {"offset": "0", "limit": str(facetPageLimit)},
            }
        },
    },
    # Glossary Facet
    {
        "mainFacet": "GLOSSARY",
        "searchGroups": [
            {
                "operator": "START",
                "active": true,
                "searches": [
                    {
                        "operator": "START",
                        "facetId": "GLOSSARY",
                        "filterGroups": [
                            {
                                "operator": "START",
                                "filters": [
                                    {
                                        "operator": "START",
                                        "type": "FROM",
                                        "properties": {"field": "lastUpdatedDate", "from": "2020-11-29 00:00:00"},
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
        "searchScopes": {
            "mainFacet": {
                "facetId": "GLOSSARY",
                "fields": [
                    "id",
                    "refNumber",
                    "name",
                    "type",
                    "parentId",
                    "parentName",
                    "parentType",
                    "kde",
                    "description",
                    "alias",
                    "lifecycle",
                    "axonStatus",
                    "securityClassification",
                    "level",
                    "createdBy",
                    "createdById",
                    "lastUpdateUser",
                    "lastUpdateUserId",
                    "createdDate",
                    "lastUpdatedDate",
                    "ldm",
                    "businessLogic",
                    "examples",
                    "format",
                    "formatType",
                    "accessControl",
                    "crating",
                    "irating",
                    "arating",
                    "ciarating",
                    "segments",
                    "segmentsName",
                    "lastApprovedDate",
                    "ShortDescription",
                ],
                "orderList": [{"field": "id", "type": "ASC"}],
                "properties": {"offset": "0", "limit": str(facetPageLimit)},
            }
        },
    },
    # People Facet
    {
        "mainFacet": "PEOPLE",
        "searchGroups": [
            {
                "operator": "START",
                "active": true,
                "searches": [
                    {
                        "operator": "START",
                        "facetId": "PEOPLE",
                        "filterGroups": [
                            {
                                "operator": "START",
                                "filters": [
                                    {
                                        "operator": "START",
                                        "type": "FROM",
                                        "properties": {"field": "lastUpdatedDate", "from": "2020-11-29 00:00:00"},
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
        "searchScopes": {
            "mainFacet": {
                "facetId": "PEOPLE",
                "fields": [
                    "id",
                    "fullName",
                    "firstName",
                    "lastName",
                    "email",
                    "function",
                    "employeeType",
                    "orgUnitRef",
                    "orgUnitId",
                    "orgUnitName",
                    "axonStatus",
                    "profileId",
                    "profileName",
                    "lastLogon",
                    "lifecycle",
                    "lanID",
                    "createdDate",
                    "lastUpdatedDate",
                    "officeLocation",
                    "internalMailCode",
                    "officeTelephone",
                    "mobileTelephone",
                ],
                "orderList": [{"field": "id", "type": "ASC"}],
                "properties": {"offset": "0", "limit": str(facetPageLimit)},
            }
        },
    },
    # System Interface Facet
    {
        "mainFacet": "SYSTEM_INTERFACE",
        "searchGroups": [
            {
                "operator": "START",
                "active": true,
                "searches": [
                    {
                        "operator": "START",
                        "facetId": "SYSTEM_INTERFACE",
                        "filterGroups": [
                            {
                                "operator": "START",
                                "filters": [
                                    {
                                        "operator": "START",
                                        "type": "FROM",
                                        "properties": {"field": "lastUpdatedDate", "from": "2020-11-29 00:00:00"},
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
        "searchScopes": {
            "mainFacet": {
                "facetId": "SYSTEM_INTERFACE",
                "fields": [
                    "id",
                    "refNumber",
                    "name",
                    "description",
                    "sourceId",
                    "sourceName",
                    "targetId",
                    "targetName",
                    "axonStatus",
                    "automation",
                    "frequency",
                    "lifecycle",
                    "synchronisation",
                    "assetId",
                    "classification",
                    "createdBy",
                    "createdById",
                    "createdDate",
                    "lastUpdatedDate",
                    "accessControl",
                    "segments",
                    "segmentsName",
                    "transfermethod",
                    "transferformat",
                ],
                "orderList": [{"field": "id", "type": "ASC"}],
                "properties": {"offset": "0", "limit": str(facetPageLimit)},
            }
        },
    },
    # Data Quality Facet
    {
        "mainFacet": "DATAQUALITY",
        "searchGroups": [
            {
                "operator": "START",
                "active": true,
                "searches": [{"operator": "START", "facetId": "DATAQUALITY", "filterGroups": []}],
            }
        ],
        "searchScopes": {
            "mainFacet": {
                "facetId": "DATAQUALITY",
                "fields": [
                    "id",
                    "refNumber",
                    "name",
                    "description",
                    "attributeId",
                    "attributeName",
                    "measuredInId",
                    "measuredInName",
                    "type",
                    "lifecycle",
                    "criticality",
                    "greenTarget",
                    "amberTarget",
                    "reportMonth",
                    "result",
                    "measured",
                    "axonStatus",
                    "accessControl",
                    "technicalDesc",
                    "population",
                    "measuringMethodDesc",
                    "automation",
                    "frequency",
                    "measuringMethod",
                    "segments",
                    "segmentsName",
                    "reportStatus",
                ],
                "orderList": [{"field": "id", "type": "ASC"}],
                "properties": {"offset": "0", "limit": str(facetPageLimit)},
            }
        },
    },
]


# Opening AXON_last_updates JSON file to import last dates that the csv is saved
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "AXON_last_updates.json")

with open(file_path, "r") as f:
    # returns JSON object as a dictionary
    data = json.load(f)

# Assing last updated date from json AXON_last_updates to facet body POST request
for facet in facets:
    name = facet.get("mainFacet")
    for key, value in data.items():
        if key == name and key not in ("BUSINESS_AREA", "DATAQUALITY"):
            facet["searchGroups"][0]["searches"][0]["filterGroups"][0]["filters"][0]["properties"]["from"] = value
