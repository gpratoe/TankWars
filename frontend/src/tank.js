import { Graphics, Container } from "pixi.js";
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
        this.#setup_container();
       // this.#setup();
    }


    #setup_container(){
        this.container = new Container({
            interactive: true,
        });
        game.app.stage.addChild(this.container);
        this.#setup();
        console.log(this.container.width,this.container.height)

        
        
    }
    #setup() {
        this.rectangle = new Graphics()
            .rect(0,0,this.w,this.h)
            .fill({
                color: this.color,
                alpha: 1
            })
            .stroke({
                width: 1,
                color: 0x000000
            });
            this.container.addChild(this.rectangle);
            
            console.log(this.container.width,this.container.height);
            
            this.healthBar = new HealthBar(this.x, this.y - this.h*0.75, this.w, 5, this.health, this.container);
            
            this.container.position.x = game.canvas.width/2 + this.x;
            this.container.position.y = game.canvas.height/2 + this.y; 
            this.container.pivot.set(this.container.width/2, this.container.height/2);
    }

    update(angle){

        this.angle = angle;
        
        this.container.rotation = this.angle;
    }
}

export {Tank};