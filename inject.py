import json
import re

items_text = """
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

images_jus = [
  "https://images.openai.com/static-rsc-4/ZmjHrZXKmOJdKkqbGQuwgkzpvgsdGzY0BkH_T2TWCUxqpqzT6XGColoXXzIN_ntu237r5Gt2jfDUGT2bFlN354B4T2Oy_VEV6oZZUStGv_FaW2nZye96QukQdsK3jByiox0eyg0EQesrXf6AOxEwLDgSPZ-_rcOlYWUGu-N31MrffV7Mt7QEhzOn84RJjTKE?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/RW0Q8uT5_y3jX0iWjj2su41ISyY73w600XWqhOFKHBAQdvbl6_NITYbPHFV-rJgbQUUlKtZw5Z-4Nj4N5beDdPJpm2n95dMNRah-7o1LL8O5QZcwlrnuIlTBIzXmXAPi_p3LUGJoWUnZi2UQVFPLoffz2zleGq1Y_nIkXhVBccCCWspxCwplc4_NHnoAyT-o?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/BrklqyQposZk7DcK6Xry0HwseAlDU_XX7k-_Oxi374Viof9BZcXgkUq7UCf0aXC4o_3-o7RzLID0v5rqoc6_RUP9VoDDZluua4G7lLnxOY6wcGjThRyoFf384mLSz0d5pRvYPnhLWKuyird5u04IPiGRp3cNcws4KSESvzULSkn0Mksqwv6JtWs7YnCZ39kA?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/YZYDH4ozV4qtJAdWhc86eRlea0b3KAHEQADPgMNiVY53MusSgwi4efHxrPbomi0XtvtjNW1Q59NAuKUnuFfW7y_fVQMC5HwoaYXBmCxabdDn85PYSN5tu3fjkSS5gZkEzqXNWL0pSkpBUla4Ao1LqNcJgOOJquC8I8g90DFGocEgJ0w9XkDShr2E3x4euazl?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/OAOhDssFyjBPCEZifZ_7yKXOwEpVO5IaculsHT0gyqm4L92wOMWJ82yYLOSpTbbiWpTspnYXwTp7mjPSZTD5rFV8LfHUQb9j4spD9BWRt9woqpYFnX847_nL94C2KoF9EWJAx9kq8zlbH94fjiCcd_GOEH5H_BwAM49aH_fk3qPSo_ZgDZKZVgsREgKpXt7M?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/9zkaSmVZlIqm78L_OAhhazEDFLVMBlKiPV1Ph3omNJcCbJcTmjj6bKOvt3_vYC9LwRKJB_J_w6q9F0Put9KwMvP60olu_RsoDsK7NkUPcG_RlMw_Sd0uiTRkx_OcxJTONdTHrDB-oXGjyDUTBSi-qO3m0gaRsUqR2uFLZucRW100jh-2dAhJs_63kliuaf7s?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/RkJWtZgWgw4-KX-Uh5Cg6MnLWm7xhHiIMEMItPyp-_J6_ZwXFF2nX9CxEyrn202r51pCY5H6jl6zVaPMQck7vd8IF12dZldLlB5fiyZzHSCrIIf-3VDKTtgo-ul4x9ixqL1MLguE6rCY3gXzT1TeXXL0z9fof7Cbzk9ntDreVijnEXZNibRs2VTUSZgXXcR4?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/STciDEGyPB-6TaSWn6f_P9hYlYzWSu4ZQRKY-Uvh_M3zA4yVPTjKL54F7TdP6mExTLJwHjS_dECmqxBEReq-JEa-c3jrLy25EvpRIf7KA_cD6TZOwhH6rhV6Cby1dvhZj0D99GAerArzn_VZY8MUpKgCu-dfWTMt8bieisr9U5o2puVQiqog0t1WUVPA_IVG?purpose=fullsize"
]

images_farines = [
  "https://images.openai.com/static-rsc-4/b1cFSyFpzTwNUCrgiv0ZHuGCUtxT90uPe2t3CTAlkCKReuclshLeSqJH9QQKR7AkTjEUD0_8AwWolmapDzX3C4T9b_E8tSm5fwy9DUwc-MQF56WlMgYJOs9SJnokbKTzpViacQsn5hi5iuaRejZPQoeimlYKKTpZYFHRrbc2R6Dh_X3S8b2l8cIL16hZkaPL?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/xqR3zszONGc_jvgpY02VHjanC5HULhS0xjmj2kaSrEjbMuqdKRd_BLMzieM8HMHeeiSpdY-QDo9P8VOOc4ndJkLXevhpRPdqtuLf7tv2RcdjY5U_wHAqU1sAQqCBRUeXdcu1ZROS5QuZOoGb9nq9jBJ0LLwwT-4hkcYmKVc5zuW3MclFS_dW1Kw8OWpMHbMy?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/1sYkZnXBIxTIC6w-m8dAk3Dw08QBujyzSwDR66QC6SoPd-2bUgJji1aUZmlo7iVOL8Qi_HA0UER_0xsEjYw0yE_vcM4h6L0sLW9GqXYzp-ZqLp3i_CbwY0cFY7GH3Po4sv9MvU36-HkJ9WZiiUBAZJMyd6I9leTcTCbxE1ejKxkLW4edsfIJD5PdTlL_1x2l?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/OwQtqnllf2q-vaQuj24-0iw_NcsbF7ZgwN2PpsFPNqOal4YYZfFOYmmz-M07l4xnaOaD-TYJ5Rv7sN5h3XLWD1R8gyU0ONwBjd6Vlnps_v3nJyOPozYi0nC89ahLGuW_yhIa-_EjY7A_Wk37N-iM0a4WKSujG8OnH-FLa6P6v3ADDof20O3dG57fub-ylWmh?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/wm958bGiGyno-gXfhLbIEoNmIPaL3YAnIZdrgQAYb8fNpSaZu70vjWjz3LGQ6qtSTCvLPWnTkXGqU-1M8MuLLHDL7ELY56Y0CAPUGXdp2Zlo5QvThJeuqL1Wmc9whcQhBYCdAicRo_cWROSGqdhqddDwoOOQSpMUq-Rmq6X6uE3zfwonmaaxdBYyrX8wY8Zt?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/5H2xkG8IL-ELZjgK01lt8af8d6OfIffsgv9zleeDLKTsd-CSmCLRfE14NaDZa_sKepR7rRyHcgp91uajbbNQ-TbjbbIBxiEnG72Zuiy4meKw7BoJSJyPN4fSx1xK9nA64yr7QSXN7bH1FyXITNFmneN6_4BaR7k2msmguorpD7WFgJC035HmGXxHb2xQ1Z6l?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/FrUxbf182poIhQf5KwYS5_0e0uVXIHQORR7Lld7Qocz9fNjNzEj3jIuYxY75zVKbPy5Py-o5KxRT62jI52PQWK4AnbjCnVSIE6Sj6I-_OIhKoaQh0Ge5EZzDz-HV7YFZqxkO6uU1jM1GsDmHoL7_S66QuD5r32CTFuWG91ZH1WfBP_bEPkQ_Q5xNAaGvmzZD?purpose=fullsize"
]

images_conserves = [
  "https://images.openai.com/static-rsc-4/-4M97FKuM93a5N1gQkxQFRPwBzhF6Ql8sA1snTOEKGV0i79w1c1I3l8AKoFNF3DgLu-U6dvuBtwLqFHhbF5Gg2xgoog3_o21V4wpPUfVua4lxn8ucpo2eO3Sto22JcPsL0YYB6QvQ0C2fennP41tg2yW6CTS8hxrGmRTWXDp8VJkpDblgunIH6E2o9vZZ4x9?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/tVa5PBilsbB_geMJYzW-i6FUh3TcWP_KF6AVCBQwOA8xy1vcgy2_ewLDXeiKFAF-SKRjamQPfZNZZKdV0rp_f0bkZ74xd8dSmUcRlnJ_z50scyzLSp2MKjILuUa5tQzTa-pwnkwgDJyXcqZljb0--3K825xuF4Uri3aTLLuIJ4kgW_w2QNIN24OWE8TU9UMV?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/jGUipbbSWbVMW5LyMAdXQSNeZ_HUMwo8Woth4YcBOTu_gJsP1hVksQp1k4CXz1BDrmsz4q3fvCzTgiw1PKFmLpu4kVh1ORynxLRGH2elJEYOywRzaai5Npu2g_Msp6eX6CK3UxMcBM9F8_pVosRLKPylK0EKQTo5kuknFutIH-jRZDa60b_h1O7VaoUTfY3M?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/diJ5SKKdkC2Hzfw7OOd3PYxAeAyj2cJXfSItKpHC40Mc9jfRXeT70XeTZp1EG9P5z-w49oUNF_hp9hPuJt2qWSaA-QiQN9Uwz-BDozkS4aKDSMLR0_AOTLXUGOgZX80zlhenG8ewv3rjLnhbpgoTL2E19l9EMNay9UWEOqwtFwPXJ1pvrjFDMIT6vOq7sgm9?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/7O9DtBDtmtUVFkoKT39nhv_05peu5-kAzG0FJL6pu9X_SoPRzQ697ntfW-RoOPTHwCIxlpbriivU8Y1C3nuxnhu1rbtUMk31itPY0Ka5NlQhk4nLxUp7mdD3aNlbIpBRN28dgHJKI0cBZ3N4Q1oD_vn4H0vbkRfaL_4hJEnrRXKqloq_ddex51_VWFBPckWZ?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/PpsaqJC_aAQhP1Lt1-JuoxA54s08D5rRgyuVtaW6xywCyRGvoG0ME1BaDx-WaRYW9FxhsFofm5Uhklghi1u0dLPP2RKOVMUEkw1lOfzuKRTsF06wiYG0NCdR6f8ai1aSmOQlQkxjc0HI9btwMu_kbeTo9VA79pAtNPY99elOdlQcnLwiHDefRrFsex2SAX9Q?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/5tj8vzihsNSXkMKeM2Q2_1i0T7V-ypelu_yJqtsLlGBbbV--iqBgO3aV5SihYyDAYb2KgnZuTs-v5jb7niwfjNsoXk-ZMEHJBjMnoXy1LcsVlZbZUG1IsBFw8E3PeOs02XCW8FgzD5kZhrVmsIZSZjX6MUPKIkIX0joqPocWaTDsPYkttceuB18xNjZBOwgx?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/z8b54MRIurf5_O1ULfkh4BZMbo3gJpDIxBtLI5EIMgySmG1e2EJoJ6oTwuu79oEOjyASCViXQa9ZkxMUEztD0OlEN-JMQRpDhLfD8SUh17zCiEqbhPYmOHeQLP4xe_sfBh-tWJVCkH0Zk217ya_I-4uMwJh6qqmU4mmv7ZdJA_Glz0vGCokNWVi2OQSiWWg9?purpose=fullsize"
]

images_snacks = [
  "https://images.openai.com/static-rsc-4/JjZkm2QCWrNxzByz_IZymAXpUx84jszyJsMcRTYBfilttvbvOwlXRn6BAjXDyL-XSu5dzs8W6d4UjunZGpmuRjy7Olp2uXfsDDEqvuGQBWqK_qWshth89g5txTDhk7DhvLPqfJ7OEBCHonaXj_-kaU6Dfc4R0ozzNlItNJSLDG1JWBS_pZKGHgipUWZlJAqm?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/ch77pgHcmj1zRg54TOcAYpzL66yvAOzTc5kfwjwapZikk1rMiROh8dAzd6JwGkYfJgphQ9uxuGDZh-m_ryprYkb6ydxje4TUtz3NOKf88q5x9Vv9G4a7SAD1LaBfMFv8T8XczHklzl_tReessHy3luTzHmnMY5CWGuJOfN1Zr5paPj1X8PTejXOp9wKjjefN?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/eJIwXk9rm7VCmrXIgt2EogaFg7dDowC2NbHLT9gR1JgJ8DBJ3GG0jHzuOuYojfJL88LqhRlq2haELUmYOAhgAoaPADOD6uExkdY4ZnvhHUhusVtKMI_CpS7imd19QGLA4nAoYJwtoxBALH25jjp6-LIrkJC9-s_2xatVEuseM6yn1bUmjnfXe1C88Su5AK_4?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/Xs0QCLGH_MFUQrfoGTFTlvokilqp79PJJ92Q1F5CevAdqbeMzMvS0dHoqFeLeRsKmmTqBNbvQKZnvyyUsdIflcl2UHmOCZsQri1YHwZHN9XWUKHKw_dBoM0wVPhnDwDNJCkwrbkyrhiww2UNz1253C_ctIEHp1Q9LmchGdrVnXTVNMOZBwJR6CIQx0EdjrdB?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/ZBZP0Gl0BauZpDWXlIuV1RJWmyuvbZO0wLA3-jKTKrHRq5RrvRmJ_tzIt4D6QRA6XbwllFdRgpe82DcAw9Il7Gwv3eFT9_p2HNSfmynza0PUn7yOXEAFj5UXT9Fb4LOwXtgCzlEE3W6meT_O_geTexORvEp7j9WFy5nGev45hprwhsgn97kJ83AeSAZChRec?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/w_htOtUWse6jGr0nDZ3_F5KF7Qj6baz_IFmunZ8MPm9TEjp1oRlY4yxvTJ25Q6XlISqUTKzo-ecCQb_lDUQg449M4ArDfT-IB62Xenmgz2K69GGocEE-tRDJ66hsPXtjdVGKCp0WIU1bhGz_1p6reMprZ-b58MBYwa5aI7Rkf8VWdC_-pS5DybpdmFi5-2XY?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/IKd4iGe42HddrJq4JLZc4i--AORt14gV4JEp9vzZuAsPk16SmvyKi8dz_I7Iu5tWOg7TTRifs2K2vON8coQNBrPRrOLK1Twp8BpBSNTtnb7PVS_sM-2xWaiAu7S4Bj7KZ7ba1zDOj3DU65yhqF42Wf1b_ELv9IY4lw7IAbblRPabavTYdtganzTTHbP5S8zi?purpose=fullsize"
]

images_huiles = [
  "https://images.openai.com/static-rsc-4/gwWGy9Fnt7Dh-iukf582eFIvdzDrJLtKQMi1-8W_USdxYw2JTsS6z9UXlRw8Ng6K62N_6bM_shna9KN0kjsB10rZhlmI1eywNe01new-w0yv0wJgG4BDLSGGl6ClUmqymOgwc3tvP81pHePwR-JswAuc4ShtrdMaj4-3PqOdjZcTkbtJIUXc_8CLNbv4zfjK?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/4p48igJUHy3IbWC9igCe9Y9_DqEwlT0qLx_Z82IG5tSIP3nXe80SjGwj9NoylGkOTQuRcdxBgEpf7ZoA9J4KtUI_pSdlB-flan3BZr-R2IOKSrPYJyeS-yi1AYg4I5JoznrY_SB2Zu061i_HV7hhJ-qjI5WVtRj5MsIzBY7TUWr2l5QuM6X-TVJAphl16L6u?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/GBDCG3BSKKraAMcP3UbzUvfRj8vwzfDGshBCJs2FpPKpstK4iaC3sTRZ0CFsHT3P-10AioL8EsKzsyVjaL_bHTULwjnkhMq3a2YjY_MHiq3y_O49Z7ZHxpgz4KmYN_t4yjiMwlY1Oba-bouE2QT6V0GW4kN4x1T07rqoR9U1krxztEAd38t_JqW4idn6UqDl?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/9-mb8RlEZKwnu7fXZPKh_rrYRUjwC3uyCTLn65rtuXl0kpJmTW2AM5BR1IzXwCtsfIKegWJyrwTi-GW9b1vUxCAz_BON_u1gFw5Vjok72jjxti28DIz6gz4EQGWx8FxZgcvz19FYWRAMRYxEgDNoZvzLOQoIUcQKDopYemgH-r7homoPNzu_JJSsxJz-5-Sn?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/eOhBjYzfF7OVDyNmmQw9g7yA-YcmaTH-Us-MFHlC7ogbkKEK0eYu1F0g0Z3Evcw-0vJSqEq7mchkMsAgaJQAVm2Ywsh6XkLwNX1GhcSkX0e7TdGF6G3pbzcN2LcbVZRpSxc9u9cdQMBh1W_mrUTlXfxiKr28zQbx03dKSXOsfCBRL9O9Jc3vIcI_-iyVerqw?purpose=fullsize",
  "https://images.openai.com/static-rsc-4/fptYPIU0Em4kcQc-CRtpv53IUjeLW8V9xEj_C4cO_Fk-4t2w2rF3k18feslZTHcL09CVP9CNAWscLpgFVlHz-yRdxs4N-j0t2QPXPdE7XAyU9X9nCDl1mLmuaXH5nlS3lrxhgp6028ybnAeFDHvsffum-qcwOSDzPuC1KBjWLdEken6ZlOjpdNya_UqdY3Xt?purpose=fullsize"
]

import math

lines = [l.strip() for l in items_text.split('\\n') if l.strip()]
js_items = []

for line in lines:
    m = re.match(r'^(\\d+)\\.\\s*(.*?)\\s*[—\\-]\\s*(.*)$', line)
    if m:
        idx = int(m.group(1))
        name = m.group(2).strip()
        desc = m.group(3).strip()
        
        if idx <= 10:
            imgs = "imgsJus"
        elif idx <= 20:
            imgs = "imgsFarines"
        elif idx <= 30:
            imgs = "imgsConserves"
        elif idx <= 40:
            imgs = "imgsSnacks"
        elif idx <= 50:
            imgs = "imgsHuiles"
            
        js_items.append(f'  {{ name: "{name}", cat: "Produits Transformés", eth: "Toutes", pMin: 5, pMax: 20, imgs: {imgs} }}')

with open('mockData.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add images variables right before baseProducts
imgs_declaration = f"""
const imgsJus = {json.dumps(images_jus, indent=2)};
const imgsFarines = {json.dumps(images_farines, indent=2)};
const imgsConserves = {json.dumps(images_conserves, indent=2)};
const imgsSnacks = {json.dumps(images_snacks, indent=2)};
const imgsHuiles = {json.dumps(images_huiles, indent=2)};

const baseProducts = [
"""

content = content.replace("const baseProducts = [\\n", imgs_declaration)

# Inject the new base products
js_items_str = ",\\n".join(js_items) + ",\\n"
content = content.replace("const baseProducts = [\\n", "const baseProducts = [\\n" + js_items_str)

with open('mockData.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
