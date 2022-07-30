import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
w_mask = df['weight'] / ((df['height'] / 100) ** 2) > 25
df.loc[w_mask, 'overweight'] = 1
df.loc[~w_mask, 'overweight'] = 0

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1
df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
  necessary_list = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
  df_cat = pd.melt(df, id_vars=["cardio"], value_vars = necessary_list)


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
  df_cat = df_cat.reset_index().groupby(['cardio', 'variable', 'value']).size().reset_index().rename(columns={0:'total'})
    

    # Draw the catplot with 'sns.catplot()'



    # Get the figure for the output
  fig = sns.catplot(x = 'variable', y = 'total', data = df_cat, col = 'cardio', kind = 'bar', hue = 'value').fig


    # Do not modify the next two lines
  fig.savefig('catplot.png')
  return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
  pr_mask = (df['ap_lo'] <= df['ap_hi'])
  lo_h_mask = (df['height'] >= df['height'].quantile(0.025))
  hi_h_mask = (df['height'] <= df['height'].quantile(0.975))
  lo_w_mask = (df['weight'] >= df['weight'].quantile(0.025))
  hi_w_mask = (df['weight'] <= df['weight'].quantile(0.975))

  df_heat = df.loc[pr_mask & lo_h_mask & hi_h_mask & lo_w_mask & hi_w_mask]

    # Calculate the correlation matrix
  corr = df_heat.corr()

    # Generate a mask for the upper triangle
  mask = np.triu(corr)



    # Set up the matplotlib figure
  fig, ax = plt.subplots(figsize=(18, 9))
  sns.heatmap(corr, ax = ax, annot = True, fmt = '.1f' ,  mask = mask, center = 0, square = True, linecolor = 'w', linewidth = 1, vmin = -0.1, vmax = 0.3)
    # Draw the heatmap with 'sns.heatmap()'



    # Do not modify the next two lines
  fig.savefig('heatmap.png')
  return fig
