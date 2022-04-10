import { StateMachine, ApplicationState } from "../fsm.js";
import { Chip8Emulator } from "../Chip-8-Emulator/chip8emulator.js";


export class GameState extends ApplicationState{

    constructor(stateMachine,containingDOMElement){
        super(stateMachine,containingDOMElement);
        this._canvasElement = document.createElement('canvas');
        this._canvasElement.id = "game_canvas";
        this._emulator = new Chip8Emulator(this._canvasElement);
    }

    enter = async ({gameData})=>{
        console.log(gameData);
        this.mapKeys(gameData.keys);
        this.container.appendChild(this._canvasElement);

    }

    mapKeys = keyData =>{
      this._emulator.keyboardMapper.clearKeyMap();
        keyData.forEach(key =>{
            this._emulator.keyboardMapper.mapKey(key.keyboard_code,key.chip8_key);
      });
    }


}


