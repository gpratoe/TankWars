import { Graphics } from "pixi.js";

class HealthBar {
    constructor(x, y, w, h, health, container) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.health = health;
        this.healthFactor = (this.w / this.health) * 10;
        this.acum = 0;
        this.container = container;
        this.#setup();
    }

    #setupBar(color, width) {
        const bar = new Graphics()
            .rect(0, -2*this.h, width, this.h)
            .fill({
                color: color,
                alpha: 1
            });
        
        this.container.addChild(bar);
        return bar;
    }

    #setup() {
        // Create the static background with a stroke
        this.backgroundBar = this.#setupBar(0xFF0000, this.w);
        this.backgroundBar.stroke({
            width: 1,
            color: 0x000000,
            alignment: 0.2,
            alpha: 1
        });
        // Create the green health bar that will decrease
        this.greenBar = this.#setupBar(0x00FF00, this.w);
       
    }

    decreaseHealth() {
        // Reduce the width of the green bar
        this.acum += this.healthFactor;
        const newWidth = Math.max(this.w - this.acum, 0); // Prevent negative width
        this.greenBar.clear()
            .rect(0, -2*this.h, newWidth, this.h)
            .fill(0x00FF00);
    }
}

export { HealthBar };
