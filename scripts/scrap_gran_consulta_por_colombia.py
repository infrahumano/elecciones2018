import funciones as f

base_consulta = 'https://resultados2018.registraduria.gov.co/99HIS/resultados/htmlfijo/consulta.html?id=boletin0104/d3'
base = 'https://resultados2018.registraduria.gov.co/resultados/99CA/BXXXX/'

for departamento in f.lista_departamentos(base, 'DCA99999.htm'):
    nombre_departamento, municipios = f.lista_municipios_consulta(departamento, base, base_consulta)
    for municipio in municipios:
        try:
            f.datos_municipio_consulta(municipio, nombre_departamento, 'gran_consulta_por_colombia')
        except:
            print(municipio, nombre_departamento)
            raise
