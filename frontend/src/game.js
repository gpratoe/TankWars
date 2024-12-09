import {Application} from "pixi.js";
import { Tank } from "./tank";

class Game {
    #mouseX;
    #mouseY;

    constructor(width, height){
        this.width = width;
        this.height = height;
        this.app = null;
        this.canvas = null;
        this.tanks = []
        this.ws = new WebSocket("ws://localhost:8000/game/testws");
        this.seconds = new Date().getTime() / 1000;
        this.name = "Player " + this.seconds;
    }

    async init() {
        this.app = new Application();
        console.log(this.app);
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
        this.#initTanks();
    }

    #initTanks(){
        const tank1w = 100;
        const tank1h = 50;
        const tank2w = 100;
        const tank2h = 50;

        this.tanks.push(new Tank(this.name, 0x00FF00, -this.width/2 + tank1w/2, 0, tank1w, tank1h, 0, 10, 17));
        //this.tanks.push(new Tank("Player 2", 0xFF0000, this.width/2 - tank2w/2, 0, tank2w, tank2h, 0, 10, 17));
    }

    update() {
        this.ws.onmessage = (event) => {
            var name = JSON.parse(event.data)["name"];
            if (name != this.name){
                var found = false;
                for (let i = 0; i < this.tanks.length; i++){
                    if (this.tanks[i].name == name){
                        this.tanks[i].container.x = JSON.parse(event.data)["x"];
                        this.tanks[i].container.y = JSON.parse(event.data)["y"];
                        this.tanks[i].container.rotation = JSON.parse(event.data)["angle"];
                        //this.tanks[i].health = JSON.parse(event.data)["health"];
                        //this.tanks[i].healthBar.update(this.tanks[i].health);
                        found = true;
                    }
                }
                if (!found){
                    this.tanks.push(new Tank(name, 0xFF0000, JSON.parse(event.data)["x"], JSON.parse(event.data)["y"], 100, 50, JSON.parse(event.data)["angle"], 10, 17));
                }
            }
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

            this.tanks[0].update();
    
        })
        .maxFPS(60);
    }
}

const game = new Game(1900,1080);
export {game}; 