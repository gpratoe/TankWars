import {Application, Assets} from "pixi.js";
import { Tank } from "./tank";
import { WebSocketManager } from "./websocketmanager";
import { Bullets } from "./bullets";

class Game {
    constructor(width, height) {
        this.initialized = false;
        this.tank_initialized = false;
        this.width = width;
        this.height = height;
        this.app = null;
        this.canvas = null;
        this.tanks = {};
        //this.bullets = new Bullets(10);
        this.bullets = {};
        this.main_tank = null;
        this.seconds = new Date().getTime() / 1000;
        this.name = "Player " + this.seconds;

        this.wsManager = new WebSocketManager(
            "ws://localhost:8000/game/testws",
            this.name,
            this.handleWebSocketMessage.bind(this)
        );
    }

    handleWebSocketMessage(fullData) {
        const event = fullData.event;
        const data = fullData.data;
        const name = data.name;
        if (event === "init_tank") {
            this.tankinitposx = data.tankx;
            this.tankinitposy = data.tanky;
            if (this.initialized) {
                this.#initTank(data.tankx, data.tanky);
                this.tank_initialized = true;
            }
        } else if (event === "state") {
            const tanks = data.tanks;
            const bullets = data.bullets;
            const tanks_to_remove = data.tanks_to_remove;

            for (const tank_name of tanks_to_remove ){
                if(this.tanks[tank_name]){
                    this.tanks[tank_name].container.destroy();
                    this.bullets[tank_name].forEach(bullet => {
                        bullet.bullet.destroy();
                    });
                    delete this.tanks[tank_name];
                }
            }
            for (const key in tanks) {
                if (this.tanks[key]) {
                    this.tanks[key].set_state(tanks[key]);
                    
                    if (this.bullets[key].length > bullets[key].length) {
                        for (let i = bullets[key].length; i < this.bullets[key].length; i++) {
                            this.bullets[key][i].bullet.destroy();
                            
                        } 
                        this.bullets[key].splice(bullets[key].length, this.bullets[key].length - bullets[key].length);

                    }
                    for (let i = 0; i < bullets[key].length; i++) {
                        if(!this.bullets[key][i]){
                            this.bullets[key][i] = new Bullets(bullets[key][i].x, bullets[key][i].y, bullets[key][i].direction, 10, 10);
                        }
                        else {
                            this.bullets[key][i].bullet.x = bullets[key][i].x;
                            this.bullets[key][i].bullet.y = bullets[key][i].y;
                            this.bullets[key][i].dir_norm = bullets[key][i].direction;
                        }
                    }
                    
                } else if (key !== this.name) {
                    this.tanks[key] = new Tank(key, 0xFF0000, tanks[key].tankx, tanks[key].tanky, 100, 100, 0, 10, 17, 2);
                    this.bullets[key] = [];
                }
            }
        } else if (event === "remove_tank") {
            console.log("trying to remove tank: ", name);
            if (this.tanks[data]) {
                this.tanks[data].container.destroy();
                this.bullets[data].forEach(bullet => {
                    bullet.bullet.destroy();
                });
                delete this.tanks[data];
            }
        }
    }

    async init() {
        await Assets.load(["/assets/tank_sprite_1.png",
                        "/assets/tank_sprite_2.png",
                        "/assets/tank_sprite_3.png",
                        "/assets/tank_sprite_4.png"]);
        this.app = new Application();
        await this.app.init({
            width: this.width,
            height: this.height,
            backgroundColor: 0x1099bb,
            resolution: 1
        });
        this.canvas = this.app.canvas;

        this.canvas.style.position = 'absolute';
        this.app.stage.hitArea = this.app.screen
        this.app.stage.interactive = true;
        document.body.appendChild(this.canvas)
        //this.#initTank(0,0);
        this.initialized = true;
        
    }

    #initTank(x, y) {
        const tank1w = 100;
        const tank1h = 100;

        const tank = new Tank(this.name, 0x00ff00, x, y, tank1w, tank1h, 0, 10, 17,1);
        this.tanks[this.name] = tank;
        this.main_tank = tank; 
        this.bullets[this.name] = [];
        this.wsManager.send("state", {
            name: this.name,
            mouseX: this.main_tank.mouseX ? this.main_tank.mouseX : x,
            mouseY: this.main_tank.mouseY ? this.main_tank.mouseY : y,
            shooting: false,
        });
    }
    send_state(){
        game.wsManager.send("state", {
            name: this.name,
            mouseX: this.main_tank.mouseX,
            mouseY: this.main_tank.mouseY,
            shooting: this.main_tank.isShooting
        })
    }
    update() {
        if (!this.tank_initialized){
            this.#initTank(this.tankinitposx,this.tankinitposy);
        }
        
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
        .maxFPS(60);
    }
}

const game = new Game(1900,1080);
export {game}; 