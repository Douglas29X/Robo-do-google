from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

pesquisa = input("Digite a pesquisa:\n")

driver = webdriver.Chrome() #se o chromedriver está na pasta ele já lê automaticamente.
driver.get("https://www.google.com")

#encontra o elemento por qualquer atributo da página (no caso input).
barra = driver.find_element_by_xpath("//input[@aria-label='Pesquisar']")

barra.send_keys(pesquisa)
barra.send_keys(Keys.ENTER)

resultados = driver.find_element_by_xpath("//div[@id='result-stats']").text

#Primeiro ele pega a segunda fatia do corte e depois a primeira, deixando só o número.
numero_resultados = int(resultados.split('Aproximadamente ')[1].split(' resultados')[0].replace('.',''))

numero_max_paginas = numero_resultados / 10

#caso queira manter o código anterior no cmd, desabilite o comando a seguir.
os.system("cls")
print(resultados)
print(f"Número de páginas: {numero_max_paginas}")
limite_usuario = int(input("Até que página você quer que o robô faça o relatório?:\n"))

url_pagina = driver.find_element_by_xpath("//a[@aria-label='Page 2']").get_attribute("href")
pagina_atual = 0
start = 10

with open("Relatório.csv", mode="w") as arquivo:
	while pagina_atual <= (limite_usuario - 1):
		if not pagina_atual == 0 and pagina_atual != 1:
			url_pagina = url_pagina.replace(f'start={start}',f'start={start+10}')
			start += 10
			driver.get(url_pagina)
		elif pagina_atual == 1:
			driver.get(url_pagina)

		#parte que engloba o resultado dos sites (elements retornam uma lista).
		divs_g_composto = driver.find_elements_by_xpath("//div[@class='g tF2Cxc']")
		divs_g_simples = driver.find_elements_by_xpath("//div[@class='g']")

		divs = divs_g_simples + divs_g_composto

		#lembrando que a tag anterior sempre fica sendo atualizada pelo google.

		for div in divs:
			nome = div.find_element_by_tag_name("h3")
			link = div.find_element_by_tag_name("a")
			resultado = f"**************\n{nome.text};{link.get_attribute('href')}\n"
			arquivo.write(resultado)
		print(f"Página {pagina_atual} processada")

		pagina_atual += 1

print("Dados registrados no arquivo 'Relatório.csv'")

