"use strict";
import { StateMachine } from "./fsm.js";
import { MenuState } from "./app_states/menu_state.js";
import { DescriptionState } from "./app_states/description_state.js";

const fsm = new StateMachine();
const containerElement = document.getElementById('player_screen');
const menu = new MenuState(fsm,containerElement,'api/');
const description = new DescriptionState(fsm,containerElement,'api/');
//set up controls for menu
menu.addButton(document.getElementById('d_pad'));
menu.addButton(document.getElementById('start_select'));
//add states to state manchine
fsm.addState('menu_state',menu);
fsm.addState('description_state',description);
//start in the menu state
fsm.changeState('menu_state');