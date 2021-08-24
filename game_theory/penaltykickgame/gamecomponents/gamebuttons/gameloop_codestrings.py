#This file contains the JavaScript code strings that are used for the main game
#loop.
#<editor-fold Function Codestrings:
  #<editor-fold iterText():
  # String containing the JavaScript code for changing the game text according
  # to the current iteration's game stats.
iterText = """
function iterText(roundsPlayed, gameScore, goal) {
  /**
   * Changes the game text to display the rounds played, game score and the
   * kicker's scoring result.
   * @param{string} roundsPlayed -- A string containing an int that shows the
   * iterations run.
   * @param{string} gameScore -- A string containing an int that shows the
   * current iteration's score.
   * @param{int} goal -- An int equal to either 1 or -1. Value of 1 is for if a
   * goal was scored during the iteration.
   */
  //Set Game Text Lines:
  txt.data['text'] = [
    `Rounds played: ${roundsPlayed}`,
    `Total score: ${gameScore}`,
    '',
    (goal === 1) ? 'GOAL!' : 'Blocked'
  ];
  txt.change.emit(); //Finalize changes by emitting to source
}
"""
  #</editor-fold>
  #<editor-fold rollKickerAction():
  # String containing the JavaScript code for deciding the kicker's actions
  # based off of the pure strategy selection chances input by the player.
rollKickerAction = """
function rollKickerAction() {
  /**
  * Selects a kicker pure strategy by converting the pure strategy selection
  * chances array to a form where each value has the previous values added to
  * them, so that the strategy can then be chosen by comparing the values to a
  * random roll. The kicker foot and direction are then determined according to
  * the strategy index before being returned in an array.
  * @return{array} -- An array that contains strings representing the kicker
  * foot, and their chosen kick direction. The kicker foot string can have value
  * equal to 'Left' or 'Right', and the kick direction has to be equal to either
  * 'Left', 'Middle', or 'Right'.
  */
  //Copy chances into array, then modify array to act as roll thresholds:
  let arrVals = [0].concat(chances.slice());
  arrVals.slice(1).forEach(
    (v, i) => arrVals[i + 1] += arrVals[i]
  );

  //Determine actions to take based off roll comparison to thresholds:
  let index = 5;
  const roll = Math.random();
  arrVals.slice(0, 6).forEach(
    (v) => {
      if(roll < v) { index -= 1; }
    }
  );
  return [
    (index < 3) ? 'Left' : 'Right',
    directions[(index % 3)]
  ];
}
"""
  #</editor-fold>
  #<editor-fold fictitiousPlay():
  # String containing the JavaScript code for handling fictitious play keeper
  # decisions.
fictitiousPlay = """
//Handle Goalie Decision
function fictitiousPlay(footIsLeft, footDict) {
  /**
  * Determines the keeper's action according to Fictitious Play.
  * @param{bool} footIsLeft -- a bool containing whether or not the kicker is
  * left-footed.
  * @param{dict} footDict -- The dict that contains the score chances for the
  * different possible kicker foot kicker action outcomes.
  * @return{array} -- An array containing the direction for the keeper to dive,
  * and the keeper's perceived risks for each possible action from left to
  * right.
  */
  //Set decision making values to use according to kickerFoot:
  const freqs = (footIsLeft) ? freq.slice(0, 3) : freq.slice(3, 6);

  //Calculate goalie perceived risks:
  const tsr = freqs.reduce(arrSumFunc);
  const eFreqs = (tsr !== 0) ? freqs.map(x => x / tsr) : [1/3, 1/3, 1/3];
  const risks = [0, 0, 0];
  directions.forEach(
    (v1, i) => directions.forEach(
      (v2, j) => risks[i] += eFreqs[j] * footDict[v2 + v1]
    )
  );

  //return goalie action and perceived risks:
  const actionIndex = risks.indexOf(Math.min(...risks));
  return [
    directions[actionIndex],
    ...risks
  ];
}
"""
  #</editor-fold>
  #<editor-fold optimalMixed():
#Runs the optimal mixed strategy found in the lab.
optimalMixed = """
function optimalMixed(kickerFoot) {
  /**
  * Determines the keeper's action according to the optimal mixed strategy for
  * the keeper.
  * param{string} kickerFoot -- Either 'Left' or 'Right' representing the
  * kicker's footedness.
  * return{string} -- Either 'Left', 'Middle', or 'Right' representing the
  * keeper's direction to dive.
  */
  //selects and returns an action based off of optimal mixed strategy chances:
  const thresholds = {
    'Left'  : 0.8,
    'Right' : 0.7419
  };
  const goKickerFoot = (Math.random() >= thresholds[kickerFoot]);
  return (goKickerFoot) ? kickerFoot : 'Middle';
}
"""
  #</editor-fold>
  #<editor-fold randomChoice():
#Runs random choices, a strategy for the goalie where they pick their actions
#at random.
randomChoice = """
function randomChoice() {
  /**
  * Determines the keeper's action at random.
  * return{string} -- Either 'Left', 'Middle', or 'Right' representing the
  * keeper's direction to dive.
  */
  //Selects and returns an action from directions at an equal chance:
  const actionIndex = Math.round(Math.random()*3 - 0.5);
  return directions[actionIndex];
}
"""
  #</editor-fold>
  #<editor-fold goalieCheats():
#This codestring runs the goalie cheats strategy, a strategy where the goalie
#Uses the optimal pure strategy to counter the player's mixed strategy.
goalieCheats = """
function goalieCheats(kickerFoot) {
  /**
  * Determines the keeper's action according to a previously created strategy.
  * param{string} kickerFoot -- Either 'Left' or 'Right' representing the
  * kicker's footedness.
  * return{string} -- Either 'Left', 'Middle', or 'Right' representing the
  * keeper's direction to dive.
  */
  //return the action of the pure strategy corresponding to the kicker foot:

  const actionIndex = counterSrc.data[kickerFoot].indexOf(1);
  return directions[actionIndex];
}
"""
  #</editor-fold>
  #<editor-fold make_handleFigVisibility():
def make_handleFigVisibility(
    stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
    stats_fig_4_enabled
):
    """Creates and returns a string containing the function for handling figure
    visibility at the end of the demo.


    Arguments:
    stats_fig_1_enabled -- A bool for whether or not Game Stats Figure 1 should
      be available.
    stats_fig_2_enabled -- A bool for whether or not Game Stats Figure 2 should
      be available.
    stats_fig_3_enabled -- A bool for whether or not Game Stats Figure 3 should
      be available.
    stats_fig_4_enabled -- A bool for whether or not Game Stats Figure 4 should
      be available.
    """
    handleFigVisibility = """
function handleFigVisibility(stratIsFictPlay) {
  nextButton.visible = false;
  distTable.visible = false;
  autoAdvButton.visible = false;
  advSpdSlider.visible = false;
  gameFigButton.visible = true;
"""
    if (stats_fig_1_enabled):
        handleFigVisibility += """
  statsFig1Button.visible = true;
  statsFig1.visible = false;
"""
    if (stats_fig_2_enabled):
        handleFigVisibility += """
  statsFig2Button.visible = true;
  statsFig2.visible = false;
"""
    if (stats_fig_3_enabled):
        handleFigVisibility += """
  statsFig3Button.visible = stratIsFictPlay;
  statsFig3.visible = false;
"""
    if (stats_fig_4_enabled):
        handleFigVisibility += """
  statsFig4Button.visible = true;
  statsFig4.visible = false;
"""

    handleFigVisibility += """
}
"""
    return handleFigVisibility

  #</editor-fold>
  #<editor-fold scoring():
scoring = """
function scoring(footDict, kickerKick, goalieAction, actionsIndexKFKK) {
  /**
  * Handles the scoring for the game.
  * param{dict} footDict -- The dict containing the score chances according to
  * the different possible kicker kick direction and keeper dive direction
  * outcomes for the kicker's footedness.
  * param{string} kickerKick -- Either 'Left', 'Middle', or 'Right' for the
  * kicker's kick direction.
  * param{string} goalieAction -- Either 'Left', 'Middle', or 'Right' for the
  * keeper's dive direction.
  * param{int} actionsIndexKFKK -- an int designating an index selected
  * previously according to the kicker's footedness and kick directions.
  */
  //Set function values:
  const scoreRoll = Math.random();
  const scoreChance = footDict[kickerKick + goalieAction];
  const roundsPlayed = parseInt(nround.text) + 1;
  const roundScore = (scoreRoll <= scoreChance) ? +1 : -1;

  //Update columns:
  const scoreChanceCol = distData['striker_score_chance'];
  const scoreRollCol = distData['striker_score_roll'];
  scoreChanceCol.fill(0);
  scoreRollCol.fill(0);
  scoreChanceCol[actionsIndexKFKK] = scoreChance;
  scoreRollCol[actionsIndexKFKK] = scoreRoll.toPrecision(6);

  //Update text:
  nround.text = roundsPlayed.toString();
  const currentGameScore = parseInt(score.text) + roundScore;
  score.text = currentGameScore.toString();

  return [roundScore, currentGameScore, roundsPlayed, scoreChance];
}
"""
  #</editor-fold>
  #<editor-fold _moveGoalie():
_moveGoalie = """
function _moveGoalie(xLoc) {
  /**
  * Moves the goalie to the specified x coordinate.
  * param{int} xLoc -- The x coord to move to.
  */
  //Move both components of the goalie:
  goalieBody.x = xLoc;
  goalieHead.x = xLoc;
}
"""
  #</editor-fold>
  #<editor-fold animateIter():
animateIter = """
function animateIter(goalieAction, kickerKick, goal) {
  /**
  * Handles the animation for the iteration.
  * @param{string} goalieAction -- Either 'Left', 'Middle', 'Right' signifying
  * the keeper's dive direction.
  * @param{string} kickerKick -- Either 'Left', 'Middle', 'Right' signifying the
  * kicker's kick direction.
  * @param{int} goal -- Either 1 or -1 for the iteration score change.
  */
  //Set positions and store ball roll for handling cases:
  const goalieActionIsKickerKick = (goalieAction === kickerKick);
  const goalNotScored = (goal === -1);
  const gPos = {
    'Left'   : [37, 43],
    'Middle' : [47, 53],
    'Right'  : [57, 63]
  };
  const outOfGoalPos = {
    'Left'   : [30, 30],
    'Middle' : [30, 70],
    'Right'  : [70, 70]
  };
  const shotUnluckyMiss = (goalNotScored && !goalieActionIsKickerKick);
  const bPos = (shotUnluckyMiss) ? outOfGoalPos : gPos;
  const bRoll = Math.round(Math.random());

  ball.x = bPos[kickerKick][bRoll];
  ball.y = 63;
  if(goalieActionIsKickerKick){
    const goalieRolledX = gPos[goalieAction][[1, 0][bRoll]];
    const goalieX = (goalNotScored) ? ball.x : goalieRolledX;
    _moveGoalie(goalieX);
  } else {
    const goalieX = gPos[goalieAction][Math.round(Math.random())];
    _moveGoalie(goalieX);
  }
}
"""
  #</editor-fold>
  #<editor-fold _updateDecisionTableRisks():
_updateDecisionTableRisks = """
function _updateDecisionTableRisks(
  perceivedRiskL,
  perceivedRiskM,
  perceivedRiskR,
  kfRAdjust
) {
  /**
  * updates the dist table's risk values.
  * @param{float} perceivedRiskL -- The keeper's perceived risks for diving left.
  * @param{float} perceivedRiskM -- The keeper's perceived risks for diving middle.
  * @param{float} perceivedRiskR -- The keeper's perceived risks for diving right.
  * @param{int} kfRAdjust -- An int for adjusting indexes if the kicker is
  * right-footed.
  */
  //Reset column then set perceived risk for rows corresponding to kicker foot:
  const risks = distData['goalie_perceived_risks'];

  risks.fill(0);
  const prs = [
    perceivedRiskL.toPrecision(6),
    perceivedRiskM.toPrecision(6),
    perceivedRiskR.toPrecision(6)
  ];
  prs.forEach(
    (v, i) => risks[kfRAdjust + i] = v
  );
}
"""
  #</editor-fold>
  #<editor-fold goalieDecisionTracking():
goalieDecisionTracking = """
function goalieDecisionTracking(
  actionsIndexKFKK,
  kfRAdjust,
  directionsIndexGa,
  stratIsFictPlay,
  perceivedRiskL,
  perceivedRiskM,
  perceivedRiskR
) {
  /**
  * Tracks game data and puts it into the dist table.
  * @param{int} actionsIndexKFKK -- An int for adjusting indexes around the
  * kicker foot and kicker kick directions.
  * @param{int} kfRAdjust -- An int for adjusting indexes if the kicker is
  * right-footed.
  * @param{int} directionsIndexGa -- An int for the index of the keeper
  * dive direction.
  * @param{bool} stratIsFictPlay -- A bool for whether or not the keeper is
  * using fictitious play.
  * @param{float} perceivedRiskL -- The keeper's perceived risks for diving left.
  * @param{float} perceivedRiskM -- The keeper's perceived risks for diving middle.
  * @param{float} perceivedRiskR -- The keeper's perceived risks for diving right.
  */

  //Increase corresponding trackers to KFKK and KFGA:
  freq[actionsIndexKFKK] += 1;
  const decisionsIndex = kfRAdjust + directionsIndexGa;
  distData['decisions'][decisionsIndex] += 1;

  //Update table perceived risks if fictitious play:
  if(stratIsFictPlay) {
    _updateDecisionTableRisks(
      perceivedRiskL,
      perceivedRiskM,
      perceivedRiskR,
      kfRAdjust
    );
  }

  //Update table by finalizing changes to source:
  distTableSrc.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold _fig1Iter():
_fig1Iter = """
function _fig1Iter(
  goal,
  directionsIndexGa,
  sections,
  fig1Data,
  actionsIndexKFKK
) {
  /**
  * Handles the data for an iteration in Game Stats Figure 1.
  * @param{int} goal -- Either -1 or 1 for the iterations score change.
  * @param{int} directionsIndexGa -- An int for the index of the keeper
  * dive direction.
  * @param{array} sections -- An array containing the column names for the bar
  * sections in Figure 1.
  * @param{dict} fig1Data -- The data for game stats figure 1.
  * @param{int} actionsIndexKFKK -- An int for adjusting indexes around the
  * kicker foot and kicker kick directions.
  */
  //Increase section value of iteration result by 1:
  const sectionIndex = (goal === 1) ? 0 : directionsIndexGa + 1;
  const section = sections[sectionIndex];
  fig1Data[section][actionsIndexKFKK] += 1;
}
"""
  #</editor-fold>
  #<editor-fold _fig1Adjust():
_fig1Adjust = """
function _fig1Adjust(sections, fig1Data) {
  /**
  * Adjusts Game Stats Figure 1.
  * @param{array} sections -- An array containing the column names for the bar
  * sections in Figure 1.
  * @param{dict} fig1Data -- The data for game stats figure 1.
  */
  //Get total heights of kfkk bars:
  const heights = [0, 0, 0, 0, 0, 0]
  sections.forEach(
    (v1) => fig1Data[v1].forEach(
      (v2, i) => heights[i] += v2
    )
  );

  //Set y max to 1.1 * the height of the tallest kfkk bar (rounded):
  statsFig1.y_range.end = Math.round(Math.max(...heights) * 1.1);
}
"""
  #</editor-fold>
  #<editor-fold updateFig1():
updateFig1 = """
function updateFig1(
  goal,
  directionsIndexGa,
  actionsIndexKFKK,
  roundIsLastIter
) {
  /**
  * Updates the data for Game Stats Figure 1.
  * @param{int} goal -- Either -1 or 1 for the iterations score change.
  * @param{int} directionsIndexGa -- An int for the index of the keeper
  * dive direction.
  * @param{int} actionsIndexKFKK -- An int for adjusting indexes around the
  * kicker foot and kicker kick directions.
  * @param{bool} roundIsLastIter -- Whether or not the iteration is the last one.
  */
  //create constants for referencing:
  const fig1Data = statsFig1Src.data;
  const sections = ['scored_y', 'blockedl_y', 'blockedm_y', 'blockedr_y'];

  //Update the figure for the iteration:
  _fig1Iter(goal, directionsIndexGa, sections, fig1Data, actionsIndexKFKK);

  //Make final adjustments if it is the final iteration:
  if(roundIsLastIter) { _fig1Adjust(sections, fig1Data); }

  //Update the figure by finalizing the changes to the data source:
  statsFig1Src.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold _fig2Iter():
_fig2Iter = """
function _fig2Iter(fig2Data, roundsPlayed, gameScore, roundScoreChance) {
  /**
  * Handles an iteration of data for Game Stats Figure 2.
  * @param{dict} fig2Data -- The data for Game Stats Figure 2.
  * @param{int} roundsPlayed -- The number of iterations played.
  * @param{int} gameScore -- The score for the game at the current iteration.
  * @param{float} roundScoreChance -- The chance of scoring for the played iteration.
  */
  //Plot Values:
  fig2Data['ys'][roundsPlayed] = gameScore;
  fig2Data['chance_ys'][roundsPlayed] = 2*roundScoreChance - 1;
}
"""
  #</editor-fold>
  #<editor-fold _fig2Adjust():
_fig2Adjust = """
function _fig2Adjust(fig2Data, itersToRun) {
  /**
  * Adjusts the data for Game Stats Figure 2.
  * @param{dict} fig2Data -- The data for Game Stats Figure 2.
  * @param{int} itersToRun -- The number of iterations total for the game.
  */
  //Adjust chanceYs:
  const chanceYs = fig2Data['chance_ys'];
  chanceYs.slice(1).forEach(
    (v, i) => chanceYs[i + 1] += chanceYs[i]
  );

  //Get max and min of figure points:
  const ys = fig2Data['ys'];
  let minVal = Math.min(... ys);
  let maxVal = Math.max(... ys, ...chanceYs);

  //Adjust figure display:
  const buffer = Math.round((Math.abs(maxVal) + Math.abs(minVal)) * 0.1);
  maxVal += buffer;
  minVal -= buffer;
  statsFig2.y_range.end   = maxVal;
  statsFig2.y_range.start = minVal;

  //Resize hit boxes:
  const hitboxHeight = 2 * Math.max(Math.abs(maxVal), Math.abs(minVal));
  fig2Data['heights'].fill(hitboxHeight);
}
"""
  #</editor-fold>
  #<editor-fold updateFig2():
updateFig2 = """
function updateFig2(
  roundsPlayed,
  gameScore,
  roundScoreChance,
  roundIsLastIter,
  itersToRun
) {
  /**
  * Updates the data for Game Stats Figure 2.
  * @param{int} roundsPlayed -- The number of iterations played.
  * @param{int} gameScore -- The score for the game at the current iteration.
  * @param{float} roundScoreChance -- The chance of scoring for the played iteration.
  * @param{bool} roundIsLastIter -- Whether or not the iteration is the last one.
  * @param{int} itersToRun -- The number of iterations total for the game.
  */
  //Store reference to fig 2 data:
  const fig2Data = statsFig2Src.data;

  //Update the figure for the iteration:
  _fig2Iter(fig2Data, roundsPlayed, gameScore, roundScoreChance);

  //Adjust the figure as needed if it is the last iteration:
  if(roundIsLastIter) { _fig2Adjust(fig2Data, itersToRun); }

  //Update the source to finalize the changes to the figure:
  statsFig2Src.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold _fig3Iter():
_fig3Iter = """
function _fig3Iter(ys, roundsPlayed) {
  /** Handles the data for an iteration for Game Stats Figure 3.
  * @param{array} ys -- An array containing the ys columns of figure 3.
  * @param{int} roundsPlayed -- The number of iterations played.
  */
  //For each foot:
  ['Left', 'Right'].forEach(
    (footVal, footIndex) => {

      //Calculate emprical frequencies of aim directions for that footedness:
      const footFreq = freq.slice((3 * footIndex), (3 * (footIndex + 1)));
      const footTsr = footFreq.reduce(arrSumFunc);
      const footChances = (
        (footTsr !== 0) ? footFreq.map(x => x/footTsr) : [1/3, 1/3, 1/3]
      );

      //calculate and plot risk of goalie taking each position:
      directions.forEach(
        (v1, i1) => directions.forEach(
          (v2, i2) => {
            const sideRisk = footChances[i2] * scoreProbDicts[footVal][v2 + v1];
            const ysIndex = 3*footIndex + i1;
            ys[ysIndex][roundsPlayed] += sideRisk;
          }
        )
      );

    }
  );
}
"""
  #</editor-fold>
  #<editor-fold _fig3Adjust():
_fig3Adjust = """
function _fig3Adjust(fig3Data, itersToRun, ys) {
  /**
  * Adjusts Game Stats Figure 3's data.
  * @param{dict} fig3Data -- The data for Game Stats figure 3.
  * @param{int} itersToRun -- The total number of iterations in the game.
  * @param{array} ys -- An array containing the ys columns of figure 3.
  */
  //store fig3Data hb columns for iteration and reference:
  const hbs = [
    fig3Data['hb1'],
    fig3Data['hb2'],
    fig3Data['hb3'],
    fig3Data['hb4'],
    fig3Data['hb5'],
    fig3Data['hb6']
  ];

  //Adjustment loop:
  let vals = [];

  //For every iteration:
  for(let iter = 0; iter <= itersToRun; iter++){
    let hbHeights = new Array(6);
    let risks = new Array(6);

    //For every risk value, send to risks list for later use and push to vals:
    ys.forEach(
      (yVal, yIndex) => {
        risks[yIndex] = yVal[iter];
        vals.push(yVal[iter]);
      }
    );

    risks.sort((a, b) => a - b); //Sort risks in ascending order to setup

    //For every entry in risks:
    risks.forEach(
      (rVal, rIndex, a) => {
        //Set upper edge of hitbox to be equal to halfway between hitbox point
        //and next point (Set top hitbox edge to 1):
        let val = (rIndex === 5) ? 1 : ((rVal + a[rIndex + 1]) / 2);

        //subtract heights of all lower hitboxes to get hitbox height:
        hbHeights.slice(0, rIndex).forEach(
          (rVal) => val -= rVal
        );

        //Save value for use in next hitbox's calculation and plot on graph:
        hbHeights[rIndex] = val;
        hbs[rIndex][iter] = val;
      }
    );
  }

  //Adjust graph based off of stored values:
  const minVal = Math.round(Math.min(...vals) * 100) / 100;
  const maxVal = Math.round(Math.max(...vals) * 100) / 100;
  const buffer = Math.round((maxVal - minVal) * 100) / 1000;
  statsFig3.y_range.end   = Math.min(maxVal + buffer, 1);
  statsFig3.y_range.start = Math.max(minVal - buffer, 0);
}
"""
  #</editor-fold>
  #<editor-fold updateFig3():
updateFig3 = """
function updateFig3(roundsPlayed, roundIsLastIter, itersToRun) {
  /**
  * Updates the data for Game Stats Figure 3.
  * @param{int} roundsPlayed -- The number of iterations played.
  * @param{bool} roundIsLastIter -- Whether or not the iteration is the last one.
  * @param{int} itersToRun -- The number of iterations total for the game.
  */
  //Store values for reference:
  let fig3Data = statsFig3Src.data;
  const ys = [
    fig3Data['ll_ys'], fig3Data['lm_ys'], fig3Data['lr_ys'],
    fig3Data['rl_ys'], fig3Data['rm_ys'], fig3Data['rr_ys']
  ];

  //Update plot points:
  _fig3Iter(ys, roundsPlayed);

  //Make final adjustments to graph on last iteration:
  if(roundIsLastIter) { _fig3Adjust(fig3Data, itersToRun, ys); }

  //Finalize changes:
  statsFig3Src.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold updateFig4():
updateFig4 = """
function updateFig4(
  roundsPlayed,
  roundScoreChance,
  kickerFoot,
  kickerKick,
  goalieAction
) {
  /**
  * Updates the data for Game Stats Figure 4.
  * @param{int} roundsPlayed -- The number of iterations played.
  * @param{float} roundScoreChance -- The chance of scoring for the most
  * recent iteration.
  * @param{string} kickerFoot -- Either 'Left' or 'Right' signifying the kicker's
  * footedness.
  * @param{string} kickerKick -- Either 'Left', 'Middle', 'Right' signifying the
  * kicker's kick direction.
  * @param{string} goalieAction -- Either 'Left', 'Middle', 'Right' signifying
  * the keeper's dive direction.
  */
  const fig4Data = statsFig4Src.data;
  const index = roundsPlayed - 1;
  fig4Data['ys'][index] = roundScoreChance;
  fig4Data['feet'][index] = kickerFoot;
  fig4Data['directions'][index] = kickerKick;
  fig4Data['actions'][index] = goalieAction;

  statsFig4Src.change.emit();
}
"""
  #</editor-fold>
#</editor-fold>

#<editor-fold Running the game Codestrings:
  #<editor-fold GameConstants:
  # A string containing the code for constants throughout the game iteration.
gameConstants = """
const rDict = {
  'LeftLeft'   : 0.55, 'LeftMiddle'   : 0.65, 'LeftRight'   : 0.93,
  'MiddleLeft' : 0.74, 'MiddleMiddle' : 0.60, 'MiddleRight' : 0.72,
  'RightLeft'  : 0.95, 'RightMiddle'  : 0.73, 'RightRight'  : 0.70
};
const lDict = {
  'LeftLeft'   : 0.67, 'LeftMiddle'   : 0.70, 'LeftRight'   : 0.96,
  'MiddleLeft' : 0.74, 'MiddleMiddle' : 0.60, 'MiddleRight' : 0.72,
  'RightLeft'  : 0.87, 'RightMiddle'  : 0.65, 'RightRight'  : 0.61
};
const scoreProbDicts = {
  'Right' : rDict,
  'Left'  : lDict
};

const directions = ['Left', 'Middle', 'Right'];

const arrSumFunc = ((a, b) => a + b);

const chances = chancesSrc.data['chances'];
const distData = distTableSrc.data;
const freq = distData['freq'];
"""
  #</editor-fold>

  #<editor-fold make_gameIter():
def make_gameIter(
    stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
    stats_fig_4_enabled
):
    """Creates and returns a string containing the code for an iteration of the
    game.


    Arguments:
    stats_fig_1_enabled -- A bool for whether or not Game Stats Figure 1 should
      be available.
    stats_fig_2_enabled -- A bool for whether or not Game Stats Figure 2 should
      be available.
    stats_fig_3_enabled -- A bool for whether or not Game Stats Figure 3 should
      be available.
    stats_fig_4_enabled -- A bool for whether or not Game Stats Figure 4 should
      be available.
    """
    gameIter = """
function gameIter(){
  const itersToRun = iterSlider.value;

  const gameStrat = stratToUseDiv.text;

  const stratIsFictPlay = (gameStrat === 'Fictitious_Play');

  let perceivedRiskL;
  let perceivedRiskM;
  let perceivedRiskR;

  let goalieAction = '';

  let kickerFoot = '';
  let kickerKick = '';

  let goal = 0;
  let gameScore = 0;
  let roundsPlayed = 0;

  let roundScoreChance = 0;

  [kickerFoot, kickerKick] = rollKickerAction();

  const footIsLeft = (kickerFoot === 'Left');
  const footDict = scoreProbDicts[kickerFoot];
  const kfRAdjust = (footIsLeft) ? 0 : 3;

  switch(gameStrat) {
    case 'Fictitious_Play':
      [goalieAction, perceivedRiskL, perceivedRiskM, perceivedRiskR] = (
        fictitiousPlay(footIsLeft, footDict)
      );
      break;
    case 'Mixed_Strategy':
      goalieAction = optimalMixed(kickerFoot);
      break;
    case 'Random':
      goalieAction = randomChoice();
      break;
    case 'Goalie_Cheats':
      goalieAction = goalieCheats(kickerFoot);
      break;
    default:
      //TODO throw an error
      break;
  }

  const directionsIndexGa = directions.indexOf(goalieAction); //DirectionsIndexGoalieAction
  const actionsIndexKFKK = kfRAdjust + directions.indexOf(kickerKick); //Actions index KFKK

  [goal, gameScore, roundsPlayed, roundScoreChance] = scoring(
    footDict,
    kickerKick,
    goalieAction,
    actionsIndexKFKK
  );

  const roundIsLastIter = (roundsPlayed >= itersToRun);

  animateIter(goalieAction, kickerKick, goal);

  goalieDecisionTracking(
    actionsIndexKFKK,
    kfRAdjust,
    directionsIndexGa,
    stratIsFictPlay,
    perceivedRiskL,
    perceivedRiskM,
    perceivedRiskR
  );
"""

    if (stats_fig_1_enabled):
        gameIter += """
  updateFig1(goal, directionsIndexGa, actionsIndexKFKK, roundIsLastIter);
"""

    if (stats_fig_2_enabled):
        gameIter += """
  updateFig2(
    roundsPlayed,
    gameScore,
    roundScoreChance,
    roundIsLastIter,
    itersToRun
  );
"""

    if (stats_fig_3_enabled):
        gameIter += """
  if(stratIsFictPlay) { updateFig3(roundsPlayed, roundIsLastIter, itersToRun); }
"""

    if (stats_fig_4_enabled):
        gameIter += """
  updateFig4(
    roundsPlayed,
    roundScoreChance,
    kickerFoot,
    kickerKick,
    goalieAction
  );
"""

    gameIter += """
  if(roundIsLastIter) { handleFigVisibility(stratIsFictPlay); }

  iterText(roundsPlayed, gameScore, goal);
}
"""

    return gameIter
  #</editor-fold>

  #<editor-fold gameRunner:
  # A string containing code to use to run the game.
gameRunner = """
//Setup the promise that enforces waiting for the delay to finish:
const iterationDelay = (
  //Creates the promise with parameter ms:
  (ms) => new Promise(
    //Waits for ms seconds before resolving:
    (resolve) => setTimeout(
      () => {
        resolve();
      },
      ms
    )
  )
);

async function gameLoop(){
  /**
  * An async function that runs each iteration of the game. Recurses after a
  * delay if the necessary conditions are fulfilled.
  */
  //Take value for if another iteration is running:
  let tempIterVal = inAnIter.text;

  //If there is not another iteration running:
  if(tempIterVal === 'false'){
    //Set the value of inAnIter to reflect that an iteration is now running:
    inAnIter.text = 'true';

    //Run the game iteration:
    gameIter();

    //Tell itself that it has finished running the iteration:
    tempIterVal = 'false';

    //True if not in the last iteration of the game:
    const notLastRound = (parseInt(nround.text) < iterSlider.value);

    //True if the button is activated by the user:
    const autoAdvActive = (autoAdvButton.active);

    //True if both conditions are true:
    const conditionsFulfilled = (notLastRound && autoAdvActive);

    //If all recursion conditions are fulfilled:
    if(conditionsFulfilled){
      //Await the delay, then recurse:
      await iterationDelay(advSpdSlider.value).then(
        () => {
          //Designate that an iteration is no longer running:
          inAnIter.text = 'false';

          //Recurse:
          gameLoop();
        }
      );
    } else {
      //Designate that an iteration is no longer running:
      inAnIter.text = 'false';
    }
  }
}

gameLoop();
"""
  #</editor-fold>
#</editor-fold>

#<editor-fold start button make_initialGuiDisplay():
#This code string changes the visibility values of various game gui elements
#in order to change the user view from that used in the earlier menu like
#screens to one used for the game screens.
def make_initialGuiDisplay(show_dist_table):
    """Creates and returns a string for setting the initial changes to viewable
    objects for the first iteration of the game.


    Argument:
    show_dist_table -- A bool for whether or not to show the dist table for
      debugging purposes.
    """
    initialGuiDisplay = """
startButton.visible = false;
nextButton.visible = true;
aimTextInputs.forEach(
  (v) => v.visible = false
)
iterSlider.visible = false;
stratDropdown.visible = false;
automationTable.visible = false;
"""

    if (show_dist_table):
        initialGuiDisplay += """
distTable.visible = true;
"""

    return initialGuiDisplay
#</editor-fold>

#<editor-fold initialIterationAdjustments:
initialIterationAdjustments = """
function initialIterationAdjustments(){
  /**
  * A function for making initial adjustments for the iteration.
  */
  //Set references:
  const fig2Data = statsFig2Src.data;
  const fig3Data = statsFig3Src.data;
  const fig4Data = statsFig4Src.data;

  //Get iteration value:
  const iterations = iterSlider.value;

  //Set figure x range limits:
  statsFig2.x_range.end = iterations + 0.5;
  statsFig3.x_range.end = iterations + 0.5;
  statsFig4.x_range.end = iterations + 0.5;

  //Get array length:
  const arrLength = iterations + 1;

  //Create x Value Arrays for Sources:
  const fig2Xs = new Array(arrLength).fill(0);
  fig2Xs.forEach(
    (v, i) => fig2Xs[i] = i
  );
  const fig3Xs = fig2Xs.slice();
  const fig4Xs = fig2Xs.slice(1);

  //Set Fig2 Source Values:
  fig2Data['xs'] = fig2Xs;
  fig2Data['ys'] = [0].concat(new Array(iterations));
  fig2Data['chance_ys'] = [0].concat(new Array(iterations));
  fig2Data['highlight_alphas'] = new Array(arrLength).fill(0);
  fig2Data['heights'] = new Array(arrLength);

  //Set Fig3 Source Values:
  fig3Data['xs'] = fig3Xs;
  //First values are manually calculated constants:
  fig3Data['ll_ys'] = [0.760000].concat(new Array(iterations).fill(0));
  fig3Data['lm_ys'] = [0.650000].concat(new Array(iterations).fill(0));
  fig3Data['lr_ys'] = [0.763333].concat(new Array(iterations).fill(0));
  fig3Data['rl_ys'] = [0.746666].concat(new Array(iterations).fill(0));
  fig3Data['rm_ys'] = [0.660000].concat(new Array(iterations).fill(0));
  fig3Data['rr_ys'] = [0.783333].concat(new Array(iterations).fill(0));
  fig3Data['hb1'] = new Array(arrLength);
  fig3Data['hb2'] = new Array(arrLength);
  fig3Data['hb3'] = new Array(arrLength);
  fig3Data['hb4'] = new Array(arrLength);
  fig3Data['hb5'] = new Array(arrLength);
  fig3Data['hb6'] = new Array(arrLength);
  fig3Data['highlight_alphas'] = new Array(arrLength).fill(0);
  fig3Data['alphas_zeroes'] = new Array(arrLength).fill(0);

  //Set Fig4 Source Values:
  fig4Data['xs'] = fig4Xs;
  fig4Data['ys'] = new Array(iterations);
  fig4Data['feet'] = new Array(iterations);
  fig4Data['directions'] = new Array(iterations);
  fig4Data['actions'] = new Array(iterations);
  fig4Data['highlight_alphas'] = new Array(iterations).fill(0);
  fig4Data['avgs_placeholder'] = new Array(iterations).fill(0);

  statsFig2Src.change.emit();
  statsFig3Src.change.emit();
  statsFig4Src.change.emit();
}

initialIterationAdjustments();
"""
#</editor-fold>

def make_gameCode(
    stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
    stats_fig_4_enabled
):
    """Puts together and returns a string containing the full code for the main
    game portion of the demo.


    Arguments:
    stats_fig_1_enabled -- A bool for whether or not Game Stats Figure 1 should
      be available.
    stats_fig_2_enabled -- A bool for whether or not Game Stats Figure 2 should
      be available.
    stats_fig_3_enabled -- A bool for whether or not Game Stats Figure 3 should
      be available.
    stats_fig_4_enabled -- A bool for whether or not Game Stats Figure 4 should
      be available.
    """

    goalieStrats = fictitiousPlay + optimalMixed + randomChoice + goalieCheats

    animation = _moveGoalie + animateIter

    decisionTracking = goalieDecisionTracking + _updateDecisionTableRisks

    fig1 = _fig1Iter + _fig1Adjust + updateFig1
    fig2 = _fig2Iter + _fig2Adjust + updateFig2
    fig3 = _fig3Iter + _fig3Adjust + updateFig3
    fig4 = updateFig4
    statFigs = fig1 + fig2 + fig3 + fig4

    handleFigVisibility = make_handleFigVisibility(
        stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
        stats_fig_4_enabled
    )

    funcDefs = (iterText + rollKickerAction + goalieStrats
                + handleFigVisibility + scoring + animation + decisionTracking
                + statFigs)

    gameIter = make_gameIter(
        stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
        stats_fig_4_enabled
    )

    gameCode = gameConstants + gameIter + gameRunner
    gameCode += funcDefs

    return gameCode

def make_automateStartCode(
    stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
    stats_fig_4_enabled, show_dist_table
):
    """Puts together and returns a string containing the full code to execute
    for the first iteration of the demo.


    Arguments:
    stats_fig_1_enabled -- A bool for whether or not Game Stats Figure 1 should
      be available.
    stats_fig_2_enabled -- A bool for whether or not Game Stats Figure 2 should
      be available.
    stats_fig_3_enabled -- A bool for whether or not Game Stats Figure 3 should
      be available.
    stats_fig_4_enabled -- A bool for whether or not Game Stats Figure 4 should
      be available.
    show_dist_table -- A bool for whether or not to show the dist table for
      debugging purposes.
    """
    initialGuiDisplay = make_initialGuiDisplay(show_dist_table)

    gameCode = make_gameCode(
        stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
        stats_fig_4_enabled
    )

    automateStartCode = (initialIterationAdjustments + initialGuiDisplay
                         + gameCode)

    return automateStartCode
