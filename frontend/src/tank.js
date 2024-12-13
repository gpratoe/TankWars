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
        this.bullets = new Bullets(this.bullet_speed);
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

    update(){
        const dx = game.mouseX - this.container.x;
        const dy = game.mouseY - this.container.y;
                
        this.angle = Math.atan2(dy,dx);
        
        this.container.rotation = this.angle;


        const mag = Math.sqrt(dx * dx + dy * dy);
        const topSpeed = 15;
        if( mag >= this.container.width && !game.isMouseDown ){        
            
            const normDx = dx / mag;
            const normDy = dy / mag;

            let ds = (mag*5) / this.container.width;
            const speed =  ds > topSpeed ? topSpeed : ds ;

            this.container.x += normDx * speed;
            this.container.y += normDy * speed;
        
        }
        
        if(game.isMouseDown){

            this.bullets.shoot(this.container.position.x, this.container.position.y, this.angle, this.damage);
        }
        this.bullets.update();
        
        game.wsManager.send("state",
            {
            name: this.name, 
            mouseX: game.mouseX ? game.mouseX : this.x, 
            mouseY: game.mouseY ? game.mouseY : this.y, 
            shooting: game.isMouseDown}
        );
    }
}

export {Tank};