# FoodieBot 🍳 — RAG-Based Recipe Recommendation Assistant

> **Week 4 RAG Assignment Project**  
> *Turn random ingredients into tasty recipes using Retrieval-Augmented Generation.*

---

## 📖 Project Overview

FoodieBot is a beginner-friendly, visually polished web app that recommends recipes based on ingredients you have at home. It uses **RAG (Retrieval-Augmented Generation)** to first search a custom recipe dataset, then generates a structured, helpful recipe using the **Gemini API** — all without making things up from general AI knowledge.

---

## 🎯 Problem Statement

When you open your fridge and see random ingredients, you often don't know what to cook. Generic AI chatbots might hallucinate recipes or suggest things that need ingredients you don't have. FoodieBot solves this by:

1. Only recommending from a curated recipe dataset (your own data)
2. Showing you exactly which ingredients match and which are missing
3. Providing step-by-step beginner-friendly instructions

---

## ✨ Features

- 🔍 **RAG-powered search** — retrieves relevant recipe chunks before generating an answer
- 🎛️ **Smart filters** — Meal type, Cuisine, Cooking time, Difficulty, Spice level
- 🎲 **Surprise Me** — randomly selects ingredient combinations
- 📋 **Structured recipe cards** — Name, description, matched/missing ingredients, steps, tips
- 🌟 **"You May Also Like"** — 2 alternative recipe suggestions
- 📂 **Dataset Preview** tab — browse the actual recipe files
- 🧠 **About RAG** tab — explains the full workflow with visual flow diagram
- ⚠️ **Error handling** — missing key, unsupported model, empty input, missing files

---

## 🛠️ Tools & Tech Stack

| Component | Tool |
|---|---|
| Frontend | Streamlit + Custom CSS |
| RAG Framework | LangChain |
| Vector Database | FAISS (local, no server needed) |
| Embeddings | Gemini Embedding API |
| LLM / Answer Generation | Gemini (Flash / Pro) |
| Dataset | Local `.txt` files in `data/recipes/` |
| Config / Secrets | python-dotenv (`.env` file) |
| Language | Python 3.9+ |

---

## 🧠 How RAG Works

```
User enters ingredients
        ↓
Ingredients converted to vector embeddings (Gemini Embedding API)
        ↓
FAISS vector store searched for similar recipe chunks
        ↓
Top-K most relevant recipe text chunks retrieved
        ↓
Retrieved context + user query + filters → sent to Gemini LLM
        ↓
Gemini generates a structured recipe ONLY from provided context
        ↓
Beautiful recipe card displayed in Streamlit UI
```

**Why RAG instead of plain AI?**
- The AI can ONLY answer from our recipe dataset
- No hallucination of random recipes
- Results are grounded, reliable, and dataset-specific
- Matches the ingredients you actually have

---

## 📁 Project Structure

```
foodiebot-rag/
│
├── app.py                      ← Main Streamlit app + RAG pipeline
├── requirements.txt            ← Python dependencies
├── .env.example                ← Template for environment variables
├── README.md                   ← This file
│
├── data/
│   └── recipes/
│       ├── breakfast_recipes.txt   (5 recipes)
│       ├── lunch_recipes.txt       (5 recipes)
│       ├── dinner_recipes.txt      (5 recipes)
│       ├── snack_recipes.txt       (5 recipes)
│       └── ingredient_substitutes.txt
│
└── vectorstore/
    └── faiss_index/            ← Auto-created on first run
        ├── index.faiss
        └── index.pkl
```

---

## ⚙️ Installation (Windows PowerShell)

### Step 1: Clone or download the project
```powershell
cd path\to\your\projects
```

### Step 2: Create and activate virtual environment
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

> **If you get a script execution error**, run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Step 3: Install dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Set up your API key
```powershell
copy .env.example .env
```
Then open `.env` in Notepad and replace `your_api_key_here` with your actual key.

**Get your free Gemini API key at:** https://aistudio.google.com/app/apikey

### Step 5: Run the app
```powershell
streamlit run app.py
```

> **If streamlit is not recognized:**
> ```powershell
> python -m streamlit run app.py
> ```

---

## 🔑 Environment Variables (`.env`)

```env
GOOGLE_API_KEY=your_actual_key_here
LLM_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=models/gemini-embedding-001
```

### 🔄 Fallback Models (if primary fails)

If `gemini-2.5-flash` gives an error, try:
```env
LLM_MODEL=gemini-2.0-flash
# or
LLM_MODEL=gemini-1.5-flash
# or
LLM_MODEL=gemini-1.5-pro
```

If `gemini-embedding-001` fails, try:
```env
EMBEDDING_MODEL=models/embedding-001
```

---

## 🎮 How to Use

1. **Enter ingredients** you have at home in the text box  
   Example: `rice, egg, onion, soy sauce`

2. **Set filters** in the sidebar (optional):
   - Meal Type: Breakfast / Lunch / Dinner / Snacks
   - Cuisine: Indian / Chinese / Italian / Continental
   - Cooking Time: Under 10 / 20 / 30 minutes
   - Difficulty: Easy / Medium
   - Spice Level: Mild / Medium / Spicy

3. Click **🔍 Find Recipe** to get your recommendation

4. Or click **🎲 Surprise Me!** for a random ingredient combo

---

## 📸 Sample Input & Output

**Input:**
```
Ingredients: rice, egg, onion, carrot, soy sauce
Filters: Meal Type = Lunch, Cuisine = Chinese
```

**Output (from Gemini, grounded in dataset):**
```
🍽️ Egg Fried Rice

Short Description: A quick and satisfying Chinese classic!
Why this matches: You have almost all the ingredients for this recipe.

✅ Matched Ingredients: rice, egg, onion, carrot, soy sauce
❌ Missing Ingredients: capsicum, garlic, spring onion

⏱️ Cooking Time: 20 minutes
🎯 Difficulty: Easy
🍽️ Meal Type: Lunch
🌍 Cuisine: Chinese

📋 Steps:
1. Use leftover or day-old rice...
2. Heat oil in a wok...
[full steps]

💡 Tips: Use high flame throughout for authentic fried rice flavor.
```

---

## 📋 Assignment Requirements Mapping

| Requirement | Implementation | Location in Code |
|---|---|---|
| **RAG Architecture** | LangChain retriever fetches chunks before LLM call | `generate_recipe_answer()` |
| **API Usage** | Gemini API for embeddings + generation | `get_embeddings()`, `generate_recipe_answer()` |
| **Vector Database** | FAISS — local, no server | `create_vector_store()`, `load_vector_store()` |
| **Custom Dataset** | 20+ recipes in 5 `.txt` files | `data/recipes/*.txt` |
| **Streamlit UI** | Full UI with tabs, filters, cards | `main()` and render functions |
| **Answer from dataset only** | Prompt explicitly says "ONLY use context" | `build_prompt()` |
| **Error Handling** | API key, model, file, FAISS errors handled | Multiple try/except blocks |
| **Configurable models** | All models loaded from `.env` | Top of `app.py` |

---

## 🐛 Common Errors & Fixes

| Error | Fix |
|---|---|
| `GOOGLE_API_KEY not found` | Create `.env` from `.env.example` and add your key |
| `Model not found` | Change `LLM_MODEL` in `.env` to a stable model like `gemini-1.5-flash` |
| `No recipe files found` | Make sure `data/recipes/*.txt` files exist |
| `streamlit not recognized` | Use `python -m streamlit run app.py` |
| `FAISS load error` | Delete `vectorstore/` folder and restart (will rebuild) |
| `Execution Policy error` | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |

---

## 🙏 Credits

- **LangChain** — RAG framework
- **Google Gemini** — LLM and Embeddings
- **Facebook AI / Meta** — FAISS vector database
- **Streamlit** — Web UI framework
- Recipe ideas from common Indian and Continental home cooking

---

*Built as a Week 4 RAG Assignment project. For learning purposes.*
