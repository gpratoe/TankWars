import {Application} from "pixi.js";
import { Tank } from "./tank";
import { WebSocketManager } from "./websocketmanager";

class Game {
    constructor(width, height) {
        this.initialized = false;
        this.tank_initialized = false;
        this.width = width;
        this.height = height;
        this.app = null;
        this.canvas = null;
        this.tanks = [];
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
            if (name !== this.name) {
                let found = false;
                for (let i = 0; i < this.tanks.length; i++) {
                    if (this.tanks[i].name === name) {
                        this.tanks[i].container.x = data.tankx;
                        this.tanks[i].container.y = data.tanky;
                        this.tanks[i].container.rotation = data.angle;
                        found = true;
                    }
                }
                if (!found) {
                    this.tanks.push(
                        new Tank(name, 0xff0000, data.tankx, data.tanky, 100, 50, data.angle, 10, 17)
                    );
                }
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

        this.tanks.push(new Tank(this.name, 0x00ff00, x, y, tank1w, tank1h, 0, 10, 17));
        this.wsManager.send("state", {
            name: this.name,
            mouseX: x,
            mouseY: y,
            shooting: false,
        });
    }

    update() {
        if (!this.tank_initialized){
            this.#initTank(this.tankinitposx,this.tankinitposy);
        }
        
        this.app.stage.on("pointermove", (event) => {
            const mousePos = event.global;
    
            this.mouseX = mousePos.x;
            this.mouseY = mousePos.y;
        });
        this.isMouseDown = false
        this.app.stage.on("mousedown", (event) => {
            this.isMouseDown = true
        })
        this.app.stage.on("mouseup", (event) => {
            this.isMouseDown = false

        })
        this.app.ticker.add(() => {
            if (this.tanks.length > 0){
                this.tanks[0].update();
            }
    
        })
        .maxFPS(60);
    }
}

const game = new Game(1900,1080);
export {game}; 