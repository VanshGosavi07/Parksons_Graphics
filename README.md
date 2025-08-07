
# 🏭 Warehouse Inventory Management System

> Streamlining Warehouse Operations — Track Products, Monitor Stock, and Manage Inventory Seamlessly 📦

---

## 📌 Overview

**Warehouse Inventory Management System** is a full-stack Django-based platform that enables real-time product tracking, stock movement monitoring (IN/OUT), and inventory analysis through an intuitive web interface and secure REST APIs.

🚀 Built using **Django**, **DRF**, and **Bootstrap**, the system supports authenticated access, product management, transaction logging, and inventory computation.

---

## 🧠 Core Features

📦 **Product Management** – Add, edit, or delete products with unique SKUs  
🔄 **Stock IN/OUT Transactions** – Record and manage all warehouse movements  
📊 **Real-Time Inventory** – Track current stock levels with validations  
🔐 **User Authentication** – Secure login and registration system  
🧾 **RESTful API Endpoints** – Interact programmatically with the system  
📃 **API Documentation** – Auto-generated Swagger (OpenAPI) docs  
🌐 **Responsive UI** – Clean, mobile-friendly interface built with Bootstrap  
🛡️ **Validation & Security** – Input validation, CSRF protection, and secure session handling  

---

## 🗂️ Folder Structure

```
warehouse_inventory/
├── inventory/                # App containing models, views, serializers
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       ├── register.html
│       ├── products.html
│       └── transactions.html
├── warehouse_inventory/      # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/
│   └── js/
├── requirements.txt          # Python dependencies
├── manage.py
├── vercel.json               # Vercel deployment config
└── README.md                 # Project Documentation
```

---

## 🛠️ Tech Stack

| Layer           | Technology              |
|------------------|--------------------------|
| Backend          | Django 5.0.7, DRF         |
| Frontend         | Django Templates, Bootstrap 5 |
| Database         | SQLite (dev), PostgreSQL (prod) |
| API Docs         | drf-yasg (Swagger/OpenAPI) |
| Hosting          | Vercel / PythonAnywhere  |
| Auth & Security  | Django Auth, CSRF, Validation |

---

## ✅ Prerequisites

- Python 3.10+ 🐍  
- Django 5.x 🦄  
- PostgreSQL or SQLite 💾  
- pip and virtualenv 🔧  

---

## 🔧 Installation & Setup

1. **Clone the Repository**

```bash
git clone https://github.com/VanshGosavi07/warehouse-inventory.git
cd warehouse-inventory
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Apply Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Run the Development Server**

```bash
python manage.py runserver
```

🌍 Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📘 How to Use

1️⃣ **Register/Login** – Secure user access  
2️⃣ **Add Products** – Manage SKUs and item info  
3️⃣ **Create Stock Transactions** – Record IN/OUT movement  
4️⃣ **Track Inventory** – Real-time stock levels computed  
5️⃣ **Use API** – Swagger docs available at `/api/docs/`

---

## 🔌 API Endpoints

| Endpoint               | Method | Description                 |
|------------------------|--------|-----------------------------|
| `/api/products/`       | GET/POST | Manage products            |
| `/api/transactions/`   | GET/POST | Record/view transactions   |
| `/api/inventory/`      | GET     | Current inventory report    |
| `/api/docs/`           | GET     | Swagger documentation       |

---

## 🛡️ Validation & Security

- 🔒 SKU Uniqueness  
- 📉 Stock OUT validation (prevent negative inventory)  
- ✅ Quantity > 0 enforced  
- 🧼 Input sanitization & CSRF protection  
- 🔐 Authenticated access for all features  

---

## 🤝 Contribution Guidelines

We welcome pull requests and contributions!

```bash
# Fork the repository
git checkout -b your-feature
git commit -m "✨ Add feature"
git push origin your-feature
```

Open a **pull request** describing your changes.

---

## 📜 License

This project is licensed under the [MIT License](./LICENSE).  
Free to use, modify, and distribute.

---

## 📬 Contact & Support

- GitHub: [@VanshGosavi07](https://github.com/VanshGosavi07)  
- Email: [vanshgosavi7@gmail.com](mailto:vanshgosavi7@gmail.com)  
- Phone: 📞 +91 9359775740  

---

🚀 **Simplify Warehouse Logistics with the Warehouse Inventory Management System**  
📦🧾📊🔄🔐🌐
