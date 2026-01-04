from pymongo import MongoClient
from datetime import datetime
from pprint import pprint

client = MongoClient('localhost', 27017)


def populate_db(db_name: str, collection:str, inserts: list):
    db = client[db_name]
    col = db[collection]
    try:
        col.insert_many(inserts)
    except Exception as e:
        print(e)


def query_db(db_name: str, collection:str, query, projection) -> list:
    if not projection:
        return list(client[db_name][collection].find(query))
    else:
        return list(client[db_name][collection].find(query, projection))

def aggregate_db(db_name:str, collection:str, pipeline: list) -> list:
    return list(client[db_name][collection].aggregate(pipeline))

if __name__ == '__main__':
    db = 'conocimiento_db'
    bandas = [
    {
        "nombre": "Pink Floyd",
        "anio_creacion": 1965,
        "discos": [
            {"titulo": "The Dark Side of the Moon", "anio": 1973},
            {"titulo": "Wish You Were Here", "anio": 1975},
            {"titulo": "The Wall", "anio": 1979},
        ],
        "metadata": {
            "pais_origen": "Reino Unido",
            "genero": ["Rock progresivo", "Psicodélico"],
            "activa": False,
            "oyentes_mensuales_millones": 14.2,
        },
        "creada_en": datetime.now(),
    },
    {
        "nombre": "Radiohead",
        "anio_creacion": 1985,
        "discos": [
            {"titulo": "OK Computer", "anio": 1997},
            {"titulo": "Kid A", "anio": 2000},
            {"titulo": "In Rainbows", "anio": 2007},
        ],
        "metadata": {
            "pais_origen": "Reino Unido",
            "genero": ["Rock alternativo", "Experimental"],
            "activa": True,
            "oyentes_mensuales_millones": 18.5,
        },
        "creada_en": datetime.now(),
    },
    {
        "nombre": "Soda Stereo",
        "anio_creacion": 1982,
        "discos": [
            {"titulo": "Signos", "anio": 1986},
            {"titulo": "Canción Animal", "anio": 1990},
        ],
        "metadata": {
            "pais_origen": "Argentina",
            "genero": ["Rock latino"],
            "activa": False,
            "oyentes_mensuales_millones": 10.1,
        },
        "creada_en": datetime.now(),
    },
    ]
    cientificos = [
    {
        "nombre": "Albert Einstein",
        "nacimiento": {
            "fecha": datetime(1879, 3, 14),
            "lugar": "Ulm, Alemania",
        },
        "papers_populares": [
            "Zur Elektrodynamik bewegter Körper",
            "Die Grundlage der allgemeinen Relativitätstheorie",
        ],
        "premio_nobel": True,
        "alma_mater": {
            "nombre": "ETH Zürich",
            "pais": "Suiza",
            "tipo": "Universidad técnica",
        },
        "campos": ["Física teórica", "Relatividad"],
        "citas_aproximadas": 150000,
        "vivo": False,
        "creado_en": datetime.now(),
    },
    {
        "nombre": "Marie Curie",
        "nacimiento": {
            "fecha": datetime(1867, 11, 7),
            "lugar": "Varsovia, Polonia",
        },
        "papers_populares": [
            "Investigations on radioactive substances",
            "The discovery of radium",
        ],
        "premio_nobel": True,
        "alma_mater": {
            "nombre": "Universidad de París",
            "pais": "Francia",
            "tipo": "Universidad pública",
        },
        "campos": ["Física", "Química"],
        "citas_aproximadas": 95000,
        "vivo": False,
        "creado_en": datetime.now(),
    },
    {
        "nombre": "Carl Sagan",
        "nacimiento": {
            "fecha": datetime(1934, 11, 9),
            "lugar": "Brooklyn, EE.UU.",
        },
        "papers_populares": [
            "Life in the Universe",
            "The Cosmic Connection",
        ],
        "premio_nobel": False,
        "alma_mater": {
            "nombre": "Universidad de Chicago",
            "pais": "Estados Unidos",
            "tipo": "Universidad privada",
        },
        "campos": ["Astrofísica", "Divulgación científica"],
        "citas_aproximadas": 42000,
        "vivo": False,
        "creado_en": datetime.now(),
    },
    ]

    bandas_col = 'bandas'
    cientificos_col = 'cientificos'
    collections = client[db].list_collection_names()
    if bandas_col not in collections:
        populate_db(db, 'bandas', bandas)
    if cientificos_col not in collections:
        populate_db(db, 'cientificos', cientificos)


    #====== query bands =======
    #find
    query = {"anio_creacion": {"$gt": 1980}}
    projection = {"_id":0, "nombre": 1}
    result = query_db(db, bandas_col, query, projection=projection)
    pprint(result)

    #Aggregation
    # las bandas que se crearon luego de 1980 y la cantidad de discos que tienen
    pipeline = [
        {"$match": {"anio_creacion": {"$gte": 1980}}},
        {"$project": {
                    "_id": 0,
                    "nombre": 1,
                    "discos": {"$sum": {"$size": "$discos"}}
                    }
        }
    ]
    result = aggregate_db(db, bandas_col, pipeline=pipeline)
    pprint(result)

    #Este pipeline cuenta discos usando unwind y sum en lugar de projection

    # pipeline = [
    # {"$unwind": "$discos"},
    # {
    #     "$group": {
    #         "_id": "$nombre",
    #         "cantidad_discos": {"$sum": 1}
    #     }
    # }
    # ]

    #Generos musicales y las bandas presentes

    pipeline = [
        {"$unwind": "$metadata.genero"},
        {"$group": {
                    "_id": "$metadata.genero",
                    "bandas": {"$push": "$nombre"}
                    }
        }
    ]
    result = aggregate_db(db, bandas_col, pipeline=pipeline)
    pprint(result)