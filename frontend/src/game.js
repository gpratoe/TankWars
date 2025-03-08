import {Application, Assets} from "pixi.js";
import { Tank } from "./tank";
import { Bullets } from "./bullets";

class Game {
    constructor(settings, game_id, player_id, sendMessage) {
        this.initialized = false;
        this.width = settings.world.width;
        this.height = settings.world.height;
        this.app = null;
        this.canvas = null;
        this.tanks = {};
        this.bullets = {};
        this.main_tank = null;
        this.seconds = new Date().getTime() / 1000;
        this.name = "Player " + this.seconds;

        this.container = document.getElementById('game-container');

        this.sendMessage = sendMessage;


        this.tank_height = settings.tank.height;
        this.tank_width = settings.tank.width;
        this.damage = settings.tank.damage;
        this.bullet_speed = settings.tank.bullet_speed;
    }

    #handleEvent(event, payload) {
        if (event === 'init_game'){
            const tanks = payload.tanks;
            for (const player_id in tanks) {
                console.log(player_id);
                const name = tanks[player_id].name;
                const color = tanks[player_id].color;
                const x = tanks[player_id].tankx;
                const y = tanks[player_id].tanky;
                // const mouseX = tanks[player_id].mouseX; // Might not need this at first
                // const mouseY = tanks[player_id].mouseY; // Might not need this at first
                const angle = tanks[player_id].angle;
                const health = tanks[player_id].health;


                this.tanks[player_id] = new Tank(player_id, name, color, x, y,
                                                 this.tank_width, this.tank_height,
                                                  angle, this.damage, this.bullet_speed, this.app);
                /**
                 * Todo: Crear un nuevo tanque con los datos recibidos
                 * luego de crear la entityManager class
                 */
            }
            console.log(this.tanks);
        }
    }

    handleWebSocketMessage(data) {
        const event = data?.event;
        const payload = data?.payload;
        console.log(event, payload);
        if (event && payload) {
            this.#handleEvent(event, payload);
        }

        // const name = data.name;
        // if (event === "init_tank") {
        //     this.tankinitposx = data.tankx;
        //     this.tankinitposy = data.tanky;
        //     if (this.initialized) {
        //         this.#initTank(data.tankx, data.tanky);
        //         this.tank_initialized = true;
        //     }
        // } else if (event === "state") {
        //     const tanks = data.tanks;
        //     const bullets = data.bullets;
        //     const tanks_to_remove = data.tanks_to_remove;

        //     for (const tank_name of tanks_to_remove ){
        //         if(this.tanks[tank_name]){
        //             this.tanks[tank_name].container.destroy();
        //             this.bullets[tank_name].forEach(bullet => {
        //                 bullet.bullet.destroy();
        //             });
        //             delete this.tanks[tank_name];
        //         }
        //     }
        //     for (const key in tanks) {
        //         if (this.tanks[key]) {
        //             this.tanks[key].set_state(tanks[key]);
                    
        //             if (this.bullets[key].length > bullets[key].length) {
        //                 for (let i = bullets[key].length; i < this.bullets[key].length; i++) {
        //                     this.bullets[key][i].bullet.destroy();
                            
        //                 } 
        //                 this.bullets[key].splice(bullets[key].length, this.bullets[key].length - bullets[key].length);

        //             }
        //             for (let i = 0; i < bullets[key].length; i++) {
        //                 if(!this.bullets[key][i]){
        //                     this.bullets[key][i] = new Bullets(bullets[key][i].x, bullets[key][i].y, bullets[key][i].direction, 10, 10);
        //                 }
        //                 else {
        //                     this.bullets[key][i].bullet.x = bullets[key][i].x;
        //                     this.bullets[key][i].bullet.y = bullets[key][i].y;
        //                     this.bullets[key][i].dir_norm = bullets[key][i].direction;
        //                 }
        //             }
                    
        //         } else if (key !== this.name) {
        //             this.tanks[key] = new Tank(key, 0xFF0000, tanks[key].tankx, tanks[key].tanky, 100, 100, 0, 10, 17, 2);
        //             this.bullets[key] = [];
        //         }
        //     }
        // } else if (event === "remove_tank") {
        //     console.log("trying to remove tank: ", name);
        //     if (this.tanks[data]) {
        //         this.tanks[data].container.destroy();
        //         this.bullets[data].forEach(bullet => {
        //             bullet.bullet.destroy();
        //         });
        //         delete this.tanks[data];
        //     }
        // }
    }

    async init() {
        await Assets.load(["/assets/tank_sprite_green.png",
                        "/assets/tank_sprite_yellow.png",
                        "/assets/tank_sprite_blue.png",
                        "/assets/tank_sprite_orange.png"]);
        this.app = new Application();
        await this.app.init({
            width: this.width,
            height: this.height,
            backgroundColor: 0x1099bb,
            resolution: 1
        });
        this.canvas = this.app.canvas;
        this.app.stage.hitArea = this.app.screen
        this.app.stage.interactive = true;
        this.container.appendChild(this.canvas)
        //this.#initTank(0,0);
        this.initialized = true;
        
    }

    send_state(){
        this.sendMessage(
            {'event': 'input',
            'payload': {
                name: this.name,
                mouseX: this.main_tank.mouseX,
                mouseY: this.main_tank.mouseY,
                shooting: this.main_tank.isShooting
                }
            });
    }
    update() {
        this.app.stage.on("pointermove", (event) => {
            const mousePos = event.global;
    
            this.main_tank.mouseX = mousePos.x;
            this.main_tank.mouseY = mousePos.y;
            this.send_state()
        });
        this.app.stage.on("mousedown", (event) => {
            this.main_tank.isShooting = true
            this.send_state()
        })
        this.app.stage.on("mouseup", (event) => {
            this.main_tank.isShooting = false
            this.send_state()

        })
        this.app.ticker.add(() => {
            for (const key in this.tanks) {
                this.tanks[key].update();
            }
        })
    }
}

export {Game}; 