import os
import sys
from xmlrpc.client import Boolean
import uvicorn
print('DEBUG: Uvicorn imported!!')
from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from mimetypes import guess_type
import toml
import glob

if os.path.isfile('media_server.toml'):
    server_settings = toml.load('media_server.toml')
else:
    server_settings = toml.load('media_server.example.toml')

MEDIA_SOURCES, MEDIA_TYPES = server_settings['MEDIA_SOURCES'], server_settings['MEDIA_TYPES']
HOST, PORT = server_settings['HOST'], server_settings['PORT']

CORS_ALLOW_ORIGINS = ['http://localhost, http://localhost:4010, http://localhost:8765']

def _rename_file_with_prefix(source: str, media_file: str, prefix: str):
    media_source = MEDIA_SOURCES[source]
    media_folder = media_source['media_folder']

    src = os.path.join(media_folder, media_file)
    dest = os.path.join(media_folder, f'{prefix}_{media_file}')

    if not os.path.isfile(src):
        return Response(status_code=404)
    
    try:
        os.rename(src, dest)
        print("Renamed:", src, 'to', dest)
    except Exception as e:
        return Response(str(e), status_code=404)
    
    return Response(status_code=200)

class MediaServerAPI_Wrapper(FastAPI):

    def __init__(self):
        """
        Initializes a custom FastAPI instance to serve media (image) files.
        """
        print('Initializing MediaServerAPI_Wrapper...')
        
        super().__init__()

        origins = CORS_ALLOW_ORIGINS

        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        def custom_openapi():
            from fastapi.openapi.utils import get_openapi

            print('Running custom_openapi...')
            
            if self.openapi_schema:
                return self.openapi_schema
            openapi_schema = get_openapi(
                title="MediaServerAPI_Wrapper",
                version='1.0',
                description="Custom API enpoints available for simple media server.",
                routes=self.routes,
            )
            openapi_schema["info"]["x-logo"] = {
                "url": "https://avatars.githubusercontent.com/u/138668"
            }
            self.openapi_schema = openapi_schema
            return self.openapi_schema

        self.openapi = custom_openapi
        
        @self.get("/")
        def home():
            return RedirectResponse(url='/docs', status_code=307)

        @self.get("/media/{source}/{media_file}")
        def media(source: str, media_file: str):
            media_source = MEDIA_SOURCES[source]
            media_folder = media_source['media_folder']

            filename = os.path.join(media_folder, media_file)

            if not os.path.isfile(filename):
                return Response(status_code=404)
            
            with open(filename, 'rb') as f:
                content = f.read()

            content_type, _ = guess_type(filename)
            
            return Response(content, media_type=content_type)

        @self.get("/delete_media/{source}/{media_file}")
        def delete_media(source: str, media_file: str):
            return _rename_file_with_prefix(source, media_file, 'DEL')

        @self.get("/favorite_media/{source}/{media_file}")
        def favorite_media(source: str, media_file: str):
            return _rename_file_with_prefix(source, media_file, 'FAV')

        @self.get("/media_sources")
        async def media_sources():
            return JSONResponse(
                {'media_sources': MEDIA_SOURCES},
                status_code=200
            )

        # TODO: https://thispointer.com/python-get-list-of-files-in-directory-sorted-by-date-and-time/
        @self.get("/media_list/{source}")
        async def media_list(source: str, filter: Union[str, None] = None, sort: bool = False):

            source = source.replace('(', '').replace(')', '').replace('"', '').strip()

            def _get_media_list():
                media_source = MEDIA_SOURCES[source]
                media_files = []
                media_filter = filter if filter else media_source['media_filter']
                if media_source.get('media_folder', None):
                    media_folder = media_source['media_folder']
                    for media_type in MEDIA_TYPES:
                        file_extension = media_type.split('/')[-1]
                        media_type_files = [url.replace(f'{media_folder}\\','') for url in glob.glob(f'{media_folder}/*.{file_extension}')]
                        media_files.extend(media_type_files)
                    media_files = sorted(media_files) if sort else media_files
                elif media_source.get('media_links', None):
                    media_files = media_source['media_links']

                if bool(media_filter):
                    media_files = [media_file for media_file in media_files if media_filter in media_file]
    
                return media_files, media_filter

            media_files, media_filter = _get_media_list()
            return JSONResponse(
                {'media_list': media_files, 'media_filter': media_filter},
                status_code=200
            )

        # Add shutdown event (would only be of any use in a multi-process, not multi-thread situation)
        @self.get("/shutdown")
        async def shutdown():
            import time
            import psutil
            import threading

            def suicide():
                time.sleep(1)
                myself = psutil.Process(os.getpid())
                myself.kill()

            threading.Thread(target=suicide, daemon=True).start()
            print(f'>>> Successfully killed API <<<')
            return Response(status_code=200)

"""
Simple bootstrapper intended to be used used to start the API as a daemon process
"""
def start(host=HOST, port=PORT):
    app = MediaServerAPI_Wrapper()
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        start(host=sys.argv[1], port=int(sys.argv[2]))
    else:
        start()
