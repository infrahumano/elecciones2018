# Tablas de Elecciones Colombianas 2018

```
Because no battle is ever won he said. They are not even fought. 
The field only reveals to man his own folly and despair, 
and victory is an illusion of philosophers and fools.

― William Faulkner, The Sound and the Fury
```

Los archivos son CSV comprimidos (con `gzip`):

* [Senado](senado/) 
* [Cámara](camara/) 
* [Consulta Petro versus Caicedo](consulta_inclusion_social_por_la_paz/) (dizque "Consulta Inclusión Social por la Paz")
* [Consulta Duque versus Ramírez versus Ordóñez](gran_consulta_por_colombia/) (dizque "Gran Consulta por Colombia")
* [Participación](participacion/) (cuentas de votos válidos e inválidos por votación y municipio) 
* [Primera vuelta presidencial](primera_vuelta_presidencial/)

Los datos vienen del [preconteo de la
registraduría](https://resultados2018.registraduria.gov.co/inicio.htm). 

Los scripts para bajarse y tablear los datos [están acá](scripts/).

Si quiere ponerle códigos del Dane a las tablas,
[aquí](https://github.com/nelsonamayad/Elecciones-presidenciales-2018/blob/master/Elecciones%202018/traductor_infrahumano.csv)
Nelson Amaya armó una tablita para conviertir cada combinación de `municipio`
y `departamento` en su respectivo código. Por supuesto, descontando los
consultados. 

Donaciones de jugo de corozo: [@infrahumano](http://twitter.com/infrahumano)
