import json
import re

user_products_text = """
1. Tomates Bio d’Abidjan — Tomates fraîches cultivées sans produits chimiques.
2. Piments Nature CI — Piments bio locaux très parfumés.
3. Oignons du Terroir — Oignons naturels cultivés en Côte d’Ivoire.
4. Salade Verte Premium — Laitue bio fraîche et croquante.
5. Carottes Naturelles — Carottes bio riches en vitamines.
6. Aubergines Akan — Aubergines fraîches issues de cultures bio.
7. Concombres Fraîcheur — Concombres naturels sans pesticides.
8. Gombo Vert Bio — Gombo ivoirien frais et tendre.
9. Manioc Nature — Manioc cultivé naturellement.
10. Bananes Plantain Bio — Plantains bio de production locale.
11. Mangues Tropicales Bio — Mangues sucrées naturelles.
12. Papayes Soleil — Papayes bio riches en nutriments.
13. Ananas Premium CI — Ananas bio ivoirien.
14. Avocats Naturels — Avocats frais issus d’agriculture durable.
15. Citrons Verts Bio — Citrons naturels et parfumés.
16. Orange Lagune Bio — Oranges bio juteuses.
17. Gingembre Nature — Gingembre frais cultivé localement.
18. Curcuma Bio Premium — Curcuma naturel ivoirien.
19. Choux Verts Nature — Choux bio frais.
20. Épinards Fraîcheur — Épinards naturels riches en fer.

21. Riz Bio de Bouaké — Riz local cultivé naturellement.
22. Maïs Nature Premium — Maïs bio ivoirien.
23. Igname Royale — Igname bio fraîche.
24. Attiéké Bio Tradition — Attiéké artisanal naturel.
25. Farine de Manioc Nature — Farine bio locale.
26. Patate Douce Bio — Patates douces naturelles.
27. Mil Bio d’Afrique — Mil cultivé sans engrais chimiques.
28. Sorgho Naturel — Sorgho bio traditionnel.
29. Fonio Premium — Fonio ivoirien naturel.
30. Tapioca Bio Maison — Tapioca artisanal bio.

31. Miel Nature d’Akoupé — Miel pur récolté localement.
32. Beurre de Karité Bio — Karité naturel non raffiné.
33. Poudre de Cacao Premium — Cacao bio ivoirien.
34. Café Nature CI — Café bio torréfié artisanalement.
35. Huile de Coco Pure — Huile naturelle pressée à froid.
36. Jus Gingembre Bio — Boisson naturelle artisanale.
37. Confiture Mangue Nature — Confiture bio locale.
38. Chips de Banane Bio — Snacks naturels sans conservateurs.
39. Purée d’Arachide Nature — Pâte d’arachide bio.
40. Thé Tropical Bio — Infusion naturelle ivoirienne.

41. Semences Tomates Bio — Graines naturelles sélectionnées.
42. Semences Piment Nature — Variété locale bio.
43. Compost Nature Premium — Engrais organique naturel.
44. Terreau Bio Jardin — Terre enrichie écologique.
45. Kit Potager Maison — Kit complet pour culture bio.
46. Arrosoir Éco Jardin — Arrosoir pratique pour potager.
47. Pelle Jardin Nature — Outil artisanal de jardinage.
48. Semences Salade Verte — Graines bio potagères.
49. Semences Gombo Nature — Variété ivoirienne naturelle.
50. Kit Agriculture Bio Débutant — Ensemble d’outils pour démarrer un potager bio.

1. Jus de Gingembre Premium — Boisson naturelle énergisante artisanale.
2. Bissap Bio Nature — Jus d’hibiscus rafraîchissant sans conservateur.
3. Jus d’Ananas Tropical — Jus frais d’ananas ivoirien.
4. Cocktail Mangue Passion — Mélange naturel de fruits tropicaux.
5. Jus Baobab Santé — Boisson naturelle riche en vitamines.
6. Jus Citron Gingembre — Jus detox artisanal.
7. Jus Tamarin Nature — Boisson traditionnelle ivoirienne.
8. Smoothie Banane Coco — Smoothie bio onctueux.
9. Jus Papaye Vitalité — Jus frais naturel.
10. Thé Glacé Hibiscus — Boisson bio artisanale.

11. Farine de Manioc Bio — Farine naturelle sans additifs.
12. Farine de Maïs Nature — Farine artisanale locale.
13. Farine d’Igname Premium — Produit naturel ivoirien.
14. Poudre de Cacao Pure — Cacao bio transformé localement.
15. Farine de Banane Verte — Farine nutritive naturelle.
16. Poudre de Gingembre Bio — Épice naturelle artisanale.
17. Farine de Mil Tradition — Farine locale bio.
18. Poudre de Baobab Nature — Complément naturel riche en fibres.
19. Farine de Riz Local — Riz transformé artisanalement.
20. Poudre de Curcuma Bio — Curcuma naturel moulu.

21. Confiture Mangue Soleil — Confiture artisanale ivoirienne.
22. Confiture Ananas Nature — Préparation naturelle sans colorant.
23. Confiture Papaye Bio — Saveur tropicale artisanale.
24. Purée de Tomate Nature — Tomates bio transformées.
25. Sauce Piment Maison — Sauce artisanale ivoirienne.
26. Pâte d’Arachide Premium — Beurre d’arachide naturel.
27. Conserve Gombo Nature — Gombo prêt à cuisiner.
28. Sauce Aubergine Tradition — Sauce locale transformée.
29. Purée de Piment Bio — Piment naturel écrasé.
30. Confiture Coco Vanille — Mélange tropical artisanal.

31. Chips de Banane Plantain — Snacks croustillants naturels.
32. Chips de Manioc Bio — Produit artisanal ivoirien.
33. Noix de Cajou Grillées — Cajou locale premium.
34. Arachides Naturelles Grillées — Snack traditionnel bio.
35. Barres Énergie Tropicales — Snacks naturels aux fruits.
36. Attiéké Déshydraté Premium — Attiéké prêt à préparer.
37. Granola Coco Mangue — Mélange nutritif artisanal.
38. Biscuits Mil Nature — Biscuits bio locaux.
39. Pop-corn Épicé Africain — Snack artisanal moderne.
40. Boules d’Arachide Sucrées — Confiserie traditionnelle ivoirienne.

41. Huile de Coco Pure — Huile naturelle pressée à froid.
42. Huile Rouge Tradition — Huile de palme artisanale.
43. Beurre de Karité Nature — Soin bio multi-usage.
44. Huile d’Arachide Premium — Huile locale naturelle.
45. Huile de Neem Bio — Produit naturel traditionnel.
46. Huile de Baobab Pure — Huile riche en nutriments.
47. Huile de Sésame Nature — Huile artisanale bio.
48. Huile Gingembre Vitalité — Huile naturelle énergisante.
49. Savon Noir Bio — Savon traditionnel transformé localement.
50. Crème Karité Coco — Soin naturel artisanal.
"""

artisans_text = """
### 1. Atelier Awa Création
* Domaine : Mode africaine
* Spécialité : Robes et ensembles en wax
* Localisation : Abidjan
* Expérience : 8 ans
* Description : Créatrice spécialisée dans les tenues modernes inspirées des tissus ivoiriens.

### 2. Kadi Couture
* Domaine : Couture traditionnelle
* Spécialité : Boubous et vêtements sur mesure
* Localisation : Bouaké
* Expérience : 10 ans
* Description : Atelier reconnu pour ses finitions artisanales haut de gamme.

### 3. Wax Prestige CI
* Domaine : Mode urbaine
* Spécialité : Chemises et ensembles wax premium
* Localisation : Yamoussoukro
* Expérience : 6 ans
* Description : Marque ivoirienne mêlant élégance africaine et style moderne.

### 4. Créa Femme CI
* Domaine : Mode féminine
* Spécialité : Robes élégantes et accessoires
* Localisation : San Pedro
* Expérience : 5 ans
* Description : Boutique dédiée à la valorisation de la femme africaine.

### 5. Gold Wax Atelier
* Domaine : Fashion design
* Spécialité : Mode africaine luxe
* Localisation : Abidjan
* Expérience : 7 ans
* Description : Créations premium pour cérémonies et événements.

### 6. Perles d’Abidjan
* Domaine : Bijoux artisanaux
* Spécialité : Bracelets et colliers en perles
* Localisation : Cocody
* Expérience : 6 ans
* Description : Fabrication de bijoux inspirés de la culture Akan.

### 7. Afro Bijoux
* Domaine : Accessoires tendance
* Spécialité : Boucles et bagues artisanales
* Localisation : Treichville
* Expérience : 4 ans
* Description : Bijoux modernes fabriqués à la main.

### 8. Royal Perles CI
* Domaine : Bijoux premium
* Spécialité : Parures africaines haut de gamme
* Localisation : Abidjan
* Expérience : 9 ans
* Description : Artisan spécialisé dans les accessoires de luxe africains.

### 9. N’zassa Style
* Domaine : Accessoires mode
* Spécialité : Sacs et pochettes wax
* Localisation : Grand-Bassam
* Expérience : 5 ans
* Description : Création d’accessoires modernes en tissus africains.

### 10. Artisan Chic Africa
* Domaine : Mode & accessoires
* Spécialité : Sandales artisanales
* Localisation : Daloa
* Expérience : 7 ans
* Description : Production artisanale inspirée du savoir-faire ivoirien.

### 11. Bois Sacré
* Domaine : Sculpture bois
* Spécialité : Masques et sculptures africaines
* Localisation : Korhogo
* Expérience : 12 ans
* Description : Artisan reconnu pour ses œuvres traditionnelles.

### 12. Baoulé Déco
* Domaine : Décoration intérieure
* Spécialité : Objets déco artisanaux
* Localisation : Bouaké
* Expérience : 8 ans
* Description : Création de décoration inspirée de l’art baoulé.

### 13. Maison Ebène
* Domaine : Mobilier artisanal
* Spécialité : Tables et chaises en bois
* Localisation : Man
* Expérience : 11 ans
* Description : Fabrication de meubles modernes en bois local.

### 14. Sculpt’Afrique
* Domaine : Sculpture artistique
* Spécialité : Statues et œuvres décoratives
* Localisation : Yamoussoukro
* Expérience : 9 ans
* Description : Valorisation de l’art africain contemporain.

### 15. Lagune Déco
* Domaine : Décoration moderne
* Spécialité : Lampes et tableaux artisanaux
* Localisation : Abidjan
* Expérience : 5 ans
* Description : Décoration premium inspirée des lagunes ivoiriennes.

### 16. Beauté Nature CI
* Domaine : Cosmétique bio
* Spécialité : Savons naturels et huiles
* Localisation : Abidjan
* Expérience : 6 ans
* Description : Fabrication de soins naturels à base de karité.

### 17. Nature Pure
* Domaine : Produits bio
* Spécialité : Huiles essentielles
* Localisation : Gagnoa
* Expérience : 4 ans
* Description : Produits naturels issus de l’agriculture locale.

### 18. Karité Prestige
* Domaine : Soins corporels
* Spécialité : Beurre de karité premium
* Localisation : Korhogo
* Expérience : 7 ans
* Description : Transformation artisanale de produits naturels.

### 19. Coco Beauty Africa
* Domaine : Beauté naturelle
* Spécialité : Produits à base de coco
* Localisation : San Pedro
* Expérience : 5 ans
* Description : Gamme de soins hydratants artisanaux.

### 20. Gold Nature Cosmetics
* Domaine : Cosmétique artisanale
* Spécialité : Crèmes et savons bio
* Localisation : Abengourou
* Expérience : 8 ans
* Description : Produits naturels sans produits chimiques.

### 21. Terre Bio CI
* Domaine : Agriculture biologique
* Spécialité : Fruits et légumes bio
* Localisation : Divo
* Expérience : 10 ans
* Description : Exploitation agricole écologique ivoirienne.

### 22. Saveurs du Terroir
* Domaine : Produits transformés
* Spécialité : Jus naturels et confitures
* Localisation : Agboville
* Expérience : 6 ans
* Description : Transformation artisanale de fruits locaux.

### 23. Nature Farm Africa
* Domaine : Agriculture durable
* Spécialité : Tubercules et céréales bio
* Localisation : Bouaflé
* Expérience : 9 ans
* Description : Production locale sans pesticides chimiques.

### 24. Coco Délices
* Domaine : Agroalimentaire
* Spécialité : Produits dérivés de coco
* Localisation : Assinie
* Expérience : 5 ans
* Description : Transformation artisanale de coco ivoirien.

### 25. Bio Market CI
* Domaine : Agriculture & bio
* Spécialité : Produits naturels transformés
* Localisation : Yamoussoukro
* Expérience : 7 ans
* Description : Distribution de produits bio ivoiriens.

### 26. Ivoire Création
* Domaine : Multi-artisanat
* Spécialité : Produits artisanaux variés
* Localisation : Abidjan
* Expérience : 8 ans
* Description : Boutique regroupant plusieurs artisans locaux.

### 27. Héritage Africain
* Domaine : Artisanat culturel
* Spécialité : Produits inspirés des traditions africaines
* Localisation : Grand-Bassam
* Expérience : 10 ans
* Description : Valorisation du patrimoine ivoirien.

### 28. Abidjan Handmade
* Domaine : Marketplace artisanale
* Spécialité : Produits faits main
* Localisation : Cocody
* Expérience : 5 ans
* Description : Sélection de créations modernes ivoiriennes.

### 29. Royal Artisan CI
* Domaine : Artisanat premium
* Spécialité : Articles haut de gamme
* Localisation : Marcory
* Expérience : 9 ans
* Description : Produits artisanaux de luxe fabriqués localement.

### 30. Afro Home Market
* Domaine : Concept store africain
* Spécialité : Maison, mode et accessoires
* Localisation : Bingerville
* Expérience : 6 ans
* Description : Espace dédié aux créations africaines contemporaines.
"""

import math
import random

lines = [l.strip() for l in user_products_text.split('\n') if l.strip()]

products = []
idx = 1
for line in lines:
    m = re.match(r'^\d+\.\s*(.*?)\s*[—\-]\s*(.*)$', line)
    if m:
        name = m.group(1).strip()
        desc = m.group(2).strip()
        
        # Decide category based on index
        if 1 <= idx <= 50:
            category = "Agriculture Bio"
        else:
            category = "Produits Transformés"
            
        products.append({
            "name": name,
            "desc": desc,
            "category": category
        })
        idx += 1

artisans = []
a_blocks = artisans_text.split("###")
for block in a_blocks:
    if not block.strip(): continue
    lines_b = [l.strip() for l in block.split('\n') if l.strip()]
    name = lines_b[0].split('.', 1)[1].strip()
    domaine = lines_b[1].split(':', 1)[1].strip()
    spec = lines_b[2].split(':', 1)[1].strip()
    loc = lines_b[3].split(':', 1)[1].strip()
    exp = lines_b[4].split(':', 1)[1].strip()
    desc = lines_b[5].split(':', 1)[1].strip()
    artisans.append({
        "name": name,
        "domaine": domaine,
        "specialty": spec,
        "city": loc,
        "exp": exp,
        "bio": desc
    })

# Add images from original mockData.js (plus default photos)
artisanPhotos = [
  "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1506803682981-6e718a9dd3ee?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1531384441138-2736e62e0919?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1589156280159-27698a70f29e?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1542596594-649edbc13630?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1523825036634-aab3cce05919?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1511556532299-8f662fc26c06?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1507152832244-10d45c7eda57?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1530268729831-4b0b9e170218?auto=format&fit=crop&w=150&q=80"
]

images_agri = [
  "https://images.openai.com/static-rsc-4/Q4r2QAmoL00ex4HGn6O0_q538GY0rLEj1CnC0ZwfOV0Z3tQyjR0Aa7Xt1UPd3wMQORFxVdCyGx2TqAM7ktt2UrAfRudeiot35xZG7cCwSX9AfLLfP0nI_gB-tfFHmeJCQfNTyEcHDaVfOUj31Uq8Z8RrSS-0u16zP-gYPYVyYkL1beGWX9z5FXcPnVrG_qHL?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/mbCUSNHyhYLw3CrqKdorPRKl5m_W80Lb2M260ktDiSk2Ouvk-vwSAvnY5JxHmr7QvBLXpvxcbxRe493nIdoVPFljDhVvZi3aV3kCmAi_wDkAOSaL9hhC9xQ2IzYIEPrNS7wIt1y6AfA4i9uPufdmwe8FEx_sm0HrRCsylf-k1FM5GAcKYBZqJGFI3XG20gxD?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/LhAU1Y7TV3EEJQ9SIeHklrhNtOVyghXWe-0WKwCfT7kVb96KOnbRWvftebFN4_L-gvxCJnb1JAAkV-XW9geSNmaAXfEU3ZkgohwXx0j6OxPOvu1L8XZkxJg8OzB8qo8TT_-8D4EJfAVI4Gabn-6UeCYoM_h6v1boSDD0AusAudajT68AHb__J5OEah2GH5hg?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/L5c_TzWW4Zehulbg-9hrchUUNcoEBil6S4X_nL_6Xnq2dcrOlXL0LSa0rqGcMyVHW4ffniC8ewKsEI7ZXA83wiSpX5ojU-v1txnVgfzZEs2noOPM6TmVWUwJaTjTke_aAv63mgn53OgrVCsnnB7C-deB1ybUmY7XKmVsHiYTMMAEV71hFxlMkbhHy1QAXLdh?purpose=fullsize"
]

images_transf = [
  "https://images.openai.com/static-rsc-4/ZmjHrZXKmOJdKkqbGQuwgkzpvgsdGzY0BkH_T2TWCUxqpqzT6XGColoXXzIN_ntu237r5Gt2jfDUGT2bFlN354B4T2Oy_VEV6oZZUStGv_FaW2nZye96QukQdsK3jByiox0eyg0EQesrXf6AOxEwLDgSPZ-_rcOlYWUGu-N31MrffV7Mt7QEhzOn84RJjTKE?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/b1cFSyFpzTwNUCrgiv0ZHuGCUtxT90uPe2t3CTAlkCKReuclshLeSqJH9QQKR7AkTjEUD0_8AwWolmapDzX3C4T9b_E8tSm5fwy9DUwc-MQF56WlMgYJOs9SJnokbKTzpViacQsn5hi5iuaRejZPQoeimlYKKTpZYFHRrbc2R6Dh_X3S8b2l8cIL16hZkaPL?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/-4M97FKuM93a5N1gQkxQFRPwBzhF6Ql8sA1snTOEKGV0i79w1c1I3l8AKoFNF3DgLu-U6dvuBtwLqFHhbF5Gg2xgoog3_o21V4wpPUfVua4lxn8ucpo2eO3Sto22JcPsL0YYB6QvQ0C2fennP41tg2yW6CTS8hxrGmRTWXDp8VJkpDblgunIH6E2o9vZZ4x9?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/JjZkm2QCWrNxzByz_IZymAXpUx84jszyJsMcRTYBfilttvbvOwlXRn6BAjXDyL-XSu5dzs8W6d4UjunZGpmuRjy7Olp2uXfsDDEqvuGQBWqK_qWshth89g5txTDhk7DhvLPqfJ7OEBCHonaXj_-kaU6Dfc4R0ozzNlItNJSLDG1JWBS_pZKGHgipUWZlJAqm?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/gwWGy9Fnt7Dh-iukf582eFIvdzDrJLtKQMi1-8W_USdxYw2JTsS6z9UXlRw8Ng6K62N_6bM_shna9KN0kjsB10rZhlmI1eywNe01new-w0yv0wJgG4BDLSGGl6ClUmqymOgwc3tvP81pHePwR-JswAuc4ShtrdMaj4-3PqOdjZcTkbtJIUXc_8CLNbv4zfjK?purpose=fullsize"
]

out = """// mockData.js : Base de données générée

const ethnies = ["Toutes", "Baoulé", "Sénoufo", "Dan (Yacouba)", "Gouro", "Bété", "Akan", "Dioula"];
const categoriesList = ["Mode & Couture", "Bijoux & Accessoires", "Décoration & Maison", "Cosmétique Naturel", "Agriculture Bio", "Produits Transformés", "Multi-artisanat"];

const artisans = [];
"""

# write artisans
for i, art in enumerate(artisans):
    img = artisanPhotos[i % len(artisanPhotos)]
    rating = round(random.uniform(4.0, 5.0), 1)
    # determine category based on index
    if i < 5: cat = "Mode & Couture"
    elif i < 10: cat = "Bijoux & Accessoires"
    elif i < 15: cat = "Décoration & Maison"
    elif i < 20: cat = "Cosmétique Naturel"
    elif i < 25: cat = "Agriculture Bio"
    else: cat = "Multi-artisanat"

    out += f"""artisans.push({{
  id: "a{i}",
  name: "{art['name']}",
  photo: "{img}",
  specialty: "{art['specialty']}",
  category: "{cat}",
  city: "{art['city']}",
  exp: "{art['exp']}",
  rating: {rating},
  isPro: true,
  bio: "{art['bio']}"
}});\n"""

out += """
const products = [];
"""

# generate 100 base products for Mode, Bijoux, Deco, Cosmétique, Multi-artisanat (20 each)
out += """
const imgsMode = [
  "https://images.openai.com/static-rsc-4/htk2m17QnCNYWAq9SpwIFPsLgd3S0y7W7aFZt1uBGoWOarU1tX41SvDAqF8_fP3-Z6BAevsO-72uIK3ZJYE4y-6KxN6F-vt4W9jJlSvZeHe_94yS3D4xgpyEPYysv-L_-ASe1HdXjUbzwHDgEOYDzA3XrVaX-iklN6gwTAO9_hHlA7G4i9hlccTzVpu40-nV?purpose=fullsize"
];
const imgsBijoux = [
  "https://images.openai.com/static-rsc-4/eROavXTNoIWFUORHd3CkFZ92S7Xyd4r7wcjGLOtPHDV26544jpnnzTniUiPvtmsC28hdOHw5iu0D72PE0OlFgSGqfU7gAJNDDX9Je5xSdaur_y2TYYqFeQ1dYua4F9yXDJ_3X3VVjAUc3ACJuk4IgymA30SphO-CP2PmDB-A6-C0u86tLFWl4lDz0TcyhDOZ?purpose=fullsize"
];
const imgsDeco = [
  "https://images.openai.com/static-rsc-4/KYDkkXfytqi7i6ChJPeRgoF992QtslNBgYiICziWYi-NLwkyGHpA0SqrwmfwfW2Ctw3aq1lFcXwz-DGglNHvGgdBIE5xWD-A-lFJah9Jwmbk_H5nOXGwqkVxJ3VlndHlbmN48fpSuop4BU3VrwH85LrVDn-LnWfEr7pm6ypbhoZK5oRcDIHXRMD7FUDUEePI?purpose=fullsize"
];
const imgsCosmetique = [
  "https://images.openai.com/static-rsc-4/rIeCxNBp9MDH1Ho3Z5lbWmxyajPlYKA_D56h28Ci8we7bUho0-qN7AAv-tnqQCwxs9ehn2gF_V9XId62xuVi-G3tMzXJEpDMwu-Fsl96xyOtUNToq1GEtVqITRLkXvjMHZQml-b4Jw0vCVi69MWG1e0ExtGidyidGmZ2B8ENkSkCr8en3WKy9ZcUwidb_-yZ?purpose=fullsize"
];
const imgsMulti = [
  "https://images.openai.com/static-rsc-4/NJVAFWiiosNqOJiiDPjjdRHLWJeFn_bC0HQGugcmmqIgKF4HvBj4pd0SIHKWwcCbp63wul6Yo4Dwp_A9aNS7ndU9qV2zz0rDLL6yHNHDGzwhN29SKu19s8bzcQICCKEGqYQdY_3WoAIDjtWNmdYBkfZk4p2CBcyux1R5kVjw5xLaW3FqDpBK5Bz_70mgdcvF?purpose=fullsize"
];

const baseProducts = [
  { name: "Robe en pagne", cat: "Mode & Couture", imgs: imgsMode },
  { name: "Chemise Wax", cat: "Mode & Couture", imgs: imgsMode },
  { name: "Ensemble traditionnel", cat: "Mode & Couture", imgs: imgsMode },
  { name: "Bracelet en perles", cat: "Bijoux & Accessoires", imgs: imgsBijoux },
  { name: "Collier artisanal", cat: "Bijoux & Accessoires", imgs: imgsBijoux },
  { name: "Panier tressé", cat: "Décoration & Maison", imgs: imgsDeco },
  { name: "Objet déco en bois", cat: "Décoration & Maison", imgs: imgsDeco },
  { name: "Savon noir", cat: "Cosmétique Naturel", imgs: imgsCosmetique },
  { name: "Beurre de karité", cat: "Cosmétique Naturel", imgs: imgsCosmetique },
  { name: "Panier cadeau artisanal", cat: "Multi-artisanat", imgs: imgsMulti }
];

for (let i = 1; i <= 100; i++) {
  const base = baseProducts[Math.floor(Math.random() * baseProducts.length)];
  const artisanCatList = artisans.filter(a => a.category === base.cat);
  let artisan = artisans[0];
  if(artisanCatList.length > 0) artisan = artisanCatList[Math.floor(Math.random() * artisanCatList.length)];
  const price = Math.floor(Math.random() * 40 + 5) * 1000;
  
  products.push({
    id: `p_base_${i}`,
    artisanId: artisan.id,
    name: `${base.name} #${i}`,
    category: base.cat,
    ethnie: ethnies[Math.floor(Math.random() * ethnies.length)],
    price: price,
    image: base.imgs[0],
    certified: Math.random() > 0.4,
    story: `Une magnifique création artisanale de la catégorie ${base.cat}.`
  });
}
"""

# generate the new products (1-100)
for i, prod in enumerate(products):
    price = random.randint(2, 20) * 1000
    if prod["category"] == "Agriculture Bio":
        img = images_agri[i % len(images_agri)]
        # Filter artisans for Agriculture Bio (id 20 to 24)
        art_id = f"a{random.randint(20,24)}"
    else:
        img = images_transf[i % len(images_transf)]
        # Filter artisans for Produits Transformés (id 20 to 24 is also for them)
        art_id = f"a{random.randint(20,24)}"
        
    out += f"""products.push({{
  id: "p_new_{i}",
  artisanId: "{art_id}",
  name: "{prod['name']}",
  category: "{prod['category']}",
  ethnie: "Toutes",
  price: {price},
  image: "{img}",
  certified: true,
  story: "{prod['desc']}"
}});\n"""


out += """
// Hero product
products.push({
  id: "p0", artisanId: artisans[0].id, name: "Collection Mode Wax & Pagne", category: "Mode & Couture", ethnie: "Toutes", price: 35000, 
  image: imgsMode[0], certified: true,
  story: "Découvrez notre nouvelle collection de vêtements en Wax. Chaque pièce raconte une histoire de l'art de vivre ivoirien avec des finitions exceptionnelles."
});

const mockData = {
  artisans: artisans,
  products: products,
  categories: ["Tous", ...categoriesList],
  ethnies: ethnies,
  orders: []
};
"""

with open("generate_mock_output.js", "w", encoding="utf-8") as f:
    f.write(out)
