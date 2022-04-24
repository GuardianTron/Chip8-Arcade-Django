"use strict";
import { StateMachine, ApplicationState } from "../fsm.js";
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

        this._menu.selectPrevious = function(){   
            if(this.selectedIndex > 0){
                this.selectedIndex--;
            }
        }

        this._menu.getSelectedId = function(){
            if(this.selectedIndex > -1){
                return this.options[this.selectedIndex].value;
            }
            throw new Error('No id selected.');
        }
    }

    addOption = (value,text) =>{
        const option = document.createElement('option');
        option.setAttribute('value',value);
        option.appendChild(document.createTextNode(text));
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
        switch(e.target.id){
            case 'dir_down':
                menu.selectNext();
                break;
            case 'dir_up': 
                menu.selectPrevious();
                break;
            case 'button_start':
                let gameId = menu.getSelectedId();
                stateMachine.changeState('description_state',{game_id:gameId});
                break;
        }
    };
}

export class MenuState extends ApplicationState{
    constructor(containingDOMElement,menuSourceUrl){
        super(containingDOMElement);
        this._url = menuSourceUrl;
        this._menuBuilder = null;
        this._buttonHandler = null;
    }

    enter = async () =>{
        //fetch and build menu if not already cached
        if(!this._menuBuilder){
            this._menuBuilder = await buildMenu(this._url,new SelectMenuBuilder());
            this._buttonHandler = createMenuButtonHandlers(this._menuBuilder.getMenu(),this.stateMachine);
        }
        let menu = this._menuBuilder.getMenu()
        //wire event handlers for buttons
        this.registerButtonHandler('click',this._buttonHandler);      
        this.container.appendChild(menu);

    }

    exit = ()=>{
        this.unregisterButtonHandler('click',this._buttonHandler);
        this.container.removeChild(this._menuBuilder.getMenu());
        
    }
}

async function buildMenu(sourceURL,menuBuilder){
    let response = await fetch(sourceURL);
    let menuData = await response.json();
    menuData.forEach( menuItem => {
        menuBuilder.addOption(menuItem['id'],menuItem['title']);

    });

    return menuBuilder;
        
}




