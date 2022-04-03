"use strict";
import { StateMachine } from "./fsm.js";
import { MenuState } from "./app_states/menu_state.js";

const fsm = new StateMachine();
const menu = new MenuState(fsm,document.getElementById('player_screen'),'api/');
menu.addButton(document.getElementById('d_pad'));
menu.addButton(document.getElementById('start_select'));
fsm.addState('menu_state',menu);
fsm.changeState('menu_state');