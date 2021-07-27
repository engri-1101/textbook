#This file contains the JavaScript code strings that are used for the main game
#loop.

#Any JavaScript Function defined in the strings with a name starting with the
#'_' character is a helper function.


#TODO: continue improving code efficiency.
#<editor-fold Functions:
  #<editor-fold iterText():
iterText = """
function iterText(roundsPlayed, gameScore, goal) {
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
rollKickerAction = """
function rollKickerAction() {
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
fictitiousPlay = """
//Handle Goalie Decision
function fictitiousPlay(footIsLeft, footDict) {
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
  //return the action of the pure strategy corresponding to the kicker foot:
  const strats = {
    'Left'  : 'leftStrat',
    'Right' : 'rightStrat'
  };
  const actionIndex = counterSrc.data[strats[kickerFoot]].indexOf(1);
  return directions[actionIndex];
}
"""
  #</editor-fold>
  #<editor-fold _handleFigVisibility():
_handleFigVisibility = """
function _handleFigVisibility(stratIsFictPlay) {
  nextButton.visible = false;
  gameFig.visible = false;
  distTable.visible = false;

  //set button visibilities:
  [true, true, stratIsFictPlay, true].forEach(
    (v, i) => figButtons[i].visible = v
  );

  statsFig1.visible = true;
  statsFig2.visible = false;
  statsFig3.visible = false;
  statsFig4.visible = false;
}
"""
  #</editor-fold>
  #<editor-fold scoring():
scoring = """
function scoring(footDict, kickerKick, goalieAction, actionsIndexKFKK) {
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
  //Move both components of the goalie:
  goalieBody.x = xLoc;
  goalieHead.x = xLoc;
}
"""
  #</editor-fold>
  #<editor-fold animateIter():
animateIter = """
function animateIter(goalieAction, kickerKick, goal) {
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
  //Plot Values:
  fig2Data['ys'][roundsPlayed] = gameScore;
  fig2Data['chance_ys'][roundsPlayed] = 2*roundScoreChance - 1;
}
"""
  #</editor-fold>
  #<editor-fold _fig2Adjust():
_fig2Adjust = """
function _fig2Adjust(fig2Data, itersToRun) {
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
  statsFig2.x_range.start -= 0.5;
  statsFig2.x_range.end   += 0.5;

  //Resize hit boxes:
  const hitboxHeight = 2 * Math.max(Math.abs(maxVal), Math.abs(minVal));
  fig2Data['height'] = new Array(itersToRun + 1).fill(hitboxHeight);
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
  statsFig3.x_range.start -= 0.5;
  statsFig3.x_range.end   += 0.5;
}
"""
  #</editor-fold>
  #<editor-fold updateFig3():
updateFig3 = """
function updateFig3(roundsPlayed, roundIsLastIter, itersToRun) {
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
  roundsPlayed, //Test comment
  roundScoreChance,
  kickerFoot,
  kickerKick,
  goalieAction
) {
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

func_defs = (iterText + rollKickerAction + fictitiousPlay + optimalMixed
             + randomChoice + goalieCheats + _handleFigVisibility + scoring
             + _moveGoalie + animateIter + _updateDecisionTableRisks
             + goalieDecisionTracking + _fig1Iter + _fig1Adjust + updateFig1
             + _fig2Iter + _fig2Adjust + updateFig2 + _fig3Iter + _fig3Adjust
             + updateFig3 + updateFig4)

#</editor-fold>

#<editor-fold Game Iteration:
game_iter = """
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

function gameIter(){
  const itersToRun = parseInt(itersToRunDiv.text);

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

  switch (gameStrat){
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

  updateFig1(goal, directionsIndexGa, actionsIndexKFKK, roundIsLastIter);

  updateFig2(
    roundsPlayed,
    gameScore,
    roundScoreChance,
    roundIsLastIter,
    itersToRun
  );

  if(stratIsFictPlay) { updateFig3(roundsPlayed, roundIsLastIter, itersToRun); }

  updateFig4(
    roundsPlayed,
    roundScoreChance,
    kickerFoot,
    kickerKick,
    goalieAction
  );

  if(roundIsLastIter) { _handleFigVisibility(stratIsFictPlay); }

  iterText(roundsPlayed, gameScore, goal);
}

async function gameLoop(){
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
    const notLastRound = (
      parseInt(nround.text) < parseInt(itersToRunDiv.text)
    );

    //True if the button is activated by the user:
    const automatedAdvancementActivated = (autoAdvanceButton.active);

    //True if both conditions are true:
    const conditionsFulfilled = (
      notLastRound && automatedAdvancementActivated
    );

    //If all recursion conditions are fulfilled:
    if(conditionsFulfilled){

      //Setup the promise that enforces waiting for the delay to finish:
      const iterationDelay = (

        //Creates the promise with parameter ms:
        (ms) => new Promise(

          //Waits for ms seconds before resolving:
          (resolve) => setTimeout(
            () => {resolve(); },
            ms
          )
        )

      );

      //Await the delay, then recurse:
      await iterationDelay(300).then(
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

game_iter += func_defs

#<editor-fold start button Initial Gui Display:
#This code string changes the visibility values of various game gui elements
#in order to change the user view from that used in the earlier menu like
#screens to one used for the game screens.
initial_gui_display = """
startButton.visible = false;
nextButton.visible = true;
llAimTextInput.visible = false;
lmAimTextInput.visible = false;
lrAimTextInput.visible = false;
rlAimTextInput.visible = false;
rmAimTextInput.visible = false;
rrAimTextInput.visible = false;
iterSlider.visible = false;
stratDropdown.visible = false;
automationTable.visible = false;
distTable.visible = true;
"""
#</editor-fold>

b_automate_start_code = initial_gui_display + game_iter
