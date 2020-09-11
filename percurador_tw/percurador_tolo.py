#!/usr/bin/env python3
"""
 Pequeno script que conecta a Twitter e proba o funcionamiento da súa web durante un rato
 (gardando os IDs dos tweets para ver que sí funcionaou todo e que non estivo voltando sempre o mesmo )
"""

# 1. Coma se pode ver no comezo, esto esta feito para Python 3 (non teño nada en contra do 2, é o que teño instalado )
# 2. É necesario instalar selenium:
#         pip install -U selenium
# 3. pero non chega con esto ... hai que instalar un webdriver ... eu instalei o de Firefox
#         https://github.com/mozilla/geckodriver/releases

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
from datetime import date,datetime,timedelta

# datas que usamos para definir o periodo que imos estar probando na percura
START_DATE = date.fromisoformat('2007-04-01')
END_DATE = date.fromisoformat('2020-06-01')

#Pausas
SCROLL_PAUSE_TIME = 1
SEARCH_PAUSE_TIME = 600

# imos definir esta lista que non é lista (é un diccionario)
lista = dict()


# agora definimos as funcións, vai ata o final para ver o código que se excuta o comezo


def open_browser():
    """ Abre o navegador na paxina de búsquedas de twitter (xa lle poñemos un texto de busqueda) """
    driver = webdriver.Firefox()
    driver.get("https://twitter.com/search?q=(from%3Asnob)%20until%3A2007-04-01&src=typed_query&f=live")
    assert "Twitter" in driver.title
    return driver


def scroll_down(driver):
    """
    unha vez feita unha busqueda, esta función vai avanzando a páxina (usando javascript na paxina)
    cada vez que avanzamos unha páxina recuperamos os tweets que teña recuperados (chamando función)
    cando xa non se pode avanzar máis, pois remata
    (todo esto é asi complexo porque Twitter é das webs que ten paxinación infinita)
    """
    assert "Twitter" in driver.title

    # obter o tamaño da páxina
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # baixar ata o fondo da páxina
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # esperamos un rato, porque a páxina ten que cargar
        time.sleep(SCROLL_PAUSE_TIME)

        # Vexamos que tweets caeron
        searching_tweets(driver)

        # calcular de novo o tamaño da páxina e ver se seguimos (cando se chega ó máximo pois xa non seguimos)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    # apañamos a ultima páxina
    searching_tweets(driver)

    return driver


def search_again(driver,init_date,end_date):
    """ apuntamos ó campo de texto para a búsqueda e metemos un novo rango de datas """
    assert "Twitter" in driver.title
    # buscamos o campo de busqueda
    search_field = driver.find_element_by_xpath("//input[@data-testid='SearchBox_Search_Input']")
    # borrar
    search_field.clear()
    # creamos o texto a escribir (leva datas)
    since_date = init_date.strftime("%Y-%m-%d");
    until_date = end_date.strftime("%Y-%m-%d")
    search_string = "from:snob since:%s until:%s" % (since_date, until_date)
    # escribimos e pulsamos ENTER
    search_field.send_keys(search_string)
    search_field.send_keys(Keys.RETURN)



def end_test(driver):
    """ remata a búsqueda e pechamos o navegador """
    # pechamos o navegador
    driver.quit()


def searching_tweets(driver):
    """
        Pois aquí buscamos dentro da páxina unhas cadeas que están dentro do tweet
        Os de twitter fixeron o seu HTML o suficientemente complexo coma para que non sexa facil topar o que hai dentro
        así que o que fago é buscar as URLs que teñen o texto que apunta a un tweet
        Logo volto a filtrar porque hai outras URLs que non son de tweets (imaxes por exemplo)
        Todo isto metese no diccionario (o feito de usar o diccionario, fai que eliminen os duplicados)
    """
    # esperamos a que cargue o choio
    time.sleep(SCROLL_PAUSE_TIME)
    # recuperamos todos os enlaces ó tweet
    elements_before_page = driver.find_elements_by_xpath('.//a[starts-with(@href,"/Snob/status")]')
    for element in elements_before_page:
        # gardamos a URL
        url = element.get_attribute("href")
        # as veces retorna a url de outras cousas (que damos so co que é un status)
        if (re.fullmatch("https://twitter.com/Snob/status/[0-9]+",url)):
            # para o id quedamos co final da URL
            tweetid = url.split('/')[-1]
            print(tweetid,url)
            tweetid_num = int(tweetid)
            lista[tweetid_num] = url
    print("------")


# para ir saltando de mes en mes na nosa búsqueda
def periodic_jump(startDate, endDate, delta=timedelta(weeks=4)):
    """ unha función sinxela que vai devolvendo unha data segundo o periodo que se define no último parametro """
    # coidoado, coma o timedelta vai contando por semanas non imos a
    # saltar de mes en mes, se non que vai a ir
    # a 28 días ... para a nosa proba non é problema pero non usedes
    # esta función para ir obtendo os meses entre 2 datas
    currentDate = startDate
    while not currentDate > endDate:
        yield currentDate
        currentDate += delta


########
#   Aquí comeza a execución

# abrimos o navegador
driver = open_browser()
scroll_down(driver)
# agora imos a facer multiples busquedas
# poñemos unha data de inicio
old_date = START_DATE
# Hai que contar porque hai que facer un descanso cada 40 chamadas
counter = 1
for dt in periodic_jump(START_DATE,END_DATE):
    # descanso cada 40 chamadas
    counter = counter + 1
    if counter > 20:
        print("--- descansamos")
        time.sleep(SEARCH_PAUSE_TIME)
        counter = 1


    # facemos unha nova busqueda entre as dúas datas
    print("---" + dt.strftime("%Y-%m-%d") )
    search_again(driver,old_date,dt)
    # percoremos todos os tweets
    scroll_down(driver)
    # gardamos a data de inicio desta busqueda
    old_date = dt

# pechamos todo
end_test(driver)

print("--- Escribindo o resultado")
# e escribimos toda a lista que fixemos
# nun ficheiro de texto id,url
with open('tweet_list.txt', 'w') as file:
  for key,value in sorted(lista.items()):
    line = "%s,%s" % (key,value)
    print(line, file=file)
