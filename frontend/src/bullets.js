import { Graphics } from "pixi.js";

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
        this.state_buffer = [];
        app.stage.addChild(this.bullet);
    }

    set_state(state){
        const new_state = {
            x: state.x,
            y: state.y,
            direction: state.direction,
            damage: state.damage,
            speed: state.speed,
            timestamp: Date.now()
        }
        this.state_buffer.push(new_state);
        this.state_buffer = this.state_buffer.filter(s => Date.now() - s.timestamp <= 200);

        this.x = state.x;
        this.y = state.y;
        this.dir_norm = state.direction;
        this.damage = state.damage;
        this.speed = state.speed;
    }

    local_update() {
        let dx = this.x - this.bullet.position.x;
        let dy = this.y - this.bullet.position.y;
        let distSq = dx*dx + dy*dy;
        
        let lerp_factor = Math.min(1.0, 0.05 + distSq / 2000);
        
        // deadzone to prevent micro-movements
        if (distSq > 0.1) {
            this.bullet.position.x += (this.x - this.bullet.position.x) * lerp_factor;
            this.bullet.position.y += (this.y - this.bullet.position.y) * lerp_factor;
        }
    }

    interpolate_from_buffer() {
        if (this.state_buffer.length < 2) return;

        const render_time = Date.now() - 50;
        let older_state = null;
        let newer_state = null;

        for (let i = 0; i < this.state_buffer.length - 1; i++) {
            const a = this.state_buffer[i];
            const b = this.state_buffer[i + 1];
            if (a.timestamp <= render_time && b.timestamp > render_time) {
                older_state = a;
                newer_state = b;
                break;
            }
        }

        if (!older_state || !newer_state) return;
        const t = (render_time - older_state.timestamp) / (newer_state.timestamp - older_state.timestamp);
        this.bullet.position.x = older_state.x + (newer_state.x - older_state.x) * t;
        this.bullet.position.y = older_state.y + (newer_state.y - older_state.y) * t;
    }

    update() {
        if (this.is_local) {
            this.local_update();
        }else{
            this.interpolate_from_buffer();
        }
    }
}

export { Bullets };