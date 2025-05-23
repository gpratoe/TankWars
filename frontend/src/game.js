import {Application, Assets, Text} from "pixi.js";
import { Tank } from "./tank";
import { Bullets } from "./bullets";
import { GameMap} from "./gameMap";

class Game {
    constructor(settings, game_id, player_id, sendMessage) {
        this.initialized = false;
        this.game_id = game_id;
        this.player_id = player_id;
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

        this.settings = settings;
        this.tank_height = settings.tank.height;
        this.tank_width = settings.tank.width;
        this.damage = settings.tank.damage;
        this.bullet_speed = settings.tank.bullet_speed;
        this.last_mousePos = null;
    }

    #handleEvent(event, payload) {
        if (event === 'init_game'){
            if (this.initialized){
                return;
            }
            const tanks = payload.tanks;
            for (const player_id in tanks) {
                const name = tanks[player_id].name;
                const color = tanks[player_id].color;
                const x = tanks[player_id].x;
                const y = tanks[player_id].y;
                const angle = tanks[player_id].angle;
                const health = tanks[player_id].health;


                this.tanks[player_id] = new Tank(player_id, name, color, x, y,
                                                 this.tank_width, this.tank_height,
                                                 angle, this.app, (player_id == this.player_id),
                                                 this.settings.update_rate);
                this.update();
            }
            this.initialized = true;
        }
        else if (event === 'state') {
            if (this.initialized){
                const tanks = payload.tanks;
                const bullets = payload.bullets;

                
                for (const player_id in tanks) {
                    if (this.tanks[player_id]) {
                        if (tanks[player_id].is_dead) {
                            this.tanks[player_id].destroy();
                            delete this.tanks[player_id];
                        } 
                        else {
                            this.tanks[player_id].set_state(tanks[player_id]);
                        }
                    }
                }
                
                for (const bullet_id in bullets) {
                    const bullet_state = bullets[bullet_id];

                    if (this.bullets[bullet_id]) {

                        if (bullets[bullet_id].is_dead) {
                            this.bullets[bullet_id].destroy();
                            delete this.bullets[bullet_id];
                        } 
                        else {
                            this.bullets[bullet_id].set_state(bullet_state);
                        }

                    } else {
                        this.bullets[bullet_id] = new Bullets(
                                                            bullet_id,
                                                            bullet_state.x,
                                                            bullet_state.y,
                                                            bullet_state.direction,
                                                            bullet_state.damage,
                                                            bullet_state.speed,
                                                            this.app,
                                                            bullet_state.owner_id == this.player_id,
                                                            this.settings.update_rate);
                    }
                }
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
    }

    send_state(){
        this.sendMessage(
            {'event': 'input',
            'payload': {
                name: this.name,
                mouseX: this.tanks[this.player_id].mouseX,
                mouseY: this.tanks[this.player_id].mouseY,
                shooting: this.tanks[this.player_id].isShooting
                }
            });
    }
    update() {
        this.app.stage.on("pointermove", (event) => {
            const mousePos = event.global;
            const rect = this.app.stage.getBounds();
            const inside_canvas = mousePos.x >= rect.x && mousePos.y >= rect.y;
            if (!inside_canvas) return;

            if (this.tanks[this.player_id] && this.last_mousePos != mousePos) {
                this.tanks[this.player_id].mouseX = mousePos.x;
                this.tanks[this.player_id].mouseY = mousePos.y;
                this.send_state()
                this.last_mousePos = mousePos.clone();
            }
        });
        this.app.stage.on("mousedown", (event) => {
            if(this.tanks[this.player_id] && !this.tanks[this.player_id].isShooting){
                this.tanks[this.player_id].isShooting = true
                this.send_state()
            }
        })
        this.app.stage.on("mouseup", (event) => {
            if(this.tanks[this.player_id] && this.tanks[this.player_id].isShooting){
                this.tanks[this.player_id].isShooting = false
                this.send_state()
            }
        })

        this.app.ticker.add(() => {
            for (const key in this.tanks) {
                this.tanks[key].update();
            }
            for (const key in this.bullets) {
                this.bullets[key].update();
            }
        })
    }
}

export {Game}; 
