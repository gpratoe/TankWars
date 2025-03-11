import { Graphics } from "pixi.js";

class HealthBar {
    constructor(x, y, w, h, health, container) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.health = health;
        this.healthFactor = (this.h / this.health) * 10;
        this.acum = 0;
        this.container = container;
        this.#setup();
    }

    #setupBar(color) {
        const bar = new Graphics()
            .rect(this.x, this.y, this.w, this.h)
            .fill({
                color: color,
                alpha: 1
            });
        
        this.container.addChild(bar);
        return bar;
    }

    #setup() {
        // Create the static background with a stroke
        this.backgroundBar = this.#setupBar(0xFF0000);
        this.backgroundBar.stroke({
            width: 1,
            color: 0x000000,
            alignment: 0.2,
            alpha: 1
        });
        // Create the green health bar that will decrease
        this.greenBar = this.#setupBar(0x00FF00);
       
    }

    decreaseHealth() {
        // Reduce the width of the green bar
        this.acum += this.healthFactor;
        const newHeight = Math.max(this.h - this.acum, 0); // Prevent negative height
        this.greenBar.clear()
            .rect(this.x, this.y, this.w, newHeight)
            .fill(0x00FF00);
    }
}

export { HealthBar };
