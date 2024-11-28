import { Graphics, Container } from "pixi.js";
import { game } from "./game";
import { HealthBar } from "./healthbar";
import { Bullet } from "./bullet";

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
        this.bullets = []
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

    update(){
        const dx = game.mouseX - this.container.x;
        const dy = game.mouseY - this.container.y;
                
        this.angle = Math.atan2(dy,dx);
        
        this.container.rotation = this.angle;


        const mag = Math.sqrt(dx * dx + dy * dy);
        const topSpeed = 15;
        const bulletSpeed = 17;
        if( mag >= this.container.width && !game.isMouseDown ){        
            
            const normDx = dx / mag;
            const normDy = dy / mag;

            let ds = (mag*5) / this.container.width;
            const speed =  ds > topSpeed ? topSpeed : ds ;

            this.container.x += normDx * speed;
            this.container.y += normDy * speed;
        
        }
        
        if(game.isMouseDown){
            const bullet = new Graphics()
                .rect(0,0,5,5)
                .fill({
                    color: 0xFF00FF,
                    alpha: 1
                    })
                .stroke({
                    width: 2,
                    color: 0x000000
                    });

            bullet.pivot.set(bullet.width/2, bullet.height/2);
            bullet.position.x = this.container.position.x;
            bullet.position.y = this.container.position.y;
            this.bullets.push([bullet, this.angle]);
            this.bullets.forEach(bullet => {
                game.app.stage.addChild(bullet[0]);
            });
        }

        for(let i = 0; i < this.bullets.length; i++) {
            if (this.bullets[i][0].x > game.app.screen.width || this.bullets[i][0].x < 0 || 
                this.bullets[i][0].y > game.app.screen.height || this.bullets[i][0].y < 0) {

                this.bullets[i][0].destroy();
                this.bullets.splice(i,1);
            } else {
                this.bullets[i][0].x += bulletSpeed*Math.cos(this.bullets[i][1]);
                this.bullets[i][0].y += bulletSpeed*Math.sin(this.bullets[i][1]);
            }
        }
    }
}

export {Tank};