from datetime import datetime


def delete_collection(coll_ref):
    batch_size = 10
    docs = coll_ref.list_documents(page_size=batch_size)
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.get().to_dict()}')
        doc.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref)

def date_from_str(d):
    try: return datetime.strptime(d, '%d-%m-%Y')
    except: return None

def str_from_date(d):
    return d.strftime('%d-%m-%Y')
