// Initialize Lucide Icons
lucide.createIcons();

let cart = [];
let currentCategory = "Tous";
let currentEthnie = "Toutes";
let currentDetailProduct = null;
let currentQty = 1;
let currentPayMethod = "Orange Money";

const categoryIcons = {
  "Tous": "grid",
  "Mode & Couture": "shirt",
  "Bijoux & Accessoires": "gem",
  "Décoration & Maison": "home",
  "Cosmétique Naturel": "droplet",
  "Agriculture Bio": "leaf",
  "Produits Transformés": "package-open",
  "Multi-artisanat": "palette"
};

const paymentMethods = [
  { id: 'orange', name: 'Orange Money', logo: 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Orange_logo.svg' },
  { id: 'wave', name: 'Wave', logo: 'https://wave.com/static/wave-logo-911854ea0134468f7601f224967a14e9.png' },
  { id: 'mtn', name: 'MTN MoMo', logo: 'https://upload.wikimedia.org/wikipedia/commons/a/af/MTN_Logo.svg' }
];

// --- Data Persistence ---
let db = JSON.parse(localStorage.getItem('empreinte_locale_db')) || mockData;

function saveData() {
  localStorage.setItem('empreinte_locale_db', JSON.stringify(db));
}

function resetDatabase() {
  if(!confirm('Attention : cela supprimera tous vos ajouts personnels et restaurera la base de données initiale. Continuer ?')) return;
  localStorage.removeItem('empreinte_locale_db');
  location.reload();
}

function switchView(viewId) {
  document.querySelectorAll('.bottom-nav .nav-item').forEach(btn => btn.classList.remove('active'));
  const navBtn = document.querySelector(`.bottom-nav .nav-item[onclick="switchView('${viewId}')"]`);
  if (navBtn) navBtn.classList.add('active');

  document.querySelectorAll('.view').forEach(view => view.classList.remove('active'));
  const targetView = document.getElementById('view-' + viewId);
  if(targetView) targetView.classList.add('active');

  const floatingBtn = document.getElementById('floating-cart-btn');
  if(floatingBtn) floatingBtn.style.display = (viewId === 'panier') ? 'none' : 'flex';

  if (viewId === 'panier') renderCart();
  if (viewId === 'orders') renderOrders();
  if (viewId === 'admin') renderAdminProducts();
  if (viewId === 'artisans') renderArtisans();
  if (viewId === 'explorer') renderProducts();
}

function toggleMenu() {
  const menu = document.getElementById('dropdown-menu');
  const overlay = document.getElementById('menu-overlay');
  menu.classList.toggle('show');
  overlay.style.display = menu.classList.contains('show') ? 'block' : 'none';
}

function addToCart(id, name, price, image, qty = 1, payMethod = "Orange Money") {
  const existingItem = cart.find(item => item.id === id);
  if (existingItem) {
    existingItem.qty += qty;
  } else {
    cart.push({ id, name, price, image, qty, payMethod });
  }
  updateCartBadge();
  alert(`"${name}" ajouté au panier !`);
}

function updateCartBadge() {
  const total = cart.reduce((sum, item) => sum + item.qty, 0);
  const badge = document.getElementById('notif-badge');
  const cartBtnCount = document.getElementById('floating-cart-count');
  if(badge) {
    badge.innerText = total;
    badge.style.display = total > 0 ? 'flex' : 'none';
  }
  if(cartBtnCount) cartBtnCount.innerText = total;
}

function renderCart() {
  const container = document.getElementById('cart-items');
  const summary = document.getElementById('cart-summary');
  if(!container) return;
  
  container.innerHTML = '';
  let total = 0;

  if (cart.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding: 40px 20px;"><p style="color:var(--text-gray);">Panier vide.</p></div>`;
    if(summary) summary.style.display = 'none';
    document.getElementById('cart-total-price').innerText = '0 FCFA';
    return;
  }

  if(summary) summary.style.display = 'block';

  cart.forEach((item, index) => {
    total += item.price * item.qty;
    const payLogo = paymentMethods.find(m => m.name === item.payMethod)?.logo || '';
    const div = document.createElement('div');
    div.className = 'cart-item';
    div.innerHTML = `
      <img src="${item.image}" style="width:60px; height:60px; border-radius:8px; object-fit:cover;">
      <div style="flex:1; margin-left:15px;">
        <div style="font-weight:700;">${item.name}</div>
        <div style="font-size:12px; color:var(--text-gray);">${item.price.toLocaleString()} F x ${item.qty}</div>
        <div style="display:flex; align-items:center; gap:5px; margin-top:5px;">
          <img src="${payLogo}" style="height:12px;"> <span style="font-size:10px;">${item.payMethod}</span>
        </div>
      </div>
      <button onclick="removeFromCart(${index})" style="background:none; border:none; color:var(--red);"><i data-lucide="trash-2" size="18"></i></button>
    `;
    container.appendChild(div);
  });
  document.getElementById('cart-total-price').innerText = `${total.toLocaleString()} FCFA`;
  lucide.createIcons();
}

function removeFromCart(index) {
  cart.splice(index, 1);
  updateCartBadge();
  renderCart();
}

function checkout() {
  if (cart.length === 0) return;
  const orderId = 'CMD-' + Math.random().toString(36).substr(2, 6).toUpperCase();
  const order = {
    id: orderId,
    date: new Date().toLocaleDateString('fr-FR'),
    items: [...cart],
    total: cart.reduce((sum, item) => sum + (item.price * item.qty), 0),
    status: 'Validée'
  };
  if(!db.orders) db.orders = [];
  db.orders.unshift(order);
  saveData();
  cart = [];
  updateCartBadge();
  alert("Commande validée !");
  switchView('orders');
}

function renderOrders() {
  const container = document.getElementById('orders-list');
  if(!container) return;
  container.innerHTML = '';
  if(!db.orders || db.orders.length === 0) {
    container.innerHTML = '<p style="text-align:center; padding:40px;">Aucune commande.</p>';
    return;
  }
  db.orders.forEach(o => {
    const div = document.createElement('div');
    div.className = 'profile-card-v1';
    div.style.flexDirection = 'column';
    div.innerHTML = `
      <div style="display:flex; justify-content:space-between; width:100%;">
        <span style="font-weight:800;">${o.id}</span>
        <span style="color:var(--accent-color); font-size:12px;">${o.status}</span>
      </div>
      <div style="font-size:11px; color:var(--text-gray); margin:5px 0;">Le ${o.date}</div>
      <div style="display:flex; gap:5px; margin:10px 0;">
        ${o.items.map(it => `<img src="${it.image}" style="width:40px; height:40px; border-radius:4px; object-fit:cover;">`).join('')}
      </div>
      <div style="font-weight:700; width:100%; text-align:right;">Total: ${o.total.toLocaleString()} F</div>
    `;
    container.appendChild(div);
  });
  lucide.createIcons();
}

function openProductModal(productId) {
  const product = db.products.find(p => p.id === productId);
  if(!product) return;
  const artisan = db.artisans.find(a => a.id === product.artisanId);
  currentDetailProduct = product;
  currentQty = 1;
  document.getElementById('detail-img').src = product.image;
  document.getElementById('detail-title').innerText = product.name;
  document.getElementById('detail-price').innerText = `${product.price.toLocaleString()} F`;
  document.getElementById('detail-qty').innerText = currentQty;
  document.getElementById('product-modal').classList.add('show');
}

function closeProductModal() {
  document.getElementById('product-modal').classList.remove('show');
}

function changeQty(n) {
  currentQty += n;
  if(currentQty < 1) currentQty = 1;
  document.getElementById('detail-qty').innerText = currentQty;
}

function selectPayMethod(el) {
  document.querySelectorAll('.pay-btn').forEach(b => b.classList.remove('selected'));
  el.classList.add('selected');
  currentPayMethod = el.innerText;
}

function addDetailToCart() {
  addToCart(currentDetailProduct.id, currentDetailProduct.name, currentDetailProduct.price, currentDetailProduct.image, currentQty, currentPayMethod);
  closeProductModal();
}

function renderProducts(query = "") {
  const container = document.getElementById('product-container');
  if(!container) return;
  container.innerHTML = '';
  
  let filtered = db.products.filter(p => {
    const matchCat = currentCategory === "Tous" || p.category === currentCategory;
    const matchEth = currentEthnie === "Toutes" || p.ethnie === currentEthnie;
    const matchQuery = !query || 
      p.name.toLowerCase().includes(query.toLowerCase()) ||
      p.category.toLowerCase().includes(query.toLowerCase());
    return matchCat && matchEth && matchQuery && p.id !== 'p0';
  });

  const titleEl = document.getElementById('grid-title');
  if(titleEl) titleEl.innerText = query ? `Résultats pour "${query}"` : (currentCategory === "Tous" ? "Tous les articles" : currentCategory);

  if(filtered.length === 0) {
    container.innerHTML = '<p style="grid-column: span 2; text-align:center; padding:40px;">Aucun article trouvé.</p>';
    return;
  }

  filtered.forEach(p => renderProductCard(p, container));
  lucide.createIcons();
}

let currentSpeech = null;

function playAudio(productId) {
  const product = db.products.find(p => p.id === productId);
  if (!product) return;
  const artisan = db.artisans.find(a => a.id === product.artisanId);

  document.getElementById('audio-artisan-img').src = artisan ? artisan.photo : '';
  document.getElementById('audio-artisan-name').innerText = artisan ? artisan.name : 'Artisan Local';
  document.getElementById('audio-story').innerText = product.story || "Cette œuvre est le fruit d'un savoir-faire ancestral transmis de génération en génération.";
  
  const modal = document.getElementById('audio-modal');
  modal.classList.add('show');

  // Animation des barres
  const waves = document.getElementById('audio-waves');
  if(waves) waves.style.display = 'flex';

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    currentSpeech = new SpeechSynthesisUtterance(product.story || document.getElementById('audio-story').innerText);
    currentSpeech.lang = 'fr-FR';
    currentSpeech.rate = 0.9;
    currentSpeech.onend = () => {
      if(waves) waves.style.display = 'none';
    };
    window.speechSynthesis.speak(currentSpeech);
  }
}

function closeAudio() {
  document.getElementById('audio-modal').classList.remove('show');
  if (window.speechSynthesis) window.speechSynthesis.cancel();
}

function renderProductCard(p, container) {

  const div = document.createElement('div');
  div.className = 'product-card';
  div.onclick = () => openProductModal(p.id);
  div.innerHTML = `
    <div class="img-wrapper">
      <img src="${p.image}" loading="lazy" onerror="this.src='https://via.placeholder.com/300x200?text=Image+Indisponible'">
      ${p.certified ? '<div class="badge-authentic"><i data-lucide="shield-check" size="12"></i> Authentique</div>' : ''}
    </div>
    <div class="product-info">
      <div style="flex:1">
        <div class="product-title">${p.name}</div>
        <div class="product-price">${p.price.toLocaleString()} F</div>
      </div>
      <div style="display:flex; gap:5px;">
        <button class="mini-audio-btn" onclick="event.stopPropagation(); playAudio('${p.id}')">
          <i data-lucide="volume-2" size="14"></i>
        </button>
        <button class="add-cart-mini" onclick="event.stopPropagation(); addToCart('${p.id}', '${p.name}', ${p.price}, '${p.image}')">
          <i data-lucide="plus" size="16"></i>
        </button>
      </div>
    </div>

  `;
  container.appendChild(div);
}

function filterByCategory(cat) {
  currentCategory = cat;
  renderCategories();
  renderProducts();
}

function filterProducts() {
  const query = document.getElementById('search-input').value;
  const eth = document.getElementById('ethnie-filter').value;
  currentEthnie = eth;
  renderProducts(query);
}

function renderCategories() {
  const container = document.getElementById('category-container');
  if(!container) return;
  container.innerHTML = '';
  db.categories.forEach(cat => {
    const icon = categoryIcons[cat] || 'box';
    const pill = document.createElement('div');
    pill.className = `category-pill ${currentCategory === cat ? 'active' : ''}`;
    pill.innerHTML = `<i data-lucide="${icon}" size="14"></i> ${cat}`;
    pill.onclick = () => filterByCategory(cat);
    container.appendChild(pill);
  });
  lucide.createIcons();
}

function renderEthniesFilter() {
  const select = document.getElementById('ethnie-filter');
  if(!select) return;
  select.innerHTML = db.ethnies.map(e => `<option value="${e}">${e}</option>`).join('');
}

function renderArtisans() {
  const container = document.getElementById('artisans-container');
  if(!container) return;
  container.innerHTML = '';
  db.artisans.forEach(a => {
    const div = document.createElement('div');
    div.className = 'artisan-card-v1';
    div.innerHTML = `
      <div style="display:flex; gap:15px; align-items:center;">
        <img src="${a.photo}" style="width:70px; height:70px; border-radius:15px; object-fit:cover; border:2px solid var(--accent-color);">
        <div style="flex:1">
          <div style="font-weight:800; font-family:serif; font-size:16px;">${a.name}</div>
          <div style="font-size:12px; color:var(--text-gray);">${a.specialty} • ${a.city}</div>
          <p style="font-size:11px; color:var(--text-dark); margin-top:5px; line-height:1.4;">${a.bio || ''}</p>
          <div style="font-size:11px; color:var(--accent-color); font-weight:700; margin-top:2px;">★ ${a.rating} / 5</div>
        </div>
      </div>

      <div style="margin-top:12px; display:flex; gap:8px;">
        <button class="btn-dark" style="flex:1; font-size:12px;" onclick="window.location.href='tel:${a.phone}'">Contact: ${a.phone}</button>
        <button class="btn-outline" style="flex:1; font-size:12px;" onclick="viewArtisanCatalogue('${a.id}')">Voir Articles</button>
      </div>
    `;
    container.appendChild(div);
  });
  lucide.createIcons();
}

function viewArtisanCatalogue(id) {
  currentCategory = "Tous";
  switchView('explorer');
  const container = document.getElementById('product-container');
  container.innerHTML = '';
  const artisan = db.artisans.find(a => a.id === id);
  const filtered = db.products.filter(p => p.artisanId === id);
  
  const titleEl = document.getElementById('grid-title');
  if(titleEl) titleEl.innerText = `Articles de ${artisan.name}`;

  if(filtered.length === 0) {
    container.innerHTML = '<p style="grid-column: span 2; text-align:center; padding:40px;">Cet artisan n\'a pas encore d\'articles.</p>';
  } else {
    filtered.forEach(p => renderProductCard(p, container));
  }
  lucide.createIcons();
  window.scrollTo({ top: 400, behavior: 'smooth' });
}

// --- ADMIN LOGIC ---
function switchAdminTab(tab) {
  document.querySelectorAll('.admin-tab-content').forEach(c => c.style.display = 'none');
  const targetTab = document.getElementById(`admin-${tab}`);
  if(targetTab) targetTab.style.display = 'block';
  document.querySelectorAll('.admin-tabs button').forEach(b => b.classList.remove('active'));
  if(event) event.target.classList.add('active');
  
  if(tab === 'products') renderAdminProducts();
  if(tab === 'artisans') renderAdminArtisans();
}

function renderAdminProducts() {
  const list = document.getElementById('admin-products-list');
  if(!list) return;
  list.innerHTML = db.products.map(p => `
    <div class="menu-item" style="justify-content:space-between">
      <div style="display:flex; align-items:center; gap:10px;">
        <img src="${p.image}" style="width:35px; height:35px; border-radius:4px; object-fit:cover;">
        <span style="font-size:13px;">${p.name}</span>
      </div>
      <div style="display:flex; gap:5px;">
        <button onclick="openAdminForm('product', '${p.id}')" style="background:none; border:none; color:var(--primary-color)"><i data-lucide="edit-3" size="16"></i></button>
        <button onclick="deleteItem('products', '${p.id}')" style="background:none; border:none; color:var(--red)"><i data-lucide="trash-2" size="16"></i></button>
      </div>
    </div>
  `).join('');
  lucide.createIcons();
}

function renderAdminArtisans() {
  const list = document.getElementById('admin-artisans-list');
  if(!list) return;
  list.innerHTML = db.artisans.map(a => `
    <div class="menu-item" style="justify-content:space-between">
      <div style="display:flex; align-items:center; gap:10px;">
        <img src="${a.photo}" style="width:35px; height:35px; border-radius:4px; object-fit:cover;">
        <span style="font-size:13px;">${a.name}</span>
      </div>
      <div style="display:flex; gap:5px;">
        <button onclick="openAdminForm('artisan', '${a.id}')" style="background:none; border:none; color:var(--primary-color)"><i data-lucide="edit-3" size="16"></i></button>
        <button onclick="deleteItem('artisans', '${a.id}')" style="background:none; border:none; color:var(--red)"><i data-lucide="trash-2" size="16"></i></button>
      </div>
    </div>
  `).join('');
  lucide.createIcons();
}

function deleteItem(type, id) {
  if(!confirm('Supprimer cet élément ?')) return;
  db[type] = db[type].filter(x => x.id !== id);
  saveData();
  if(type === 'products') renderAdminProducts();
  else renderAdminArtisans();
}

function openProfileOption(title, content) {
  const modal = document.getElementById('option-modal');
  const titleEl = document.getElementById('option-title');
  const contentEl = document.getElementById('option-content');
  if(modal && titleEl && contentEl) {
    titleEl.innerText = title;
    contentEl.innerHTML = content;
    modal.classList.add('show');
  }
}

function closeProfileOption() {
  const modal = document.getElementById('option-modal');
  if(modal) modal.classList.remove('show');
}

function openAdminForm(type, id = null) {

  const item = id ? (type === 'product' ? db.products.find(p => p.id === id) : db.artisans.find(a => a.id === id)) : null;
  
  let html = '';
  if(type === 'product') {
    html = `
      <div style="text-align:left;">
        <input type="hidden" id="edit-id" value="${id || ''}">
        <label style="font-size:12px; color:var(--text-gray);">Nom de l'article</label>
        <input type="text" id="adm-name" value="${item ? item.name : ''}" style="width:100%; margin-bottom:10px; padding:10px; border-radius:8px; border:1px solid #ddd;">
        
        <label style="font-size:12px; color:var(--text-gray);">Prix (FCFA)</label>
        <input type="number" id="adm-price" value="${item ? item.price : ''}" style="width:100%; margin-bottom:10px; padding:10px; border-radius:8px; border:1px solid #ddd;">
        
        <label style="font-size:12px; color:var(--text-gray);">Catégorie</label>
        <select id="adm-cat" style="width:100%; margin-bottom:10px; padding:10px; border-radius:8px; border:1px solid #ddd;">
          ${db.categories.map(c=>`<option ${item && item.category === c ? 'selected' : ''}>${c}</option>`).join('')}
        </select>
        
        <label style="font-size:12px; color:var(--text-gray);">Lien Image</label>
        <input type="text" id="adm-img" value="${item ? item.image : ''}" style="width:100%; margin-bottom:10px; padding:10px; border-radius:8px; border:1px solid #ddd;">
        
        <label style="font-size:12px; color:var(--text-gray);">Histoire du produit (Audio)</label>
        <textarea id="adm-story" style="width:100%; height:100px; margin-bottom:15px; padding:10px; border-radius:8px; border:1px solid #ddd; font-family:inherit;">${item ? item.story : ''}</textarea>
        
        <button class="btn-dark" style="width:100%" onclick="saveAdminItem('product')">Enregistrer l'article</button>
      </div>
    `;
  } else {
    html = `
      <div style="text-align:left;">
        <input type="hidden" id="edit-id" value="${id || ''}">
        <label style="font-size:12px; color:var(--text-gray);">Nom de l'artisan</label>
        <input type="text" id="adm-name" value="${item ? item.name : ''}" style="width:100%; margin-bottom:10px; padding:10px; border-radius:8px; border:1px solid #ddd;">
        
        <label style="font-size:12px; color:var(--text-gray);">Spécialité</label>
        <input type="text" id="adm-spec" value="${item ? item.specialty : ''}" style="width:100%; margin-bottom:10px; padding:10px; border-radius:8px; border:1px solid #ddd;">
        
        <label style="font-size:12px; color:var(--text-gray);">Téléphone</label>
        <input type="text" id="adm-phone" value="${item ? item.phone : ''}" style="width:100%; margin-bottom:10px; padding:10px; border-radius:8px; border:1px solid #ddd;">
        
        <label style="font-size:12px; color:var(--text-gray);">Lien Photo</label>
        <input type="text" id="adm-img" value="${item ? item.photo : ''}" style="width:100%; margin-bottom:15px; padding:10px; border-radius:8px; border:1px solid #ddd;">
        
        <button class="btn-dark" style="width:100%" onclick="saveAdminItem('artisan')">Enregistrer l'artisan</button>
      </div>
    `;
  }
  openProfileOption(item ? 'Modifier' : 'Ajouter', html);
}

function saveAdminItem(type) {
  const id = document.getElementById('edit-id').value;
  const name = document.getElementById('adm-name').value;
  const img = document.getElementById('adm-img').value;

  if(type === 'product') {
    const price = parseInt(document.getElementById('adm-price').value);
    const cat = document.getElementById('adm-cat').value;
    const story = document.getElementById('adm-story').value;
    
    if(id) {
      const p = db.products.find(x => x.id === id);
      p.name = name; p.price = price; p.category = cat; p.image = img; p.story = story;
    } else {
      db.products.push({ 
        id: 'p' + Date.now(), 
        name, price, category: cat, image: img, 
        story: story || "Cette pièce unique raconte l'excellence du savoir-faire de nos artisans ivoiriens.",
        certified: true, artisanId: 'a1', ethnie: 'Toutes' 
      });
    }
  } else {
    const spec = document.getElementById('adm-spec').value;
    const phone = document.getElementById('adm-phone').value;
    if(id) {
      const a = db.artisans.find(x => x.id === id);
      a.name = name; a.specialty = spec; a.phone = phone; a.photo = img;
    } else {
      db.artisans.push({ id: 'a' + Date.now(), name, specialty: spec, phone, photo: img, city: 'Abidjan', rating: 5 });
    }
  }
  saveData();
  closeProfileOption();
  alert('Enregistré !');
  if(type === 'product') { renderAdminProducts(); renderProducts(); }
  else { renderAdminArtisans(); renderArtisans(); }
}

// Carousel
let currentSlide = 0;
function renderHeroCarousel() {
  const track = document.getElementById('carousel-track');
  if(!track) return;
  const featured = db.products.filter(p => p.certified).slice(0, 5);
  track.innerHTML = featured.map(p => `
    <div class="carousel-slide" onclick="openProductModal('${p.id}')">
      <img src="${p.image}">
      <div class="slide-content">
        <div class="slide-title">${p.name}</div>
        <div class="slide-price">${p.price.toLocaleString()} F</div>
      </div>
    </div>
  `).join('');
  setInterval(() => {
    currentSlide = (currentSlide + 1) % featured.length;
    track.style.transform = `translateX(-${currentSlide * 100}%)`;
  }, 5000);
}

window.onload = () => {
  renderEthniesFilter();
  renderCategories();
  renderProducts();
  renderArtisans();
  renderHeroCarousel();
  updateCartBadge();
};
