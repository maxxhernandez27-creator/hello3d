
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, session
)
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = "replace-with-a-long-random-secret-key"

WHATSAPP_NUMBER = "584123997293"


# =====================================
# PRODUCT CATALOG
# =====================================

PRODUCTS = {
    "grinch": {
        "id": "grinch",
        "name": "Grinch Christmas Figure",
        "name_es": "Figura Navideña del Grinch",
        "price": 24.99,
        "image": "images/grinch-christmas.webp.jpeg",
        "description": "Bring some Christmas mischief to your collection with this festive 3D printed Grinch wearing a Santa outfit.",
        "description_es": "Agrega un toque de diversión navideña a tu colección con esta figura del Grinch impresa en 3D.",
        "model": "models/grinch.glb"
    },

    "octopus": {
        "id": "octopus",
        "name": "Articulated Octopus",
        "name_es": "Pulpo Articulado",
        "price": 15.00,
        "image": "images/articulated-octopus.webp.png",
        "description": "A fun articulated octopus with flexible moving legs, 3D printed with care.",
        "description_es": "Un divertido pulpo articulado con patas flexibles y móviles, impreso en 3D con cuidado.",
        "model": "models/articulated-octopus.glb"
    }
}


# =====================================
# TRANSLATIONS
# =====================================

TRANSLATIONS = {
    "en": {
        "home": "Home",
        "shop": "Shop",
        "about": "About",
        "contact": "Contact",
        "welcome": "WELCOME TO HELLO 3D",
        "hero_title": "Ideas Made Real.",
        "hero_text": "Discover unique 3D-printed creations designed to bring creativity, personality, and imagination into everyday life.",
        "explore": "EXPLORE OUR COLLECTION",
        "collection": "OUR COLLECTION",
        "discover": "Discover Our Creations",
        "collection_text": "Explore our collection of unique 3D printed creations.",
        "view_product": "VIEW PRODUCT",
        "view_all": "VIEW ALL PRODUCTS",
        "all_products": "ALL PRODUCTS",
        "all_products_title": "Explore Our Shop",
        "all_products_text": "Discover all our unique 3D printed creations.",
        "price_request": "Price available upon request",
        "story": "OUR STORY",
        "story_title": "Creativity Has No Limits.",
        "story_text": "At Hello 3D, we believe every great creation starts with an idea. We turn imagination into unique 3D-printed products, bringing creative designs to life.",
        "connect": "LET'S CONNECT",
        "idea": "Have an Idea?",
        "contact_text": "Interested in a product or have a custom design in mind? Send us a message. We'd love to hear from you.",
        "your_name": "Your Name",
        "your_email": "Your Email",
        "message_placeholder": "Tell us what you're looking for...",
        "send": "SEND MESSAGE",
        "product_collection": "HELLO 3D COLLECTION",
        "request_item": "REQUEST THIS ITEM",
        "back_collection": "← Back to collection",
        "back_product": "← Back to product",
        "product_request": "Product Request",
        "request_text": "Interested in this product? Send us your questions or request more information.",
        "selected_item": "YOUR SELECTED ITEM",
        "ask_product": "Ask us anything about this product...",
        "send_request": "SEND PRODUCT REQUEST",
        "footer_text": "Turning ideas into creations.",
        "copyright": "All Rights Reserved.",
        "complete_fields": "Please complete all fields.",
        "contact_success": "Thank you! Your idea or question has been received.",
        "product_message": "I am interested in the",
        "more_information": "Please provide more information.",
        "language_label": "Language"
    },

    "es": {
        "home": "Inicio",
        "shop": "Tienda",
        "about": "Nosotros",
        "contact": "Contacto",
        "welcome": "BIENVENIDOS A HELLO 3D",
        "hero_title": "Ideas Hechas Realidad.",
        "hero_text": "Descubre creaciones únicas impresas en 3D, diseñadas para agregar creatividad, personalidad e imaginación a tu vida.",
        "explore": "EXPLORA NUESTRA COLECCIÓN",
        "collection": "NUESTRA COLECCIÓN",
        "discover": "Descubre Nuestras Creaciones",
        "collection_text": "Explora nuestra colección de creaciones únicas impresas en 3D.",
        "view_product": "VER PRODUCTO",
        "view_all": "VER TODOS LOS PRODUCTOS",
        "all_products": "TODOS LOS PRODUCTOS",
        "all_products_title": "Explora Nuestra Tienda",
        "all_products_text": "Descubre todas nuestras creaciones únicas impresas en 3D.",
        "price_request": "Precio disponible a solicitud",
        "story": "NUESTRA HISTORIA",
        "story_title": "La Creatividad No Tiene Límites.",
        "story_text": "En Hello 3D, creemos que cada gran creación comienza con una idea. Transformamos la imaginación en productos únicos impresos en 3D.",
        "connect": "CONECTEMOS",
        "idea": "¿Tienes una Idea?",
        "contact_text": "¿Te interesa algún producto o tienes un diseño personalizado en mente? Envíanos un mensaje.",
        "your_name": "Tu Nombre",
        "your_email": "Tu Correo Electrónico",
        "message_placeholder": "Cuéntanos qué estás buscando...",
        "send": "ENVIAR MENSAJE",
        "product_collection": "COLECCIÓN HELLO 3D",
        "request_item": "SOLICITAR ESTE ARTÍCULO",
        "back_collection": "← Volver a la colección",
        "back_product": "← Volver al producto",
        "product_request": "Solicitud de Producto",
        "request_text": "¿Te interesa este producto? Envíanos tus preguntas o solicita más información.",
        "selected_item": "ARTÍCULO SELECCIONADO",
        "ask_product": "Pregúntanos cualquier cosa sobre este producto...",
        "send_request": "ENVIAR SOLICITUD",
        "footer_text": "Transformando ideas en creaciones.",
        "copyright": "Todos los derechos reservados.",
        "complete_fields": "Por favor, completa todos los campos.",
        "contact_success": "¡Gracias! Hemos recibido tu idea o pregunta.",
        "product_message": "Estoy interesado/a en",
        "more_information": "Por favor, proporciona más información.",
        "language_label": "Idioma"
    }
}


# =====================================
# LANGUAGE MANAGEMENT
# =====================================

@app.context_processor
def inject_language():
    language = session.get("language", "en")

    if language not in TRANSLATIONS:
        language = "en"

    return {
        "lang": language,
        "t": TRANSLATIONS[language]
    }


@app.route("/set-language/<language>")
def set_language(language):
    if language in ("en", "es"):
        session["language"] = language

    next_page = request.args.get("next", "")

    if next_page.startswith("/") and not next_page.startswith("//"):
        return redirect(next_page)

    return redirect(url_for("home"))


# =====================================
# PRODUCT TRANSLATION
# =====================================

def get_product(product):
    product = product.copy()

    if session.get("language", "en") == "es":
        product["name"] = product.get("name_es", product["name"])
        product["description"] = product.get(
            "description_es", product["description"]
        )

    return product


# =====================================
# HOMEPAGE
# =====================================

@app.route("/")
def home():
    featured_ids = ["grinch", "octopus"]

    products = [
        get_product(PRODUCTS[item_id])
        for item_id in featured_ids
    ]

    return render_template(
        "index.html",
        products=products
    )


# =====================================
# COMPLETE SHOP PAGE
# =====================================

@app.route("/shop")
def shop():
    products = [
        get_product(product)
        for product in PRODUCTS.values()
    ]

    return render_template(
        "shop.html",
        products=products
    )


# =====================================
# PRODUCT DETAIL PAGE
# =====================================

@app.route("/product/<product_id>")
def product(product_id):
    selected_product = PRODUCTS.get(product_id)

    if not selected_product:
        return redirect(url_for("shop"))

    return render_template(
        "product.html",
        product=get_product(selected_product)
    )


# =====================================
# GENERAL CONTACT FORM
# =====================================

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    translations = TRANSLATIONS.get(
        session.get("language", "en"),
        TRANSLATIONS["en"]
    )

    if not name or not email or not message:
        flash(translations["complete_fields"])
        return redirect(url_for("home") + "#contact")

    print("NEW HELLO 3D CONTACT")
    print("Customer:", name)
    print("Email:", email)
    print("Message:", message)

    flash(translations["contact_success"])

    return redirect(url_for("home") + "#contact")


# =====================================
# PRODUCT REQUEST + WHATSAPP
# =====================================

@app.route(
    "/product-request/<product_id>",
    methods=["GET", "POST"]
)
def product_request(product_id):
    selected_product = PRODUCTS.get(product_id)

    if not selected_product:
        return redirect(url_for("shop"))

    translations = TRANSLATIONS.get(
        session.get("language", "en"),
        TRANSLATIONS["en"]
    )

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash(translations["complete_fields"])
            return redirect(
                url_for("product_request", product_id=product_id)
            )

        product_price = (
            f"${selected_product['price']:.2f} USD"
            if selected_product["price"] > 0
            else translations["price_request"]
        )

        whatsapp_message = (
            "NEW HELLO 3D ORDER REQUEST\n\n"
            f"Customer: {name}\n"
            f"Email: {email}\n"
            f"Product: {selected_product['name']}\n"
            f"Price: {product_price}\n\n"
            f"Customer Message:\n{message}"
        )

        whatsapp_url = (
            "https://wa.me/"
            + WHATSAPP_NUMBER
            + "?text="
            + quote(whatsapp_message)
        )

        print("NEW HELLO 3D PRODUCT REQUEST")
        print("Customer:", name)
        print("Email:", email)
        print("Product:", selected_product["name"])
        print("Price:", product_price)
        print("Message:", message)

        return redirect(whatsapp_url)

    return render_template(
        "product_request.html",
        selected_product=get_product(selected_product)
    )


# =====================================
# START FLASK
# =====================================

if __name__ == "__main__":
    app.run(debug=True)
