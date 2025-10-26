# 🧠 Multi-modal Misinformation Detector: The Fusion Engine

This is a comprehensive set of instructions for setting up and deploying your **Multi-modal Misinformation Detector** repository on GitHub, focusing on best practices for a Python/Streamlit hackathon project.

Follow these two main steps: **Local Setup** and **GitHub Deployment**.

---

## 🚀 Step 1: Local Setup and File Preparation

Before pushing to GitHub, ensure your project folder is clean and ready.

### 🗂️ 1. Organize Your Project Files

Your project directory (`multi-modal-detector/`) should look something like this:

```
multi-modal-detector/
├── app_web.py          # Main Streamlit application
├── requirements.txt    # List of required Python packages
├── .env                # File to store API Keys (DO NOT push this)
├── README.md           # Project description and setup guide
└── src/                # Core Python logic directory
    ├── main_app.py
    ├── nlp_module/
    │   └── tone_analyzer.py
    └── cv_module/
        └── reverse_search.py
```

### ⚙️ 2. Create `requirements.txt`

This file tells the deployment platform (like Streamlit Cloud or Heroku) exactly which libraries to install.
**Run this command** in your project's terminal to generate it automatically:

```bash
pip freeze > requirements.txt
```

### 🔒 3. Create `.gitignore`

This crucial file prevents sensitive files and unnecessary artifacts from being uploaded to your public repository.
Create a file named **`.gitignore`** in your project root and paste the following content:

```
# Dependency folders
venv/
__pycache__/
*.pyc

# Environment/API Keys (CRITICAL for security)
.env

# Streamlit/System files
.streamlit/
*.log

# Data/Media files (if not needed for deployment)
credibility_db.json
*.jpg
*.mp4
```

### 🧾 4. Create `README.md`

A good `README.md` is vital for the judges. It should clearly explain the setup.

````markdown
# Multi-modal Misinformation Detector: The Fusion Engine

## 🏆 Project Overview
This project is a Multi-modal Misinformation Detector built for the 24 Hour Hackathon. It uses a **Fusion Engine** to analyze Text, Source URL, and Media (Image/Video) simultaneously to provide a unified Credibility Score.

## ✨ Key Features
1. **Visual Context Check:** Uses the **BLIP VQA Model** to detect if media is used out of context.  
2. **Real-Time Security:** Integrates the **Google Safe Browsing API** to flag malicious source URLs.  
3. **Weighted Fusion Logic:** Combines scores from 4 separate modules into a single, comprehensive risk score.

## 🛠️ Setup Instructions (Local)

1. **Clone the Repository:**
    ```bash
    git clone [YOUR_GITHUB_REPO_URL]
    cd multi-modal-detector
    ```

2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use .\venv\Scripts\activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Environment Variables:**
    Create a file named `.env` in the root directory and add your secret API keys (e.g., Google Safe Browsing Key, HuggingFace/BLIP Key, etc.).
    ```
    GOOGLE_SAFE_BROWSING_API_KEY=your_key_here
    HUGGINGFACE_API_KEY=your_key_here
    ```

5. **Run the App:**
    ```bash
    streamlit run app_web.py
    ```
````

---

## 🌐 Step 2: GitHub Repository Setup

### 🧩 1. Initialize Git and Commit

Run these commands inside your **`multi-modal-detector`** project directory:

```bash
# Initialize a Git repository
git init

# Add all tracked files (excluding those in .gitignore)
git add .

# Make the first commit
git commit -m "Initial commit: Set up Multi-modal Fusion Detector structure and README"
```

### 🧭 2. Create a GitHub Repository

1. Go to your GitHub profile and click **“New”** to create a new repository.
2. Name it something clear, like `Multi-Modal-Misinformation-Detector`.
3. Set the repository visibility to **Public** (important for hackathons).
4. Do **NOT** check the boxes to add a README or `.gitignore`, as you already created them locally.
5. Click **“Create repository.”**

### 🔗 3. Link Local Repository to GitHub

GitHub will provide two lines of code to connect your local repository. Run them in your terminal:

```bash
# 1. Link your local repository to the new GitHub remote repository
git remote add origin [YOUR_GITHUB_REPO_URL]

# 2. Push the content of your local 'main' branch to GitHub
git push -u origin main
```

Your code, minus your secret API keys, is now live on GitHub and ready for submission and deployment!
