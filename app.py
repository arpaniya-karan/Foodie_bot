"""
FoodieBot 🍳 - RAG-Based Recipe Recommendation Assistant
=========================================================
Week 4 RAG Assignment Project
Tech Stack: Python, Streamlit, LangChain, FAISS, Gemini API
"""

import os
import glob
import random
import streamlit as st
from dotenv import load_dotenv

# ── Load environment variables ────────────────────────────────────────────────
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL") or st.secrets.get("LLM_MODEL", "gemini-1.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL") or st.secrets.get("EMBEDDING_MODEL", "models/gemini-embedding-001")
VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH") or st.secrets.get("VECTORSTORE_PATH", "vectorstore/faiss_index")
RECIPES_PATH = os.getenv("RECIPES_PATH") or st.secrets.get("RECIPES_PATH", "data/recipes")

# ── Streamlit page config (MUST be first Streamlit call) ─────────────────────
st.set_page_config(
    page_title="FoodieBot 🍳",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root Variables ── */
:root {
    --cream:    #FDF6EC;
    --orange:   #E8621A;
    --amber:    #F5A623;
    --green:    #2D7A4F;
    --brown:    #6B3A2A;
    --warm-bg:  #FFF8F0;
    --card-bg:  #FFFFFF;
    --shadow:   rgba(107, 58, 42, 0.12);
    --text:     #2C1810;
    --muted:    #7A6355;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--warm-bg);
    color: var(--text);
}

/* ── Hide only menu/footer, keep header visible for sidebar toggle ── */
#MainMenu, footer { visibility: hidden; }

header[data-testid="stHeader"] {
    visibility: visible !important;
    background: transparent !important;
}

/* ── Hero Section ── */
.hero-section {
    background: linear-gradient(135deg, #E8621A 0%, #F5A623 50%, #E8621A 100%);
    border-radius: 24px;
    padding: 48px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 40px rgba(232, 98, 26, 0.35);
}
.hero-section::before {
    content: '🍳🥘🍜🥗🍛';
    position: absolute;
    top: -10px; right: -10px;
    font-size: 80px;
    opacity: 0.15;
    letter-spacing: -10px;
    transform: rotate(-15deg);
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: white;
    margin: 0 0 8px 0;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.hero-subtitle {
    font-size: 1.25rem;
    color: rgba(255,255,255,0.9);
    margin: 0 0 16px 0;
    font-weight: 300;
}
.hero-desc {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.8);
    max-width: 600px;
    line-height: 1.6;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.4);
    color: white;
    padding: 4px 14px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Cards ── */
.recipe-card {
    background: var(--card-bg);
    border-radius: 20px;
    padding: 28px 32px;
    box-shadow: 0 4px 24px var(--shadow);
    border: 1px solid rgba(232, 98, 26, 0.1);
    margin-bottom: 20px;
    animation: fadeSlideIn 0.4s ease-out;
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.recipe-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--orange);
    margin-bottom: 6px;
}
.recipe-desc {
    color: var(--muted);
    font-size: 1rem;
    margin-bottom: 20px;
    line-height: 1.6;
}

/* ── Tag Chips ── */
.tags-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
}
.tag {
    padding: 4px 14px;
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 600;
}
.tag-meal  { background: #FFF0E0; color: #C85A00; border: 1px solid #FFD4A8; }
.tag-time  { background: #E8F5E9; color: #2D7A4F; border: 1px solid #B8DFC5; }
.tag-diff  { background: #EAF2FF; color: #1A5CB3; border: 1px solid #BDD4F8; }
.tag-cuisine{ background: #F5E6FF; color: #6A1B9A; border: 1px solid #D9B3F8; }

/* ── Ingredient Lists ── */
.ing-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin: 20px 0;
}
.ing-box {
    background: #FDF6EC;
    border-radius: 14px;
    padding: 16px;
    border: 1px solid #F0DCC0;
}
.ing-box h4 {
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
    margin-bottom: 10px;
}
.ing-box.matched h4 { color: var(--green); }
.ing-box.missing h4 { color: var(--orange); }
.ing-chip {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 50px;
    font-size: 0.83rem;
    margin: 3px;
}
.chip-green { background: #D4EDDA; color: #155724; }
.chip-orange { background: #FFE5CC; color: #7A3400; }

/* ── Steps ── */
.steps-section {
    background: #FAFAFA;
    border-radius: 14px;
    padding: 20px;
    margin: 16px 0;
    border: 1px solid #F0E8DC;
}
.step-item {
    display: flex;
    gap: 14px;
    margin-bottom: 14px;
    align-items: flex-start;
}
.step-num {
    min-width: 30px; height: 30px;
    background: var(--orange);
    color: white;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700;
    flex-shrink: 0;
}
.step-text { color: var(--text); font-size: 0.95rem; line-height: 1.6; padding-top: 4px; }

/* ── Also Like Section ── */
.also-like-card {
    background: linear-gradient(135deg, #FFF8F0, #FDF0E0);
    border-radius: 16px;
    padding: 20px;
    border: 1px dashed #F0C080;
    margin-bottom: 12px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.also-like-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(232, 98, 26, 0.15);
}
.also-like-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: var(--orange);
    font-weight: 600;
    margin-bottom: 4px;
}

/* ── Info/Tips Box ── */
.tip-box {
    background: linear-gradient(135deg, #FFF8E1, #FFF3CD);
    border-left: 4px solid var(--amber);
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    margin: 16px 0;
    font-size: 0.92rem;
    color: #5D4037;
}

/* ── Status Messages ── */
.status-msg {
    background: linear-gradient(135deg, #E8621A, #F5A623);
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    font-weight: 500;
    font-size: 0.95rem;
    margin: 8px 0;
    text-align: center;
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.75; }
}

/* ── No Match Box ── */
.no-match-box {
    background: #FFF0E0;
    border: 2px dashed var(--orange);
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    color: var(--brown);
}
.no-match-box h3 { font-family: 'Playfair Display', serif; color: var(--orange); font-size: 1.4rem; }

/* ── About / RAG Box ── */
.rag-flow {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin: 24px 0;
}
.rag-step {
    background: white;
    border: 2px solid var(--orange);
    border-radius: 12px;
    padding: 12px 20px;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--orange);
    text-align: center;
}
.rag-arrow { font-size: 1.4rem; color: var(--amber); }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2C1810 0%, #3D2010 100%);
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] h2 {
    color: white !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 50px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover { transform: translateY(-2px); }

/* ── Section Divider ── */
.section-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 700;
    color: var(--muted);
    margin: 24px 0 8px 0;
}

/* ── Dataset Preview ── */
.dataset-file-card {
    background: white;
    border-radius: 14px;
    padding: 16px 20px;
    border: 1px solid #F0DCC0;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px var(--shadow);
}

/* ── Keep Streamlit sidebar reopen button visible ── */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 999999 !important;
    position: fixed !important;
    top: 0.75rem !important;
    left: 0.75rem !important;
    background: white !important;
    border-radius: 10px !important;
    padding: 6px !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# BACKEND: RAG Pipeline Functions
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def get_embeddings():
    """Initialize Gemini embedding model (cached)."""
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY,
    )


def load_documents(recipes_path: str = RECIPES_PATH):
    """Load all .txt recipe files from the recipes folder."""
    from langchain_community.document_loaders import TextLoader
    from langchain_core.documents import Document

    txt_files = glob.glob(os.path.join(recipes_path, "*.txt"))
    if not txt_files:
        raise FileNotFoundError(
            f"No .txt recipe files found in '{recipes_path}'. "
            "Make sure data/recipes/ folder exists with recipe files."
        )

    documents = []
    for filepath in txt_files:
        loader = TextLoader(filepath, encoding="utf-8")
        docs = loader.load()
        # Tag each doc with its source filename
        for doc in docs:
            doc.metadata["source_file"] = os.path.basename(filepath)
        documents.extend(docs)

    return documents


def split_documents(documents):
    """Split loaded documents into smaller overlapping chunks."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80,
        separators=["\n---\n", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(documents)
    return chunks


def create_vector_store(chunks, vectorstore_path: str = VECTORSTORE_PATH):
    """Embed chunks and save FAISS vector store to disk."""
    from langchain_community.vectorstores import FAISS

    embeddings = get_embeddings()
    os.makedirs(os.path.dirname(vectorstore_path), exist_ok=True)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(vectorstore_path)
    return vectorstore


def load_vector_store(vectorstore_path: str = VECTORSTORE_PATH):
    """Load existing FAISS vector store from disk."""
    from langchain_community.vectorstores import FAISS

    if not os.path.exists(vectorstore_path):
        return None
    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(
        vectorstore_path,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    return vectorstore


def get_retriever(vectorstore, k: int = 5):
    """Return a FAISS retriever that fetches top-k relevant chunks."""
    return vectorstore.as_retriever(search_kwargs={"k": k})


def build_prompt(user_query: str, context: str, filters: dict) -> str:
    """Build a structured prompt string for Gemini."""
    filter_text = "\n".join(
        [f"- {key}: {val}" for key, val in filters.items() if val != "Any"]
    )
    if not filter_text:
        filter_text = "None (suggest the best matching recipe)"

    prompt = f"""You are FoodieBot 🍳, a fun and friendly RAG-based recipe assistant for home cooks.

MAIN GOAL:
Turn the user's random or incomplete ingredients into the best possible recipe idea using ONLY the retrieved recipe context.

STRICT RAG RULES:
1. Use ONLY the recipes and details found in the RETRIEVED RECIPE CONTEXT.
2. Do NOT invent a new recipe that is not present in the context.
3. Choose the closest matching recipe from the context based on the user's available ingredients and filters.
4. If the user's ingredients only partially match a recipe, still suggest the closest useful recipe.
5. Do not reject a recipe just because small flavor ingredients, garnish, spices, or optional vegetables are missing.
6. Keep the answer warm, fun, simple, and beginner-friendly.

VERY IMPORTANT INGREDIENT MATCHING RULES:
1. "Ingredients You Have" must include ONLY ingredients explicitly typed by the user in USER'S AVAILABLE INGREDIENTS.
2. Do NOT add ingredients from the recipe context into "Ingredients You Have" unless the user actually typed them.
3. Do NOT add assumed basic kitchen items like salt, oil, water, sugar, pepper, chilli powder, turmeric, cumin, or common spices under "Ingredients You Have" unless the user typed them.
4. Basic kitchen items like salt, oil, water, sugar, pepper, chilli powder, turmeric, cumin, and common spices may be assumed available for cooking, but they should NOT be listed as user-owned ingredients.
5. If the user typed "egg and tomato", then "Ingredients You Have" should only include egg and tomato, not onion, salt, oil, or other recipe ingredients.
6. Ingredients from the recipe that are not typed by the user should go under either "Optional Extras" or "Required Missing Ingredients".
7. "Optional Extras" should include ingredients that improve taste but are not compulsory, such as onion, garlic, coriander, spring onion, herbs, carrot, capsicum, peas, garnish, sauces, and extra vegetables.
8. "Required Missing Ingredients" should include only main ingredients without which the recipe cannot reasonably be made.
9. If the recipe can be made with the user's main ingredients plus assumed basic kitchen items, write Required Missing Ingredients as: None — you can make this with your main ingredients!
10. The answer should help the user cook something from what they have, not discourage them.

FILTER RULES:
- Try to follow the user's selected filters when possible.
- If no retrieved recipe perfectly matches the filters, choose the closest recipe from the context and briefly mention that it is the closest match.
- Do not ignore ingredient matching just to satisfy a filter.

═══════════════════════════════════════
USER'S AVAILABLE INGREDIENTS:
{user_query}

USER'S FILTERS:
{filter_text}

═══════════════════════════════════════
RETRIEVED RECIPE CONTEXT from dataset:
{context}
═══════════════════════════════════════

If a useful recipe match is found, reply EXACTLY in this markdown format:

## 🍽️ [Recipe Name]

**Short Description:** [1-2 fun lines about the dish]

**Why this works with your ingredients:** [Explain how the user's typed ingredients can be used in this recipe. Mention if it is a close/partial match.]

**✅ Ingredients You Have:** [ONLY ingredients from USER'S AVAILABLE INGREDIENTS that match this recipe. Do not include assumed basics or recipe-only ingredients.]

**🟡 Optional Extras:** [Recipe ingredients not typed by the user but useful/optional. Include garnish, spices, sauces, onion, garlic, vegetables, or toppings here if they are not essential.]

**❌ Required Missing Ingredients:** [Only main required ingredients not typed by the user. If none, write: None — you can make this with your main ingredients!]

**⏱️ Cooking Time:** [time from the recipe context]

**🎯 Difficulty:** [difficulty from the recipe context]

**🍽️ Meal Type:** [meal type from the recipe context]

**🌍 Cuisine:** [cuisine from the recipe context]

**📋 Steps:**
1. [Step one using the user's available ingredients first]
2. [Step two]
3. [Continue with simple beginner-friendly steps based on the recipe context]

**💡 Tips:** [1-2 useful tips for making it tasty with limited ingredients]

---

## 🌟 You May Also Like:
1. **[Alternative Recipe 1 from context]** — [one line why it may fit]
2. **[Alternative Recipe 2 from context]** — [one line why it may fit]

---

If NO recipe in the retrieved context has even a weak match with the user's ingredients, reply with exactly:
"NO_MATCH_FOUND"

Do not invent a recipe. Do not use outside knowledge. Do not list ingredients as "Ingredients You Have" unless the user typed them.
"""
    return prompt


def generate_recipe_answer(user_query: str, filters: dict, vectorstore) -> str:
    """Full RAG pipeline: retrieve → prompt → generate."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage

    # Step 1: Retrieve relevant recipe chunks
    retriever = get_retriever(vectorstore, k=6)
    relevant_docs = retriever.invoke(user_query)

    if not relevant_docs:
        return "NO_MATCH_FOUND"

    # Step 2: Build context from retrieved chunks
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # Step 3: Build the prompt
    prompt_text = build_prompt(user_query, context, filters)

    # Step 4: Call Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3,
        convert_system_message_to_human=True,
    )
    response = llm.invoke([HumanMessage(content=prompt_text)])
    return response.content


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Ensure Vector Store Exists
# ─────────────────────────────────────────────────────────────────────────────

def ensure_vectorstore():
    """Load or build the FAISS vectorstore. Returns vectorstore or None on error."""
    vs = load_vector_store()
    if vs is not None:
        return vs, None  # (vectorstore, error_message)

    # Build it from scratch
    try:
        with st.spinner("🔨 Building recipe knowledge base... (first run only)"):
            docs   = load_documents()
            chunks = split_documents(docs)
            vs     = create_vector_store(chunks)
        return vs, None
    except FileNotFoundError as e:
        return None, str(e)
    except Exception as e:
        return None, f"Error building vector store: {str(e)}"


# ─────────────────────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────

SURPRISE_INGREDIENTS = [
    "rice, egg, onion, soy sauce",
    "bread, potato, butter, cheese",
    "tomato, onion, pasta, garlic",
    "poha, onion, mustard seeds, curry leaves",
    "noodles, carrot, capsicum, garlic",
    "oats, banana, milk, honey",
    "paneer, capsicum, onion, chilli sauce",
    "semolina, onion, peas, curry leaves",
]

def render_hero():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">✨ RAG-Powered</div>
        <h1 class="hero-title">FoodieBot 🍳</h1>
        <p class="hero-subtitle">Turn random ingredients into tasty recipes using RAG.</p>
        <p class="hero-desc">
            Open your fridge, type what you have, and let AI powered by Retrieval-Augmented Generation 
            (RAG) find you the perfect recipe from our curated dataset — not from general AI knowledge.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🎛️ Recipe Filters")
        st.markdown("---")
        meal_type   = st.selectbox("🍽️ Meal Type",    ["Any", "Breakfast", "Lunch", "Dinner", "Snacks"])
        cuisine     = st.selectbox("🌍 Cuisine",       ["Any", "Indian", "Chinese", "Italian", "Continental"])
        cook_time   = st.selectbox("⏱️ Cooking Time",  ["Any", "Under 10 minutes", "Under 20 minutes", "Under 30 minutes"])
        difficulty  = st.selectbox("🎯 Difficulty",    ["Any", "Easy", "Medium"])
        spice_level = st.selectbox("🌶️ Spice Level",   ["Any", "Mild", "Medium", "Spicy"])
        st.markdown("---")
        st.markdown("""
        <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem; line-height: 1.7;'>
        <b style='color:white;'>📚 How RAG Works</b><br>
        1. Your ingredients are embedded<br>
        2. FAISS retrieves matching recipe chunks<br>
        3. Context is sent to Gemini<br>
        4. Gemini generates your recipe!
        </div>
        """, unsafe_allow_html=True)

    return {
        "Meal Type":    meal_type,
        "Cuisine":      cuisine,
        "Cooking Time": cook_time,
        "Difficulty":   difficulty,
        "Spice Level":  spice_level,
    }


def render_recipe_result(answer: str):
    """Render the LLM markdown answer inside a beautiful recipe card."""
    if "NO_MATCH_FOUND" in answer:
        st.markdown("""
        <div class="no-match-box">
            <h3>😕 No perfect match found!</h3>
            <p>I couldn't find a strong match in the recipe dataset.<br>
            Try adding more common ingredients like:<br>
            <b>rice, egg, bread, potato, onion, tomato, pasta, noodles</b></p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
    st.markdown(answer)
    st.markdown('</div>', unsafe_allow_html=True)


def render_about_rag():
    st.markdown("## 🧠 How RAG Works in FoodieBot")
    st.markdown("""
    **Retrieval-Augmented Generation (RAG)** is an AI technique that improves LLM answers 
    by grounding them in a specific dataset — so the AI can't just make things up!
    """)
    st.markdown("""
    <div class="rag-flow">
        <div class="rag-step">👤 User enters<br>ingredients</div>
        <div class="rag-arrow">→</div>
        <div class="rag-step">🔢 Ingredients are<br>embedded to vectors</div>
        <div class="rag-arrow">→</div>
        <div class="rag-step">🗄️ FAISS searches<br>recipe vector store</div>
        <div class="rag-arrow">→</div>
        <div class="rag-step">📄 Top recipe chunks<br>are retrieved</div>
        <div class="rag-arrow">→</div>
        <div class="rag-step">🤖 Gemini generates<br>structured answer</div>
        <div class="rag-arrow">→</div>
        <div class="rag-step">🍳 Recipe card<br>displayed!</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📌 Assignment Requirements")
        st.markdown("""
        | Requirement | Implementation |
        |---|---|
        | RAG Architecture | ✅ LangChain retriever + Gemini |
        | API Usage | ✅ Gemini API (LLM + Embeddings) |
        | Vector Database | ✅ FAISS (local) |
        | Custom Dataset | ✅ 5 recipe .txt files |
        | Streamlit UI | ✅ Full UI with filters |
        """)
    with col2:
        st.markdown("### 🛠️ Tech Stack")
        st.markdown("""
        - **Frontend:** Streamlit + Custom CSS
        - **RAG Framework:** LangChain
        - **Vector Store:** FAISS (Facebook AI)
        - **Embeddings:** Gemini Embedding API
        - **LLM:** Gemini (Flash / Pro)
        - **Dataset:** Local .txt recipe files
        - **Config:** python-dotenv
        """)


def render_dataset_preview():
    st.markdown("## 📂 Recipe Dataset Preview")
    st.info("These are the local .txt files used as the knowledge base for RAG.")

    recipe_files = glob.glob(os.path.join(RECIPES_PATH, "*.txt"))
    if not recipe_files:
        st.error(f"No recipe files found in `{RECIPES_PATH}/`")
        return

    for filepath in sorted(recipe_files):
        filename = os.path.basename(filepath)
        with st.expander(f"📄 {filename}"):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            # Show first 1500 chars to keep it readable
            preview = content[:1500] + ("\n\n...[truncated for preview]" if len(content) > 1500 else "")
            st.code(preview, language="text")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # ── Check API Key ─────────────────────────────────────────────────────────
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_api_key_here":
        st.error(
            "🔑 **Google API Key not found!**\n\n"
            "1. Copy `.env.example` to `.env`\n"
            "2. Add your `GOOGLE_API_KEY`\n"
            "3. Restart the app\n\n"
            "Get your free key at: https://aistudio.google.com/app/apikey"
        )
        st.stop()

    # ── Render Hero & Sidebar ─────────────────────────────────────────────────
    render_hero()
    filters = render_sidebar()

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["🍳 Find Recipe", "📂 Dataset Preview", "🧠 About RAG"])

    # ═══════════════════════════
    # TAB 1 — FIND RECIPE
    # ═══════════════════════════
    with tab1:
        st.markdown('<p class="section-label">Enter Your Ingredients</p>', unsafe_allow_html=True)

        ingredient_input = st.text_area(
            label="ingredients",
            label_visibility="collapsed",
            placeholder="Enter ingredients you have... e.g. rice, egg, onion, tomato",
            height=100,
            key="ingredient_box",
        )

        col_find, col_surprise, col_clear = st.columns([2, 2, 1])
        with col_find:
            find_clicked = st.button("🔍 Find Recipe", use_container_width=True, type="primary")
        with col_surprise:
            surprise_clicked = st.button("🎲 Surprise Me!", use_container_width=True)
        with col_clear:
            clear_clicked = st.button("🗑️ Clear", use_container_width=True)

        # ── Handle Surprise Me ────────────────────────────────────────────────
        if surprise_clicked:
            surprise_query = random.choice(SURPRISE_INGREDIENTS)
            st.session_state["surprise_query"] = surprise_query
            st.rerun()

        # ── Handle Clear ──────────────────────────────────────────────────────
        if clear_clicked:
            st.session_state.pop("last_answer", None)
            st.session_state.pop("surprise_query", None)
            st.rerun()

        # ── Resolve final query ───────────────────────────────────────────────
        final_query = ingredient_input.strip()
        if not final_query and "surprise_query" in st.session_state:
            final_query = st.session_state["surprise_query"]
            st.info(f"🎲 **Surprise Ingredients:** {final_query}")

        # ── Process query ─────────────────────────────────────────────────────
        if find_clicked or (surprise_clicked and "surprise_query" in st.session_state):
            if not final_query:
                st.warning("🥕 Please enter at least one ingredient first!")
            else:
                # Load / build vectorstore
                vectorstore, err = ensure_vectorstore()
                if err:
                    st.error(f"❌ {err}")
                    st.stop()

                # Generate answer
                               with st.status("🍳 Cooking up your recipe...", expanded=True) as status_widget:
                    st.write("🔍 Searching the recipe pantry...")
                    try:
                        answer = generate_recipe_answer(final_query, filters, vectorstore)
                        st.write("✅ Recipe found!")
                        status_widget.update(label="Recipe Ready!", state="complete")
                        st.session_state["last_answer"] = answer

                    except Exception as e:
                        status_widget.update(label="Error", state="error")
                        err_str = str(e)

                        if "API_KEY" in err_str.upper() or "authentication" in err_str.lower():
                            st.error("🔑 API Key error. Check your GOOGLE_API_KEY in Streamlit Cloud secrets.")
                        else:
                            st.error(f"❌ Actual error: {err_str}")
                            st.info(f"Current LLM_MODEL: {LLM_MODEL}")
                            st.info(f"Current EMBEDDING_MODEL: {EMBEDDING_MODEL}")

                        st.stop()

        # ── Show last answer ──────────────────────────────────────────────────
        if "last_answer" in st.session_state:
            st.markdown("---")
            st.markdown('<p class="section-label">🍽️ Your Recipe</p>', unsafe_allow_html=True)
            render_recipe_result(st.session_state["last_answer"])

        # ── Empty state ───────────────────────────────────────────────────────
        if not final_query and "last_answer" not in st.session_state:
            st.markdown("""
            <div style="text-align:center; padding: 48px; color: #A09080;">
                <div style="font-size:4rem;">🥘</div>
                <h3 style="color:#C86020; font-family:'Playfair Display',serif;">What's in your kitchen?</h3>
                <p>Type your ingredients above and click <b>Find Recipe</b>.<br>
                Or hit <b>Surprise Me!</b> for a random combination.</p>
            </div>
            """, unsafe_allow_html=True)

    # ═══════════════════════════
    # TAB 2 — DATASET PREVIEW
    # ═══════════════════════════
    with tab2:
        render_dataset_preview()

    # ═══════════════════════════
    # TAB 3 — ABOUT RAG
    # ═══════════════════════════
    with tab3:
        render_about_rag()


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
