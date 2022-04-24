import { StateMachine, ApplicationState } from "../fsm.js";
import { Chip8Emulator } from "../Chip-8-Emulator/chip8emulator.js";
import { loadGame } from "../Chip-8-Emulator/loaders.js";


export class GameState extends ApplicationState{

    constructor(containingDOMElement, chip8FontURL, superChipFontURL){
        super(containingDOMElement);
        this._canvasElement = document.createElement('canvas');
        this._canvasElement.id = "game_canvas";
        this._emulator = new Chip8Emulator(this._canvasElement);
        this._chip8FontURL = chip8FontURL;
        this._superChipFontURL = superChipFontURL
    }

    enter = async ({gameData})=>{
        console.log(gameData);
        this.mapKeys(gameData.keys);
        loadGame(this._emulator,this._chip8FontURL,this._superChipFontURL,gameData.file,fetchAndTranscodeGameRom);

    }

    mapKeys = keyData =>{
      this._emulator.keyboardMapper.clearKeyMap();
        keyData.forEach(key =>{
            this._emulator.keyboardMapper.mapKey(key.keyboard_code,key.chip8_key);
      });
    }


}


async function fetchAndTranscodeGameRom(romURL){
    const response = await fetch(romURL);
    if(!response.ok){
        throw new Error(`Unable to load rom ${romURL}`);
    }
    const hexString = await response.text();
    return hexStringToBinBuffer(hexString);
}

function hexStringToBinBuffer(hexString){
    //note: hex string is twice the size of actual data
    const buffer = new Uint8Array(hexString.length/2);
    //every two characters represents a byte.
    for(let i=0; i < hexString.length; i+=2){
        const byteString = hexString.slice(i,i+1);
        buffer[i/2] = parseInt(byteString,16);
        
    }
    return buffer

}


