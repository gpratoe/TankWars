import { Graphics } from "pixi.js";
import {game} from "./game";
class Bullet {
    constructor(speed){
        this.speed = speed;
        this.alive_bullets = [];
    }

    shoot(x, y, dir_norm, damage){
        this.dir_norm = dir_norm;
        this.alive_bullets.push(new Graphics()
            .circle(x, y, 5)
            .fill(0x000000)
        );
        game.app.stage.addChild(this.alive_bullets[this.alive_bullets.length - 1]);
    }

    update(){
        for(let i = 0; i < this.alive_bullets.length; i++){
            if(this.alive_bullets[i].x > game.canvas.width || this.alive_bullets[i].x < 0 || 
                this.alive_bullets[i].y > game.canvas.height || this.alive_bullets[i].y < 0) {
                this.alive_bullets[i].destroy();
                this.alive_bullets.splice(i, 1);
            } else {
                this.alive_bullets[i].x += this.dir_norm*this.speed;
            }
        }
    }
}

export { Bullet };