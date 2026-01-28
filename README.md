🏥 Medical Store Management System (Flask)

A role-based Medical Store Management System built using Flask (Python) and MySQL, designed to manage medical stores, medicines, admins, and users efficiently.

🚀 Features
👤 User Roles

•Admin

    • Admin registration & login
    
    •Manage medical stores
    
    •Add / edit / delete medical users
    
    •View all medical stores
    
    •Upload & manage profile photo
    
    •Change password

•Medical Store

    •Medical store registration (by admin)
    
    •Login & profile management
    
    •Add, edit, delete medicines
    
    •Upload & manage store photo
    
    •Change password

•Public User

    •Search medicines by name
    
    •View available medical stores

🛠️ Tech Stack

•Backend: Python, Flask

•Frontend: HTML, Jinja2 Templates

•Database: MySQL

•ORM/DB Driver: PyMySQL

•File Uploads: Werkzeug

•Session Management: Flask Sessions

📂 Project Structure
```
project/
│
├── main.py                  # Main Flask application
├── MyLib.py                 # Database helper functions
├── templates/               # HTML templates
├── static/
│   └── images/              # Uploaded images
├── README.md
└── requirements.txt
```

🧩 Database Tables Used

```
•logindata

•admindata

•medicaldata

•medicinedata

•medical_medicine

•photodata
```

⚠️ Make sure the database name is vgt

⚙️ Installation & Setup
1️⃣ Clone the Repository
```
git clone https://github.com/your-username/medical-store-management.git
cd medical-store-management
```

2️⃣ Install Dependencies
```
pip install flask pymysql
```

3️⃣ Configure MySQL

•Create database:
```
CREATE DATABASE vgt;
```

•Import tables (as per your schema)

•Update DB credentials in main.py if needed:
```
host='localhost'
user='root'
password=''
db='vgt'
```
4️⃣ Run the Application
```
python main.py
```

App will run at:
```
http://127.0.0.1:5000/
```

📸 Image Upload Support

•Admin & Medical store profile photo upload

•Secure filenames

•Stored in:
```
/static/images
```
⚠️ Security Note

This project uses plain SQL queries.
For production:

•Use password hashing

•Use prepared statements

•Add CSRF protection

📌 Future Improvements

•Password hashing (bcrypt)

•REST API support

•Role-based decorators

•Pagination & search filters

•Deployment (Render / Railway / AWS)

🤝 Contributing

Contributions are welcome!
Fork the repo, create a branch, and submit a pull request.

📜 License

This project is for educational purposes.
