import { Graphics } from "pixi.js";

class HealthBar {
    constructor(x, y, w, h, maxHealth, container) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.maxHealth = 100;
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

    setHealth(health) {
        const newh = this.h * (health / this.maxHealth)
        this.greenBar.clear()
            .rect(this.x, this.y, this.w, newh)
            .fill(0x00FF00);

    }
}

export { HealthBar };
