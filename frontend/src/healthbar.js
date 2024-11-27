import { Graphics } from "pixi.js";
import { game } from "./game";

class HealthBar {
    constructor(x, y, w, h, health) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.health = health;
        this.healthFactor = (this.w / this.health) * 10;
        this.acum = 0;
        this.#setup();
        this.decreaseHealth();
    }

    #setupBar(color, width) {
        const bar = new Graphics()
            .rect(this.x, this.y, width, this.h)
            .fill(color);
        bar.pivot.set(this.w / 2, this.h / 2);
        bar.position.set(game.canvas.width / 2, game.canvas.height / 2);
        game.app.stage.addChild(bar);
        return bar;
    }

    #setup() {
        // Create the static background with a stroke
        this.backgroundBar = this.#setupBar(0xFF0000, this.w);
        this.backgroundBar.stroke({
            width: 1,
            color: 0x000000,
            alignment: 0.2
        });
        // Create the green health bar that will decrease
        this.greenBar = this.#setupBar(0x00FF00, this.w);
       
    }

    decreaseHealth() {
        // Reduce the width of the green bar
        this.acum += this.healthFactor;
        const newWidth = Math.max(this.w - this.acum, 0); // Prevent negative width
        this.greenBar.clear()
            .rect(this.x, this.y, newWidth, this.h)
            .fill(0x00FF00);
    }
}

export { HealthBar };
