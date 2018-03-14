import funciones as f

base = 'https://resultados2018.registraduria.gov.co/resultados/99SE/BXXXX/'
departamentos = f.lista_departamentos(base)

for departamento in f.lista_departamentos(base):
    nombre_departamento, municipios = f.lista_municipios(departamento, base)
    for municipio in municipios:
        try:
            f.datos_municipio(municipio, nombre_departamento, 'senado')
        except:
            print(municipio, nombre_departamento)
            raise
