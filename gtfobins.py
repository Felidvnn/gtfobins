import argparse
import requests
from bs4 import BeautifulSoup 

url = 'https://gtfobins.github.io/'
respuesta = requests.get(url)

def ListaBins():
    global respuesta
    if respuesta.status_code == 200: 
        soup = BeautifulSoup(respuesta.text, 'html.parser')

        bins = soup.find_all('a', href=True)  # Busca dentro de etiquetas <a> con atributos href
        binarios = {}
        for bin in bins:
            binario = bin['href'].split('/')
            if len(binario) == 4 and binario[1] == 'gtfobins' and binario[3]:
                if binario[2] in binarios:
                    binarios[binario[2]].append(binario[3][1:])
                else:
                    binarios[binario[2]] = [binario[3][1:]]
            
        return binarios

def Buscarbins(lista, function=''):
    function = function.lower()
    ListBins = ListaBins()
    toSearch = []
    aux = 0

    for bin in lista:
        bin = bin.split('/')
        toSearch.append(bin[-1])

    if not function:
        print("\033[32m[+] Binarios encontrados en GTFOBins:\033[0m")
        for index, bin in enumerate(toSearch):
            if bin in ListBins:
                print(f"\033[35m[*] \033[0m\033[1;31m{lista[index]}\033[0m: {' | '.join(ListBins[bin])} ")
                aux = 1
    elif function:
        print(f"\033[32m[+] Binarios encontrados en GTFOBins con {function}:\033[0m")
        for index, bin in enumerate(toSearch):
            if bin in ListBins:
                if function in ListBins[bin]:
                    print(f"\033[35m[*] \033[0m\033[1;31m{lista[index]}\033[0m: {url}gtfobins/{bin}/#{function}")
                    aux = 1
        if aux == 0:
            print(f"\n\033[32m[!] No existen binarios con {function}, revisar otras opciones o sintaxis.\033[0m")

def main():
    parser = argparse.ArgumentParser(description='App para buscar binarios en GTFOBins dado una lista.txt')
    parser.add_argument('list', type=str, help='Lista con binarios en formato txt')
    parser.add_argument('-f', '--function', type=str, default='', help='Filtro opcional para buscar binarios por funciones especificas (ejemplo: sudo, suid, shell, etc)')
    args = parser.parse_args()

    try:
        with open(args.list, 'r') as f:
            lista = [linea.strip() for linea in f]
    except FileNotFoundError:
        print(f"\033[31mError: El archivo '{args.list}' no se encontró.\033[0m")
        return
    
    Buscarbins(lista, args.function)

if __name__ == "__main__":
    main()
