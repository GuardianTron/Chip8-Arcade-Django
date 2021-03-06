"use strict";
import { StateMachine } from "./fsm.js";
import { MenuState } from "./app_states/menu_state.js";
import { DescriptionState } from "./app_states/description_state.js";
import { GameState } from "./app_states/game_state.js";

const fsm = new StateMachine();
const containerElement = document.getElementById('player_screen');
const menu = new MenuState(containerElement,'api/');
const description = new DescriptionState(containerElement,'api/');
const gamePlayer = new GameState(containerElement);

const startSelect = document.getElementById('start_select');
const dPad = document.getElementById('d_pad');
const actionButtons = document.getElementById('buttons');

//set up controls for menu
menu.addButton(dPad);
menu.addButton(startSelect);

//set up conrols for description
description.addButton(startSelect);

//add states to state manchine
fsm.addState('menu_state',menu);
fsm.addState('description_state',description);
fsm.addState('game_state',gamePlayer);
//start in the menu state
fsm.changeState('menu_state');