// mockData.js : Base de données Master - Authentique Côte d'Ivoire
// Sélection d'images réelles pour un rendu Premium

const ethnies = ["Baoulé", "Sénoufo", "Dan (Yacouba)", "Gouro", "Bété", "Akan", "Dioula"];

const artisans = [
  { 
    id: "a1", 
    name: "Atelier Awa Création", 
    specialty: "Robes et ensembles en Wax", 
    city: "Abidjan (Treichville)", 
    phone: "+225 07 01 02 03 04", 
    category: "Mode & Couture", 
    photo: "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?q=80&w=400", 
    rating: 4.9, 
    bio: "Spécialiste de la couture africaine moderne. Awa travaille les tissus Wax et Pagne Baoulé pour créer des tenues d'exception." 
  },
  { 
    id: "a6", 
    name: "Perles d’Abidjan", 
    specialty: "Bijoux Royaux Akan", 
    city: "Abidjan (Cocody)", 
    phone: "+225 01 11 22 33 44", 
    category: "Bijoux & Accessoires", 
    photo: "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?q=80&w=400", 
    rating: 4.8, 
    bio: "Créatrice de bijoux inspirés des parures traditionnelles des reines Akan. Chaque perle est sélectionnée avec soin." 
  },
  { 
    id: "a11", 
    name: "Sculptures du Nord", 
    specialty: "Masques et Objets d'Art", 
    city: "Korhogo", 
    phone: "+225 05 23 45 67 89", 
    category: "Décoration & Maison", 
    photo: "https://images.unsplash.com/photo-1523438885200-e635ba2c371e?q=80&w=400", 
    rating: 5.0, 
    bio: "Maître sculpteur héritier du savoir-faire Senoufo. Ses masques sont reconnus pour leur finesse et leur authenticité." 
  },
  { 
    id: "a16", 
    name: "Karité & Savane", 
    specialty: "Beurre de Karité & Cosmétique Bio", 
    city: "Boundiali", 
    phone: "+225 07 10 20 30 40", 
    category: "Cosmétique Naturel", 
    photo: "https://images.unsplash.com/photo-1509099836639-18ba1795216d?q=80&w=400", 
    rating: 4.8, 
    bio: "Coopérative de femmes produisant un beurre de karité pur, transformé selon les méthodes ancestrales." 
  },
  { 
    id: "a21", 
    name: "Saveurs du Terroir", 
    specialty: "Produits Agricoles & Attiéké", 
    city: "Grand-Lahou", 
    phone: "+225 01 02 03 04 05", 
    category: "Agriculture Bio", 
    photo: "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?q=80&w=400", 
    rating: 4.7, 
    bio: "Producteur engagé dans l'agriculture biologique. Spécialiste de l'attiéké de qualité premium et des épices locales." 
  }
];

const categoriesConfig = [
  { 
    name: "Mode & Couture", 
    img: "https://images.unsplash.com/photo-1590739225287-bd31519780c3?q=80&w=800", 
    examples: ["Robe de Soirée Wax", "Ensemble Pagne Baoulé", "Tunique Homme Kita", "Jupe Fleurie Wax", "Veste Ethnique"] 
  },
  { 
    name: "Bijoux & Accessoires", 
    img: "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?q=80&w=800", 
    examples: ["Collier Akan en Or", "Bracelet Perles Multicolores", "Boucles d'oreilles Cauri", "Sautoir Traditionnel", "Pochette de Soirée Wax"] 
  },
  { 
    name: "Décoration & Maison", 
    img: "https://images.unsplash.com/photo-1555580399-68df41416868?q=80&w=800", 
    examples: ["Masque Baoulé de collection", "Statue Sénoufo en bois d'ébène", "Poterie de Katiola", "Nappe en Tissu Kita", "Vase Artisanal"] 
  },
  { 
    name: "Cosmétique Naturel", 
    img: "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?q=80&w=800", 
    examples: ["Pot de Beurre de Karité Brut", "Savon Noir aux Huiles", "Huile de Coco Vierge", "Baume à Lèvres Karité", "Masque Argile & Plantes"] 
  },
  { 
    name: "Agriculture Bio", 
    img: "https://images.unsplash.com/photo-1542601906990-b4d3fb773b09?q=80&w=800", 
    examples: ["Attiéké de Grand-Lahou", "Café de Man en Grains", "Cacao de Soubré", "Piment Sec Concassé", "Gingembre Frais Bio"] 
  }
];

const products = [];

categoriesConfig.forEach((cat, cIdx) => {
  // On prend les artisans qui correspondent à la catégorie
  const catArtisans = artisans.filter(a => a.category === cat.name);
  
  for(let i=1; i<=20; i++) {
    const baseName = cat.examples[(i-1) % cat.examples.length];
    const ethnie = ethnies[i % ethnies.length];
    // Si pas d'artisan spécifique, on prend le premier de la liste par défaut
    const artisan = catArtisans[i % catArtisans.length] || artisans[i % artisans.length];
    
    products.push({
      id: `p_${cIdx}_${i}`,
      artisanId: artisan.id,
      name: `${baseName} Authentique`,
      category: cat.name,
      ethnie: ethnie,
      price: 3500 + (Math.floor(Math.random() * 40) * 500),
      image: `${cat.img}&sig=${cIdx}${i}`,
      certified: i % 4 === 0,
      story: `Cette pièce est une création originale de ${artisan.name}. Elle symbolise l'excellence culturelle de la communauté ${ethnie} et le raffinement de l'artisanat de Côte d'Ivoire. En l'achetant, vous soutenez directement l'économie locale.`
    });
  }
});

const mockData = {
  artisans,
  categories: ["Tous", ...categoriesConfig.map(c => c.name)],
  products,
  ethnies: ["Toutes", ...ethnies],
  orders: []
};
