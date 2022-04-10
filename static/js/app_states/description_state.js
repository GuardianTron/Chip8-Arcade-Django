import { ApplicationState, StateMachine } from "../fsm.js";

export class DescriptionState extends ApplicationState{

    constructor(stateMachine,containingDOMElement, url){
        super(stateMachine,containingDOMElement);
        this._games = new GameModel(url);
        this._descriptionBuilder = new DescriptionBuilder();
        this._buttonHandler = null;
        
       }

    enter = async ({game_id = null}) => {
        const gameData = await this._games.fetch(game_id);
        this._descriptionBuilder.titleText = gameData.title;
        this._descriptionBuilder.descriptionText = gameData.description;
        this.container.appendChild(this._descriptionBuilder.element);
        this._buttonHandler = createButtonHandler(gameData,this.stateMachine);
        this.registerButtonHandler('click',this._buttonHandler);
    }

    exit = ()=>{
        this.unregisterButtonHandler('click',this._buttonHandler);
        this.container.removeChild(this._descriptionBuilder.element);
    }
    
}

class GameModel{

    constructor( base_url ){
        this._base_url = base_url;
        this._gameCache = new Map();
    }

    fetch = async (game_id)=>{
        if(this._gameCache.has(game_id)){
            return this._gameCache.get(game_id);
        }
        const gameResponse = await fetch(`${this._base_url}${game_id}?format=json`);
        const gameData = await gameResponse.json();
        this._gameCache.set(game_id,gameData);
        return gameData;

    }





}

class ElementBuilder{
     constructor(elementType,{id = null, htmlClass = null}={}){
         this._element = document.createElement(elementType);
         if(id){
             this._element.setAttribute('id',id);
         }
         if(htmlClass){
             this._element.setAttribute('class',htmlClass)
         }
     }

     get element(){
         return this._element;
     }

     set textContent(content){
         this.removeChildren();
         this.element.appendChild(document.createTextNode(content));
     }

     removeChildren = ()=>{
         while(this._element.firstChild){
             this._element.removeChild(this._element.firstChild);
         }
     }






}

class ParagraphContainerBuilder extends ElementBuilder{

    set textContent(content){
        this.removeChildren();
        const paragraphContent = content.split(/\r?\n/);

        paragraphContent.forEach(element => {
            let paragraph = document.createElement('p');
            paragraph.appendChild(document.createTextNode(content));
            this.element.appendChild(paragraph);

        });

    }
}



class DescriptionBuilder extends ElementBuilder{

    constructor({id=null,htmlClass=null}={}){
        super('div',{id:id,htmlClass:htmlClass});
        this._titleElement = new ElementBuilder('h1');
        this._descriptionElement = new ParagraphContainerBuilder('div');

        this.element.appendChild(this._titleElement.element);
        this.element.appendChild(this._descriptionElement.element);
    }

    set titleText(content){
        this._titleElement.textContent = content;
    }

    set descriptionText(content){
        this._descriptionElement.textContent = content;
    }




}

function createButtonHandler(gameData,stateMachine){
    if(! stateMachine instanceof StateMachine){
        throw new TypeError('StateMachine instance required for first parameter.');
    }
    return e =>{
        if(e.target.id = "button_start"){
            stateMachine.changeState('game_state',{gameData:gameData});
        }
    }
}