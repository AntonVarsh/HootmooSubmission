import os
import streamlit as st
import replicate
import openai
os.environ["REPLICATE_API_TOKEN"] = "r8_QgVoRNJeicYI95tVYunvlpKJzJVFCAe47uzdH"
openai.api_key = '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'
st.title("Hootmoo - Experience The World!")
st.text("Dont press next until all of your animals have been generated please")
st.markdown("---")
def generate_image(prompt):
    output = replicate.run(
        "stability-ai/sdxl:d830ba5dabf8090ec0db6c10fc862c6eb1c929e1a194a5411852d25fd954ac82",
        input={"prompt": f"a {prompt}, cute, family friendly, realistic", "negative_prompt":"scary, evil, horrible, ugly, disfigured, disgusting, destroyed"}
    )
    st.text("Done! Creating audio.")
    return output[0]
st.session_state.setdefault("sounds", ["koala.mp3", "panda.mp3"])
st.session_state.setdefault("animals", ["koala", "panda"])
st.session_state.setdefault("animal_images", ["koala.png", "panda.png"])
st.session_state.setdefault("current_animal_index", 0)
def audio(animal):
    st.text(f"generating {animal} sound")
    output = replicate.run(
        "sepal/audiogen:154b3e5141493cb1b8cec976d9aa90f2b691137e39ad906d2421b74c2a8c52b8",
        input={"prompt": f"{animal} making the sound that {animal} makes"}
    )
    st.text("Done! Press \"Next\" to see your result!")
    return output
# Create a placeholder for the image
image_placeholder = st.empty()
# Create two columns for buttons
col1, col2 = st.columns([1, 1])
# Create the "Back" and "Next" buttons in their respective columns
with col1:
    back_button = st.button("Back")
with col2:
    next_button = st.button("Next")
def new_animal_generation_calls(new_animals):
    animals_to_generate = []
    for animal in new_animals:
        if animal not in st.session_state.animals:
            st.session_state.animals.append(animal)
            st.text(f"Generating {animal}")
            st.session_state.animal_images.append(generate_image(animal))
            st.session_state.animals.append(animal)
            st.session_state.sounds.append(audio(animal))
    new_animals = []
def generate_animals(animals):
    new_animals = []
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"write a list of 5 animals, make sure they arent in this list:{animals}. Format it as a python list"}],
        temperature=.88
    )
    total_tokens_used_c = response['usage']['total_tokens']
    price = (total_tokens_used_c / 1000) * .0015
    actual_response = response['choices'][0]['message']['content']
    for choice in actual_response.strip('[]').replace("'", '').split(', '):
        new_animals.append(choice) # st.session_state.animals.append(choice)
    new_animal_generation_calls(new_animals)
# Initialize the current animal index using session state
if 'current_animal_index' not in st.session_state:
    st.session_state.current_animal_index = 0
# Update the animal image when the "Next" button is clicked
if next_button:
    st.session_state.current_animal_index = (st.session_state.current_animal_index + 1) % len(st.session_state.animal_images)
elif back_button:
    st.session_state.current_animal_index = (st.session_state.current_animal_index - 1) % len(st.session_state.animal_images)
# Display the current animal image
image_placeholder.image(st.session_state.animal_images[st.session_state.current_animal_index])
st.audio(st.session_state.sounds[st.session_state.current_animal_index],
         format='audio/mp3')
options = st.button("Generate Random Animals")
if options:
    generate_animals(st.session_state.animals)
own = st.text_input("Add Your Own Animals! (comma separated)")
if own != "":
    new_animals = own.split(",")
    own = st.empty()
    new_animal_generation_calls(new_animals)

st.markdown("---")
