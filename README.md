Multiple Disease Detection Expert System

Multiple Disease Detection Expert System

A Streamlit multi-page app that bundles several lightweight medical screening tools:

- Symptom-based Diagnosis (rule/model-based)
- Malaria Diagnosis (image classifier)
- Diabetes Diagnosis (simple input-based screening)
- Disease Chatbot (document lookup / optional LangChain)

This README explains how to set up, where to place model files, and how to run the app locally for development.

## Project layout (important files)

```
Multiple-Disease-Detection-Expert-System/
├─ Models/                # put model files here (preferred)
├─ main.py                # Streamlit entrypoint
├─ symptom_module.py
├─ malaria_module.py
├─ diabetes_module.py
├─ bot_module.py
├─ medical.txt            # optional: knowledge base for chatbot
├─ requirements.txt
├─ README.md
```

## Quick start (Windows / PowerShell)

1) Create & activate a virtualenv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3) Place your model files in `Models/` (recommended)

The modules look in `Models/` first, then fall back to the project root. Expected names (adjust modules if your files have different names):

- `Models/symptom.sav`  — symptom-based classifier (joblib pickle)
- `Models/MalariaCnn.sav` — malaria image classifier (joblib pickle)
- (Optional) other .sav models used by modules

4) (Optional) Prepare the database used for login/registration

Default DB connection (in `main.py`):

- host: `localhost`
- user: `root`
- password: `` (blank)
- database: `disease`

Create the `user` table and seed a test user:

```sql
CREATE DATABASE IF NOT EXISTS disease;
USE disease;
CREATE TABLE IF NOT EXISTS `user` (
  id INT AUTO_INCREMENT PRIMARY KEY,
  firstname VARCHAR(100),
  lastname VARCHAR(100),
  email VARCHAR(255) UNIQUE,
  gender VARCHAR(20),
  age INT,
  username VARCHAR(100),
  password VARCHAR(128)
);

-- Example insert (hash password with SHA-256 and use the hex string):
-- compute hash in PowerShell: python -c "import hashlib;print(hashlib.sha256(b'password123').hexdigest())"
INSERT INTO `user` (firstname, lastname, email, gender, age, username, password)
VALUES ('Test','User','test@example.com','Other',30,'testuser','<HASH_HEX>');
```

5) Run the app

```powershell
streamlit run main.py
```
