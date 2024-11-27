import { Graphics } from "pixi.js";
import { game } from "./game";
import { HealthBar } from "./healthbar";

class Tank {

    constructor(name, color, x, y, w , h, angle, damage, bullet_speed)
    {
        this.name = name;
        this.health = 100;
        this. color = color;
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.angle = angle;
        this.damage = damage;
        this.bullet_speed = bullet_speed;
        this.#setup();
    }


    
    #setup() {
        this.rectangle = new Graphics()
            .rect(this.x,this.y,this.w,this.h)
            .fill({
                color: this.color,
                alpha: 1
            })
            .stroke({
                width: 1,
                color: 0x000000
            });
        this.rectangle.pivot.set(this.w/2,this.h/2);
        this.rectangle.position.x = game.canvas.width/2;
        this.rectangle.position.y = game.canvas.height/2;
        game.app.stage.addChild(this.rectangle);
        this.healthBar = new HealthBar(this.x, this.y - this.h*0.75, this.w, 5, this.health);
    }
}

export {Tank};