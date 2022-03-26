"use strict";
export class SelectMenuBuilder{

    construct(){
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