// Agent robot1 in project mas_ros.mas2j

/* Initial beliefs and rules */

atPosition(0.0).

/* Initial goals */

!start.

/* Plans */

// Setup
+!start : true <- .my_name(Name);.print(Name," active").
+!get_team(T) : true <- .my_name(Name);.send(control,askOne,isIn(Name,Team));T=Team.

// Declaring playstyle as actions for the interface
+playstyle(Style)[source(control)] : true <- Style.

// Movement plans - detecting objects
+frontObject[source(percept)] : true <- turn_away;-frontObject[source(percept)].

// Visualisation of coloured cubes
+flagDetected(Pos)[source(percept)] : true <- !get_team(Team);
	.print("Flat detected at ",Pos);
	.send(control,achieve,add_point(Team,1));
	if(.send(control,askOne,hasFlag(Team,P)) & Pos > P+2){
		if(.send(control,askOne,isOpponent(Team,OtherTeam)) & 
		.send(control,askOne,teams(OtherTeam))){
			.send(control,achieve,deduct_point(OtherTeam,1))
		}
	}.

// Odometry data reception
+newPosition(Val)[source(percept)] : atPosition(OldVal)[source(self)] & not (OldVal == Val) <-
	+newPosition(Val);-newPosition(OldVal).
-newPosition(Val)[source(percept)] : true <- .print("In same position").
