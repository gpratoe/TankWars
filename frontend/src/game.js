import {Application, Assets, Text} from "pixi.js";
import { Tank } from "./tank";
import { Bullet } from "./bullet";
import { GameMap} from "./gameMap";
import { EntityManager } from "./entityManager.js"

class Game {
    constructor(settings, game_id, player_id, sendMessage, onGameOver) {
        this.initialized = false;
        this.game_id = game_id;
        this.player_id = player_id;
        this.width = settings.world.width;
        this.height = settings.world.height;
        this.app = null;
        this.canvas = null;
        this.container = document.getElementById('game-container');
        this.sendMessage = sendMessage;
        this.settings = settings;
        this.last_mousePos = null;
        this.onGameOver = onGameOver;
    }

    #handleEvent(event, payload) {
        if (event === 'init_game'){
            if (this.initialized){
                return;
            }
            const tanks = payload.tanks;
            for (const id in tanks) {
                this.entityManager.add('tank', id, tanks[id]);
            }
            this.update()
           this.initialized = true;
        }
        else if (event === 'state') {
            if(payload['game_over']) {
                this.onGameOver(payload['winner'])
            }
            if (this.initialized){
               this.entityManager.setStates(payload);
            }
        } else if (event === 'countdown') {
            const countdown_ms = payload.countdown_ms;
            const timestamp = payload.timestamp;
            const now = Date.now();
            const time_left = countdown_ms - (now - timestamp);
            if (time_left > 0) {
                const seconds_left = Math.floor(time_left / 1000);
                this.showCountdown(this.app, seconds_left, () => {
                    this.sendMessage({event: 'countdown_complete', payload: {}});
                });
            }
        }
    }

    showCountdown(app, secondsLeft = 3, onComplete) {
        const countdownText = new Text('', {
          fontFamily: 'Arial',
          fontSize: 120,
          fill: 0xffffff,
          align: 'center',
        });
      
        countdownText.anchor.set(0.5);
        countdownText.x = app.renderer.width / 2;
        countdownText.y = app.renderer.height / 2;
      
        app.stage.addChild(countdownText);
      
        let current = secondsLeft;
      
        const interval = setInterval(() => {
          if (current > 0) {
            countdownText.text = current.toString();
            current--;
          } else {
            countdownText.text = 'GO!';
            setTimeout(() => {
              app.stage.removeChild(countdownText);
              if (onComplete) onComplete();
            }, 800);
            clearInterval(interval);
          }
        }, 1000);
      }

    handleWebSocketMessage(data) {
        const event = data?.event;
        const payload = data?.payload;
        if (event && payload) {
            this.#handleEvent(event, payload);
        }
    }

    async init() {
        await Assets.load([`${import.meta.env.VITE_BASE_URL}tank_sprite_blue.png`,
                           `${import.meta.env.VITE_BASE_URL}tank_sprite_green.png`,
                           `${import.meta.env.VITE_BASE_URL}tank_sprite_orange.png`,
                           `${import.meta.env.VITE_BASE_URL}tank_sprite_yellow.png`,
                           `${import.meta.env.VITE_BASE_URL}boundries_tile.png`,
                        ]);
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
        this.gameMap = new GameMap(this.app, this.settings.map);
        this.entityManager = new EntityManager(this.app, this.settings, this.player_id);
    }

    send_state(){
        const tank = this.entityManager.get('tank', this.player_id);
        this.sendMessage(
            {'event': 'input',
            'payload': {
                mouseX: tank.mouseX,
                mouseY: tank.mouseY,
                shooting: tank.isShooting
                }
            });
    }
    update() {
        this.app.stage.on("pointermove", (event) => {
            const mousePos = event.global;
            const rect = this.app.stage.getBounds();
            const inside_canvas = mousePos.x >= rect.x && mousePos.y >= rect.y;
            if (!inside_canvas) return;
            const tank = this.entityManager.get('tank', this.player_id);

            if (tank && this.last_mousePos != mousePos) {
                tank.mouseX = mousePos.x;
                tank.mouseY = mousePos.y;
                this.send_state()
                this.last_mousePos = mousePos.clone();
            }
        });
        this.app.stage.on("mousedown", (event) => {
            const tank = this.entityManager.get('tank', this.player_id);
            if(tank && !tank.isShooting){
                tank.isShooting = true
                this.send_state()
            }
        })
        this.app.stage.on("mouseup", (event) => {
            const tank = this.entityManager.get('tank', this.player_id);
            if(tank && tank.isShooting){
                tank.isShooting = false
                this.send_state()
            }
        })
        this.app.ticker.add(() => {
            this.entityManager.updateEntities();
        })
    }
}

export {Game}; 
