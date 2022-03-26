"use strict";
import { StateMachine } from "./fsm";
export class SelectMenuBuilder{

    constructor(){
        this._menu = document.createElement('select');
        this._listeners = {};
        this._areListenersActivated = false;
        this._menu.selectNext = function(){
            if(this.selectedIndex < this.children.length -1){
                this.selectedIndex++;
            }
        }

        this._menu.selectPrevious() = function(){   
            if(this.selectedIndex > 0){
                this.selectedIndex--;
            }
        }

        this._menu.getSelectedId() = function(){
            if(this.selectedIndex > -1){
                return this.options[this.selectedIndex].value;
            }
            throw new Error('No id selected.');
        }
    }

    addOption = (value,text) =>{
        option = document.createElement('option');
        option.setAttribute('value',value);
        option.appendChild(document.createTextNode('text'));
        this._menu.appendChild(option);
        this._menu.setAttribute('size',this._menu.children.length);
        
    }

    registerEventListener = (listenerType,func)=>{
         if(!listenerType in this._listeners){
             this._listeners[listenerType] = [];
         }   
         this._listeners[listenerType] = func;
         
    }

    activateEventListeners = () =>{
        if(!this._areListenersActivated){
            Object.key(this._listeners).forEach( key =>{
                this._menu.addEventListener(key,this._listeners[key]);
            });
            this._areListenersActivated = true;
        }
    }

    deactivateEventListeners = () =>{
        if(this._areListenersActivated){
            Object.keys(this._listeners).forEach( key =>{
                this._menu.removeEventListener(key,this)
            });
            this._areListenersActivated = false;
        }
    }

    getMenu = () =>{
        return this._menu;
    }


}

export function createMenuButtonHandlers(menu,stateMachine){
    if(!stateMachine instanceof StateMachine){
        throw new TypeError('stateMachine must be an instance of StateMachine.');

    }



    return e =>{
        switch(e.targe.id){
            case 'dir_down':
                menu.selectNext();
                break;
            case 'dir_up': 
                menu.selectPrevious();
            case 'button_start':
                let gameId = menu.getSelectedId();
                stateMachine.changeState('description_state',{'id':gameId});
        }
    };
}


