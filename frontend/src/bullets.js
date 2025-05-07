import { Graphics } from "pixi.js";
import { InterpolationBuffer } from "./InterpolationBuffer";

class Bullets {
    constructor(id, x,y,dir_norm,damage,speed, app, is_local = false) {
        this.is_local = is_local;
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
        this.initial_state = {
            x: x,
            y: y,
            direction: dir_norm,
            damage: damage,
            speed: speed,
        }
        this.interpolation_buffer = new InterpolationBuffer(this.initial_state, 50, this.interp_states);
        app.stage.addChild(this.bullet);
    }

    interp_states(older_state, newer_state, t){
        const x = older_state.x + (newer_state.x - older_state.x) * t;
        const y = older_state.y + (newer_state.y - older_state.y) * t;
        const direction = older_state.direction + (newer_state.direction - older_state.direction) * t;
        const speed = older_state.speed + (newer_state.speed - older_state.speed) * t;
        const damage = this.damage;

        return {
            x: x,
            y: y,
            direction: direction,
            damage: damage,
            speed: speed
        }
    }

    set_state(state){
        const new_state = {
            x: state.x,
            y: state.y,
            direction: state.direction,
            damage: state.damage,
            speed: state.speed,
            timestamp: state.timestamp
        }
        this.interpolation_buffer.enqueue(new_state);

        this.x = state.x;
        this.y = state.y;
        this.dir_norm = state.direction;
        this.damage = state.damage;
        this.speed = state.speed;
    }

    interpolate_from_buffer() {
        const state = this.interpolation_buffer.getInterpolatedState(Date.now());
        console.log(state);
        this.bullet.position.x = state.x;
        this.bullet.position.y = state.y;
        this.dir_norm = state.direction;
    }

    update() {

        this.interpolate_from_buffer();
    }
}

export { Bullets };