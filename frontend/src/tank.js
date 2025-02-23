import { Graphics, Container } from "pixi.js";
import { game } from "./game";
import { HealthBar } from "./healthbar";
import { Bullets } from "./bullets";

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
        this.bullets = game.bullets;
        this.isShooting = false;
        this.mouseX = x;
        this.mouseY = y;
       // this.#setup();
    }


    #setup_container(){
        this.container = new Container({
            interactive: true,
        });
        game.app.stage.addChild(this.container);
        this.#setup();
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
            
            this.healthBar = new HealthBar(this.x, this.y - this.h*0.75, this.w, 5, this.health, this.container);
            
            this.container.position.x = this.x;
            this.container.position.y = this.y; 
            this.container.pivot.set(this.container.width/2, this.container.height/2);
    }
    
    set_state(state){
        this.x = state.tankx;
        this.y = state.tanky;
        //this.container.x = state.tankx;
        //this.container.y = state.tanky;
        this.angle = state.angle;
        this.container.rotation = state.angle;
        if(this.health > state.health){
            this.healthBar.decreaseHealth();
        }
        this.health = state.health;
    }

    update() {
        let lerp_factor = 0.1;
        this.container.position.x += (this.x - this.container.position.x) * lerp_factor;
        this.container.position.y += (this.y - this.container.position.y) * lerp_factor;

    }
}

export {Tank};