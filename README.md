# Premier League & Top Leagues Tracker

## Descripción del proyecto

Premier League & Top Leagues Tracker es una aplicación Python de consola que consume una API REST externa para consultar tablas de posiciones de ligas de fútbol según una temporada determinada.

La aplicación obtiene datos desde TheSportsDB, procesa la respuesta JSON y muestra por consola el campeón o líder de la temporada junto con el top de equipos de la tabla.

## Stakeholder

El stakeholder principal es un analista deportivo o periodista de datos que necesita consultar rápidamente el rendimiento de equipos en distintas ligas europeas sin revisar manualmente múltiples sitios web.

## Problema

Consultar tablas de posiciones históricas o recientes de ligas de fútbol de forma manual consume tiempo, puede generar errores y dificulta reutilizar la información en procesos automatizados.

## Solución

La aplicación automatiza la consulta a una API REST, procesa los datos obtenidos en formato JSON y entrega una salida clara por consola. Además, el proyecto se ejecuta mediante contenedores Docker y puede automatizarse con Jenkins dentro de un flujo CI/CD.

## API utilizada

La aplicación utiliza TheSportsDB API.

Endpoint utilizado:

```text
https://www.thesportsdb.com/api/v1/json/{SPORTSDB_API_KEY}/lookuptable.php
