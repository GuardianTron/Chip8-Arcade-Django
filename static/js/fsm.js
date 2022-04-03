"use strict";

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


export class ApplicationState extends AbstractState{

    constructor(stateMachine,containingDOMElement){
        super(stateMachine);
        this._containingDOMElement = containingDOMElement;
    }

    get container(){
        return this._containingDOMElement;
    }
}

