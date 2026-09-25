# NutriGen AI — Generative AI Personal Nutrition & Meal Planner

A comprehensive university Generative AI project designed to create personalized nutrition recommendations, tailored weekly meal plans, step-by-step recipes, smart ingredient substitutions, and conversational cooking assistance using Google Gemini.

---

## 1. Project Overview

**NutriGen AI** is a Generative AI-based personal nutrition and meal planning web application. Users configure their dietary preferences, weekly grocery budget, cooking constraints, allergies, and available home ingredients. Using Google Gemini (`gemini-3.7-flash`), NutriGen AI synthesizes personalized weekly meal plans, detailed recipes, zero-waste ingredient substitutions, and interactive conversational nutrition guidance.

---

## 2. Problem Statement

Deciding what to cook daily is a common challenge for individuals, students, and families. People frequently struggle to balance multiple conflicting factors:
- **Dietary restrictions & allergies** (e.g., vegetarian, vegan, peanut allergies, celiac/gluten limits).
- **Available ingredients at home** leading to forgotten groceries and avoidable food waste.
- **Budgetary constraints** requiring affordable meals that maximize nutritional value.
- **Time limitations & cooking skill levels** that require realistic, quick-prep meal suggestions.

Traditional static recipe apps lack personalization and cannot dynamically reason about what ingredients are currently sitting in the user's fridge or adjust recipes in real-time.

---

## 3. Objectives

- **Personalized Meal Planning:** Generate multi-day meal schedules tailored to dietary styles, household sizes, and financial budgets.
- **AI Recipe Synthesis:** Generate step-by-step cooking instructions with exact ingredient quantities and preparation timings for any selected meal.
- **Pantry & Fridge Inventory Awareness:** Prioritize utilizing in-stock ingredients to reduce grocery costs and eliminate food waste.
- **Smart Ingredient Substitution:** Recommend practical, allergy-safe alternative ingredients when items are missing from the pantry.
- **Natural Language Modifications:** Allow users to adjust recipes or meal plans on-the-fly (e.g., *"Make it faster"*, *"Make it cheaper"*, *"Use less oil"*).
- **Conversational Nutrition Assistant:** Provide an interactive chatbot that reasons over the user's profile, fridge inventory, active meal plan, and recipes.

---

## 4. Main Features

| Module | Feature | Description |
|---|---|---|
| 👤 **Preferences** | User Profile Management | Stores dietary style, cuisine preference, weekly budget, cooking skill, allergies, and disliked foods. |
| 🥕 **My Fridge** | Ingredient Inventory | Tracks pantry/fridge stock with quantities, units, categories, and automated expiry tracking (Fresh, Expiring Soon, Expired). |
| 🍽️ **Meal Planner** | AI Meal Plan Generator | Generates 1–7 day meal schedules adhering to budget, time, and allergy constraints with 1-click regeneration and natural-language modification. |
| 🍳 **Recipes** | AI Recipe Generator | Synthesizes full step-by-step recipes for any meal with prep/cook time, ingredient measurements, and chef tips. |
| ✏️ **Adjustments** | AI Recipe Modification | Quick-action chips (💰 *Make Cheaper*, ⏱️ *Make Faster*, 🌶️ *Make Less Spicy*, 🫒 *Use Less Oil*) and free-form custom instructions. |
| 🔄 **Substitution** | AI Ingredient Substitution | Suggests 2–4 practical replacements for missing ingredients, prioritizing items already in the fridge while enforcing strict allergen safety. |
| 🤖 **AI Assistant** | Conversational Chatbot | Answers questions with full situational context (profile + fridge stock + meal plan + active recipe) with isolated session chat history. |

---

## 5. Technology Stack

- **Core Language:** Python 3 (3.10+)
- **Web UI Framework:** [Streamlit](https://streamlit.io/) (1.36+)
- **Generative AI Provider:** Google Gemini API (`gemini-3.7-flash`) via `google-genai` SDK
- **Environment & Configuration:** `python-dotenv` (Local `.env` and `.streamlit/secrets.toml` support)
- **Styling:** Custom CSS design system (Responsive cards, glassmorphic badges, modern typography)
- **State Management:** Streamlit Session State (`st.session_state`)

---

## 6. System Workflow

```text
       User Preferences (Diet, Budget, Allergies, Cooking Time)
                                +
             Fridge Stock (In-Stock Ingredients)
                                ↓
                 Structured Context Aggregator
                                ↓
                   Context-Aware Prompt Builder
                                ↓
                   Google Gemini API (GenAI)
                                ↓
        ┌───────────────────────┼───────────────────────┐
        ↓                       ↓                       ↓
AI-Generated Meal Plan     AI-Generated Recipe     AI Substitutions
        ↓                       ↓                       ↓
  Plan Modifications      Recipe Adjustments       Chat Assistant
        └───────────────────────┬───────────────────────┘
                                ↓
                 Interactive Streamlit Web UI
```

---

## 7. GenAI Implementation

NutriGen AI employs **structured prompt engineering** to transform user data into rich contextual prompts for Google Gemini without requiring complex databases or multi-agent frameworks:

1. **Persona Grounding:** Establishes NutriGen AI as a helpful, safety-first personal nutrition assistant.
2. **Context Injection:** Formats active user profile attributes, fridge inventory summaries, and active meal plans/recipes into clean prompt sections.
3. **Pantry Prioritization Rule:** Instructs Gemini to prefer using available in-stock ingredients before suggesting new grocery purchases.
4. **Allergen Guardrails:** Enforces critical safety directives that strictly prohibit suggesting ingredients listed under user allergies.
5. **Output Standardization:** Formats model outputs into clean GitHub Flavored Markdown with bold headings, ingredient lists, and timing metrics.

---

## 8. Project Architecture

```text
Streamlit User Interface (app.py & pages/*.py)
                    ↓
Page Logic & State Management (st.session_state)
                    ↓
Prompt Builder Utilities (utils/prompts.py)
                    ↓
Service Layer (services/gemini_service.py)
                    ↓
Google Gemini API (gemini-3.7-flash)
                    ↓
Markdown Renderers & Interactive UI Controls
```

### Directory Structure:
```
nutrition-meal-planner/
│
├── app.py                  # Main entry point & multi-page navigation router
├── requirements.txt        # Minimal Python dependencies
├── README.md               # Complete project documentation
├── test_app.py             # 18 automated unit and integration tests
│
├── pages/                  # Application multi-page views
│   ├── dashboard.py        # Overview metrics & quick actions
│   ├── preferences.py      # Profile management & validation
│   ├── fridge.py           # Inventory tracking & expiry engine
│   ├── meal_planner.py     # Gemini meal plan generator & modifications
│   ├── recipes.py          # AI recipe generator, modifications & substitutions
│   └── ai_assistant.py     # Context-aware conversational assistant
│
├── services/
│   └── gemini_service.py   # Reusable Google Gemini client & inference handler
│
├── utils/
│   ├── helpers.py          # Session state initializer, validators & styling helpers
│   └── prompts.py          # Prompt builders for Q&A, Meal Plans, Recipes, Substitutions & Assistant
│
└── assets/
    └── styles.css          # Custom styling for cards, metrics, badges, & headers
```

---

## 9. Testing

The project includes a comprehensive automated test suite in [`test_app.py`](test_app.py) using `streamlit.testing.v1.AppTest` and mock response fixtures to ensure zero API quota consumption during automated runs:

```bash
# 1. Verify Syntax & Compilation
python3 -m py_compile app.py pages/*.py utils/*.py services/*.py

# 2. Run Automated Test Suite
python3 test_app.py
```

### Test Suite Summary:
- **18 Total Unit & Integration Tests Passed (100% Pass Rate)**
  - Assistant prompt builder with full multi-source context
  - Assistant prompt builder with missing optional context
  - Full system data flow & inter-module integration
  - Substitution prompt builder with allergy safety checks
  - Recipe modification prompt builder
  - Meal plan modification prompt builder
  - Recipe prompt builder with profile, allergies, and fridge stock
  - Meal plan prompt builder
  - Simple prompt builder
  - Missing Gemini API key graceful handling
  - Comma-separated parser
  - User profile validator
  - Expiry status calculator (Fresh / Expiring Soon / Expired)
  - App initialization integration test
  - Dashboard page component test
  - Preferences page profile update test
  - Fridge page inventory management test
  - Meal Planner & Recipe Generator UI tests
  - AI Assistant UI, conversation history, and Clear Chat isolation test

---

## 10. Limitations

- **API Connectivity:** Requires an active internet connection and a valid Google Gemini API key for live generative inference.
- **Free-Tier Quota:** Google Gemini's free tier (15 requests/minute) may trigger rate limit notices under rapid clicks.
- **Session-Based Storage:** Data is persisted in `st.session_state` for the active browser session and resets upon browser tab reload.
- **Approximated Nutrition:** Calorie and protein values are AI estimates intended for general guidance, not clinical medical advice.

---

## 11. Future Scope

- **Persistent Multi-User Accounts:** User authentication with encrypted database storage (e.g., PostgreSQL/Supabase).
- **Automated Grocery List Export:** Automatic aggregation of missing recipe ingredients into downloadable shopping lists.
- **Verified Nutrition Integration:** Pairing GenAI outputs with verified nutritional databases (USDA / IFCT).
- **Barcode & Receipt Scanning:** Camera-based ingredient logging for instant fridge inventory updates.
- **Mobile Native Application:** Cross-platform mobile deployment for iOS and Android.

---

## 12. Conclusion

**NutriGen AI** demonstrates the practical application of Generative AI in addressing everyday household nutrition and cooking challenges. By combining simple, transparent prompt engineering with user preferences and real-time fridge inventory, the system delivers personalized, cost-effective, and zero-waste meal recommendations in an intuitive Streamlit interface.

---

## 🔮 Project Roadmap

```text
Phase 1 — Project Foundation & Basic UI              ✅
Phase 2 — User Preferences & Profile                ✅
Phase 3 — Fridge / Ingredient Manager               ✅
Phase 4 — Gemini GenAI Integration                  ✅
Phase 5 — AI Meal Plan Generator                    ✅
Phase 6 — AI Recipe Generator                       ✅
Phase 7 — AI Modifications & Substitution           ✅
Phase 8 — Simple AI Assistant                       ✅
Phase 9 — Final Testing & Documentation             ✅
```

---

## 💻 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the project root:
```bash
echo "GEMINI_API_KEY=your_actual_gemini_api_key" > .env
```

### 3. Run Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.
