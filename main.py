from flask import Flask, render_template_string, request, redirect, url_for, session
import datetime

app = Flask(__name__)
app.secret_key = 'premium_shop_secret'  # Required for session cart

# --- 1. DATA (PYTHON LISTS & DICTIONARIES) ---
PRODUCTS = [
    {"id": 1, "name": "Gaming Laptop", "price": 1200.00, "stock": 5, "category": "Electronics", "image": "💻", "rating": 4.8},
    {"id": 2, "name": "Wireless Headset", "price": 150.00, "stock": 15, "category": "Audio", "image": "🎧", "rating": 4.5},
    {"id": 3, "name": "Mechanical Keyboard", "price": 80.00, "stock": 20, "category": "Accessories", "image": "⌨️", "rating": 4.7},
    {"id": 4, "name": "Smart Watch", "price": 200.00, "stock": 10, "category": "Wearables", "image": "⌚", "rating": 4.2},
    {"id": 5, "name": "4K Monitor", "price": 350.00, "stock": 8, "category": "Electronics", "image": "🖥️", "rating": 4.6},
    {"id": 6, "name": "Ergonomic Chair", "price": 250.00, "stock": 0, "category": "Furniture", "image": "🪑", "rating": 4.9},
    {"id": 7, "name": "Smartphone", "price": 899.00, "stock": 12, "category": "Electronics", "image": "📱", "rating": 4.8},
    {"id": 8, "name": "Gaming Mouse", "price": 49.99, "stock": 25, "category": "Accessories", "image": "🖱️", "rating": 4.4},
    {"id": 9, "name": "Desk Lamp", "price": 45.00, "stock": 18, "category": "Furniture", "image": "💡", "rating": 4.3},
    {"id": 10, "name": "Bluetooth Speaker", "price": 59.99, "stock": 14, "category": "Audio", "image": "🔊", "rating": 4.5},
]

# --- 2. HTML TEMPLATES (EMBEDDED FOR SINGLE-FILE CONVENIENCE) ---

# Shared Header/Footer & CSS
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyShop Premium</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-gray-50 font-sans text-slate-900 min-h-screen flex flex-col">
    
    <!-- Navbar -->
    <nav class="bg-gradient-to-r from-violet-600 via-indigo-600 to-purple-600 text-white p-4 sticky top-0 z-50 shadow-lg ring-1 ring-white/10">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <a href="/" class="flex items-center gap-2 text-2xl font-bold hover:opacity-90 transition group">
          <div class="bg-white/20 p-2 rounded-lg group-hover:bg-white/30 transition">
            <i data-lucide="store" class="w-6 h-6 text-white"></i>
          </div>
          <span class="tracking-tight">PyShop<span class="text-yellow-300">Online</span></span>
        </a>
        
        <a href="/cart" class="relative bg-white/10 hover:bg-white/20 px-5 py-2.5 rounded-full flex items-center gap-3 transition border border-white/10 backdrop-blur-sm group">
          <i data-lucide="shopping-cart" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>
          <span class="font-bold bg-yellow-400 text-indigo-900 px-2 py-0.5 rounded-full text-sm min-w-[24px] text-center">
            {{ cart_count }}
          </span>
        </a>
      </div>
    </nav>

    <!-- Content -->
    <div class="flex-grow">
        {% block content %}{% endblock %}
    </div>

    <script>
      lucide.createIcons();
    </script>
</body>
</html>
"""

HOME_TEMPLATE = BASE_LAYOUT + """
<div class="max-w-7xl mx-auto p-6">
    <div class="mb-12 text-center relative">
        <div class="absolute top-0 left-1/2 -translate-x-1/2 w-64 h-32 bg-indigo-500/20 blur-3xl rounded-full -z-10"></div>
        <h1 class="text-5xl font-extrabold text-slate-800 mb-4 tracking-tight">
        Discover <span class="text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-pink-600">Premium Gear</span>
        </h1>
        <p class="text-slate-500 text-lg max-w-2xl mx-auto">Powered by Python & Flask.</p>
    </div>

    <!-- Category Filter -->
    <div class="flex flex-wrap justify-center gap-3 mb-12">
        <a href="/" class="px-6 py-2.5 rounded-full text-sm font-bold transition-all duration-300 shadow-sm {% if category == 'All' %}bg-indigo-600 text-white shadow-indigo-200 scale-105{% else %}bg-white text-slate-600 border border-slate-200 hover:border-indigo-200{% endif %}">All</a>
        {% for cat in categories %}
            <a href="/?category={{ cat }}" class="px-6 py-2.5 rounded-full text-sm font-bold transition-all duration-300 shadow-sm {% if category == cat %}bg-indigo-600 text-white shadow-indigo-200 scale-105{% else %}bg-white text-slate-600 border border-slate-200 hover:border-indigo-200{% endif %}">{{ cat }}</a>
        {% endfor %}
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        {% for p in products %}
        <div class="group bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col border border-slate-100 overflow-hidden hover:-translate-y-1">
            <div class="relative h-56 bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-8 group-hover:from-indigo-50 group-hover:to-purple-50 transition-colors duration-500">
                <span class="text-7xl drop-shadow-lg transform group-hover:scale-110 transition-transform duration-300">{{ p.image }}</span>
                {% if p.stock < 5 and p.stock > 0 %}
                   <div class="absolute top-4 right-4 bg-red-100 text-red-600 text-xs font-bold px-3 py-1 rounded-full flex items-center gap-1 shadow-sm animate-pulse">
                     Low Stock
                   </div>
                {% endif %}
            </div>
            
            <div class="p-6 flex-1 flex flex-col">
                <div class="mb-4">
                  <div class="flex justify-between items-start mb-2">
                    <span class="text-xs font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full uppercase tracking-wider">{{ p.category }}</span>
                    <div class="flex items-center gap-1 text-amber-400 text-sm font-bold">
                      ★ {{ p.rating }}
                    </div>
                  </div>
                  <h3 class="text-xl font-bold text-slate-800 leading-tight mb-1 group-hover:text-indigo-600 transition-colors">{{ p.name }}</h3>
                </div>
                
                <div class="mt-auto">
                  <div class="flex justify-between items-end mb-4">
                    <span class="text-2xl font-bold text-slate-900">${{ p.price }}</span>
                     <span class="text-sm font-medium {% if p.stock > 0 %}text-slate-400{% else %}text-red-500{% endif %}">
                      {% if p.stock > 0 %}{{ p.stock }} left{% else %}Out of Stock{% endif %}
                    </span>
                  </div>
                  
                  {% if p.stock > 0 %}
                  <a href="/add/{{ p.id }}" class="block w-full py-3 rounded-xl font-bold text-center bg-slate-900 text-white hover:bg-indigo-600 shadow-lg hover:shadow-indigo-200 active:scale-95 transition-all duration-300">
                    Add to Cart
                  </a>
                  {% else %}
                  <button disabled class="w-full py-3 rounded-xl font-bold bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200">
                    Sold Out
                  </button>
                  {% endif %}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
"""

CART_TEMPLATE = BASE_LAYOUT + """
<div class="max-w-7xl mx-auto p-6">
    <a href="/" class="group flex items-center gap-2 text-slate-500 hover:text-indigo-600 mb-8 transition font-medium">
        <div class="w-8 h-8 rounded-full bg-white shadow-sm flex items-center justify-center border border-slate-200 group-hover:border-indigo-200 transition">
        ←
        </div>
        Continue Shopping
    </a>

    <h2 class="text-3xl font-bold text-slate-800 mb-8 flex items-center gap-3">
        Your Cart
    </h2>

    {% if cart_items|length == 0 %}
    <div class="text-center py-24 bg-white rounded-3xl border border-dashed border-slate-300 shadow-sm max-w-2xl mx-auto">
        <h3 class="text-2xl font-bold text-slate-800 mb-2">Your cart is empty</h3>
        <p class="text-slate-500 mb-8">Looks like you haven't added anything yet.</p>
        <a href="/" class="bg-indigo-600 text-white px-8 py-3 rounded-full font-bold hover:bg-indigo-700 transition shadow-lg shadow-indigo-200">Start Shopping</a>
    </div>
    {% else %}
    <div class="grid lg:grid-cols-3 gap-8">
        <!-- Cart Items -->
        <div class="lg:col-span-2 space-y-4">
            {% for item in cart_items %}
            <div class="bg-white p-6 rounded-2xl border border-slate-100 flex items-center justify-between shadow-sm hover:shadow-md transition">
                <div class="flex items-center gap-6">
                    <div class="w-20 h-20 bg-gradient-to-br from-slate-50 to-slate-100 rounded-xl flex items-center justify-center text-4xl shadow-inner">
                    {{ item.product.image }}
                    </div>
                    <div>
                    <h4 class="font-bold text-lg text-slate-800 mb-1">{{ item.product.name }}</h4>
                    <p class="text-slate-500 text-sm font-medium bg-slate-100 inline-block px-2 py-1 rounded-md">${{ item.product.price }} x {{ item.qty }}</p>
                    </div>
                </div>
                <div class="text-right flex flex-col items-end gap-2">
                    <p class="font-bold text-xl text-indigo-600">${{ item.subtotal }}</p>
                    <a href="/remove/{{ item.product.id }}" class="text-red-400 hover:text-red-600 text-sm font-medium flex items-center gap-1 hover:bg-red-50 px-2 py-1 rounded-lg transition">
                    Remove
                    </a>
                </div>
            </div>
            {% endfor %}
            <div class="flex justify-end pt-4">
                <a href="/clear" class="text-red-500 hover:text-red-700 text-sm font-bold flex items-center gap-2 hover:bg-red-50 px-4 py-2 rounded-lg transition">Clear All Items</a>
            </div>
        </div>

        <!-- Checkout -->
        <div class="lg:col-span-1">
            <div class="bg-white p-8 rounded-3xl border border-indigo-100 shadow-xl shadow-indigo-100 sticky top-24">
                <h3 class="font-bold text-xl mb-6 text-slate-800">Payment Details</h3>
                
                <div class="space-y-4 mb-8">
                    <div class="flex justify-between text-slate-600 font-medium"><span>Subtotal</span><span>${{ total }}</span></div>
                    <div class="flex justify-between text-slate-600 font-medium"><span>Tax (5%)</span><span>${{ tax }}</span></div>
                    <div class="h-px bg-slate-200 my-4"></div>
                    <div class="flex justify-between font-extrabold text-2xl text-slate-900"><span>Total</span><span>${{ grand_total }}</span></div>
                </div>

                <form action="/checkout" method="POST">
                    <div class="mb-6">
                    <label class="block text-sm font-bold text-slate-700 mb-2">Card Number</label>
                    <input type="text" name="card_number" placeholder="1234 5678 1234 5678" class="w-full p-3.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition font-mono" required>
                    <p class="text-xs text-slate-400 mt-2 font-medium">Demo: Enter 16 random digits</p>
                    </div>
                    <button type="submit" class="w-full py-4 rounded-xl font-bold text-lg text-white bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-700 hover:to-violet-700 shadow-lg shadow-indigo-200 transition-all">Pay ${{ grand_total }}</button>
                </form>
            </div>
        </div>
    </div>
    {% endif %}
</div>
"""

INVOICE_TEMPLATE = BASE_LAYOUT + """
<div class="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
    <div class="bg-white max-w-lg w-full p-10 rounded-3xl shadow-2xl border border-white/50 relative overflow-hidden backdrop-blur-xl">
    <div class="absolute top-0 left-0 w-full h-3 bg-gradient-to-r from-emerald-400 to-teal-500"></div>
    
    <div class="text-center mb-10">
        <div class="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm">
        <i data-lucide="check-circle" class="w-10 h-10"></i>
        </div>
        <h2 class="text-3xl font-extrabold text-slate-800 mb-2">Payment Successful!</h2>
        <p class="text-slate-500 font-medium">Order confirmed.</p>
    </div>

    <div class="bg-slate-50 rounded-2xl p-6 mb-8 border border-slate-100">
        <div class="flex justify-between text-sm mb-3"><span class="text-slate-500 font-medium">Order ID</span><span class="font-mono font-bold text-slate-800">#{{ order_id }}</span></div>
        <div class="flex justify-between text-sm mb-3"><span class="text-slate-500 font-medium">Date</span><span class="text-slate-800 font-medium">{{ date }}</span></div>
        <div class="flex justify-between text-sm"><span class="text-slate-500 font-medium">Card</span><span class="text-slate-800 font-medium">**** {{ card_last4 }}</span></div>
    </div>

    <div class="space-y-4 mb-8">
        <h4 class="font-bold text-slate-800 text-sm uppercase tracking-wider border-b border-slate-100 pb-2">Items Purchased</h4>
        {% for item in items %}
        <div class="flex justify-between text-sm items-center">
            <span class="text-slate-600 font-medium">{{ item.qty }} x {{ item.name }}</span>
            <span class="font-bold text-slate-900">${{ item.subtotal }}</span>
        </div>
        {% endfor %}
    </div>

    <div class="flex justify-between items-center bg-indigo-900 text-white p-6 rounded-2xl shadow-lg shadow-indigo-200 mb-8">
        <span class="font-medium text-indigo-200">Total Paid</span>
        <span class="font-bold text-2xl">${{ total }}</span>
    </div>

    <a href="/" class="block w-full text-center bg-white text-slate-900 border-2 border-slate-200 py-3.5 rounded-xl font-bold hover:bg-slate-50 transition">Return to Shop</a>
    </div>
</div>
"""

# --- 3. PYTHON LOGIC (ROUTES) ---

@app.route('/')
def home():
    # Setup Cart in Session if not exists
    if 'cart' not in session:
        session['cart'] = {}
    
    # Calculate cart count for navbar
    cart_count = sum(session['cart'].values())
    
    # Category Filter
    category = request.args.get('category', 'All')
    categories = sorted(list(set(p['category'] for p in PRODUCTS)))
    
    if category == 'All':
        display_products = PRODUCTS
    else:
        display_products = [p for p in PRODUCTS if p['category'] == category]

    return render_template_string(HOME_TEMPLATE, products=display_products, categories=categories, category=category, cart_count=cart_count)

@app.route('/add/<int:pid>')
def add_to_cart(pid):
    if 'cart' not in session:
        session['cart'] = {}
    
    # Python Logic: Add to Dictionary
    cart = session['cart']
    str_id = str(pid) # JSON keys are always strings
    
    product = next((p for p in PRODUCTS if p['id'] == pid), None)
    
    if product and product['stock'] > 0:
        if str_id in cart:
            cart[str_id] += 1
        else:
            cart[str_id] = 1
        
        # Simple Stock Logic (In real app, use DB)
        product['stock'] -= 1
        session.modified = True
        
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    if 'cart' not in session:
        session['cart'] = {}
        
    cart_items = []
    total = 0
    
    for pid, qty in session['cart'].items():
        product = next((p for p in PRODUCTS if p['id'] == int(pid)), None)
        if product:
            subtotal = product['price'] * qty
            total += subtotal
            cart_items.append({'product': product, 'qty': qty, 'subtotal': "{:.2f}".format(subtotal)})
    
    tax = total * 0.05
    grand_total = total + tax
    
    return render_template_string(CART_TEMPLATE, 
                                  cart_items=cart_items, 
                                  total="{:.2f}".format(total),
                                  tax="{:.2f}".format(tax),
                                  grand_total="{:.2f}".format(grand_total),
                                  cart_count=sum(session['cart'].values()))

@app.route('/remove/<int:pid>')
def remove_from_cart(pid):
    str_id = str(pid)
    cart = session['cart']
    
    if str_id in cart:
        qty = cart[str_id]
        # Restore stock
        product = next((p for p in PRODUCTS if p['id'] == pid), None)
        if product:
            product['stock'] += qty
        
        del cart[str_id]
        session.modified = True
        
    return redirect(url_for('view_cart'))

@app.route('/clear')
def clear_cart():
    # Restore all stock logic would go here
    session['cart'] = {}
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    card_number = request.form.get('card_number', '').replace(' ', '')
    
    # 1. Validation Logic in Python
    if len(card_number) != 16 or not card_number.isdigit():
        return "<h1>Invalid Card Number. <a href='/cart'>Try Again</a></h1>"
    
    # 2. Calculate Totals
    total = 0
    items_summary = []
    for pid, qty in session['cart'].items():
        product = next((p for p in PRODUCTS if p['id'] == int(pid)), None)
        if product:
            sub = product['price'] * qty
            total += sub
            items_summary.append({'name': product['name'], 'qty': qty, 'subtotal': sub})
    
    grand_total = "{:.2f}".format(total * 1.05)
    
    # 3. Clear Cart & Show Invoice
    session['cart'] = {}
    
    return render_template_string(INVOICE_TEMPLATE, 
                                  items=items_summary,
                                  total=grand_total,
                                  order_id=str(int(datetime.datetime.now().timestamp())),
                                  date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                  card_last4=card_number[-4:],
                                  cart_count=0)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
