import json
import uuid
from typing import List

import aiofiles
import inflection
from fastapi import APIRouter, HTTPException, Depends, Request, Body
from fastapi import File, UploadFile
from google.protobuf import json_format
from starlette.responses import FileResponse
from werkzeug.utils import secure_filename

from komodo.server.globals import get_email_from_header, get_appliance
from komodo.shared.documents.text_extract_helper import TextExtractHelper
from komodo.shared.utils.filestats import file_details
from komodo.store.collection_store import CollectionStore

router = APIRouter(
    prefix='/api/v1/collections',
    tags=['Collections']
)


@router.post('')
async def create_collection(shortcode=Body(""), name=Body(), description=Body(),
                            email=Depends(get_email_from_header)):
    try:
        store = CollectionStore()
        path = inflection.underscore(secure_filename(name)) + "_" + str(uuid.uuid4())[0:6]
        collection = store.get_or_create_collection(shortcode, path=path, name=name, description=description)
        store.add_user_collection(email, collection.shortcode)
        collection_dict = json.loads(json_format.MessageToJson(collection))
        return collection_dict
    except:
        raise HTTPException(status_code=500, detail="Failed to create collection")


@router.get('')
async def list_collection(email=Depends(get_email_from_header)):
    store = CollectionStore()
    collections = store.retrieve_collections_by_user(email)
    response = []
    for collection in collections:
        try:
            collection_dict = json.loads(json_format.MessageToJson(collection))
            collection_dict['guid'] = collection.shortcode
            if 'files' in collection_dict:
                del collection_dict['files']
            response.append(collection_dict)
        except Exception as e:
            print("Failed to list collection with shortcode: ", collection.shortcode, e)

    return response


@router.get('/{shortcode}')
async def get_collection(shortcode: str):
    store = CollectionStore()
    try:
        collection = store.retrieve_collection(shortcode)
        collection_dict = json.loads(json_format.MessageToJson(collection))
        return collection_dict
    except Exception:
        raise HTTPException(status_code=404, detail="Collection not found")


@router.delete('/{shortcode}')
async def delete_collection(shortcode: str):
    try:
        store = CollectionStore()
        response = store.remove_collection(shortcode)
        return response
    except Exception:
        raise HTTPException(status_code=404, detail="Error deleting collection: " + shortcode)


@router.delete('/everything/forsure')
async def delete_all_collections():
    try:
        store = CollectionStore()
        store.remove_everything()
        return {"message": "Successfully deleted all collections"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Error deleting collections: " + str(e))


def get_collection_from_store(shortcode):
    store = CollectionStore()
    collection = store.retrieve_collection(shortcode)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.post("/upload_files/{shortcode}")
async def upload(files: List[UploadFile] = File(...),
                 email=Depends(get_email_from_header),
                 appliance=Depends(get_appliance),
                 collection=Depends(get_collection_from_store)):
    try:
        locations = appliance.config.locations()
        home = locations.user_collections(email)
        folder = home / secure_filename(collection.path)

        for file in files:
            filepath = await get_writable_filepath(folder, file.filename)
            contents = await file.read()
            async with aiofiles.open(filepath, 'wb') as f:
                await f.write(contents)

            await update_file_in_collection(collection, filepath)

        store = CollectionStore()
        store.store_collection(collection)
        collection_dict = json.loads(json_format.MessageToJson(collection))

    except Exception as e:
        return {"message": "There was an error uploading the file: " + str(e)}

    return {"message": f"Successfully uploaded {[file.filename for file in files]}", "collection": collection_dict}


async def get_writable_filepath(folder, filename):
    filename = os.path.basename(secure_filename(os.path.basename(filename)))
    filepath = folder / filename
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    return filepath


async def update_file_in_collection(collection, filepath):
    updated_files = []
    for file in collection.files or []:
        if file.path != str(filepath):
            updated_files.append(file)

    uploaded = file_details(str(filepath))
    updated_files.append(uploaded)

    del collection.files[:]
    collection.files.extend(updated_files)
    return collection


@router.post('/upload_stream/{shortcode}')
async def upload_stream(request: Request,
                        email=Depends(get_email_from_header),
                        appliance=Depends(get_appliance),
                        collection=Depends(get_collection_from_store)):
    # For full discussion on this approach, see:
    # https://stackoverflow.com/questions/65342833/fastapi-uploadfile-is-slow-compared-to-flask/70667530#70667530
    try:
        locations = appliance.config.locations()
        home = locations.user_collections(email)
        folder = home / secure_filename(collection.path)
        filename = request.headers['filename']
        filepath = await get_writable_filepath(folder, filename)

        async with aiofiles.open(filepath, 'wb') as f:
            async for chunk in request.stream():
                await f.write(chunk)

        await update_file_in_collection(collection, filepath)

        store = CollectionStore()
        store.store_collection(collection)
        collection_dict = json.loads(json_format.MessageToJson(collection))

    except Exception as e:
        return {"message": "There was an error uploading the file: " + str(e)}

    return {"message": f"Successfully uploaded {filename}", "collection": collection_dict}


@router.get('/{shortcode}/{file_guid}')
def download_file(file_guid: str, collection=Depends(get_collection_from_store)):
    for file in collection.files:
        if file.guid == file_guid:
            return FileResponse(file.path, media_type='application/octet-stream', filename=file.name)

    raise HTTPException(status_code=404, detail="File not found")


import os


def adjust_filename_to_txt(filename):
    base = os.path.splitext(filename)[0]  # Removes current extension if present
    return f"{base}.txt"


@router.get('/{shortcode}/{file_guid}/{format}')
def download_file_format(file_guid: str, format: str, collection=Depends(get_collection_from_store),
                         appliance=Depends(get_appliance)):
    for file in collection.files:
        if file.guid == file_guid:
            if format == 'text':
                cache = appliance.config.locations().cache()
                helper = TextExtractHelper(file.path, cache)
                text = helper.extract_text()
                path = helper.extracted_path()
                return FileResponse(path, media_type='text/plain', filename=adjust_filename_to_txt(file.name))

    raise HTTPException(status_code=404, detail="File not found")


@router.delete('/{shortcode}/{file_guid}')
async def remove_file(file_guid: str, collection=Depends(get_collection_from_store)):
    for file in collection.files:
        if file.guid == file_guid:
            collection.files.remove(file)
            store = CollectionStore()
            store.store_collection(collection)
            return {"message": "File removed"}

    raise HTTPException(status_code=404, detail="File not found")
