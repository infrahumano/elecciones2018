import funciones as f

base = 'https://resultados2018.registraduria.gov.co/resultados/99CA/BXXXX/'

for departamento in f.lista_departamentos(base, 'DCA99999.htm'):
    nombre_departamento, municipios = f.lista_municipios(departamento, base)
    for municipio in municipios:
        try:
            f.datos_municipio(municipio, nombre_departamento, 'camara')
        except:
            print(municipio, nombre_departamento)
            raise
