param P>=0; # Number of players available to choose

param GLOBAL_SCORE{1..P}; # Global (score) of every player
param PRICE{1..P}; # Price of every player

param NATIONALITY{1..P}; # Nationality of every player

# Positions
param IS_GK{1..P}; # Is player i a goalkeeper?
param IS_DEF{1..P}; # Is player i a defender?
param IS_MID{1..P}; # Is player i midfielder?
param IS_FOR{1..P}; # Is player i forward?

param IS_ICON{1..P}; # Is player i an icon?
param IS_HERO{1..P}; # Is player i an hero?

set NORMAL_PLAYERS := {i in 1..P: IS_ICON[i] = 0 and IS_HERO[i] = 0};
set ICONS := {i in 1..P: IS_ICON[i] = 1};
set HEROES := {i in 1..P: IS_HERO[i] = 1};
set ICONS_HEROES := ICONS union HEROES;


param BUDGET >= 0; # Budget available to spend
param M>=0; 

param MIN_CHEMISTRY >= 0; # Minimum chemistry required
param NUMBER_DEF >= 0; # Number of defenders available to choose
param NUMBER_MID >= 0; # Number of midfielders available to choose
param NUMBER_FOR >= 0; # Number of forwards available to choose


var y{1..P} binary; # binary variable to select the player

var natCount{1..P} integer; # integer variable. The item i of this array will store the number of selected players that have the same nationility as player i
var chemistryNat1{1..P} binary; # True value to represent that the the player i meets the 1st nationality chemistry condition
var chemistryNat2{1..P} binary; # True value to represent that the the player i meets the 2nd nationality chemistry condition
var chemistryNat3{1..P} binary; # True value to represent that the the player i meets the 3rd nationality chemistry condition
var natCountAll{1..P} integer; #auxiliary variable necessary for direct linearization of the constraint to count all players with the same nationality

maximize Avg_Global: 
    sum{i in 1..P} (GLOBAL_SCORE[i] * y[i])/11;


############################################################################################
# Constraints to ensure that the team has the right number of players in each position

subject to PositionGK: 
    sum{i in 1..P} IS_GK[i]*y[i] = 1;

subject to PositionDEF: 
    sum{i in 1..P} IS_DEF[i]*y[i] = NUMBER_DEF;

subject to PositionMID: 
    sum{i in 1..P} IS_MID[i]*y[i] = NUMBER_MID;

subject to PositionFOR: 
    sum{i in 1..P} IS_FOR[i]*y[i] = NUMBER_FOR;
############################################################################################


############################################################################################
# Other constraints
subject to Budget: 
    sum{i in 1..P} PRICE[i]*y[i] <= BUDGET;
############################################################################################


############################################################################################
# Constaint to ensure nationality chemistry

subject to R31{i in NORMAL_PLAYERS}:
    natCount[i] <= M * y[i];

subject to R32{i in NORMAL_PLAYERS}:
    natCount[i] <= sum{j in 1..P: NATIONALITY[i] = NATIONALITY[j]} y[j] + sum{j in ICONS: NATIONALITY[i] = NATIONALITY[j]} y[j];
    
subject to R33A{i in NORMAL_PLAYERS}:
    natCount[i] >= 2*chemistryNat1[i];
subject to R33B{i in NORMAL_PLAYERS}:
    natCount[i] >= 5*chemistryNat2[i];
subject to R33C{i in NORMAL_PLAYERS}:
    natCount[i] >= 7*chemistryNat3[i];

subject to R34A{i in NORMAL_PLAYERS}:
    natCount[i]-1 <= M*chemistryNat1[i];
subject to R34B{i in NORMAL_PLAYERS}:
    natCount[i]-4 <= M*chemistryNat2[i];
subject to R34C{i in NORMAL_PLAYERS}:
    natCount[i]-6 <= M*chemistryNat3[i];
############################################################################################

#Contraints to ensure nationality chemistry via direct linealizing
subject to R35{i in NORMAL_PLAYERS}:
    natCountAll[i] = sum{j in 1..P: NATIONALITY[i] = NATIONALITY[j]} y[j] + sum{j in ICONS: NATIONALITY[i] = NATIONALITY[j]} y[j];
subject to R36{i in NORMAL_PLAYERS}:
    natCount[i] <= natCountAll[i];
subject to R37{i in NORMAL_PLAYERS}:
    natCount[i] <= M*y[i];
subject to R38{i in NORMAL_PLAYERS}:
    natCount[i] >= natCountAll[i] + M*(y[i]-1);
subject to R39{i in NORMAL_PLAYERS}:
    natCount[i] >= 0;

############################################################################################
# Constraints to ensure a minumum of chemistry is met
subject to R4:
    sum{i in NORMAL_PLAYERS}  (chemistryNat1[i] + chemistryNat2[i] + chemistryNat3[i])  + 3*sum{i in ICONS_HEROES} y[i] >= MIN_CHEMISTRY;
    
subject to R4B:
    sum{i in NORMAL_PLAYERS}  ((10**7)*chemistryNat1[i] + (10**7)*chemistryNat2[i] + (10**7)*chemistryNat3[i])  + 3*sum{i in ICONS_HEROES} (10**7)*y[i] >= (10**7)*MIN_CHEMISTRY;    
############################################################################################