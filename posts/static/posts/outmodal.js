
const outclick = new Event("outsideclick");

class elementClickoutside {
    constructor(element, anotherelement = null) {
        this.element = element;
        if (anotherelement) {
            this.anotherelement = anotherelement;
        }
        document.addEventListener("click", this);
    }
    detectClickOutside(event) {
        if (!this.element.contains(event.target)) {
            this.element.dispatchEvent(outclick);
            if (this.anotherelement) {
                this.anotherelement.dispatchEvent(outclick);
            }
        }
    }
    handleEvent(event) {
        if (event.type === "click") {
            this.detectClickOutside(event);
        }
    }
}

function successmodalinit(event) {
    if (document.querySelector(".successmodal")) {
        successmodal = document.querySelector(".successmodal");
        elementClickoutside0 = new elementClickoutside(successmodal, document.querySelector(".post-list"));
    }
}

document.addEventListener('htmx:load', successmodalinit);




