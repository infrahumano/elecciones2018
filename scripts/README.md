# Scripts para bajarse los datos

Los archivos con prefijo `scrap` son scripts que se bajan los datos de cada
municipio en un archivo `json` con nombre apropiado (necesitan que exista un
directorio llamado `datos` donde ponen las cosas. 

`funciones.py` es un módulo que contiene todas las funciones para bajarse los
datos. Con senado y cámara se puede depender de `BeautifulSoup` pero para las
páginas de las consultas los de la registraduría están experimentando con un
modelo de "página única" que se genera dinámicamente y en consecuencia tuve que
usar `selenium` con un `Firefox` descabezado. Esos procesos son, en
consecuencia, muchísimo más lentos. 

Una vez recolectados los `json` armé unas funciones (también en `funciones.py`)
que los convierten en tablas de `pandas` para poder generar los archivos CSV.

Sobra decir que esto debe usarse bajo su propio riesgo. Fue escrito a la
carrera ayer pues no encontré mis viejos scripts en R que usaba hace unos años.
Quería probar qué tan complicado sería hacerlo con Python. Fácil, en últimas.
