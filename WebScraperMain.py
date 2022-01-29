# -*- coding: utf-8 -*-

"""

*******EQUIPO 11*******
García Hernández Andrea A.
López Aparicio Ángel
López González Mariangely
Rosas Léon Diego

Fecha de entrega: 28/enero/2022
Versión de Python: 3.8.8

"""

import pandas as pd
import pandasql as ps
import time 
import numpy as np
import re
from selenium import webdriver
import matplotlib.pyplot as plt


aux=pd.DataFrame()

aux.to_excel("df_lumen.xlsx",index=False)
aux.to_excel("df_officedepot.xlsx",index=False)
aux.to_excel("df_officemax.xlsx",index=False)

def Buscador_Precios_Selenium_Lumen(producto):
    
    ### ingresamos a la pagina web
    ### El directorio del webdriver varía de
    ### computadora a computadora; se debe 
    ### actualizar dependiendo donde esté 
    ### almacenado.
    path ="C:\webdriver\chromedriver.exe"

    driver=webdriver.Chrome(path)
    url= "https://lumen.com.mx/search?q="+producto
    driver.get(url)
    
    ####### Accedemos a los elementos que contienen 
    ####### los datos que queremos de la pagina web 
    

    productos= driver.find_elements_by_class_name("item-box")
    ### Accedemos a las url's almacenadas en la variable productos


    lista_urls=list()
    for i in range(len(productos)):
        try:
            lista_urls.append(
                productos[i].find_element_by_tag_name(
                    "a").get_attribute("href"))
        except:
            lista_urls.append(np.nan)
            
    ### accedemos a los nombres de los productos

    lista_nombres=list()
    for i in range(len(productos)):
        try:
            # La sintáxis cuando un producto tiene descuento, cambia
            # para ello, hacemos un if-else que separe 
            # los productos con descuento
            if "%" in productos[i].text.split("\n")[0]:
                lista_nombres.append(productos[i].text.split("\n")[1])
            else:
                lista_nombres.append(productos[i].text.split("\n")[0])
        except:
            lista_nombres.append(np.nan)
            
    ### accedemos a los precios base y promo de los productos 

    lista_precios=list()
    lista_promos=list()
    for i in range(len(productos)):
        try:
            if "%" in productos[i].text.split("\n")[0]:
                lista_precios.append(
                    productos[i].text.split("\n")[4].split(" ")[0])
            else: 
                lista_precios.append(
                    productos[i].text.split("\n")[3])
        except:
            lista_precios.append(np.nan)
        try:
            if "%" in productos[i].text.split("\n")[0]:
                lista_promos.append(
                    productos[i].text.split("\n")[4].split(" ")[1])
            else:
                lista_promos.append(
                    productos[i].text.split("\n")[4])
        except:
            lista_promos.append(np.nan)



    df_lumen =pd.DataFrame({"nombre":lista_nombres,"url":lista_urls,
                            "precio_promocion":lista_promos,
                            "precio_original":lista_precios})
    df_lumen["autoservicio"]="Lumen"
    df_lumen["marca"]= producto
    df_lumen["fecha"]= time.strftime("%d/%m/%y")

    df_lumen = df_lumen[["fecha","autoservicio",
                         "marca","nombre","url",
                         "precio_promocion","precio_original"]]
    ## este filtro apenas se agrega

    df_lumen  =df_lumen.reset_index(drop=True)

    datos_webscraper=pd.read_excel("df_lumen.xlsx")

    datos_webscraper= pd.concat([datos_webscraper,df_lumen],axis=0)

    datos_webscraper.to_excel("df_lumen.xlsx",index=False)

    driver.quit()
    return df_lumen

def Buscador_Precios_Selenium_OfficeDepot(producto):
    
    ### ingresamos a la pagina web 
    path = "C:\webdriver\chromedriver.exe"
    url = "https://www.officedepot.com.mx/officedepot/en/search/?text="
    ## Creamos el url al que se quiere acceder, 
    ## sólo observando el link base de la página
    productoc = producto.replace(" ","+")
    url = url+productoc

    ### Accedemos a la página web deseada
    
    driver = webdriver.Chrome(path)
    driver.get(url)   
    
    ####### Accedemos a los elementos que contienen 
    ####### los datos que queremos de la pagina web 
    
    productos= driver.find_elements_by_class_name("product-item")
    ### accedemos a las urls almacenadas en la variable productos
    
    lista_urls = list()
    ### Obtenemos los URLS de productos    
    for i in range(len(productos)):
        try:
            lista_urls.append(
                productos[i].find_element_by_tag_name(
                    "a").get_attribute("href"))
        except:
            lista_urls.append(np.nan)

    ### accedemos a los nombres de los productos

    lista_nombres = list()
    ### Obtenemos los nombres de productos
    for i in range(len(productos)):
        try:
            if "%" in productos[i].text.split("\n")[0]:
                lista_nombres.append(productos[i].text.split("\n")[2])
            elif "SKU" not in productos[i].text.split("\n")[0]:
                lista_nombres.append(productos[i].text.split("\n")[2])
            else:
                lista_nombres.append(productos[i].text.split("\n")[1])
        except:
            lista_nombres.append(np.nan)
            

    ### accedemos a los precios base y promo de los productos 

    lista_precios=list()
    lista_promos=list()
    for i in range(len(productos)):
        try:
            if "%" in productos[i].text.split("\n")[0]:
                lista_precios.append(productos[i].text.split("\n")[3])
            elif "SKU" not in productos[i].text.split("\n")[0]:
                lista_precios.append(productos[i].text.split("\n")[3])
            else: 
                lista_precios.append(productos[i].text.split("\n")[2])
        except:
            lista_precios.append(np.nan)
        try:
            if "%" in productos[i].text.split("\n")[0]:
                lista_promos.append(productos[i].text.split("\n")[4])
            elif "SKU" not in productos[i].text.split("\n")[0]:
                lista_promos.append(np.nan)
            else:
                lista_promos.append(np.nan)
        except:
            lista_promos.append(np.nan)
            

    df_officedepot =pd.DataFrame({"nombre":lista_nombres,"url":lista_urls,
                                  "precio_promocion":lista_promos,
                                  "precio_original":lista_precios})
    df_officedepot["autoservicio"]="Office Depot"
    df_officedepot["marca"]= producto
    df_officedepot["fecha"]= time.strftime("%d/%m/%y")
    df_officedepot = df_officedepot[["fecha","autoservicio",
                             "marca","nombre","url",
                             "precio_promocion","precio_original"]]
        ## este filtro apenas se agrega

    df_officedepot  =df_officedepot.reset_index(drop=True)

    datos_webscraper=pd.read_excel("df_officedepot.xlsx")

    datos_webscraper= pd.concat([datos_webscraper,df_officedepot],axis=0)

    datos_webscraper.to_excel("df_officedepot.xlsx",index=False)

    driver.quit()
    return df_officedepot

def Buscador_Precios_Selenium_OfficeMax(producto):
    
    ### ingresamos a la pagina web 
    path = "C:\webdriver\chromedriver.exe"
    url = "https://www.officemax.com.mx/"
    ## Creamos el url al que se quiere acceder, 
    ## sólo observando el link base de la página
    productoc = producto.replace(" ","%20")
    url = url+productoc

    ### Accedemos a la página web deseada
    
    driver = webdriver.Chrome(path)
    driver.get(url)   
    
    ####### Accedemos a los elementos que contienen los datos
    ####### que queremos de la pagina web 
    
    productos= driver.find_elements_by_class_name("product-item__info")
    ### accedemos a las urls almacenadas en la variable productos
    
    lista_urls = list()
    ### Obtenemos los URLS de productos    
    for i in range(len(productos)):
        try:
            lista_urls.append(
                productos[i].find_element_by_tag_name(
                    "a").get_attribute("href"))
        except:
            lista_urls.append(np.nan)

    ### accedemos a los nombres de los productos

    lista_nombres = list()
    ### Obtenemos los nombres de productos
    for i in range(len(productos)):
        try:
            lista_nombres.append(productos[i].text.split("\n")[0])
        except:
            lista_nombres.append(np.nan)
            

    ### accedemos a los precios base y promo de los productos 

    lista_precios = list()
    lista_promos = list()

    ### Obtenemos los precios normales y promocionales de productos 
    for i in range(len(productos)):
        lista_precios.append(productos[i].text.split("\n")[1])
        if (len(productos[i].text.split("\n")) == 4):
            lista_promos.append(productos[i].text.split("\n")[2])
        else:        
            lista_promos.append(np.nan)



    df_officemax =pd.DataFrame({"nombre":lista_nombres,"url":lista_urls,
                            "precio_promocion":lista_promos,
                            "precio_original":lista_precios})
    df_officemax["autoservicio"]="Office Max"
    df_officemax["marca"]= producto
    df_officemax["fecha"]= time.strftime("%d/%m/%y")

    df_officemax = df_officemax[["fecha","autoservicio",
                         "marca","nombre","url",
                         "precio_promocion","precio_original"]]
    ## este filtro apenas se agrega


    df_officemax  =df_officemax.reset_index(drop=True)

    datos_webscraper=pd.read_excel("df_officemax.xlsx")

    datos_webscraper= pd.concat([datos_webscraper,df_officemax],axis=0)

    datos_webscraper.to_excel("df_officemax.xlsx",index=False)

    driver.quit()
    return df_officemax

def precios_floats(datos,archivo):

        
    #### eliminamos el signo de pesos de ambas columnas
    
    for i in range(len(datos["precio_promocion"])):
        try:
            datos["precio_promocion"].iloc[i]=datos[
                "precio_promocion"].iloc[i].strip("$")
        except:
            pass
        
    for i in range(len(datos["precio_original"])):
        try:
            datos["precio_original"].iloc[i]=datos[
                "precio_original"].iloc[i].strip("$")
        except:
            pass
        
    
    ### quitamos la separacion de comas para miles
    
    datos["precio_promocion"]=datos[
        "precio_promocion"].replace(",","",regex=True)
    
    datos["precio_original"]=datos[
        "precio_original"].replace(",","",regex=True)
    
     
    
    ### quitamos las letras MXN
    
    datos["precio_promocion"]=datos[
        "precio_promocion"].replace(" MXN","",regex=True)
    
    datos["precio_original"]=datos[
        "precio_original"].replace(" MXN","",regex=True)
    
        
    ### convertimos los precios a numéricos    
    datos['precio_promocion'] = pd.to_numeric(
        datos['precio_promocion'], errors='coerce')
    
    datos['precio_original'] = pd.to_numeric(
        datos['precio_original'], errors='coerce')

    datos.to_excel(archivo,index=False)
        
    return datos

for productos in [
        "crayolas","grapas","borrador", "resaltador", "regla"]:
    Buscador_Precios_Selenium_Lumen(productos)
    Buscador_Precios_Selenium_OfficeDepot(productos)
    Buscador_Precios_Selenium_OfficeMax(productos)
    
    
df_officedepot=pd.read_excel("df_officedepot.xlsx")
df_lumen=pd.read_excel("df_lumen.xlsx")
df_officemax = pd.read_excel("df_officemax.xlsx")


precios_floats(df_lumen, "df_lumen_limpio.xlsx")
df_lumen=pd.read_excel("df_lumen_limpio.xlsx")
df_lumen


precios_floats(df_officedepot, "df_officedepot_limpio.xlsx")
df_officedepot=pd.read_excel("df_officedepot_limpio.xlsx")
df_officedepot

precios_floats(df_officemax, "df_officemax_limpio.xlsx")
df_officemax=pd.read_excel("df_officemax_limpio.xlsx")
df_officemax

df_final= pd.concat([df_lumen, df_officedepot, df_officemax],axis=0, 
                    ignore_index=True, 
                    sort=True, verify_integrity=False )
df_final.to_excel("df_final.xlsx", index = False)
df_final


# GRÁFICA 1. PRECIOS PROMEDIOS
sql1 = ps.sqldf(
    "select marca,avg(precio_original) as \
        preciopromedio from df_final group by marca")
grafica1 = sql1.plot("marca", "preciopromedio",
                     kind="barh", color="red")
plt.title("Precio promedio de cada producto")
plt.ylabel("Productos")
plt.xticks([0,25,50,75,100,125,150,175,200],
           ["$0","$25","$50","$75","$100","$125","$150","$175","$200"])
plt.xlabel("Precio en pesos MXN")
plt.show()


# GRÁFICA 2. PRECIO CRAYOLAS
sql2 = ps.sqldf(
    "select marca, autoservicio, precio_original as 'Precio' \
        from df_final where (marca='crayolas' and precio_original\
                             is not null) order by precio_original")
sql2
colores = []
for i in sql2["autoservicio"]:
    if i =="Lumen":
        colores.append("skyblue")
    elif i =="Office Depot":
        colores.append("orangered")
    elif i == "Office Max":
        colores.append("gold")
        
grafica2 = sql2.plot("autoservicio", "Precio", 
                     kind="barh", color=colores)
plt.title("Precio de 'crayolas' en cada autoservicio")
plt.ylabel("Autoservicio")
plt.xticks([0,50,100,150,200,250],
           ["$0","$50","$100","$150","$200", "$250"])
plt.xlabel("Precio en pesos MXN")
plt.rcParams["figure.figsize"] = (15,15)
plt.show()


# GRÁFICA 3. PRECIO RESALTADORES
sql3 = ps.sqldf(
    "select marca, autoservicio, precio_original as 'Precio' \
        from df_final where (marca='resaltador' and precio_original \
                             is not null) order by precio_original")
sql3
colores = []
for i in sql3["autoservicio"]:
    if i =="Lumen":
        colores.append("cyan")
    elif i =="Office Depot":
        colores.append("magenta")
    elif i == "Office Max":
        colores.append("greenyellow")
grafica3 = sql3.plot("autoservicio", "Precio", 
                     kind="barh", color=colores)
plt.title("Precio de 'resaltador' en cada autoservicio")
plt.ylabel("Autoservicio")
plt.xticks([0,50,100,150,200,250],
           ["$0","$50","$100","$150","$200", "$250"])
plt.xlabel("Precio en pesos MXN")
plt.rcParams["figure.figsize"] = (10,10)
plt.show()

# GRÁFICA 4. PRECIO REGLAS
sql4 = ps.sqldf(
    "select marca, autoservicio, precio_original as 'Precio' \
        from df_final where (marca='regla' and precio_original \
                             is not null) order by precio_original")
sql4
colores = []
for i in sql4["autoservicio"]:
    if i =="Lumen":
        colores.append("lightskyblue")
    elif i =="Office Depot":
        colores.append("peachpuff")
    elif i == "Office Max":
        colores.append("palegreen")
grafica4 = sql4.plot("autoservicio", "Precio", 
                     kind="barh", color=colores)
plt.title("Precio de 'regla' en cada autoservicio")
plt.ylabel("Autoservicio")
plt.xlabel("Precio en pesos MXN")
plt.xticks([0,200,400,600,800,1000],
           ["$0","$200","$400","$600","$800", "$1000"])
plt.rcParams["figure.figsize"] = (10,10)
plt.show()

# GRÁFICA 5. PRECIO BORRADORES
sql5 = ps.sqldf(
    "select marca, autoservicio, precio_original as 'Precio' \
        from df_final where (marca='borrador' and precio_original \
                             is not null) order by precio_original")
sql5
colores = []
for i in sql5["autoservicio"]:
    if i =="Lumen":
        colores.append("slateblue")
    elif i =="Office Depot":
        colores.append("turquoise")
    elif i == "Office Max":
        colores.append("forestgreen")
grafica5 = sql5.plot("autoservicio", "Precio", 
                     kind="barh", color=colores)
plt.title("Precio de 'borrador' en cada autoservicio")
plt.ylabel("Autoservicio")
plt.xlabel("Precio en pesos MXN")
plt.xticks([0,20,40,60,80,100, 120, 140],
           ["$0","$20","$40","$60","$80", "$100", "$120", "$140"])
plt.rcParams["figure.figsize"] = (10,10)
plt.show()

# GRÁFICA 6. PRECIO GRAPAS
sql6 = ps.sqldf(
    "select marca, autoservicio, precio_original as 'Precio' \
        from df_final where (marca='grapas' and precio_original \
                             is not null) order by precio_original")
sql6
colores = []
for i in sql6["autoservicio"]:
    if i =="Lumen":
        colores.append("r")
    elif i =="Office Depot":
        colores.append("lightsalmon")
    elif i == "Office Max":
        colores.append("turquoise")
grafica6 = sql6.plot("autoservicio", "Precio", 
                     kind="barh", color=colores)
plt.title("Precio de 'grapas' en cada autoservicio")
plt.ylabel("Autoservicio")
plt.xlabel("Precio en pesos MXN")
plt.xticks([0,200,400,600,800,1000],
           ["$0","$200","$400","$600","$800", "$1000"])
plt.rcParams["figure.figsize"] = (10,10)
plt.show()

# GRÁFICA 7. CANTIDAD DE ARTÍCULOS
sql7=ps.sqldf(
    "select marca,count(*) \
        from df_final \
            group by marca")
plt.pie(sql7["count(*)"], labels=sql7["marca"], autopct="%0.1f %%")
plt.axis("equal")
plt.title("Porcentaje de productos")
plt.show()

########### CONSULTAS SQL ##########

# 1. Nombre de los productos de mayor precio en Office Max por marca
ps.sqldf(
    "select marca,nombre,MAX(precio_original) as preciomaximo \
        from df_final where (autoservicio='Office Max') group by marca")

# 2. Nombre de los productos de mayor precio en Lumen por marca
ps.sqldf(
    "select marca,nombre,MAX(precio_original) as preciomaximo \
        from df_final where (autoservicio='Lumen') group by marca")

# 3. Los precios originales de los productos de 
#    Lumen que estan entre 50 y 100 pesos
ps.sqldf(
    "select * from df_lumen where precio_original between 50 and 100")

# 4. Los precios originales de los productos de Office Max
#    que estan entre 100 y 300 pesos ordenados de menor a mayor
ps.sqldf(
    "select * from df_officemax where precio_original \
        between 100 and 300 order by precio_original")

# 5. Los precios originales de los productos de Office Depot 
#    que estan entre 50 y 300 pesos ordenados de menor a mayor
ps.sqldf(
    "select * from df_officedepot where precio_original \
        between 50 and 300 order by precio_original")

# 6. Promedio del precio de cada producto
ps.sqldf(
    "select marca,avg(precio_original) as PrecioPromedio \
        from df_final group by marca order by marca")

# 7. Cantidad de artículos por marca
ps.sqldf(
    "select marca,count(*) as CantidadDeArticulosPorMarca \
        from df_final group by marca")

# 8. Productos en los cuales se descuenta $100 o más
ps.sqldf(
    "select marca, nombre,precio_original, precio_promocion \
        from df_final where(precio_original>precio_promocion+100)")

# 9. Productos en los cuales se descuenta 30% o más
ps.sqldf(
    "select marca, nombre, precio_original, precio_promocion \
        from df_final where(precio_promocion<=precio_original*0.7)")

# 10. Cantidad de productos con el 50% o más de descuento
ps.sqldf(
    "select marca,count(*) as CantidadDeProductosPorMarca \
        from df_final where (precio_promocion<=precio_original*0.5) \
            group by marca")

