import streamlit as st
import itertools
import pandas as pd
import altair as alt

st.title("ELO ranking system")
items = st.text_input('Please add the items to rank with , seperation. (e.g. item1, item2. item3, item4) ')

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
        st.write(f"Which item do you prefer: {item1} or {item2}?")
        choice = st.text_input(f'{i}: Enter your choice')

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

    if st.button('Show the results'):
        pd.set_option('display.precision', 2)
        ranking = pd.DataFrame(list(scores.items()), columns = ['items', 'scores'])
        ranking.scores = ranking.scores.astype(int)
        #st.write(ranking)
        st.write(ranking.sort_values(by='scores', ascending=False))
        chart = (
            alt.Chart(ranking, title='Comparison results')
            .mark_bar()
            .encode(
                x=alt.X('items', title=''), 
                y=alt.Y('scores', title='Rank'),
                color=alt.Color('variable', type='nominal')
            )
        )
        st.altair_chart(chart, use_container_width=True)
             