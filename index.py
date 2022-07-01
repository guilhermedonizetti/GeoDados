import requests
from json import loads

class Geolocalizacao:

    def receber_dados():
        valores_cep = open("dados_cep.txt").readlines()
        
        return valores_cep

    def limpar_dados(valores):
        dados = []
        cep = ""

        for i in valores:
            cep = i.replace(".", "")
            cep = cep.replace("-", "")
            dados.append(cep)
            cep = ""
        
        return dados
            

    def buscar_coordenadas(dados):

        coordenadas = []

        for i in dados:
            rota = "https://nominatim.openstreetmap.org/search?city={}&format=json".format(i)
            response = requests.get(rota)

            dados_cidade = loads(response.content)[0]
            coordenadas.append([dados_cidade['lat'], dados_cidade['lon']])

        return coordenadas
    
    def criar_insert_sql(dados, insert):

        comandos = []
        comando_insert = ""

        for i in dados:
            comando_insert = insert.replace("/latitude/", i[0])
            comando_insert = comando_insert.replace("/longitude/", i[1])

            comandos.append(comando_insert)
            comando_insert = ""
        
        return comandos
    
    def executor(self, insert):
        dados = self.receber_dados()
        dados_ajustados = self.limpar_dados(dados)
        coordenadas = self.buscar_coordenadas(dados_ajustados)
        comandos = self.criar_insert_sql(coordenadas, insert)

        for i in comandos:
            print("{}\n\n".format(i))


insert = "INSERT INTO localizacao(id, latitude, longitude) VALUES('/latitude/', '/longitude/')"

obj_geolocalizacao = Geolocalizacao
obj_geolocalizacao.executor(obj_geolocalizacao, insert)
