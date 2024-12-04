import io
import os
import csv
import datetime
import chromadb
import pandas as pd
import traceback

from chromadb.utils import embedding_functions

from model_configurations import get_model_configuration

gpt_emb_config = get_model_configuration('gpt-3.5-embeddings')

dbpath = "./"

def get_chromadb_id():
    count = 1
    today = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    ids = f"{today}{count:04}"
    return ids

def chromadb_add(metadata, text, total_count=1):
    print('===== Add from vector database =====')

    chroma_client = chromadb.PersistentClient(path=dbpath)
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key = gpt_emb_config['api_key'],
        api_base = gpt_emb_config['api_base'],
        api_type = gpt_emb_config['openai_type'],
        api_version = gpt_emb_config['api_version'],
        deployment_id = gpt_emb_config['deployment_name']
    )
    collection = chroma_client.get_or_create_collection(
        name="TRAVEL",
        metadata={"hnsw:space": "cosine"},
        embedding_function=openai_ef)

    id = get_chromadb_id()
    ids =[]
    for i in range(total_count):
        ids.append(f"{id[:-4]}{int(id[-4:]) + i:04}")

    collection.add(
        documents=text,
        metadatas=metadata,
        ids=ids
    )

def process_text_data(file_name, fname, ftype, faddress, ftel, fcity, ftown ,fdate, content_list, metadatas, total_count, ftext):
    metadata_template = {
        "file_name": file_name,
        "name": fname,
        "type": ftype,
        "address": faddress,
        "tel": ftel,
        "city": fcity,
        "town": ftown,
        "date": int(datetime.datetime.strptime(fdate, "%Y-%m-%d").timestamp())
    }

    metadatas.append(metadata_template.copy())
    content_list.append(ftext)
    total_count += 1

    return total_count

def init_chromadb():
    content_list = []
    metadatas = []
    total_count = 0

    file_name = 'COA_OpenData.csv'
    with open(file_name, 'r', encoding='utf-8-sig') as file:
        csv_content = file.read()

    csv_buffer = io.StringIO(csv_content)
    csv_reader = csv.DictReader(csv_buffer)

    for row in csv_reader:
        fname = row['Name']
        ftype = row['Type']
        faddress = row['Address']
        ftel = row['Tel']
        ftext = row['HostWords']
        fcity = row['City']
        ftown = row['Town']
        fdate = row['CreateDate']

        total_count = process_text_data(file_name, fname, ftype, faddress, ftel, fcity, ftown, fdate, content_list, metadatas, total_count, ftext)
    
    chromadb_add(metadatas, content_list, total_count)

def generate_hw01():
    chroma_client = chromadb.PersistentClient(path=dbpath)

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=gpt_emb_config['api_key'],
        api_base=gpt_emb_config['api_base'],
        api_type=gpt_emb_config['openai_type'],
        api_version=gpt_emb_config['api_version'],
        deployment_id=gpt_emb_config['deployment_name']
    )

    collection = chroma_client.get_or_create_collection(
        name="TRAVEL",
        metadata={"hnsw:space": "cosine"},
        embedding_function=openai_ef
    )

    return collection

def generate_hw02(question, city, store_type, start_date, end_date):
    chroma_client = chromadb.PersistentClient(path=dbpath)

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=gpt_emb_config['api_key'],
        api_base=gpt_emb_config['api_base'],
        api_type=gpt_emb_config['openai_type'],
        api_version=gpt_emb_config['api_version'],
        deployment_id=gpt_emb_config['deployment_name']
    )

    collection = chroma_client.get_or_create_collection(
        name="TRAVEL",
        metadata={"hnsw:space": "cosine"},
        embedding_function=openai_ef
    )

    # Convert dates to timestamps
    start_date_ts = int(start_date.timestamp()) if start_date else None
    end_date_ts = int(end_date.timestamp()) if end_date else None

    where_conditions = []
    if city:
        where_conditions.append({"city": {"$in": city}})
    if store_type:
        where_conditions.append({"type": {"$in": store_type}})
    if start_date_ts:
        where_conditions.append({"date": {"$gte": start_date_ts}})
    if end_date_ts:
        where_conditions.append({"date": {"$lte": end_date_ts}})

    # Combine conditions with "$and" if there are any
    where_clause = {"$and": where_conditions} if where_conditions else None

    # Execute the query using the provided parameters
    results = collection.query(
        query_texts=[question],
        n_results=10,
        where=where_clause
    )
    
    # Collect query results
    filtered_results = [
        (metadata['name'], 1 - dist)
        for metadata, dist in zip(results['metadatas'][0], results['distances'][0])
        if metadata
    ]

    # Sort results in descending order of similarity scores
    sorted_results = sorted(filtered_results, key=lambda x: x[1], reverse=True)

    # Filter results with a similarity score of 0.80 or higher
    final_results = [name for name, score in sorted_results if score >= 0.80]

    return final_results

def generate_hw03(question, store_name, new_store_name, city, store_type):
    chroma_client = chromadb.PersistentClient(path=dbpath)

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=gpt_emb_config['api_key'],
        api_base=gpt_emb_config['api_base'],
        api_type=gpt_emb_config['openai_type'],
        api_version=gpt_emb_config['api_version'],
        deployment_id=gpt_emb_config['deployment_name']
    )

    collection = chroma_client.get_or_create_collection(
        name="TRAVEL",
        metadata={"hnsw:space": "cosine"},
        embedding_function=openai_ef
    )

    store_data = collection.get(
        where={"name": store_name}, 
        include=["metadatas", "documents"]
    )

    if store_data["metadatas"] and len(store_data["metadatas"]) > 0:
        for metadata in store_data["metadatas"]:
            if metadata["name"] == store_name:
                # Update the metadata and save it to the collection
                metadata["new_store_name"] = new_store_name
                collection.update(
                    ids=[store_data["ids"][0]],
                    metadatas=[metadata]
                )
                print(f"Updated store metadata: {metadata}")

    # Dynamically build the 'where' clause for the query
    where_conditions = []

    if city:
        where_conditions.append({"city": {"$in": city}})
    if store_type:
        where_conditions.append({"type": {"$in": store_type}})

    where_clause = {"$and": where_conditions} if where_conditions else None

    # Execute the query using the provided parameters
    results = collection.query(
        query_texts=[question],
        n_results=10,
        where=where_clause
    )

    #print(results)
    # Collect query results
    processed_results = []
    for metadata, dist in zip(results["metadatas"][0], results["distances"][0]):
        similarity = 1 - dist
        if similarity >= 0.80:
            display_name = metadata.get("store_name", metadata["name"])
            processed_results.append((display_name, similarity))

    # Sort results in descending order of similarity scores
    sorted_results = sorted(processed_results, key=lambda x: x[1], reverse=True)

    return [name for name, _ in sorted_results]



