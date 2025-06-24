import { Container, Assets, AnimatedSprite } from "pixi.js";

class Buff {
    constructor(id, type, x, y, app) {
        this.id = id;
        this.type = type;
        this.x = x;
        this.y = y;
        this.app = app;
        this.animatedSprite = null;
        this.#setup();
    }

    #setup() {
        let textureArray = []
        for (let i = 0; i< 3; i++) {
            const texture = Assets.get(`${import.meta.env.VITE_BASE_URL}/buff/${this.type}Buff${i+1}.png`);
            textureArray.push(texture);
        }
        this.animatedSprite = new AnimatedSprite(textureArray);
        this.animatedSprite.x = this.x;
        this.animatedSprite.y = this.y;
        this.animatedSprite.width = 30;
        this.animatedSprite.height = 30;
        this.animatedSprite.animationSpeed = 0.2;
        this.animatedSprite.play();
        this.app.stage.addChild(this.animatedSprite);
    }

    destroy() {
        this.animatedSprite.destroy({ children: true })
    }
}

export { Buff };
