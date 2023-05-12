from props.paramsAxon import facetPageLimit, relationsPageLimit
true = True


# Dictionary list of facets body POST request
facets = [
    # BUSINESS_AREA_X_BUSINESS_AREA
    {
        "mainFacet": "BUSINESS_AREA",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "BUSINESS_AREA",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "BUSINESS_AREA",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "BUSINESS_AREA",
                    "fields": ["id", "relTypeId", "name"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }
            ]
        }
    },
    # BUSINESS_AREA_X_SYSTEM
    {
        "mainFacet": "BUSINESS_AREA",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "BUSINESS_AREA",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "BUSINESS_AREA",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "SYSTEM",
                    "fields": ["id", "relTypeId", "name"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }
            ]
        }
    },
    # BUSINESS_AREA_X_ROLE
    {
        "mainFacet": "BUSINESS_AREA",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "BUSINESS_AREA",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "BUSINESS_AREA",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "ROLE",
                    "fields": ["id", "roleId", "roleName", "roleTypeId", "roleTypeName", "peopleId", "roleAccepted", "dateAccepted"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }
            ]
        }
    },
    # BUSINESS_AREA_X_GLOSSARY
    {
        "mainFacet": "BUSINESS_AREA",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "BUSINESS_AREA",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "BUSINESS_AREA",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "GLOSSARY",
                    "fields": ["id", "relTypeId", "name"],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }
            ]
        }
    },
    # ATTRIBUTE_X_FIELD
    {
        "mainFacet": "ATTRIBUTE",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "ATTRIBUTE",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "ATTRIBUTE",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "FIELD",
                    "fields": ["id", "objectId", "name"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }

            ]
        }
    },
    # ATTRIBUTE_X_ROLE
    {
        "mainFacet": "ATTRIBUTE",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "ATTRIBUTE",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "ATTRIBUTE",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [

                {
                    "facetId": "ROLE",
                    "fields": ["id", "roleId", "roleName", "roleTypeId", "roleTypeName", "peopleId", "roleAccepted", "dateAccepted"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}

                }
            ]
        }
    },
    # ATTRIBUTE_X_ATTRIBUTE
    {
        "mainFacet": "ATTRIBUTE",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "ATTRIBUTE",
                "filterGroups": [
                ]
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "ATTRIBUTE",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "ATTRIBUTE",
                    "fields": ["id", "name"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }
            ]
        }
    },
    # ATTRIBUTE_X_DATAQUALITY
    {
        "mainFacet": "ATTRIBUTE",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "ATTRIBUTE",
                "filterGroups": [
                ]
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "ATTRIBUTE",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "DATAQUALITY",
                    "fields": ["id", "name"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }
            ]
        }
    },
    # ATTRIBUTE_X_GLOSSARY
    {
        "mainFacet": "ATTRIBUTE",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "ATTRIBUTE",
                "filterGroups": [
                ]
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "ATTRIBUTE",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "GLOSSARY",
                    "fields": ["id", "name"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }

            ]
        }
    },
    # SYSTEM_X_ROLE
    {
        "mainFacet": "SYSTEM",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "SYSTEM",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "SYSTEM",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [

                {
                    "facetId": "ROLE",
                    "fields": ["id", "roleId", "roleName", "roleTypeId", "roleTypeName", "peopleId", "roleAccepted", "dateAccepted"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}

                }
            ]
        }
    },
    # SYSTEM_X_DATASET
    {
        "mainFacet": "SYSTEM",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "SYSTEM",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "SYSTEM",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "DATASET",
                    "fields": ["id", "name"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}

                },

            ]
        }
    },
    # SYSTEM_X_SYSTEM_INTERFACE
    {
        "mainFacet": "SYSTEM",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "SYSTEM",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "SYSTEM",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "SYSTEM_INTERFACE",
                    "fields": ["id", "name"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}

                }

            ]
        }
    },
    # DATASET_X_ROLE
    {
        "mainFacet": "DATASET",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "DATASET",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "DATASET",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [

                {
                    "facetId": "ROLE",
                    "fields": ["id", "roleId", "roleName", "roleTypeId", "roleTypeName", "peopleId", "roleAccepted", "dateAccepted"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }
            ]

        }
    },
    # DATASET_X_ATTRIBUTE
    {
        "mainFacet": "DATASET",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "DATASET",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "DATASET",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "ATTRIBUTE",
                    "fields": ["id", "name"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }

            ]

        }
    },
    # GLOSSARY_X_ROLE
    {
        "mainFacet": "GLOSSARY",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "GLOSSARY",
                "filterGroups": [
                ]
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "GLOSSARY",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "ROLE",
                    "fields": ["id", "roleId", "roleName", "roleTypeId", "roleTypeName", "peopleId", "roleAccepted", "dateAccepted"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }
            ]
        }
    },
    # GLOSSARY_X_GLOSSARY
    {
        "mainFacet": "GLOSSARY",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "GLOSSARY",
                "filterGroups": [
                ]
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "GLOSSARY",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [
                {
                    "facetId": "GLOSSARY",
                    "fields": ["id", "name"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }

            ]
        }
    },
    # SYSTEM_INTERFACE_X_ROLE
    {
        "mainFacet": "SYSTEM_INTERFACE",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "SYSTEM_INTERFACE",
                "filterGroups": [
                ]
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "SYSTEM_INTERFACE",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [

                {
                    "facetId": "ROLE",
                    "fields": ["id", "roleId", "roleName", "roleTypeId", "roleTypeName", "peopleId", "roleAccepted", "dateAccepted"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }

            ]
        }
    },
    # DATAQUALITY_X_ROLE
    {
        "mainFacet": "DATAQUALITY",
        "searchGroups": [{
            "operator": "START",
            "active": true,
            "searches": [{
                "operator": "START",
                "facetId": "DATAQUALITY",
                "filterGroups": []
            }
            ]
        }],
        "searchScopes": {
            "mainFacet": {
                "facetId": "DATAQUALITY",
                "fields": [
                    "id",
                    "name"
                ],
                "orderList": [{
                    "field": "id",
                    "type": "ASC"
                }],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            },
            "relationships": [

                {
                    "facetId": "ROLE",
                    "fields": ["id", "roleId", "roleName", "roleTypeId", "roleTypeName", "peopleId", "roleAccepted", "dateAccepted"
                               ],
                    "properties": {"offset": "0", "limit": str(relationsPageLimit)}
                }

            ]
        }
    },
]
