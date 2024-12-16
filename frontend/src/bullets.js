import { Graphics } from "pixi.js";
import {game} from "./game";
class Bullets {
    constructor(x,y,dir_norm,damage,speed){
        this.speed = speed;
        this.dir_norm = dir_norm;
        this.bullet = new Graphics()
        .circle(0, 0, 5)
        .fill(0x000000);
        this.bullet.pivot.set(this.bullet.width/2, this.bullet.height/2);
        this.bullet.position.x = x;
        this.bullet.position.y = y;
        game.app.stage.addChild(this.bullet);
    }
}

export { Bullets };