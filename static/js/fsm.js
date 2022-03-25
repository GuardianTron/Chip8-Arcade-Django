"use strict";

import { SelectMenuBuilder } from "./ui_builders";

export class AbstractState{

    construct(stateMachine){
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
        
        if(!stateInstance instanceof State){
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

    construct(stateMachine,containingDOMElement){
        super(stateMachine);
        this._containingDOMElement = containingDOMElement;
    }

    get container(){
        return this._containingDOMElement;
    }
}

class MenuState extends ApplicationState{
    contsruct(stateMachine,containingDOMElement,menuSourceUrl){
        super(stateMachine,containingDOMElement);
        this._url = menuSourceUrl;
        this._menuBuilder = null;
    }

    enter = async () =>{
        //fetch and build menu if not already cached
        if(!this._menuBuilder){
            this._menuBuilder = await buildMenu(this._url,SelectMenuBuilder());
        }
        this._menuBuilder.activateEventListeners();
        this.container.appendChild(this._menuBuilder.getMenu());

    }

    exit = ()=>{
        this.container.removeChild(this._menuBuilder.getMenu());
        this._menuBuilder.deactivateEventListeners();
    }
}

async function buildMenu(sourceURL,menuBuilder){
    let response = await fetch(sourceURL);
    let menuData = await response.json();
    Object.keys(menuData).forEach( key => {
        menuBuilder.addOption(key,menuData[key]);

    });

    return menuBuilder;
        
}

