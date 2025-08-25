import requests
from bs4 import BeautifulSoup
import pandas as pd
url="https://www.iplt20.com/auction/2022"
r=requests.get(url)
#print(r) if 200 we can get
soup = BeautifulSoup(r.text,"lxml")
#print(soup)
table = soup.find("table",class_ ="ih-td-tab w-100 auction-tbl")
#print(table)
title = soup.table("th")
#print(title)
header=[]
for i in title:
    name = i.text
    header.append(name)
df=pd.DataFrame(columns=header)
#print(row)
rows=table.find_all("tr")
#print(row)
for i in rows[1:]:
    # First, try to find the container div
    # Your original code to get the rows
    rows = table.find_all("tr")

    # Loop through each row, skipping the header
    for i in rows[1:]:
        # Find all cells in the current row
        all_cells = i.find_all("td")
        # 1. Get the team name specifically from the <h2> tag in the second cell (index 1)
        team_name = all_cells[1].find("h2").text.strip()
        # 2. Get the funds from the third cell (index 2) and remove the bad characters
        funds = all_cells[2].text.strip().replace('â,¹', '')
        # 3. Get the text from all other cells
        # We will replace the original team and funds data with our clean versions
        row_data = [cell.text.strip() for cell in all_cells]
        row_data[1] = team_name
        row_data[2] = funds
        l = len(df)
        df.loc[l] = row_data

    print(df)
    l = len(df)
    df.loc[l] = row_data

print(df)
df.to_csv("ipl auction stats4.csv")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
# Make sure 'ipl auction stats4.csv' is in the same directory as your script
df = pd.read_csv('ipl auction stats4.csv')

# --- Data Cleaning ---

# There are leading spaces in the column names. Let's fix that.
df.columns = df.columns.str.strip()

# Drop the 'Unnamed: 0' and 'SR. NO.' columns as they are not needed for this analysis
df_cleaned = df.drop(columns=['Unnamed: 0', 'SR. NO.'])

# Remove duplicate rows to ensure data integrity
df_cleaned = df_cleaned.drop_duplicates()

# The 'FUNDS REMAINING' column is a string with currency symbols and commas.
# We need to convert it to a number to perform calculations.
df_cleaned['FUNDS REMAINING'] = df_cleaned['FUNDS REMAINING'].str.replace('₹', '').str.replace(',', '').astype(float)

# --- Exploratory Data Analysis (EDA) ---

# Display summary statistics (mean, standard deviation, etc.) for the numerical columns
print("Summary Statistics:")
print(df_cleaned.describe())

# Set a visually appealing style for the plots
sns.set_style("whitegrid")

# 1. Bar plot for FUNDS REMAINING by TEAM
# This helps us see which teams have the most and least money left.
plt.figure(figsize=(12, 6))
sns.barplot(x='TEAM', y='FUNDS REMAINING', data=df_cleaned.sort_values('FUNDS REMAINING', ascending=False))
plt.xticks(rotation=45, ha='right')
plt.title('Funds Remaining for Each Team')
plt.xlabel('Team')
plt.ylabel('Funds Remaining (in Crores)')
plt.tight_layout()
plt.savefig('funds_remaining.png')


# 2. Bar plot for TOTAL PLAYERS by TEAM
# This shows the squad size for each team.
plt.figure(figsize=(12, 6))
sns.barplot(x='TEAM', y='TOTAL PLAYERS', data=df_cleaned.sort_values('TOTAL PLAYERS', ascending=False), palette='viridis')
plt.xticks(rotation=45, ha='right')
plt.title('Total Players for Each Team')
plt.xlabel('Team')
plt.ylabel('Number of Players')
plt.tight_layout()
plt.savefig('total_players.png')


# 3. Bar plot for OVERSEAS PLAYERS by TEAM
# This visualizes the number of foreign players in each team.
plt.figure(figsize=(12, 6))
sns.barplot(x='TEAM', y='OVERSEAS PLAYERS', data=df_cleaned.sort_values('OVERSEAS PLAYERS', ascending=False), palette='plasma')
plt.xticks(rotation=45, ha='right')
plt.title('Overseas Players for Each Team')
plt.xlabel('Team')
plt.ylabel('Number of Overseas Players')
plt.tight_layout()
plt.savefig('overseas_players.png')


# 4. Correlation Heatmap
# This shows if there's a relationship between the numerical features.
# For example, we can see if teams with more players have less money.
plt.figure(figsize=(8, 6))
correlation_df = df_cleaned[['FUNDS REMAINING', 'OVERSEAS PLAYERS', 'TOTAL PLAYERS']]
correlation_matrix = correlation_df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Numerical Features')
plt.savefig('correlation_heatmap.png')

print("\nEDA visualizations have been generated and saved as PNG files.")
