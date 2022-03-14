#Bibliothèques
import requests
from bs4 import BeautifulSoup
import csv  # Nécessaire pour la rédaction du fichier CSV
import shutil  # to save it locally
import os


# Déclaration de variables
## Listes  de stockage de liens à  parcourir:
"""""Tous les print dans le code sont utilisés pour suivre le déroulement de code"""

category_links = []        ### Liens des catégories
books_links = []           ###Lien des livres
caractericstic_list = []   ### Listes de tout le tableau des paramètres
cat_page = []              ### Liste des pages si elles existent

## Listes de stockage des caractéristiques des livres à stocker:

Books_titles = []          ### Liste des titres des livres
cup_list=[]                ### Liste des UCP
description_list =[]       ### Liste des descriptions des livres
TTC = []                   ### Liste des prix en Toute Taxe Comprise
HT=[]                      ### Liste des Prix en Hors Taxe
image_url = []             ### Liste des liens des images
availability = []          ### Liste de nombre des livres valable en stock
rating_list=[]             ### Liste d'évaluation des libres en étoile de 1-5
category_list = []         ### Liste des catégories

## Retourner au répértoire principal
Directory = os.getcwd()

## Fonction pour changer de répértoir, nécéssaire pour l'hiérarchei de stockage des livres selon le typ des données à enregistrer et la catégorie
def changeDir(newPath):
  if os.path.exists(newPath):
    os.chdir(newPath)
    os.getcwd()
  else:
    print("Directory ", newPath, " not found.")

#Fonction pour télécharger les images des livres
def Image_download(r, filename):
    # Check if the image was retrieved successfully
    # Open a local file with wb ( write binary ) permission.
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            s = shutil.copyfileobj(r.raw, f)
            print('Image sucessfully Downloaded: ', titles)
    else:
        print("Image Couldn't be retreived")

    title = ''.join(char for char in titles if char.isalnum())

    new_title, fext = os.path.splitext(title)

    #if os.path.exists(new_title)==False:
    try:
       os.rename(filename, new_title+'.png')

    except IOError:
        os.rename(filename, new_title + '_2' + '.png')
# Fonction de récupération des url des images et téléchargement
def Récupération_url_image_et_telechargement():
    img = soup2.find('img')
    image = img['src']
    image = image.replace('../..', '')
    image_url.append("https://books.toscrape.com/" + image)
    url_image = r"https://books.toscrape.com" + image
    ## Set up the image URL and filename
    filename = url_image.split("/")[-1]

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(url_image, stream=True)
    Image_download(r, filename)

#Fonction pour création de fichier csv des données récupérées
def CSV_data(category):
    en_tete = ["product_page_url", "universal_ product_code (upc)", 'title', "price_including_tax",
               "price_excluding_tax", "availability", "product_description", "review_rating", 'image_url']
    with open(f'{category}.csv', 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(en_tete)
        for Bl, cup, tit, ttc, ht, av, des, rat, img in zip(books_links, cup_list, Books_titles, TTC, HT, availability,
                                                            description_list, rating_list, image_url):
            writer.writerow([Bl, cup, tit, ttc, ht, av, des, rat, img])

#Fonction pour récuperer les liens de toutes les pages supplémentaires de chaque catégorie
def pagination(category_links):
    cat_page.append(category_links[i])
    for k in range(2, 1000):
        next_page = category_links[i].replace('index.html', f'page-{k}.html')
        next_page = next_page.replace("books_1", "xxxxxx")                 ### Pour éviter le parcours du premier lien comportant les liens de tous les livres, on change la structure de ce dernier pour qu'il ne soit pas conforme au pages des catégories
        request = requests.get(next_page)
        if request.status_code == 200:
            cat_page.append(next_page)
        else:
            break
    print(cat_page)

## Parcourir le site principal et récupération d'une liste comportant les liens de la première page de chaque catégories
URL = 'http://books.toscrape.com/'                                            ### URL principal du site à gratter
global_reponse = requests.get(URL)
if global_reponse.ok:
    page = global_reponse.content
    soup = BeautifulSoup(page, "html.parser")
    li = soup.findAll('li', class_='')
    for l in li:
        a_category = l.find('a')
        link = a_category['href']
        link.replace('books_1',"pagenonvalide")
        category_link = 'http://books.toscrape.com/'+link
        category_links.append('http://books.toscrape.com/'+link)


#Création de fichier principal pour y extraire les données
if not os.path.exists("Sortie"):
    os.makedirs("Sortie")
Directory = os.getcwd()
New_path = Directory+"/Sortie/"

## Parcourir les liens des catégories et récupérer dans une liste intermédiaire provisoire (cat_page) les liens de toutes les pages de chaque catégorie
for i  in range(2,len(category_links)):
    cat_page.clear()
    URL3 = category_links[i]
    pagination(category_links)
                                                ### Je fais un affichage de la liste provisoires de liens des apges juste pour un suivi de bon déroulement de code


    ### On parcourt la premiere page de chaque catégorie pour récupérer la liste des catégories pour pouvoir créer les dossier qui vont contenir les données extraites
    category_reponse = requests.get(URL3)
    if category_reponse.ok:
        page1 = category_reponse.content
        soup1 = BeautifulSoup(page1, 'html.parser')
        category = soup1.find('h1')
        category = category.text
        category = category.replace('<h1>', '')
        category_list.append(category)


    ### On créer le dossier de la catégorie et on se place dans ce dernier pour commencer l'éxtraction des données
    changeDir(New_path)
    if not os.path.exists(category):
        os.makedirs(category)
    changeDir(f'{New_path}{category}')

    ### On crée un sous dossier nommé "Image" pour séparer entre le fichier csv à créer et les images dse livres
    if not os.path.exists("Images"):
        os.makedirs("Images")
    ### Boucle pour parcourir chaque page d'une catégorie et récupérer en parallèle les liens des livres dans chaque page
    for k in cat_page:
        print(k)
        page_reponse = requests.get(k)
        pages = page_reponse.content
        soup8 = BeautifulSoup(pages, 'html.parser')
        products = soup8.findAll('article')
    ### Bouble pour parcourir chaque lien de livre et récupére les données demandées
        for ar in products:
            a_article = ar.find('a')
            article = a_article['href']
            article = article.replace('../../../','')
            books_links.append('http://books.toscrape.com/catalogue/'+ article)
            s = 'http://books.toscrape.com/catalogue/'+ article
            title_reponse = requests.get(s)
            if title_reponse.ok:
                page2 = title_reponse.content
                soup2 = BeautifulSoup(page2, 'html.parser')
            #### Titres
                titles = soup2.find('h1')
                titles = titles.string
                Books_titles.append(titles)

            #### Description
                desc = soup2.find('p', class_='')
                if desc != None:
                    desc = desc.text
                else:
                    desc= ''
                description_list.append(desc)

            #### Evaluation
                star_rat= soup2.find("p",class_='star-rating')
                star = star_rat["class"]
                if star[1] == "1":
                    star[1] = "Une_Etoile"
                elif star[1] == 'Two':
                    star[1] = "2"
                elif star[1] == 'Three':
                    star[1] = "3"
                elif star[1] == 'Four':
                    star[1] = "4"
                elif star[1] == 'Five':
                    star[1] = "5"
                rating_list.append(star[1])
                print(titles)
            #### Récupération des caractéristiques structurée en tabulation
                caract = soup2.findAll('tr')
                for c in caract:
                    cup = c.find('td')
                    cup=cup.text
                    cup=cup.replace('In stock (','')
                    cup = cup.replace(' available)','')
                    caractericstic_list.append(cup)
            #### Stockages des information extraites de la tabulation récupérée

                for j in range(0,len(caractericstic_list),7):     #### CUP
                     cup_list.append(caractericstic_list[j])
                for j in range(3,len(caractericstic_list),7):     #### Prix en TTC
                     TTC.append(caractericstic_list[j])
                for j in range(2, len(caractericstic_list),7):    #### Prix en HT
                     HT.append(caractericstic_list[j])
                for j in range(5,len(caractericstic_list),7):     #### Disponibilité
                     availability.append(caractericstic_list[j])
                caractericstic_list.clear()
            #### Téléchargement des images dans un sous dossier nommé 'Images'
                changeDir(f'{New_path}{category}/Images')
                Récupération_url_image_et_telechargement()

        #### Revenir dans le dossier catégorie et créer le fichier csv contenant les données
            changeDir(f'{New_path}{category}')
            CSV_data(category)