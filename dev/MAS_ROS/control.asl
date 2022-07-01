// Agent control in project mas_ros.mas2j

/* Initial beliefs and rules */

// Set robot teams
teams(team1).
teams(team2).
isIn(robot1,team1).
isIn(robot2,team1).
isIn(robot3,team2).
isIn(robot4,team2).
isOpponent(team1,team2).
isOpponent(team2,team1).

// Number of flags
hasFlags(team1,0).
hasFlags(team2,0).


/* Initial goals */

!start.

/* Plans */

// Setup
+!start : true <- .findall(X,teams(X),L);.print(L," set");!initial_playstyles.
+!initial_playstyles : true <- .broadcast(tell,playstyle(aggressive)).

// Points management
+!add_point(T,V) : hasFlags(T,N)[source(self)] & not N==4 <- +hasFlags(T,N+V);-hasFlags(T,N).
-!add_point(T,V) : true <- .print(T," has maximum points!").
+!deduct_point(T,V) : hasFlags(T,N)[source(self)] & not N==0 <- +hasFlags(T,N-V);-hasFlags(T,N).
-!deduct_point(T,V) : true <- .print(T," has no points to deduct!").

// Different game clauses for scoring points - change in playstyle
// Change in style for any team scoring two points
+hasFlags(Team,2)[source(Robot)] : isIn(Team,Robot)[source(self)] <- 
	.send(Robot,untell,playstyle(aggressive));.send(Robot,tell,playstyle(defensive)).

// Example loop
/*
+!test : true <- !loop([1,2,3]).
+!loop(L) : not .empty(L) <-
	.nth(0,L,X);
	.print(X);
	.delete(0,L,Nl);
	!loop(Nl).
-!loop(L) : true <- true.
*/


// Change in style for any team scoring four points
+hasFlags(Team,4)[source(Robot)] : isIn(Robot,Team)[source(self)] <-
	.findall(Robots,isIn(Robots,Team),List);
	!loop_team(List).
+!loop_team(List) : not .empty(List) <-	// Tells all members of a team to play defensively
	.nth(0,List,Robot);
	.send(Robot,tell,playstyle(defensive));
	.send(Robot,untell,playstyle(aggressive));
	.delete(0,List,NewList);
	!loop(NewList).
-!loop(List) : true <- true.

// Example game end
/*
+hasFlags(T,4)[source(R)] : team1(R)[source(self)] | team2(R)[source(self)] <- 
	.print("Winning team is ",T);.stopMAS(8000).
*/
