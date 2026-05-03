# FoodieBot 🍳 — RAG-Based Recipe Recommendation Assistant

> **Week 4 RAG Assignment Project**
> *Turn random ingredients into tasty recipes using Retrieval-Augmented Generation.*

---

## 📖 Project Overview

FoodieBot is a beginner-friendly AI-powered web app that recommends recipes based on the ingredients you have at home. Instead of relying on general AI knowledge, it uses **RAG — Retrieval-Augmented Generation**.

The app loads a custom recipe dataset from local `.txt` files, converts them into vector embeddings, stores them in a FAISS vector database, and retrieves the most relevant recipe chunks when a user enters ingredients. Those retrieved chunks are then sent to the **Gemini API**, which generates a structured recipe answer — grounded only in the provided dataset, not made-up knowledge.

---

## 🎯 Problem Statement

You open your fridge. You see rice, eggs, and onion. You have no idea what to cook.

You could ask a general AI chatbot — but it might suggest a recipe requiring 10 ingredients you don't have, or invent something that doesn't exist in your dataset.

**FoodieBot solves this by:**
1. Only recommending recipes from a curated local dataset you control
2. Retrieving the closest matching recipe from the dataset based on your ingredients
3. Clearly showing which ingredients you already have, which basic items are assumed, and what extra items (if any) you'd need
4. Giving beginner-friendly, step-by-step instructions

---

## ✨ Features

- 🔍 **RAG-powered search** — retrieves relevant recipe chunks before generating any answer
- 🎛️ **Smart filters** — Meal Type, Cuisine, Cooking Time, Difficulty, Spice Level
- 🎲 **Surprise Me!** — randomly picks an ingredient combination for you
- 📋 **Structured recipe cards** — ingredient breakdown, steps, and tips
- 🌟 **"You May Also Like"** — 2 alternative recipe suggestions from the dataset
- 📂 **Dataset Preview tab** — browse the actual recipe `.txt` files used
- 🧠 **About RAG tab** — visual flow diagram explaining the RAG workflow
- ⚠️ **Error handling** — missing API key, unsupported model, empty input, missing files

---

## 🛠️ Tech Stack

| Component | Tool / Library |
|---|---|
| Frontend UI | Streamlit + Custom CSS |
| RAG Framework | LangChain |
| Vector Database | FAISS (local, no server needed) |
| Embeddings | Gemini Embedding API (`models/gemini-embedding-001`) |
| LLM / Generation | Gemini API (`gemini-2.5-flash`) |
| Recipe Dataset | Local `.txt` recipe files in `data/recipes/` |
| Config & Secrets | python-dotenv (`.env` file) |
| Language | Python 3.9+ |

---

## 🧠 How RAG Works

```
1. User enters ingredients (e.g. "rice, egg, onion")
        ↓
2. Ingredients converted into vector embeddings using Gemini Embedding API
        ↓
3. FAISS vector store searched for most similar recipe chunks
        ↓
4. Top-K relevant recipe chunks retrieved from local dataset
        ↓
5. Retrieved context + user ingredients + filters → sent to Gemini LLM
        ↓
6. Gemini generates a structured recipe ONLY from the provided context
        ↓
7. Recipe card displayed in Streamlit UI
```

**Why RAG instead of plain AI?**

| Plain AI Chatbot | FoodieBot with RAG |
|---|---|
| Can hallucinate any recipe | Only uses your local dataset |
| No control over the source | You control exactly what the AI knows |
| May ignore your ingredients | Retrieves based on your actual ingredients |
| Generic, unpredictable answers | Dataset-specific, grounded answers |

---

## 📁 Project Structure

This is the GitHub-safe project structure — only these files should be uploaded:

```
foodiebot-rag/
│
├── app.py                      ← Main Streamlit app + full RAG pipeline
├── requirements.txt            ← All Python dependencies
├── .env.example                ← Template for API key (upload this, NOT .env)
├── .gitignore                  ← Tells Git which files to exclude
├── README.md                   ← This file
│
├── data/
│   └── recipes/
│       ├── breakfast_recipes.txt
│       ├── lunch_recipes.txt
│       ├── dinner_recipes.txt
│       ├── snack_recipes.txt
│       ├── ingredient_substitutes.txt
│       └── quick_2_3_ingredient_recipes.txt
│
└── vectorstore/
    └── .gitkeep                ← Empty placeholder to keep the folder in Git
```

> **Note:** The `vectorstore/faiss_index/` folder — containing `index.faiss` and `index.pkl` — is **automatically created** the first time you run the app. You do not need to create it or upload it to GitHub.

---

## 🔒 GitHub Upload Safety Note

Before pushing to GitHub, make sure your `.gitignore` contains the following:

```gitignore
# Your real API key — never upload this
.env

# Python virtual environment
venv/

# Python cache
__pycache__/
*.pyc
*.pyo

# FAISS index files — auto-created on first run
vectorstore/faiss_index/
*.faiss
*.pkl
```

**Safe to upload:**
`app.py`, `requirements.txt`, `.env.example`, `README.md`, `.gitignore`, `data/recipes/*.txt`, `vectorstore/.gitkeep`

**Never upload:**
`.env`, `venv/`, `__pycache__/`, `vectorstore/faiss_index/`, `index.faiss`, `index.pkl`

Upload `.env.example` (the template with a placeholder key), never the real `.env` file.

---

## ⚙️ Installation (Windows PowerShell)

### Step 1 — Go to your project folder
```powershell
cd path\to\foodiebot-rag
```

### Step 2 — Create a virtual environment
```powershell
python -m venv venv
```

### Step 3 — Activate it
```powershell
venv\Scripts\Activate.ps1
```

> **If you get a script execution error**, run this once first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Step 4 — Install dependencies
```powershell
pip install -r requirements.txt
```

### Step 5 — Set up your API key
```powershell
copy .env.example .env
```
Open `.env` in Notepad and replace `your_api_key_here` with your actual Gemini API key.

**Get your free key at:** https://aistudio.google.com/app/apikey

### Step 6 — Run the app
```powershell
streamlit run app.py
```

> **If `streamlit` is not recognized:**
> ```powershell
> python -m streamlit run app.py
> ```

The app opens automatically at `http://localhost:8501`

---

## 🔑 Environment Variables (`.env`)

```env
GOOGLE_API_KEY=your_actual_key_here
LLM_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=models/gemini-embedding-001
```

All model names are read from `.env` — nothing is hardcoded in `app.py`.

### 🔄 Fallback models (if you get a model error)

```env
# LLM fallbacks
LLM_MODEL=gemini-2.0-flash
LLM_MODEL=gemini-1.5-flash
LLM_MODEL=gemini-1.5-pro

# Embedding fallback
EMBEDDING_MODEL=models/embedding-001
```

---

## 🎮 How to Use

1. **Type your ingredients** in the main input box
   > Example: `rice, egg, onion, soy sauce`

2. **Set optional filters** in the left sidebar:
   - 🍽️ Meal Type: Any / Breakfast / Lunch / Dinner / Snacks
   - 🌍 Cuisine: Any / Indian / Chinese / Italian / Continental
   - ⏱️ Cooking Time: Any / Under 10 / 20 / 30 minutes
   - 🎯 Difficulty: Any / Easy / Medium
   - 🌶️ Spice Level: Any / Mild / Medium / Spicy

3. Click **🔍 Find Recipe** — FoodieBot retrieves the closest matching recipe from the dataset and generates a structured answer

4. Or click **🎲 Surprise Me!** for a random ingredient combination

5. Explore the **Dataset Preview** tab to browse all recipe files

6. Explore the **About RAG** tab to see how the workflow operates

---

## 🤖 AI Prompt Used — Explained

The prompt sent to Gemini is built inside the `build_prompt()` function in `app.py`.

Here is a plain-English explanation of what the prompt tells Gemini:

```
You are FoodieBot 🍳, a friendly recipe assistant for home cooks.

Rules you must follow:
- ONLY use the recipe context retrieved from the dataset below.
  Do NOT invent any recipe from general knowledge.
- Find the best matching recipe based on the user's ingredients and filters.
- If the ingredients only partially match a recipe, suggest the closest one
  and clearly explain what extra items would be needed.
- Assume the user has basic kitchen staples like salt, oil, water, and
  common spices — do not count these as missing or required.
- Keep your tone friendly, warm, and beginner-friendly.
- Return your answer in structured markdown with these sections:
    Recipe Name, Short Description, Why This Matches,
    Ingredients Used From Your Input,
    Assumed Basic Kitchen Items,
    Extra / Optional Ingredients (if helpful),
    Extra Main Ingredients Needed (only if truly required),
    Cooking Time, Difficulty, Meal Type, Cuisine,
    Steps, Tips, You May Also Like.

If no recipe in the retrieved context matches the ingredients at all,
reply only with: NO_MATCH_FOUND
Do not make up a recipe. Just say NO_MATCH_FOUND.
```

**Why this matters for RAG:**
- The rule *"ONLY use the provided context"* is what makes this RAG, not just a chatbot
- Splitting ingredients into three clear categories makes the output more honest and useful
- The `NO_MATCH_FOUND` fallback prevents hallucination when nothing relevant is retrieved
- Assuming basic staples avoids misleading "you're missing salt" type warnings

---

## 📸 Sample Input & Output — 3 Examples

### Example 1 — Egg Fried Rice

**Input:**
```
Ingredients: rice, egg, onion, soy sauce
Filters: Meal Type = Lunch, Cuisine = Chinese
```

**Output:**
```
🍽️ Egg Fried Rice

Short Description: A quick and satisfying Chinese classic, ready in 20 minutes.
Why this matches: You have the core ingredients — this is the closest match in the dataset.

🧂 Ingredients Used From Your Input: rice, egg, onion, soy sauce
🫙 Assumed Basic Kitchen Items: salt, oil, pepper
🌿 Extra / Optional Ingredients: spring onion (garnish)
🛒 Extra Main Ingredients Needed: carrot, capsicum, garlic

⏱️ Cooking Time: 20 minutes    🎯 Difficulty: Easy
🍽️ Meal Type: Lunch            🌍 Cuisine: Chinese

📋 Steps:
1. Use day-old or leftover rice for best results.
2. Heat oil in a wok on high flame. Add minced garlic.
3. Add onion, carrot, and capsicum. Stir fry for 2-3 minutes.
4. Push veggies to side, crack in eggs, and scramble.
5. Mix everything together, add rice and soy sauce. Toss well.
6. Garnish with spring onion. Serve hot.

💡 Tips: Keep the flame high throughout — this gives the rice a proper stir-fried texture.

🌟 You May Also Like:
1. Veg Noodles — similar stir-fry method, uses noodles instead of rice
2. Tomato Rice — a simpler Indian rice dish if you prefer less stir-frying
```

---

### Example 2 — Cheese Egg Sandwich

**Input:**
```
Ingredients: bread, egg, cheese
Filters: Meal Type = Breakfast, Difficulty = Easy
```

**Output:**
```
🍽️ Cheese Egg Sandwich

Short Description: A quick cheesy breakfast sandwich you can make in under 10 minutes.
Why this matches: You have all the main ingredients for this recipe.

🧂 Ingredients Used From Your Input: bread, egg, cheese
🫙 Assumed Basic Kitchen Items: salt, pepper, butter
🌿 Extra / Optional Ingredients: ketchup (for serving)
🛒 Extra Main Ingredients Needed: None — you have everything!

⏱️ Cooking Time: 10 minutes    🎯 Difficulty: Easy
🍽️ Meal Type: Breakfast        🌍 Cuisine: Continental

📋 Steps:
1. Beat eggs with salt and pepper in a bowl.
2. Heat butter in a pan. Pour eggs and scramble on medium flame until just set.
3. Lightly toast bread slices with butter.
4. Place scrambled egg on one slice, add cheese on top.
5. Cover with the second slice, press gently, and serve with ketchup.

💡 Tips: Add a bit of chopped capsicum or tomato to the egg for extra flavour.

🌟 You May Also Like:
1. Bread Omelette — same ingredients, different style
2. Pancake — another easy Continental breakfast option
```

---

### Example 3 — Masala Maggi

**Input:**
```
Ingredients: maggi noodles, tomato
Filters: Meal Type = Dinner, Cooking Time = Under 10 minutes
```

**Output:**
```
🍽️ Masala Maggi

Short Description: The ultimate quick dinner — spicy, comforting, and ready in 10 minutes.
Why this matches: Maggi and tomato are the core of this recipe. The rest are common items.

🧂 Ingredients Used From Your Input: maggi noodles, tomato
🫙 Assumed Basic Kitchen Items: salt, oil, water, chilli flakes
🌿 Extra / Optional Ingredients: egg, peas (great add-ins)
🛒 Extra Main Ingredients Needed: onion (recommended for better flavour)

⏱️ Cooking Time: 10 minutes    🎯 Difficulty: Easy
🍽️ Meal Type: Dinner           🌍 Cuisine: Indian

📋 Steps:
1. Boil 2 cups of water with a pinch of salt.
2. Heat a little oil in a pan. Add chopped tomato and sauté for 1-2 minutes.
3. Add the boiled Maggi noodles and the included masala packet. Mix well.
4. Add chilli flakes and cook for 2 more minutes. Serve hot.

💡 Tips: Adding a chopped onion makes it much more flavourful. Egg is also a great add-in.

🌟 You May Also Like:
1. Veg Noodles — if you want a healthier noodle dish with more vegetables
2. Tomato Soup — lighter option using your tomatoes
```

## 🐛 Common Errors & Fixes

| Error | What It Means | Fix |
|---|---|---|
| `GOOGLE_API_KEY not found` | `.env` file missing or key not filled in | Copy `.env.example` to `.env` and add your key |
| `Model not found` / `404` | Model not available on your account | Change `LLM_MODEL` to `gemini-1.5-flash` in `.env` |
| `No recipe files found` | Recipe `.txt` files missing from `data/recipes/` | Make sure all recipe files are in the correct folder |
| `streamlit not recognized` | Streamlit not in PATH | Use `python -m streamlit run app.py` |
| `FAISS load error` | Corrupted or outdated vectorstore | Delete `vectorstore/faiss_index/` folder and restart |
| `Execution Policy error` | PowerShell blocked the activation script | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |

---

## 🙏 Credits

- **LangChain** — RAG framework connecting retrieval and generation
- **Google Gemini** — LLM for recipe generation + Embedding API for vector search
- **Facebook AI / Meta** — FAISS vector database (free, fast, runs locally)
- **Streamlit** — Python web UI framework
- **python-dotenv** — Clean API key and config management
- Recipe ideas inspired by common Indian and Continental home cooking

---

*Built as a Week 4 RAG Assignment. For learning and educational purposes.*
