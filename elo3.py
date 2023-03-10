import streamlit as st
import itertools
import pandas as pd
import altair as alt

st.title("ELO ranking system")
st.write('Elo ratings are comparative only to rate the items in a given pool. After the comparative selection, the Elo rating formula calculates the score for every given items')
items = st.text_input('Introduce the items to the box below. Seperate items with a comma please.(e.g. item1, item2. item3, item4)')

if st.button:
    #items.append(item)
    item_list = items.split(",")
    k = 32
    scores = {item: 100 for item in item_list}
    comparison_pairs = list(itertools.combinations(item_list,2))

    #for comparison in comparison_pairs:
    #   st.write(comparison)

    
    i = 0
    for item1, item2 in comparison_pairs:
        i+=1
        # Ask the user to choose the preferred item
        #st.write(f"Which item do you prefer: {item1} or {item2}?")
        items = item1, item2
        choice = st.radio(label='Which item do you prefer?',options=items)

        if choice == item1:
            winner, loser = item1, item2
        elif choice == item2:
            winner, loser = item2, item1
        else:
            st.error("Invalid input, please choose one of the items")
            continue
        expected_score_winner = 1 / (1 + 10 ** ((scores[loser] - scores[winner]) / 400))
        expected_score_loser = 1 / (1 + 10 ** ((scores[winner] - scores[loser]) / 400))
        scores[winner] += k * (1 - expected_score_winner)
        scores[loser] += k * (0 - expected_score_loser)
        #st.success(f"{winner} score: {scores[winner]}, {loser} score: {scores[loser]}")

    if st.button('Start ranking'):
        pd.set_option('display.precision', 2)
        ranking = pd.DataFrame(list(scores.items()), columns = ['items', 'scores'])
        ranking.scores = ranking.scores.astype(int)
        
        
        col1,col2 = st.columns(2)
        

        chart = (
            alt.Chart(ranking, title='Comparison results')
            .mark_bar()
            .encode(
                x=alt.X('items', title=''), 
                y=alt.Y('scores', title='Rank'),
                color=alt.Color('variable', type='nominal')
            )
        )
        col1.altair_chart(chart, use_container_width=True)

        #st.write(ranking)
        col2.write(ranking.sort_values(by='scores', ascending=False))



footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;' href="https://www.linkedin.com/in/ugurkayran/" target="_blank">Ugur Kayran</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)