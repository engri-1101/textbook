\* Max␣flow␣Problem *\
Maximize
OBJ: Edges_(4,_'T') + Edges_(5,_'T') + Edges_(6,_'T')
Subject To
_C1: Edges_('S',_2) - Edges_(2,_3) - Edges_(2,_4) - Edges_(2,_5) = 0
_C2: Edges_('S',_3) + Edges_(2,_3) - Edges_(3,_5) - Edges_(3,_6) = 0
_C3: Edges_(2,_4) - Edges_(4,_'T') + Edges_(5,_4) = 0
_C4: Edges_(2,_5) + Edges_(3,_5) - Edges_(5,_'T') - Edges_(5,_4)
 - Edges_(5,_6) = 0
_C5: Edges_(3,_6) + Edges_(5,_6) - Edges_(6,_'T') = 0
Bounds
0 <= Edges_('S',_3) <= 7
0 <= Edges_(2,_3) <= 5
0 <= Edges_(2,_4) <= 6
0 <= Edges_(2,_5) <= 2
0 <= Edges_(3,_5) <= 2
0 <= Edges_(3,_6) <= 4
0 <= Edges_(4,_'T') <= 5
0 <= Edges_(5,_'T') <= 4
0 <= Edges_(5,_6) <= 4
0 <= Edges_(6,_'T') <= 3
Generals
Edges_('S',_3)
Edges_(2,_3)
Edges_(2,_4)
Edges_(2,_5)
Edges_(3,_5)
Edges_(3,_6)
Edges_(4,_'T')
Edges_(5,_'T')
Edges_(5,_6)
Edges_(6,_'T')
Binaries
Edges_('S',_2)
Edges_(5,_4)
End
