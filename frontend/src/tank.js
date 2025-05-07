import { Container, Assets, Sprite } from "pixi.js";
import { HealthBar } from "./healthbar";
import { InterpolationBuffer } from "./InterpolationBuffer";

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
        const initial_state = {
            x: x,
            y: y,
            angle: angle,

        }
        this.interpolation_buffer = new InterpolationBuffer(initial_state, 50, this.interp_states);
    }

    interp_states(older_state, newer_state, t){
        const x = older_state.x + (newer_state.x - older_state.x) * t;
        const y = older_state.y + (newer_state.y - older_state.y) * t;

        // Para la rotacion:
        // Normalizar la diferencia al rango [-π, π]
        const end = newer_state.angle;
        const start = older_state.angle;
        const twoPi = 2 * Math.PI;
        let diff = (end - start) % twoPi;   // Diferencia módulo 2π
        if (diff > Math.PI) diff -= twoPi;  // Si es mayor a π, ajusta al camino corto negativo
        if (diff < -Math.PI) diff += twoPi; // Si es menor a -π, ajusta al camino corto positivo
        const angle = start + diff * t;     // Interpolar con la diferencia ajustada
        

        return {
            x: x,
            y: y,
            angle: angle
        }
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
        this.interpolation_buffer.enqueue(new_state);

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
        const state = this.interpolation_buffer.getInterpolatedState(Date.now());
        this.container.position.x = state.x;
        this.container.position.y = state.y;
        this.container.rotation = state.angle;

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