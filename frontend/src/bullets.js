import { Graphics } from "pixi.js";
import {game} from "./game";
class Bullets {
    constructor(speed){
        this.speed = speed;
        this.alive_bullets = [];
    }

    shoot(x, y, dir_norm, damage){
        this.dir_norm = dir_norm;
        const bullet = new Graphics()
        .circle(0, 0, 5)
        .fill(0x000000);
        bullet.pivot.set(bullet.width/2, bullet.height/2);
        bullet.position.x = x;
        bullet.position.y = y;
        this.alive_bullets.push([bullet, dir_norm]);
        game.app.stage.addChild(this.alive_bullets[this.alive_bullets.length - 1][0]);
    }

    update(){
        for(let i = 0; i < this.alive_bullets.length; i++){
            if(this.alive_bullets[i][0].x > game.canvas.width || this.alive_bullets[i][0].x < 0 || 
                this.alive_bullets[i][0].y > game.canvas.height || this.alive_bullets[i][0].y < 0) {

                this.alive_bullets[i][0].destroy();
                this.alive_bullets.splice(i, 1);
            } else {
                this.alive_bullets[i][0].x += this.speed*Math.cos(this.alive_bullets[i][1]);
                this.alive_bullets[i][0].y += this.speed*Math.sin(this.alive_bullets[i][1]);
            }
        }
    }
}

export { Bullets };