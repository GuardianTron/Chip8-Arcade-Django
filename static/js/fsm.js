"use strict";

export class AbstractState{

    constructor(){
        this._fsm = null;
    }

    get stateMachine(){
        return this._fsm;
    }

    set stateMachine(stateMachine){
        if(this._fsm !== null){
            throw new Error("This state is around bound to a state machine.");
        }
        else if(!(stateMachine instanceof StateMachine)){
            throw new Error("The state machine set was not an instance of StateMachine.");
        }

        this._fsm = stateMachine;
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
        stateInstance.stateMachine = this;
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

    constructor(containingDOMElement){
        super();
        this._containingDOMElement = containingDOMElement;
        this._buttonElements = [];
    }

    addButton = buttonElement =>{
        this._buttonElements.push(buttonElement);
    }

    get buttons(){
        return this._buttonElements;
    }

    get container(){
        return this._containingDOMElement;
    }

    registerButtonHandler = (eventType,handlerFunction) =>{
        this.buttons.forEach(button => {
            button.addEventListener(eventType,handlerFunction);
        });
    }

    unregisterButtonHandler = (eventType,handlerFunction) =>{
        this.buttons.forEach(button =>{
            button.removeEventListener(eventType,handlerFunction);
        });
    }
}

