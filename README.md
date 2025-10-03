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

## Development conveniences

- Want to skip login while developing? Set `SKIP_AUTH = True` in `main.py`.
- The chatbot uses `medical.txt` in the project root as its knowledge base.
- Optional packages (LangChain, FAISS) are used only when installed — the bot falls back to a simple text search otherwise.

## Notes about models and compatibility

- If you get errors unpickling models (e.g., ModuleNotFoundError referencing `keras.src...`), that means the model was saved with a different Keras/TensorFlow version. Fixes:
  - Recreate the model in your current environment and re-save, or
  - Install a tensorflow/keras version matching the model's original environment (e.g., `pip install tensorflow==2.11.0`), or
  - Re-save model using `model.save()` (Keras native) and load with `keras.models.load_model()`.

## Moving models into `Models/` (I can do this for you)

If you want, I can move any existing .sav files in the project root into `Models/` and update modules accordingly. Tell me which files to move or confirm and I'll perform the move.

## Troubleshooting

- Missing Lottie/animation files: the symptom module now ignores missing animation files (no crash).
- Missing optional packages: the app provides fallbacks; install optional packages only if you need those features.
- If you hit a runtime error while launching the app, paste the traceback and I'll fix it.

---

If you'd like, I can now:

- Move any existing model files into `Models/` automatically (I can run filesystem commands here), or
- Update all module paths to point to a different centralized models directory of your choosing.
