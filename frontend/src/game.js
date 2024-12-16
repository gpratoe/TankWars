import {Application} from "pixi.js";
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
        this.tanks[this.name] = null;
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
            console.log("tanks: ", tanks);
            for (const key in tanks) {
                if (this.tanks[key]) {
                    this.tanks[key].container.x = tanks[key].tankx;
                    this.tanks[key].container.y = tanks[key].tanky;
                    this.tanks[key].angle = tanks[key].angle;
                    this.tanks[key].container.rotation = tanks[key].angle;
                    
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
                    this.tanks[key] = new Tank(key, 0xFF0000, tanks[key].tankx, tanks[key].tanky, 100, 50, 0, 10, 17);
                    this.bullets[key] = [];
                }
            }
        } else if (event === "remove_tank") {
            console.log("trying to remove tank: ", name);
            if (this.tanks[data]) {
                this.tanks[data].container.destroy();
                delete this.tanks[data];
            }
        }
    }

    async init() {
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
        const tank1h = 50;

        this.tanks[this.name] = new Tank(this.name, 0x00ff00, x, y, tank1w, tank1h, 0, 10, 17);
        this.bullets[this.name] = [];
        this.wsManager.send("state", {
            name: this.name,
            mouseX: this.tanks[this.name].mouseX ? this.tanks[this.name].mouseX : x,
            mouseY: this.tanks[this.name].mouseY ? this.tanks[this.name].mouseY : y,
            shooting: false,
        });
    }

    update() {
        if (!this.tank_initialized){
            this.#initTank(this.tankinitposx,this.tankinitposy);
        }
        
        this.app.stage.on("pointermove", (event) => {
            const mousePos = event.global;
    
            this.tanks[this.name].mouseX = mousePos.x;
            this.tanks[this.name].mouseY = mousePos.y;
            game.wsManager.send("state", {
                name: this.name,
                mouseX: this.tanks[this.name].mouseX,
                mouseY: this.tanks[this.name].mouseY,
                shooting: this.tanks[this.name].isShooting,
            });
        });
        this.app.stage.on("mousedown", (event) => {
            this.tanks[this.name].isShooting = true
            game.wsManager.send("state", {
                name: this.name,
                mouseX: this.tanks[this.name].mouseX,
                mouseY: this.tanks[this.name].mouseY,
                shooting: true,
            });
        })
        this.app.stage.on("mouseup", (event) => {
            this.tanks[this.name].isShooting = false
            game.wsManager.send("state", {
                name: this.name,
                mouseX: this.tanks[this.name].mouseX,
                mouseY: this.tanks[this.name].mouseY,
                shooting: false, // Enviar el estado actualizado
            });

        })
        this.app.ticker.add(() => {
            
        })
        .maxFPS(20);
    }
}

const game = new Game(1900,1080);
export {game}; 