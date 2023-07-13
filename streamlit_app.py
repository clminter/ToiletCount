import streamlit as st
import math

def calculate_toilets(population, levels, level_populations, multipliers, level_multipliers, men_percentage):
    men_population = population * men_percentage / 100
    women_population = population - men_population

    men_urinals_per_level = []
    men_lavatories_per_level = []
    men_toilets_per_level = []
    women_toilets_per_level = []
    women_lavatories_per_level = []

    for i in range(levels):
        level_population = level_populations[i]
        level_percentage = level_population / population

        men_toilets = math.ceil(((1500 // 75) + ((men_population - 1500) // 120)) * multipliers["Men Toilets"] * level_multipliers[i])
        men_urinals = math.ceil(((1500 // 75) + ((men_population - 1500) // 120)) * multipliers["Men Urinals"] * level_multipliers[i])
        men_lavatories = math.ceil(men_population // 200) * level_multipliers[i]

        women_lavatories = math.ceil(women_population // 150) * level_multipliers[i]
        women_toilets = math.ceil((1520 // 40) + ((women_population - 1520) // 60)) * multipliers["Women Toilets"] * level_multipliers[i]

        men_urinals_per_level.append(math.ceil(men_urinals * level_percentage))
        men_lavatories_per_level.append(math.ceil(men_lavatories * level_percentage))
        men_toilets_per_level.append(math.ceil(men_toilets * level_percentage))
        women_toilets_per_level.append(math.ceil(women_toilets * level_percentage))
        women_lavatories_per_level.append(math.ceil(women_lavatories * level_percentage))

    return {
        "Men Urinals": men_urinals_per_level,
        "Men Lavatories": men_lavatories_per_level,
        "Men Toilets": men_toilets_per_level,
        "Women Toilets": women_toilets_per_level,
        "Women Lavatories": women_lavatories_per_level
    }

def main():
    st.title(" 🚻 POPULOUS RESTROOM BOT")
    st.write(" ⚠️ Stadium and Arena fixture calculations based on IBC 2021 Assembly Classification  ⚠️ ")
    st.write("A MINTER 🤖")

    population = st.number_input("Enter the total population", min_value=1, value=100)
    men_percentage = st.slider("Percentage of Men", 0, 100, 50, 5)
   
    levels = st.number_input("Enter the number of levels in the building", min_value=1, value=1)

    level_names = []
    level_populations = []
    level_multipliers = []

    with st.sidebar:
        st.subheader("Level Names and Populations")
        for i in range(levels):
            level_name = st.text_input(f"Enter the name of Level {i+1}")
            level_names.append(level_name)

            level_percentage = st.empty()
            level_pop = st.number_input(f"Enter the population on Level {i+1}", min_value=1, value=1)
            level_populations.append(level_pop)
            level_percentage.markdown(f"Population Percentage: {level_pop / population * 100:.2f}%")

            level_multiplier = st.slider(f"Enter the PREMIUM multiplier for Level {i+1}", 1.0, 3.0, 1.0, 0.25)
            level_multipliers.append(level_multiplier)

    with st.expander("Fixture Type Multipliers: Adjust to increase over Code"):
        multipliers = {
            "Men Urinals": st.slider("Men Urinals Multiplier", 1.0, 5.0, 1.0, 0.1),
            "Men Lavatories": st.slider("Men Lavatories Multiplier", 1.0, 5.0, 1.0, 0.1),
            "Men Toilets": st.slider("Men Toilets Multiplier", 1.0, 5.0, 1.0, 0.1),
            "Women Toilets": st.slider("Women Toilets Multiplier", 1.0, 5.0, 1.0, 0.1),
            "Women Lavatories": st.slider("Women Lavatories Multiplier", 1.0, 5.0, 1.0, 0.1)
        }

    if st.button("Calculate"):
        result = calculate_toilets(population, levels, level_populations, multipliers, level_multipliers, men_percentage)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Fixtures per Level:")
            for i in range(levels):
                st.markdown(f"**<span style='font-size:20px'>{level_names[i]}</span>**", unsafe_allow_html=True)
                st.write(f"🚹Men Urinals: {result['Men Urinals'][i]} (1:{(level_populations[i] // 2) // result['Men Urinals'][i]})")
                st.write(f"🚹Men Lavatories: {result['Men Lavatories'][i]} (1:{(level_populations[i] // 2) // result['Men Lavatories'][i]})")
                st.write(f"🚹Men Toilets: {result['Men Toilets'][i]} (1:{(level_populations[i] // 2) // result['Men Toilets'][i]})")
                st.write(f"🚺Women Toilets: {result['Women Toilets'][i]} (1:{(level_populations[i] // 2) // result['Women Toilets'][i]})")
                st.write(f"🚺Women Lavatories: {result['Women Lavatories'][i]} (1:{(level_populations[i] // 2) // result['Women Lavatories'][i]})")

        with col2:
            st.subheader("Total Fixtures:")
            total_urinals = sum(result['Men Urinals'])
            total_lavatories = sum(result['Men Lavatories'])
            total_toilets = sum(result['Men Toilets'])
            total_women_toilets = sum(result['Women Toilets'])
            total_women_lavatories = sum(result['Women Lavatories'])

            st.write(f"🚹Total Men Urinals: {total_urinals} (1:{(population // 2) // total_urinals})")
            st.write(f"🚹Total Men Lavatories: {total_lavatories} (1:{(population // 2) // total_lavatories})")
            st.write(f"🚹Total Men Toilets: {total_toilets} (1:{(population // 2) // total_toilets})")
            st.write(f"🚺Total Women Toilets: {total_women_toilets} (1:{(population // 2) // total_women_toilets})")
            st.write(f"🚺Total Women Lavatories: {total_women_lavatories} (1:{(population // 2) // total_women_lavatories})")

if __name__ == "__main__":
    main()
