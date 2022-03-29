"use strict";

import { SelectMenuBuilder,createMenuButtonHandlers } from "./ui_builders.js";

export class AbstractState{

    constructor(stateMachine){
        if(!stateMachine instanceof StateMachine){
            throw new TypeError('Instance of class StateMachine required.')
        }
        this._fsm = stateMachine
    }

    get stateMachine(){
        return this._fsm;
    }

    enter = async () =>{
        throw new Error("Callers must override base implementation.");
    }

    exit = ()=>{
        throw new Error("Callers must override base implementation.");
    }

}


export class StateMachine{
    constructor(){
        this._states = new Map();
        this._currentStateLabel = null;

    }

    addState = (stateLabel,stateInstance)=>{
        
        if(!stateInstance instanceof AbstractState){
            throw new TypeError("An object of type State is required.");
        }

        this._states.set(stateLabel,stateInstance);


    }

    changeState = (stateLabel,argumentsObject = {})=>{
        // only exit if there is a current state and it is different from the one being called
        if(this._currentStateLabel && this._currentStateLabel != stateLabel){
            this._states.get(this._currentStateLabel).exit();
        }

        if(!this._states.has(stateLabel)){
            throw new Error(`State Label ${stateLabel} is not a registered state identifier.`);
        }

        this._currentStateLabel = stateLabel
        this._states.get(stateLabel).enter(argumentsObject);
    }




}


class ApplicationState extends AbstractState{

    constructor(stateMachine,containingDOMElement){
        super(stateMachine);
        this._containingDOMElement = containingDOMElement;
    }

    get container(){
        return this._containingDOMElement;
    }
}

export class MenuState extends ApplicationState{
    constructor(stateMachine,containingDOMElement,menuSourceUrl){
        super(stateMachine,containingDOMElement);
        this._buttonElements = [];
        this._url = menuSourceUrl;
        this._menuBuilder = null;
        this._buttonHandler = null;
    }

    addButton = (buttonElement) =>{
        this._buttonElements.push(buttonElement);
    }

    enter = async () =>{
        //fetch and build menu if not already cached
        if(!this._menuBuilder){
            this._menuBuilder = await buildMenu(this._url,new SelectMenuBuilder());
            this._buttonHandler = createMenuButtonHandlers(this._menuBuilder.getMenu(),this.stateMachine);
        }
        let menu = this._menuBuilder.getMenu()
        //wire event handlers for buttons
        this._buttonElements.forEach(button =>{
            button.addEventListener('click',this._buttonHandler);
        });        
        this.container.appendChild(menu);

    }

    exit = ()=>{
        this._buttonElements.forEach(button =>{
            button.removeEventListener('click',this._buttonHandler);
        });
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

