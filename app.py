import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

# Initialize session state
if 'current_session' not in st.session_state:
    st.session_state.current_session = {
        'bean_name': '',
        'grinder': '',
        'dose': 18.0,
        'grind_size': 5.0,
        'pre_infusion_time': 5.0,
        'yield': 36.0,
        'shot_time': 30.0,
        'sourness': 3,
        'bitterness': 3,
        'sweetness': 3,
        'body': 3,
        'overall_satisfaction': 3,
        'notes': '',
        'favorite': False
    }

# Load or create CSV file
CSV_FILE = 'brew_log.csv'
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=[
        'timestamp', 'bean_name', 'grinder', 'dose', 'grind_size', 'pre_infusion_time',
        'yield', 'shot_time', 'sourness', 'bitterness', 'sweetness', 'body',
        'overall_satisfaction', 'notes', 'suggestions', 'favorite'
    ])
    df.to_csv(CSV_FILE, index=False)
else:
    df = pd.read_csv(CSV_FILE)

# Function to get brew suggestions
def get_brew_suggestions(session):
    suggestions = []
    changes = {}
    
    # Too Sour
    if session['sourness'] >= 4:
        sour_suggestions = [
            "→ Grind finer (decrease grind size by 0.5)"
        ]
        suggestions.append(f"- Too sour:\n" + "\n".join(sour_suggestions))
        changes['grind_size'] = session['grind_size'] - 0.5
    
    # Too Bitter
    elif session['bitterness'] >= 4:
        bitter_suggestions = [
            "→ Grind coarser (increase grind size by 0.5)"
        ]
        suggestions.append(f"- Too bitter:\n" + "\n".join(bitter_suggestions))
        changes['grind_size'] = session['grind_size'] + 0.5
    
    # Too Weak or Bland
    elif session['sweetness'] <= 2 and session['body'] <= 2:
        weak_suggestions = [
            "→ Increase dose by 0.5g"
        ]
        suggestions.append(f"- Too weak or bland:\n" + "\n".join(weak_suggestions))
        changes['dose'] = session['dose'] + 0.5
    
    # Too Aggressive or Overpowering
    elif (session['bitterness'] + session['sourness']) >= 8 and session['body'] >= 4:
        aggressive_suggestions = [
            "→ Reduce dose by 0.5g"
        ]
        suggestions.append(f"- Too aggressive or overpowering:\n" + "\n".join(aggressive_suggestions))
        changes['dose'] = session['dose'] - 0.5
    
    # Good Sweetness but Still Unbalanced
    elif session['sweetness'] >= 4 and session['bitterness'] >= 3:
        unbalanced_suggestions = [
            "→ Increase yield by 2g"
        ]
        suggestions.append(f"- Good sweetness but still unbalanced:\n" + "\n".join(unbalanced_suggestions))
        changes['yield'] = session['yield'] + 2
    
    return "\n\n".join(suggestions) if suggestions else "Brew looks balanced! Keep these parameters.", changes

# Main app layout
st.title("☕ EspressoLog")

# Dial-In Input Section
st.header("1. Dial-In Input")
col1, col2 = st.columns(2)

with col1:
    st.session_state.current_session['bean_name'] = st.text_input("Bean Name", value=st.session_state.current_session['bean_name'])
    st.session_state.current_session['grinder'] = st.text_input("Grinder", value=st.session_state.current_session['grinder'])
    st.session_state.current_session['dose'] = st.number_input("Dose (g)", min_value=0.0, max_value=30.0, value=st.session_state.current_session['dose'], step=0.1)
    st.session_state.current_session['grind_size'] = st.number_input("Grind Size", value=st.session_state.current_session['grind_size'], step=0.5)

with col2:
    st.session_state.current_session['pre_infusion_time'] = st.number_input("Pre-infusion Time (s)", min_value=0.0, max_value=30.0, value=st.session_state.current_session['pre_infusion_time'], step=0.1)
    st.session_state.current_session['yield'] = st.number_input("Yield (g)", min_value=0.0, max_value=100.0, value=st.session_state.current_session['yield'], step=0.1)
    st.session_state.current_session['shot_time'] = st.number_input("Shot Time (s)", min_value=0.0, max_value=60.0, value=st.session_state.current_session['shot_time'], step=0.1)

# Save & Brew button
if st.button("Save & Brew"):
    st.session_state.brewing = True
    st.success("Session saved! Now you can rate your brew.")
    st.rerun()

# Post-Brew Rating Section
if 'brewing' in st.session_state and st.session_state.brewing:
    st.header("2. Post-Brew Rating")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.current_session['sourness'] = st.slider(
            "Sourness (1-5)", 
            min_value=1, 
            max_value=5, 
            value=st.session_state.current_session['sourness'],
            help="High = sharp, tangy, acidic. Low = mellow or flat."
        )
        st.session_state.current_session['bitterness'] = st.slider(
            "Bitterness (1-5)", 
            min_value=1, 
            max_value=5, 
            value=st.session_state.current_session['bitterness'],
            help="High = harsh, burnt, over-extracted. Low = smooth."
        )
        st.session_state.current_session['sweetness'] = st.slider(
            "Sweetness (1-5)", 
            min_value=1, 
            max_value=5, 
            value=st.session_state.current_session['sweetness'],
            help="High = chocolate, caramel, fruit. Low = dry or hollow taste."
        )
    
    with col2:
        st.session_state.current_session['body'] = st.slider(
            "Body (1-5)", 
            min_value=1, 
            max_value=5, 
            value=st.session_state.current_session['body'],
            help="High = rich, syrupy, thick. Low = watery or thin."
        )
        st.session_state.current_session['overall_satisfaction'] = st.slider(
            "Overall Satisfaction (1-5)", 
            min_value=1, 
            max_value=5, 
            value=st.session_state.current_session['overall_satisfaction'],
            help="Personal taste score (can be used to favorite top brews)"
        )
    
    st.session_state.current_session['notes'] = st.text_area("Notes", value=st.session_state.current_session['notes'])
    st.session_state.current_session['favorite'] = st.checkbox("Mark as Favorite", value=st.session_state.current_session['favorite'])
    
    if st.button("Get Suggestions"):
        suggestions, changes = get_brew_suggestions(st.session_state.current_session)
        st.info(suggestions)
        
        # Display suggested changes in a table
        if changes:
            st.subheader("Suggested Change")
            current_values = {
                'Parameter': list(changes.keys()),
                'Current': [st.session_state.current_session[k] for k in changes.keys()],
                'Suggested': [changes[k] for k in changes.keys()]
            }
            st.table(pd.DataFrame(current_values))
        
        # Save to CSV
        new_row = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **{k: v for k, v in st.session_state.current_session.items() if k != 'favorite'},
            'suggestions': suggestions,
            'favorite': st.session_state.current_session['favorite']
        }
        
        # Read the current CSV file to get the latest data
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
        else:
            df = pd.DataFrame(columns=[
                'timestamp', 'bean_name', 'grinder', 'dose', 'grind_size', 'pre_infusion_time',
                'yield', 'shot_time', 'sourness', 'bitterness', 'sweetness', 'body',
                'overall_satisfaction', 'notes', 'suggestions', 'favorite'
            ])
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success("Session saved to log!")
        st.session_state.brewing = False  # Reset brewing state
        st.rerun()  # Rerun the app to show the updated table

# Historical Brews Table
st.header("3. Historical Brews")
if not df.empty:
    # Add a selection column for deletion
    if 'selected_for_deletion' not in df.columns:
        df['selected_for_deletion'] = False
    
    # Reorder columns to put favorite and selection first
    column_order = ['selected_for_deletion', 'favorite'] + [col for col in df.columns if col not in ['selected_for_deletion', 'favorite']]
    df_display = df[column_order]
    
    edited_df = st.data_editor(
        df_display.sort_values('timestamp', ascending=False),
        column_config={
            "selected_for_deletion": st.column_config.CheckboxColumn(
                "Select",
                help="Select records to delete",
                default=False
            ),
            "favorite": st.column_config.CheckboxColumn(
                "Favorite",
                help="Mark your favorite brews",
                default=False
            ),
            "timestamp": "Timestamp",
            "bean_name": "Bean",
            "grinder": "Grinder",
            "dose": "Dose (g)",
            "grind_size": "Grind",
            "pre_infusion_time": "Pre-infusion (s)",
            "yield": "Yield (g)",
            "shot_time": "Time (s)",
            "sourness": "Sourness",
            "bitterness": "Bitterness",
            "sweetness": "Sweetness",
            "body": "Body",
            "overall_satisfaction": "Overall",
            "notes": "Notes",
            "suggestions": "Suggestions"
        },
        hide_index=True,
        disabled=["timestamp", "bean_name", "grinder", "dose", "grind_size", 
                 "pre_infusion_time", "yield", "shot_time", "sourness", 
                 "bitterness", "sweetness", "body", "overall_satisfaction", 
                 "notes", "suggestions"]
    )
    
    # Create columns for the buttons with adjusted widths
    col1, col2, col3, col4 = st.columns([2, 2, 4, 4])
    
    with col1:
        if st.button("Select All", use_container_width=True):
            edited_df['selected_for_deletion'] = True
            st.rerun()
    
    with col2:
        if st.button("Deselect All", use_container_width=True):
            edited_df['selected_for_deletion'] = False
            st.rerun()
    
    with col3:
        # Add delete button for batch deletion
        selected_count = edited_df['selected_for_deletion'].sum()
        if selected_count > 0:
            if st.button(f"Delete Selected ({selected_count} records)", use_container_width=True):
                # Keep only unselected records
                df = edited_df[edited_df['selected_for_deletion'] == False].drop('selected_for_deletion', axis=1)
                df.to_csv(CSV_FILE, index=False)
                st.success(f"{selected_count} records deleted successfully!")
                st.rerun()
    
    # Update favorites in the original dataframe
    df['favorite'] = edited_df['favorite']
    df.to_csv(CSV_FILE, index=False)
    
    # Load previous session
    st.subheader("Load Previous Session")
    selected_index = st.selectbox(
        "Select a session to load",
        range(len(df)),
        format_func=lambda x: f"{df.iloc[x]['bean_name']} - {df.iloc[x]['timestamp']}"
    )
    
    if st.button("Load Selected Session"):
        selected_session = df.iloc[selected_index]
        for key in st.session_state.current_session:
            if key in selected_session:
                st.session_state.current_session[key] = selected_session[key]
        st.success("Session loaded!")
else:
    st.info("No previous brews logged yet.") 