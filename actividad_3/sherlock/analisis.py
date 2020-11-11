#%%
import os
os.getcwd()
os.chdir("./personal/scripts/cursos/exactas_programa2/actividad_3/sherlock/")

#%%
import re
import itertools
import matplotlib.pyplot as plt
from wordcloud import WordCloud
wordcloud = WordCloud(width=480, height=480, margin=0)

#%%
def separar_texto(texto):
    texto_corregido = []
    texto = texto.replace("\\n", " ")
    texto = texto.replace("\\\\n", " ")
    texto = texto.replace("\\r", " ")
    texto = texto.replace("\\\\r", " ")
    for word in re.findall(r'\S+', texto):
        word = word.lower()
        if len(word) > 1:
            texto_corregido.append( "".join( filter(lambda ch: ch not in " ?.!/;:,\\*#>'_()[]1234567890", word) ) )
    return texto_corregido

#%%
def generar_dic(lista):
    conjunto = set(lista)
    dic = {}
    for elemento in conjunto:
        dic[elemento] = lista.count(elemento)
    return dic

#%%
def generar_dic_filtro(lista, filtro, n):
    conjunto = filter( lambda pal: True if pal not in filtro else False, set(lista) )
    dic = {}
    for elemento in conjunto:
        dic[elemento] = lista.count(elemento)
    if n <= 0:
        return dic
    else:
        return dict( sorted(dic.items(), key=lambda item: item[1])[::-1][:n] )

#%%
def filtrar(texto):
    texto = texto.lower()
    texto = texto[ ( texto.find("abstract") + len("abstract") ): ]
    for final in finales:
        if final in texto:
            texto = texto[ :texto.find(final) ]
    return texto

#%%
def merge_dict(dict1, dict2):
    return(dict1.update(dict2))

#%% palabras clave
stop_words = ["for", "a", "the", "in", "as", "with", "and", "of", "to", "his",
              "was", "is", "that", "he", "she", "had", "which", "there", "not",
              "have", "he", "i", "of", "from", "you", "it", "but", "we", "this",
              "me", "they", "at", "on", "they", "so", "are", "by", "has", "than",
              "those", "these", "be", "or", "may"]

finales = ["acknowledgements", "references"]

#%%
diccionarios = []
i = 1
while i <= 10:
    archivo = "cultevo_"+str(i)+".txt"
    if os.path.exists(archivo):
        f = open(archivo, "r")
        texto = f.read()
        texto = filtrar(texto)
        texto = separar_texto(texto)
        dict_texto = generar_dic_filtro(texto, stop_words, 20)
        diccionarios.append(dict_texto)
    i = i + 1

#%%
i = 0
while i < len(diccionarios):
    cloud = wordcloud.generate_from_frequencies(diccionarios[i])
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)
    archivo = "cultevo_cloud_"+str(i)+".png"
    cloud.to_file(archivo)
    i = i + 1


#%%
diccionario_final = diccionarios[0]
i = 1
while i < len(diccionarios):
    diccionario_final.update(diccionarios[i])
    i = i + 1
diccionario_final = dict( sorted( diccionario_final.items(), key=lambda item: item[1])[::-1][:20] )
#diccionario_final = dict( itertools.islice(diccionario_final.items(), 20) )

#%%
cloud = wordcloud.generate_from_frequencies(diccionario_final)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
cloud.to_file("nube_final.png")
