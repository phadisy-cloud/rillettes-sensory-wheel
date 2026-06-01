import pandas as pd
import plotly.express as px
import streamlit as st

# Set widescreen layout configuration cleanly
st.set_page_config(page_title="Rillettes Sensory Wheel", layout="wide")

# ============================================================
# 1. CONSTANTS & SYSTEM CONFIGURATION
# ============================================================
CAT_APPEARANCE = "<b>Appearance</b>"
CAT_AROMA = "<b>Aroma</b>"
CAT_TASTE = "<b>Taste</b>"
CAT_TEXTURE = "<b>Texture</b>"
CAT_OVERALL = "<b>Overall</b>"

R_BASE = "Base Recipe"
R_1 = "Recipe 1"
R_2 = "Recipe 2"
R_3 = "Recipe 3"
R_4 = "Recipe 4"

RECIPE_COLORS = {
    R_BASE: "#A6A6A6",  # Grey
    R_1: "#F4B6ED",     # Light Pink
    R_2: "#D633B0",     # Magenta
    R_3: "#94C4EB",     # Light Blue
    R_4: "#4A004A"      # Deep Purple
}

FAMILY_TRACK_COLORS = {
    CAT_APPEARANCE: "#FFD966",   # Group 1: Bright Gold/Yellow
    CAT_AROMA:      "#F4C430",   # Group 2: Saffron Yellow
    CAT_TASTE:      "#FFEAA7",   # Group 3: Soft Pastel Yellow
    CAT_TEXTURE:    "#C29200",   # Group 4: Dark Amber Gold
    CAT_OVERALL:    "#FFF0C2"    # Group 5: Light Ivory Cream
}

# Strictly defined whitelist map ensuring descriptor-to-parent exclusivity
ALLOWED_ATTRIBUTES = {
    CAT_APPEARANCE: ["Pale", "Colorful", "Thick", "Particles", "Oily"],
    CAT_AROMA: ["Fish", "Shallot", "Vegetal", "Pepper", "Sulfur", "Weak aroma", "Strong aroma"],
    CAT_TASTE: ["Fish", "Fresh", "Spicy", "Salty"],
    CAT_TEXTURE: ["Smooth", "Liquid", "Granular", "Lumpy", "Sticky", "Easy swallowing", "Difficult swallowing"],
    CAT_OVERALL: ["Not appetizing", "Texture not great"]
}

# ============================================================
# 2. CLEANED DATASET
# ============================================================
RAW_DATA = [
    # --- BASE RECIPE ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Pale", "Recipe": R_BASE, "Value": 2, "Verbatim": "pale color; too pale"},
    {"Category": CAT_TEXTURE, "Descriptor": "Liquid", "Recipe": R_BASE, "Value": 2, "Verbatim": "liquid-like; un peu liquide"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Thick", "Recipe": R_BASE, "Value": 1, "Verbatim": "aspect de bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particles", "Recipe": R_BASE, "Value": 1, "Verbatim": "petites particules"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Oily", "Recipe": R_BASE, "Value": 2, "Verbatim": "brillant; huileux, gras"},
    {"Category": CAT_AROMA, "Descriptor": "Shallot", "Recipe": R_BASE, "Value": 1, "Verbatim": "échalotte"},
    {"Category": CAT_AROMA, "Descriptor": "Weak aroma", "Recipe": R_BASE, "Value": 2, "Verbatim": "très peu d’odeur; odeur équilibrée"},
    {"Category": CAT_TASTE, "Descriptor": "Fish", "Recipe": R_BASE, "Value": 2, "Verbatim": "goût de poisson pas très prononcé"},
    {"Category": CAT_TASTE, "Descriptor": "Fresh", "Recipe": R_BASE, "Value": 2, "Verbatim": "humide; frais; léger"},
    {"Category": CAT_TEXTURE, "Descriptor": "Easy swallowing", "Recipe": R_BASE, "Value": 1, "Verbatim": "fondant"},
    {"Category": CAT_TEXTURE, "Descriptor": "Lumpy", "Recipe": R_BASE, "Value": 1, "Verbatim": "texture un peu grumeleuse / collante"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granular", "Recipe": R_BASE, "Value": 1, "Verbatim": "peu granuleux"},
    {"Category": CAT_OVERALL, "Descriptor": "Not appetizing", "Recipe": R_BASE, "Value": 1, "Verbatim": "dommage que la couleur soit peu attractive"},

    # --- RECIPE 1 ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Thick", "Recipe": R_1, "Value": 1, "Verbatim": "Aspect de bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particles", "Recipe": R_1, "Value": 1, "Verbatim": "particule végétale agréable"},
    {"Category": CAT_AROMA, "Descriptor": "Strong aroma", "Recipe": R_1, "Value": 1, "Verbatim": "plus forte à l'ouverture"},
    {"Category": CAT_AROMA, "Descriptor": "Sulfur", "Recipe": R_1, "Value": 1, "Verbatim": "légère odeur fromagère; note soufrée"},
    {"Category": CAT_AROMA, "Descriptor": "Shallot", "Recipe": R_1, "Value": 1, "Verbatim": "échalote"},
    {"Category": CAT_AROMA, "Descriptor": "Weak aroma", "Recipe": R_1, "Value": 2, "Verbatim": "Peu d’odeur; Pas de véritable odeur"},
    {"Category": CAT_TASTE, "Descriptor": "Salty", "Recipe": R_1, "Value": 1, "Verbatim": "salé"},
    {"Category": CAT_TASTE, "Descriptor": "Spicy", "Recipe": R_1, "Value": 2, "Verbatim": "épicé avec ail un peu prononcé; poivré"},
    {"Category": CAT_TASTE, "Descriptor": "Fish", "Recipe": R_1, "Value": 1, "Verbatim": "Bon goût de poisson"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granular", "Recipe": R_1, "Value": 2, "Verbatim": "un peu plus granuleux; plus granuleux"},
    {"Category": CAT_TEXTURE, "Descriptor": "Lumpy", "Recipe": R_1, "Value": 1, "Verbatim": "plus grumelux"},
    {"Category": CAT_TEXTURE, "Descriptor": "Smooth", "Recipe": R_1, "Value": 1, "Verbatim": "moins crémeux / plus pâteux"},
    {"Category": CAT_OVERALL, "Descriptor": "Texture not great", "Recipe": R_1, "Value": 1, "Verbatim": "texture pas super"},

    # --- RECIPE 2 ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Thick", "Recipe": R_2, "Value": 1, "Verbatim": "Fait un peu bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Colorful", "Recipe": R_2, "Value": 2, "Verbatim": "Plus coloré (poireaux); belles couleurs"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particles", "Recipe": R_2, "Value": 1, "Verbatim": "particules végétales appréciées"},
    {"Category": CAT_AROMA, "Descriptor": "Pepper", "Recipe": R_2, "Value": 2, "Verbatim": "odeur de poivron de moyenne à forte"},
    {"Category": CAT_AROMA, "Descriptor": "Vegetal", "Recipe": R_2, "Value": 1, "Verbatim": "Bonne odeur d’aromates"},
    {"Category": CAT_AROMA, "Descriptor": "Weak aroma", "Recipe": R_2, "Value": 2, "Verbatim": "très faible; Je ne perçois pas d’odeur"},
    {"Category": CAT_AROMA, "Descriptor": "Fish", "Recipe": R_2, "Value": 1, "Verbatim": "poisson très présent"},
    {"Category": CAT_TASTE, "Descriptor": "Fish", "Recipe": R_2, "Value": 1, "Verbatim": "on ne sent pas le goût de poisson"},
    {"Category": CAT_TASTE, "Descriptor": "Salty", "Recipe": R_2, "Value": 1, "Verbatim": "salé"},
    {"Category": CAT_TASTE, "Descriptor": "Fresh", "Recipe": R_2, "Value": 1, "Verbatim": "Goût frais"},
    {"Category": CAT_TASTE, "Descriptor": "Spicy", "Recipe": R_2, "Value": 1, "Verbatim": "piquant"},
    {"Category": CAT_TEXTURE, "Descriptor": "Lumpy", "Recipe": R_2, "Value": 1, "Verbatim": "aspect un peu grumeleuse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Sticky", "Recipe": R_2, "Value": 1, "Verbatim": "collant aux dents"},
    {"Category": CAT_TEXTURE, "Descriptor": "Difficult swallowing", "Recipe": R_2, "Value": 1, "Verbatim": "moyen car beaucoup de grains"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granular", "Recipe": R_2, "Value": 1, "Verbatim": "plus granuleux"},
    {"Category": CAT_OVERALL, "Descriptor": "Texture not great", "Recipe": R_2, "Value": 1, "Verbatim": "la texture pourrait être améliorée"},

    # --- RECIPE 3 ---
    {"Category": CAT_TEXTURE, "Descriptor": "Smooth", "Recipe": R_3, "Value": 1, "Verbatim": "bien lisse mais pas liquide"},
    {"Category": CAT_TEXTURE, "Descriptor": "Liquid", "Recipe": R_3, "Value": 1, "Verbatim": "white and liquid-like"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Pale", "Recipe": R_3, "Value": 2, "Verbatim": "un peu pâle; pâle"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Thick", "Recipe": R_3, "Value": 1, "Verbatim": "aspect de bouillie"},
    {"Category": CAT_AROMA, "Descriptor": "Shallot", "Recipe": R_3, "Value": 1, "Verbatim": "échalote"},
    {"Category": CAT_AROMA, "Descriptor": "Fish", "Recipe": R_3, "Value": 1, "Verbatim": "arôme de poisson dominant"},
    {"Category": CAT_AROMA, "Descriptor": "Weak aroma", "Recipe": R_3, "Value": 2, "Verbatim": "odeur assez faible; aucune odeur"},
    {"Category": CAT_TASTE, "Descriptor": "Fish", "Recipe": R_3, "Value": 1, "Verbatim": "goût de poisson plus prononcé"},
    {"Category": CAT_TASTE, "Descriptor": "Fresh", "Recipe": R_3, "Value": 2, "Verbatim": "humide; frais"},
    {"Category": CAT_TASTE, "Descriptor": "Salty", "Recipe": R_3, "Value": 1, "Verbatim": "très salé"},
    {"Category": CAT_TEXTURE, "Descriptor": "Smooth", "Recipe": R_3, "Value": 2, "Verbatim": "très crémeux; on sent comme de la crème"},
    {"Category": CAT_TEXTURE, "Descriptor": "Easy swallowing", "Recipe": R_3, "Value": 1, "Verbatim": "fondant en bouche"},
    {"Category": CAT_TEXTURE, "Descriptor": "Lumpy", "Recipe": R_3, "Value": 1, "Verbatim": "texture un peu grumeleuse"},
    {"Category": CAT_OVERALL, "Descriptor": "Not appetizing", "Recipe": R_3, "Value": 1, "Verbatim": "not appealing"},

    # --- RECIPE 4 ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Thick", "Recipe": R_4, "Value": 1, "Verbatim": "Aspect de bouillie"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granular", "Recipe": R_4, "Value": 1, "Verbatim": "aspect granuleux"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Colorful", "Recipe": R_4, "Value": 1, "Verbatim": "de la couleur, particules vertes et rouges"},
    {"Category": CAT_AROMA, "Descriptor": "Weak aroma", "Recipe": R_4, "Value": 1, "Verbatim": "could be stronger"},
    {"Category": CAT_AROMA, "Descriptor": "Fish", "Recipe": R_4, "Value": 1, "Verbatim": "odeur de poisson"},
    {"Category": CAT_AROMA, "Descriptor": "Vegetal", "Recipe": R_4, "Value": 1, "Verbatim": "odeur végétale appréciée"},
    {"Category": CAT_TASTE, "Descriptor": "Fish", "Recipe": R_4, "Value": 1, "Verbatim": "Bon parfum gustatif de poisson"},
    {"Category": CAT_TASTE, "Recipe": R_4, "Descriptor": "Fresh", "Value": 1, "Verbatim": "plus frais"},
    {"Category": CAT_TASTE, "Descriptor": "Salty", "Recipe": R_4, "Value": 1, "Verbatim": "salty"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granular", "Recipe": R_4, "Value": 1, "Verbatim": "texture granuleuse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Sticky", "Recipe": R_4, "Value": 1, "Verbatim": "impression de coller aux dents"},
    {"Category": CAT_OVERALL, "Descriptor": "Texture not great", "Recipe": R_4, "Value": 1, "Verbatim": "texture moyenne"}
]

# ============================================================
# 3. INTERACTIVE ENGINE WITH GEOMETRY AND TEXT FIXED
# ============================================================
df = pd.DataFrame(RAW_DATA)

valid_rows = []
for idx, row in df.iterrows():
    cat = row["Category"]
    desc = row["Descriptor"]
    if cat in ALLOWED_ATTRIBUTES and desc in ALLOWED_ATTRIBUTES[cat]:
        valid_rows.append(row)

filtered_df = pd.DataFrame(valid_rows)

clean_df = (
    filtered_df.groupby(["Category", "Descriptor", "Recipe"], as_index=False)
    .agg({
        "Value": "sum",
        "Verbatim": lambda x: " | ".join(set(x.dropna()))
    })
)

fig = px.sunburst(
    clean_df,
    path=['Category', 'Descriptor', 'Recipe'], 
    values='Value',
    custom_data=['Verbatim'],
    title="sensory profile wheel of 5 recepes of rillettes",
)

ids = fig.data[0].ids
colors_assigned = []

for element_id in ids:
    parts = element_id.split('/')
    leaf = parts[-1]
    if leaf in RECIPE_COLORS:
        colors_assigned.append(RECIPE_COLORS[leaf])
    else:
        assigned_color = "#F2F2F2"
        for category, color in FAMILY_TRACK_COLORS.items():
            if element_id.startswith(category):
                assigned_color = color
                break
        colors_assigned.append(assigned_color)

fig.data[0].marker.colors = colors_assigned

# FIX applied here: Changed text orientation parameters to avoid corner crowding
fig.update_traces(
    textinfo="label",
    insidetextorientation='auto',  # Realigns skewed text segments nicely to their natural sector centers
    branchvalues="total",
    insidetextfont=dict(size=12, family="Arial, sans-serif"),
    hovertemplate="<b>Segment:</b> %{label}<br><b>Panel Mentions:</b> %{value}<br><br><i>Verbatims:</i><br>%{customdata[0]}<extra></extra>"
)

# Title perfectly centered over the plot canvas
fig.update_layout(
    margin=dict(t=80, l=10, r=10, b=10),
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=850,
    title_font=dict(size=24, family="Arial, sans-serif"),
    title_x=0.5,            
    title_xanchor='center', 
    title_yanchor='top'
)

st.plotly_chart(fig, use_container_width=True)
