
#!/bin/bash

# En caso de hacerlo con compose-up.
#docker compose-up # Desde carpeta donde esta el dockercompose.yaml

# En caso de tener la imagen subida al Docker Hub descomentar y comentar arriba, como es nuestro caso.
docker pull sergiopardofernandez/spotifylist_web:v1
docker run -p 8000:8000 -v /code  sergiopardofernandez/spotifylist_web:v1 python3 manage.py runserver 0.0.0.0:8000