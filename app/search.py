from flask import current_app

def add_to_index (index, model):
    # Return without doing anything in the event search server isn't configured
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index = index, doc_type = index, id = model.id, body = payload)

def remove_from_index (index, model):
    if not current_app.elasticsearch:
        return
    # Deletes document stored under a given ID
    current_app.elasticsearch.delete(index = index, doc_type = index, id = model.id)

def query_index (index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        # Body includes pagination arguments. Takes a look at all indices that are currently stored.
        index = index, doc_type = index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})

    ids = [int(hit['_id']) for hit in search['hits']['hits']]

    # Search returns with a list of id elements for the search results, and the total number of hits
    return ids, search['hits']['total']