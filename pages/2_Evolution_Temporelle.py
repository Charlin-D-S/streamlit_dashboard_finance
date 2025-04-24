import pandas as pd
import plotly.express as px

st.title("Évolution Temporelle")

df = pd.read_csv("data/worldbank_macro.csv")
fig = px.line(df.reset_index(), x='date', y='GDP', color='country')
st.plotly_chart(fig)
