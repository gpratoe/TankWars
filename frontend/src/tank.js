import { Container, Assets, Sprite } from "pixi.js";
import { HealthBar } from "./healthbar";

class Tank {
    constructor(player_id, name, color, x, y, w , h, angle, damage, bullet_speed, app, is_local = false)
    {
        this.player_id = player_id
        this.app = app;
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
        this.isShooting = false;
        this.mouseX = x;
        this.mouseY = y;
        this.is_local = is_local;
        this.state_buffer = [{
            x: x,
            y: y,
            angle: angle,
            timestamp: Date.now()
        }];
       // this.#setup();
    }


    #setup_container(){
        this.container = new Container({
            interactive: true,
        });
        this.container.position.x = this.x;
        this.container.position.y = this.y; 
        this.container.pivot.set(this.container.width/2, this.container.height/2);

        this.container.angle = this.angle;
        
        this.app.stage.addChild(this.container);
        
        this.#setup();
    }
    #setup() {
        const texture = Assets.get(`/assets/tank_sprite_${this.color}.png`);

        this.sprite = new Sprite(texture);

        this.sprite.x = 0;
        this.sprite.y = 0;
        this.sprite.width = this.w;
        this.sprite.height = this.h;
        this.sprite.anchor.set(0.5);

        this.container.addChild(this.sprite);
        
        
        this.healthBar = new HealthBar(-this.w*0.75, -this.h/2, 3, this.h, this.health, this.container);
    }
    
    set_state(state){
        const new_state = {
            x: state.tankx,
            y: state.tanky,
            angle: state.angle,
            timestamp: Date.now()
        }
        this.state_buffer.push(new_state);
        this.state_buffer = this.state_buffer.filter(s => Date.now() - s.timestamp <= 200);

        this.x = state.tankx;
        this.y = state.tanky;
        this.angle = state.angle;

        if(this.health > state.health){
            this.healthBar.decreaseHealth();
        }
        this.health = state.health;
    }
    
    #lerpAngle(start, end, t) {
        // Normalizar la diferencia al rango [-π, π]
        const twoPi = 2 * Math.PI;
        let diff = (end - start) % twoPi; // Diferencia módulo 2π
        if (diff > Math.PI) diff -= twoPi; // Si es mayor a π, ajusta al camino corto negativo
        if (diff < -Math.PI) diff += twoPi; // Si es menor a -π, ajusta al camino corto positivo
        return start + diff * t; // Interpolar con la diferencia ajustada
    }

    local_update(){
        let lerp_factor = 0.1;
        this.container.position.x += (this.x - this.container.position.x) * lerp_factor;
        this.container.position.y += (this.y - this.container.position.y) * lerp_factor;
        this.container.rotation = this.#lerpAngle(this.container.rotation, this.angle, lerp_factor);
    }
    
    interpolate_from_buffer() {
        if (this.state_buffer.length < 2) return;

        const render_time = Date.now() - 50;
        if (this.state_buffer[0].timestamp > render_time){
            return;
        }
        
        this.x = this.state_buffer[0].x;
        this.y = this.state_buffer[0].y;
        this.angle = this.state_buffer[0].angle;
        this.local_update();
        this.state_buffer.splice(0, 1);
    }

    update() {
        if (this.is_local) {
            this.local_update();
        }else{
            this.interpolate_from_buffer();
        }
    }

    destroy() {
        this.container.destroy({children: true});
    }
}

export {Tank};