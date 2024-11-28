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

        this.tanks.push(new Tank("Player 1", 0x00FF00, -this.width/2 + tank1w/2, 0, tank1w, tank1h, 0, 10, 10));
        //this.tanks.push(new Tank("Player 2", 0xFF0000, this.width/2 - tank2w/2, 0, tank2w, tank2h, 0, 10, 10));
    }

    update() {
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
            for (let i = 0; i < this.tanks.length; i++){
    
                this.tanks[i].update();
            }
    
        })
        .maxFPS(60);
    }
}

const game = new Game(1900,1080);
export {game}; 