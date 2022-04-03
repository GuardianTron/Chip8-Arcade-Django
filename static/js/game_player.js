"use strict";
import { StateMachine } from "./fsm.js";
import { MenuState } from "./app_states/menu_state.js";

const fsm = new StateMachine();
const menu = new MenuState(fsm,document.getElementById('player_screen'),'api/');
//set up controls for menu
menu.addButton(document.getElementById('d_pad'));
menu.addButton(document.getElementById('start_select'));
//add states to state manchine
fsm.addState('menu_state',menu);
//start in the menu state
fsm.changeState('menu_state');