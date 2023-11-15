es_mappings = {
    'persons': {
        "properties": {
            "films": {"properties": {
                "id": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
                "roles": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}}}
            },
            "id": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "name": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}}
        }
    },
    'movies': {"dynamic": "strict",
               "properties": {
                   "actors": {"type": "nested", "dynamic": "strict", "properties": {
                       "id": {"type": "keyword"},
                       "name": {"type": "text"}}},
                   "actors_names": {"type": "text"},
                   "description": {"type": "text"},
                   "director": {"type": "text"},
                   "directors": {"type": "nested", "dynamic": "strict",
                                 "properties": {
                                     "id": {"type": "keyword"},
                                     "name": {"type": "text"}}
                                 },
                   "genre": {"type": "keyword"},
                   "id": {"type": "keyword"},
                   "imdb_rating": {"type": "float"},
                   "title": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
                   "writers": {"type": "nested", "dynamic": "strict",
                               "properties": {
                                   "id": {"type": "keyword"},
                                   "name": {"type": "text"}}},
                   "writers_names": {"type": "text"}}
               },
    'genres': {"dynamic": "strict",
               "properties": {
                   "description": {"type": "text"},
                   "id": {"type": "keyword"},
                   "name": {"type": "text", "fields": {"raw": {"type": "keyword"}}}}
               }
}
