import { Graphics } from "pixi.js";

class Bullets {
    constructor(id, x,y,dir_norm,damage,speed, app){
        this.id = id;
        this.x = x;
        this.y = y;
        console.log(x,y)
        this.damage = damage;
        this.app = app;
        this.speed = speed;
        this.dir_norm = dir_norm;
        this.bullet = new Graphics()
        .circle(0, 0, 5)
        .fill(0x000000);
        this.bullet.pivot.set(this.bullet.width/2, this.bullet.height/2);
        this.bullet.position.x = x;
        this.bullet.position.y = y;
        app.stage.addChild(this.bullet);
    }
}

export { Bullets };