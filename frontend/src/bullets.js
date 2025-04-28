import { Graphics } from "pixi.js";

class Bullets {
    constructor(id, x,y,dir_norm,damage,speed, app){
        this.id = id;
        this.x = x;
        this.y = y;
        this.damage = damage;
        this.app = app;
        this.speed = speed;
        this.dir_norm = dir_norm;
        this.bullet = new Graphics()
        .circle(1.5, 1.5, 3)
        .fill(0x000000);
        this.bullet.pivot.set(this.bullet.width/2, this.bullet.height/2);
        this.bullet.position.x = x;
        this.bullet.position.y = y;
        app.stage.addChild(this.bullet);
    }

    set_state(state){
        this.x = state.x;
        this.y = state.y;
        this.dir_norm = state.direction;
        this.damage = state.damage;
        this.speed = state.speed;
    }

    update() {
        let dx = this.x - this.bullet.position.x;
        let dy = this.y - this.bullet.position.y;
        let distSq = dx*dx + dy*dy;
    
        let lerp_factor = Math.min(1.0, 0.1 + distSq / 1000);

        this.bullet.position.x += (this.x - this.bullet.position.x) * lerp_factor;
        this.bullet.position.y += (this.y - this.bullet.position.y) * lerp_factor;
    }
}

export { Bullets };