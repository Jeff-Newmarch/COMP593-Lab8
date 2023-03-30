"""
Description:
 Generates a CSV reports containing all married couples in
 the Social Network database.

Usage:
 python marriage_report.py
"""
import os
import sqlite3
from create_relationships import db_path
import pandas as pd


def main():
    # Query DB for list of married couples
    married_couples = get_married_couples()

    # Save all married couples to CSV file
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'married_couples.csv')
    save_married_couples_csv(married_couples, csv_path)

def get_married_couples():
    """Queries the Social Network database for all married couples.

    Returns:
        list: (name1, name2, start_date) of married couples 
    """
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    all_relationships_query = f"""
        SELECT person1.name, person2.name, start_date, type FROM relationships 
        JOIN people person1 ON relationships.person1_id = person1.id
        JOIN people person2 ON relationships.person2_id = person2.id
        WHERE person1.id = person1_id AND person2.id = person2_id;
    """
    cur.execute(all_relationships_query)
    all_relationships = cur.fetchall()
    con.close()
    for person1, person2, start_date, spouse in all_relationships:
        print(f'{person1} has been a {spouse} of {person2} since {start_date}.')
    return (person1, person2, start_date)

def save_married_couples_csv(married_couples, csv_path):
    """Saves list of married couples to a CSV file, including both people's 
    names and their wedding anniversary date  

    Args:
        married_couples (list): (name1, name2, start_date) of married couples
        csv_path (str): Path of CSV file
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    married_couples = cur.fetchall()
    header_row = ('Person 1', 'Person 2', 'Anniversary')
    
    csv_path = pd.DataFrame(married_couples)
    csv_path.to_csv(f'married couples.csv', index=False, header=header_row)


if __name__ == '__main__':
   main()