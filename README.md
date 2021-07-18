# pi-sergiosdaniel

- Para ejecutar lanzar el script setup.sh , se puede hacer con compose-up o con docker pull, las opciones aparecen comentadas en el propio script.

- Respecto a fallos conocidos y otros aspectos importantes hemos actualizado el doc de la propuesta, ahí está todo incluído.

- Las horas de trabajo se han especificado al final del documento citado anteriormente.

- Para poder hacer los test hemos incluído en algunas funciones lo siguiente:

        try:
            request.session['access_token']
        except:
            request.session['access_token'] = 'a2fbd32563c04123a3515c45951206ca'

	Para poder obtener el access_token.