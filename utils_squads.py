def get_squad(y, data, print_squad=True):
    cols = ['name', 'generic_position','position', 'price', 'global_score', "nation"]
    squad = data.loc[y > 0.5, cols]
    # sort by position: GK, DEF, MID, FOR
    squad = squad.sort_values(by='generic_position', key=lambda x: x.map({'GK': 0, 'DEF': 1, 'MID': 2, 'FOR': 3})).reset_index(drop=True)
    if print_squad:
        display(squad)
        price = squad['price'].sum()
        mean_score = squad['global_score'].mean()
        chemistry_nationality = calculate_chemistry_nationality(squad)
        print(f"Price: {price}€, Mean score: {mean_score:.2f}, Nationality chemistry:{chemistry_nationality}")
    return squad
    
def calculate_chemistry_nationality(squad):
    nat_count = squad['nation'].value_counts()
    nat_chem = 0
    # loop over players
    for i in range(len(squad)):
        nat_i = squad.iloc[i]['nation']
        common_nat = nat_count[nat_i]
        # if common_nat >= 2 and common_nat <= 4:
        #     nat_chem += 1  
        # elif common_nat >= 5 and common_nat <= 7:
        #     nat_chem += 2
        # elif common_nat >= 8:
        #     nat_chem += 3
        if common_nat >= 2:
            nat_chem += 1
    return nat_chem


position_mapping = {
    "GK": "GK",
    "LB": "DEF", "CB": "DEF", "RB": "DEF", "LWB": "DEF", "RWB": "DEF",
    "CM": "MID", "CDM": "MID", "CAM": "MID", "RM": "MID", "LM": "MID",
    "LW": "FOR", "RW": "FOR", "ST": "FOR", "CF": "FOR"
}
        