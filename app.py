import streamlit as st

theme_available = [
    "Abstractionism", "Artist_Sketch", "Blossom_Season", "Bricks", "Byzantine", "Cartoon",
    "Cold_Warm", "Color_Fantasy", "Comic_Etch", "Crayon", "Cubism", "Dadaism", "Dapple",
    "Defoliation", "Early_Autumn", "Expressionism", "Fauvism", "French", "Glowing_Sunset",
    "Gorgeous_Love", "Greenfield", "Impressionism", "Ink_Art", "Joy", "Liquid_Dreams",
    "Magic_Cube", "Meta_Physics", "Meteor_Shower", "Monet", "Mosaic", "Neon_Lines", "On_Fire",
    "Pastel", "Pencil_Drawing", "Picasso", "Pop_Art", "Red_Blue_Ink", "Rust", "Seed_Images",
    "Sketch", "Sponge_Dabbed", "Structuralism", "Superstring", "Surrealism", "Ukiyoe",
    "Van_Gogh", "Vibrant_Flow", "Warm_Love", "Warm_Smear", "Watercolor", "Winter",
]

class_available = [
    "Architectures", "Bears", "Birds", "Butterfly", "Cats", "Dogs", "Fishes", "Flame", "Flowers",
    "Frogs", "Horses", "Human", "Jellyfish", "Rabbits", "Sandwiches", "Sea", "Statues", "Towers",
    "Trees", "Waterfalls",
]

# Dummy model “config” – just names to keep the UI structure
original_display_name = "Original (dummy, no unlearning)"
theme_model_for = {key: f"Style Unlearned (dummy): {key}" for key in theme_available}
class_model_for = {key: f"Object Unlearned (dummy): {key}" for key in class_available}
other_models = {"Mickey Mouse"}

# -----------------------------------------------------------------------------
# Dummy image generation – returns a random internet image URL
# -----------------------------------------------------------------------------

def get_random_image_url(seed: int | None = None, width: int = 512, height: int = 512) -> str:
    """
    Return a random image URL from the internet.
    Uses picsum.photos; the seed makes it deterministic for a given value.
    """

    # picsum for a stable random image for a given seed.
    return f"https://picsum.photos/seed/{seed}/{width}/{height}"


def generate_image_dummy(
    model_name: str,
    prompt: str | None,
    seed: int,
    H: int,
    W: int,
):
    """
    Dummy generate: ignore model and prompt, just return a random image URL.
    """
    image_url = get_random_image_url(seed=seed, width=W, height=H)
    used_prompt = prompt or "(no prompt)"
    used_model = model_name or "(no model selected)"
    return image_url, used_prompt, used_model


# -----------------------------------------------------------------------------
# Streamlit UI
# -----------------------------------------------------------------------------

st.set_page_config(page_title="Unlearning Styles Demo (Dummy)", layout="wide")

st.title("Machine Unlearning Demo - Styles and Objects (Dummy Version)")

# ---------------------------------------------------------------------
# Sidebar – model selection 
# ---------------------------------------------------------------------

st.sidebar.header("Model selection")

model_family_options = []
if original_display_name is not None:
    model_family_options.append("Original")
if theme_model_for:
    model_family_options.append("Style Unlearned")
if class_model_for:
    model_family_options.append("Object Unlearned")
if other_models:
    model_family_options.append("Other")

model_family = st.sidebar.radio(
    "Which model family?",
    model_family_options,
    label_visibility="hidden",
)

selected_model_display_name = None

if model_family == "Original":
    st.sidebar.markdown(f"**Using Model:**  \n {original_display_name}")
    selected_model_display_name = original_display_name

elif model_family == "Style Unlearned":
    available_theme_keys = sorted(theme_model_for.keys())
    chosen_theme_model = st.sidebar.selectbox(
        "Unlearned style model",
        available_theme_keys,
    )
    selected_model_display_name = theme_model_for[chosen_theme_model]
    st.sidebar.markdown(f"**Using Model:**  \n {selected_model_display_name}")

elif model_family == "Object Unlearned":
    available_class_keys = sorted(class_model_for.keys())
    chosen_class_model = st.sidebar.selectbox(
        "Unlearned object model",
        available_class_keys,
    )
    selected_model_display_name = class_model_for[chosen_class_model]
    st.sidebar.markdown(f"**Using Model:**  \n {selected_model_display_name}")

elif model_family == "Other":
    other_list = sorted(other_models)
    selected_model_display_name = st.sidebar.selectbox(
        "Other models",
        other_list,
    )

# ---------------------------------------------------------------------
# Sidebar – “Generation settings” 
# ---------------------------------------------------------------------

st.sidebar.header("Generation settings")

seed = st.sidebar.number_input("Random seed", value=256, step=1)
# These are left here for UI continuity; they are not actually used
steps = 100
cfg_text = 9.0
H = 512
W = 512
ddim_eta = 0.0

st.sidebar.markdown(
    "<sub>Note: In this dummy version, these settings do not affect the image.</sub>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# Prompt selection
# ---------------------------------------------------------------------

prompt_mode = st.radio(
    "Prompt mode",
    ["Preset Style/Object", "Free Text Prompt"],
    horizontal=True,
)

if prompt_mode == "Preset Style/Object":
    st.subheader("Style")
    theme = st.pills("Choose style", theme_available)

    st.subheader("Object")
    object_class = st.pills("Choose object", class_available)

    prompt = None
    if theme and object_class:
        prompt = f"A {object_class} image in {theme.replace('_', ' ')} style."
else:
    st.subheader("Free Text Prompt")
    prompt = st.text_area(
        "Enter your prompt",
        placeholder="e.g., A beautiful sunset over mountains, digital art",
        height=100,
    )
    theme = None
    object_class = None

st.markdown("---")

# ---------------------------------------------------------------------
# Generate button 
# ---------------------------------------------------------------------

if st.button("Generate"):
    if selected_model_display_name is None:
        st.error("Please select a model in the sidebar.")
    elif prompt_mode == "Preset Style/Object":
        if theme is None:
            st.error("Please select a style.")
        elif object_class is None:
            st.error("Please select an object.")
        else:
            with st.spinner("Fetching a random image from the internet..."):
                image_url, used_prompt, used_model = generate_image_dummy(
                    model_name=selected_model_display_name,
                    prompt=prompt,
                    seed=int(seed),
                    H=int(H),
                    W=int(W),
                )

            st.image(
                image_url,
                caption=f"Model (dummy): {used_model} | Prompt: {used_prompt}",
            )
    else:  # Free Text Prompt mode
        if not prompt or not prompt.strip():
            st.error("Please enter a prompt.")
        else:
            with st.spinner("Fetching a random image from the internet..."):
                image_url, used_prompt, used_model = generate_image_dummy(
                    model_name=selected_model_display_name,
                    prompt=prompt.strip(),
                    seed=int(seed),
                    H=int(H),
                    W=int(W),
                )

            st.image(
                image_url,
                caption=f"Model (dummy): {used_model} | Prompt: {used_prompt}",
            )
