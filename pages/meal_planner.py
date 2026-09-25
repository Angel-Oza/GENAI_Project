"""
NutriGen AI - Meal Planner Page (Phase 5)
AI-powered personalized meal plan generator using Google Gemini.
Orchestrates User Profile constraints, in-stock pantry ingredients, and natural language modifications.
"""

import streamlit as st
from utils.helpers import (
    render_header,
    load_css,
    init_session_state,
    get_default_user_profile
)
from utils.prompts import build_meal_plan_prompt, build_modify_meal_plan_prompt
from services.gemini_service import generate_ai_response, is_gemini_configured

init_session_state()
load_css()

# Branded Header
render_header(
    title="AI Meal Planner",
    subtitle="Generate a personalized meal plan based on your preferences and ingredients.",
    icon="🍽️"
)

profile = st.session_state.get("user_profile", get_default_user_profile())
fridge_items = st.session_state.get("fridge_items", [])
has_profile = bool(profile.get("name") or profile.get("weekly_budget"))

# 1. Profile Verification & Guidance
if not has_profile:
    st.warning(
        "⚠️ **Please complete your preferences first.**\n\n"
        "Go to **My Preferences** in the sidebar and save your dietary style, budget, and restrictions before generating a personalized meal plan."
    )
else:
    # Profile Context Banner
    diet_val = profile.get("dietary_preference", "Vegetarian")
    cuisine_val = profile.get("cuisine_preference", "Indian")
    budget_val = profile.get("weekly_budget", 500)
    cook_val = profile.get("maximum_cooking_time", 30)
    allergies_val = profile.get("allergies", [])
    allergies_str = ", ".join(allergies_val) if allergies_val else "None"
    
    st.markdown(
        f"""
        <div class="demo-banner">
            <span>👤</span>
            <span><b>Active Profile Context:</b> Diet: <b>{diet_val}</b> | Cuisine: <b>{cuisine_val}</b> | Budget: <b>₹{budget_val}/week</b> | Time: <b>{cook_val} min</b> | Allergies: <b>{allergies_str}</b></span>
        </div>
        """,
        unsafe_allow_html=True
    )

# 2. Fridge Context Banner (Section 16 Empty Fridge Handling)
if fridge_items:
    available_ing_names = " • ".join([item["name"] for item in fridge_items[:8]])
    if len(fridge_items) > 8:
        available_ing_names += f" • +{len(fridge_items) - 8} more"
        
    st.markdown(
        f"""
        <div class="demo-banner" style="background-color: #ecfdf5; border-color: #a7f3d0; color: #065f46;">
            <span>🥕</span>
            <span><b>Available Ingredients in Fridge:</b> {available_ing_names}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("ℹ️ No fridge ingredients found. Gemini will suggest commonly available budget-friendly staples.")

# 3. Planner Parameters Form & Controls
with st.container(border=True):
    st.markdown("### ⚙️ Plan Generator Parameters")
    st.caption("Customize the duration, meal structure, and budget for your AI generation:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        num_days = st.slider("Number of Days", min_value=1, max_value=7, value=7, help="Select duration (e.g., 3, 5, or 7 days).")
    with col2:
        meal_types = st.multiselect(
            "Meals Per Day",
            options=["Breakfast", "Lunch", "Dinner", "Snacks"],
            default=["Breakfast", "Lunch", "Dinner"],
            help="Choose the meals you want Gemini to schedule."
        )
        default_budget_val = float(max(50.0, float(profile.get("weekly_budget") or 500)))
        budget_limit = st.number_input(
            "Budget Allocation (₹)",
            min_value=50.0,
            max_value=20000.0,
            value=default_budget_val,
            step=50.0
        )
        
    diet_options = ["Vegetarian", "Vegan", "Non-Vegetarian", "Jain", "Eggetarian", "Other"]
    saved_diet = profile.get("dietary_preference", "Vegetarian")
    diet_idx = diet_options.index(saved_diet) if saved_diet in diet_options else 0
    
    cuisine_options = ["Indian", "Gujarati", "North Indian", "South Indian", "Chinese", "Italian", "Mexican", "Mediterranean", "Other"]
    saved_cuisine = profile.get("cuisine_preference", "Indian")
    cuisine_idx = cuisine_options.index(saved_cuisine) if saved_cuisine in cuisine_options else 0

    col4, col5 = st.columns(2)
    with col4:
        selected_diet = st.selectbox("Dietary Style", options=diet_options, index=diet_idx)
    with col5:
        selected_cuisine = st.selectbox("Cuisine Style", options=cuisine_options, index=cuisine_idx)

    st.markdown("<br>", unsafe_allow_html=True)
    generate_clicked = st.button("✨ Generate Meal Plan", type="primary", use_container_width=True)

# 4. Handle Generation Trigger
if generate_clicked:
    if not has_profile:
        st.error("Please configure your profile under 'My Preferences' before generating a plan.")
    else:
        # Override profile copy with current form selections if changed
        current_request_profile = profile.copy()
        current_request_profile["dietary_preference"] = selected_diet
        current_request_profile["cuisine_preference"] = selected_cuisine
        current_request_profile["weekly_budget"] = budget_limit
        
        prompt = build_meal_plan_prompt(
            user_profile=current_request_profile,
            fridge_items=fridge_items,
            num_days=num_days,
            meal_types=meal_types,
            target_budget=budget_limit
        )
        
        with st.spinner("🤖 NutriGen AI is creating your personalized meal plan with Google Gemini..."):
            success, response_text = generate_ai_response(prompt)
            
        if success:
            st.session_state.generated_meal_plan = response_text
            st.toast("Personalized meal plan generated successfully!", icon="✨")
            st.rerun()
        else:
            st.error(response_text)

# 5. Display Meal Plan (AI Generated or Sample Preview)
st.markdown("---")

generated_plan = st.session_state.get("generated_meal_plan")

if generated_plan:
    # Header for AI Generated Plan
    st.markdown(
        """
        <div class="demo-banner" style="background-color: #ecfdf5; border-color: #a7f3d0; color: #065f46;">
            <span>✨</span>
            <span><b>AI Generated Meal Plan</b> — Personalized with Google Gemini based on your dietary profile and fridge inventory.</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display AI Generated Markdown
    with st.container(border=True):
        st.markdown(generated_plan)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action Bar: Regenerate & Reset
    act_col1, act_col2 = st.columns([1, 1])
    with act_col1:
        if st.button("🔄 Regenerate Meal Plan", use_container_width=True, help="Ask Gemini to generate another variation with the same requirements."):
            current_request_profile = profile.copy()
            current_request_profile["dietary_preference"] = selected_diet
            current_request_profile["cuisine_preference"] = selected_cuisine
            current_request_profile["weekly_budget"] = budget_limit
            
            prompt = build_meal_plan_prompt(
                user_profile=current_request_profile,
                fridge_items=fridge_items,
                num_days=num_days,
                meal_types=meal_types,
                target_budget=budget_limit
            )
            with st.spinner("🤖 Regenerating your meal plan..."):
                success, response_text = generate_ai_response(prompt)
            if success:
                st.session_state.generated_meal_plan = response_text
                st.toast("Regenerated fresh meal plan!", icon="🔄")
                st.rerun()
            else:
                st.error(response_text)
                
    with act_col2:
        if st.button("🗑️ Reset Plan", use_container_width=True):
            st.session_state.generated_meal_plan = None
            st.rerun()

    # Section: Natural Language Modification Option
    st.markdown("### ✏️ Customize or Modify This Plan")
    st.caption("Tell NutriGen AI what you'd like to adjust with quick actions or custom instructions:")
    
    # Quick Plan Action Chips
    qp1, qp2, qp3, qp4 = st.columns(4)
    quick_plan_mod = None
    with qp1:
        if st.button("💰 Make Cheaper", use_container_width=True, help="Adjust plan to reduce total grocery costs with budget staples."):
            quick_plan_mod = "Modify the meal plan to reduce total grocery cost and use more budget-friendly ingredients."
    with qp2:
        if st.button("⏱️ Faster Meals", use_container_width=True, help="Ensure all meals take 20 mins or less."):
            quick_plan_mod = "Modify all meals in the plan to take 20 minutes or less to prepare and cook."
    with qp3:
        if st.button("🥕 Use More Fridge Items", use_container_width=True, help="Maximize in-stock pantry/fridge ingredients."):
            quick_plan_mod = "Modify the plan to prioritize and maximize the usage of ingredients already in my fridge."
    with qp4:
        if st.button("🍛 More Indian Meals", use_container_width=True, help="Focus on traditional Indian home cooking."):
            quick_plan_mod = "Include more comforting, traditional Indian home-style meals and curries."

    if quick_plan_mod:
        mod_prompt = build_modify_meal_plan_prompt(
            current_meal_plan=generated_plan,
            user_request=quick_plan_mod,
            user_profile=profile,
            fridge_items=fridge_items
        )
        with st.spinner(f"🤖 Applying plan modification: '{quick_plan_mod}'..."):
            success, response_text = generate_ai_response(mod_prompt)
        if success:
            st.session_state.generated_meal_plan = response_text
            st.toast("Meal plan updated with quick action!", icon="✨")
            st.rerun()
        else:
            st.error(response_text)

    with st.form("modify_plan_form", clear_on_submit=True):
        mod_request = st.text_input("Custom Modification Request", placeholder="e.g., Make dinners lighter, replace Tuesday dinner, or increase protein")
        submit_mod = st.form_submit_button("✨ Modify Meal Plan", type="secondary", use_container_width=True)
        
    if submit_mod:
        if not mod_request.strip():
            st.warning("Please enter a modification request.")
        else:
            mod_prompt = build_modify_meal_plan_prompt(
                current_meal_plan=generated_plan,
                user_request=mod_request.strip(),
                user_profile=profile,
                fridge_items=fridge_items
            )
            with st.spinner(f"🤖 Applying changes: '{mod_request}'..."):
                success, response_text = generate_ai_response(mod_prompt)
                
            if success:
                st.session_state.generated_meal_plan = response_text
                st.toast("Plan modified successfully!", icon="✅")
                st.rerun()
            else:
                st.error(response_text)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Want step-by-step cooking instructions or ingredient substitutes?** Navigate to **Recipes** in the sidebar to generate personalized AI recipes and substitutions with Gemini.")

else:
    # Display Sample Preview Plan
    st.markdown(
        """
        <div class="demo-banner">
            <span>🗓️</span>
            <span><b>No AI meal plan generated yet.</b> Click <b>'✨ Generate Meal Plan'</b> above to create your personalized meal plan using your preferences and fridge ingredients.</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(f"### 🗓️ {num_days}-Day Sample Meal Schedule")
    days_to_show = st.session_state.get("meal_plan", [])[:num_days]
    
    for idx, day_info in enumerate(days_to_show):
        with st.container(border=True):
            h_col1, h_col2 = st.columns([3, 1])
            with h_col1:
                st.markdown(f"#### 📅 {day_info['day']}")
            with h_col2:
                st.markdown(f"<span class='badge badge-green'>{day_info.get('calories', '1,500 kcal')}</span>", unsafe_allow_html=True)
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown("🟡 **Breakfast**")
                st.write(day_info["breakfast"])
            with m2:
                st.markdown("🟢 **Lunch**")
                st.write(day_info["lunch"])
            with m3:
                st.markdown("🟣 **Dinner**")
                st.write(day_info["dinner"])
