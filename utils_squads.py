def get_squad(y, data, print_squad=True):
    cols = ['name', 'player_type', 'generic_position','position', 'price', 'global_score', "nation", "is_hero", "is_icon"]
    squad = data.loc[y > 0.5, cols]
    # sort by position: GK, DEF, MID, FOR
    squad = squad.sort_values(by='generic_position', key=lambda x: x.map({'GK': 0, 'DEF': 1, 'MID': 2, 'FOR': 3})).reset_index(drop=True)
    if print_squad:
        # check if function display exists
        if 'display' in globals():
            display(squad)
        else:
            print(squad)
        price = squad['price'].sum()
        mean_score = squad['global_score'].mean()
        chemistry_nationality = calculate_chemistry_nationality(squad)
        print(f"Price: {price}€, Mean score: {mean_score:.4f}, Nationality chemistry:{chemistry_nationality}")
    return squad
    
def calculate_chemistry_nationality(squad):
    nat_count = squad['nation'].value_counts()
    nat_chem = 0
    # loop over players
    for i in range(len(squad)):
        if squad.iloc[i]['is_icon']:
            nat_count[squad.iloc[i]['nation']] += 1
    for i in range(len(squad)):
        is_icon = squad.iloc[i]['is_icon']
        is_hero = squad.iloc[i]['is_hero']
        if is_icon or is_hero:
            nat_chem += 3
            continue
        nat_i = squad.iloc[i]['nation']
        common_nat = nat_count[nat_i]
        if common_nat >= 2 and common_nat <= 4:
            nat_chem += 1  
        elif common_nat >= 5 and common_nat <= 7:
            nat_chem += 2
        elif common_nat >= 8:
            nat_chem += 3
    return nat_chem


position_mapping = {
    "GK": "GK",
    "LB": "DEF", "CB": "DEF", "RB": "DEF", "LWB": "DEF", "RWB": "DEF",
    "CM": "MID", "CDM": "MID", "CAM": "MID", "RM": "MID", "LM": "MID",
    "LW": "FOR", "RW": "FOR", "ST": "FOR", "CF": "FOR"
}


def summary_squad(squad):
    print("\n########################################################")
    print("################# SUMMARY OF THE SQUAD #################")
    number_players = len(squad)
    number_icons = squad['is_icon'].sum()
    number_heroes = squad['is_hero'].sum()
    number_regular_players = number_players - number_icons - number_heroes
    print(f"Number of players: {number_players}, number of regular players: {number_regular_players}, number of icons: {number_icons}, number of heroes: {number_heroes}.")
    print("The mean Overall rating of each player is", squad['global_score'].mean())
    print("The mean price of each player is", squad['price'].mean())
    print("########################################################\n")
        