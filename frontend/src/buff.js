import { Container, Assets, AnimatedSprite } from "pixi.js";

class Buff {
    constructor(id, type, x, y, radius, app) {
        this.id = id;
        this.type = type;
        this.x = x;
        this.y = y;
        this.w = radius * 2
        this.h = radius * 2
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
        this.animatedSprite.position.x = this.x;
        this.animatedSprite.position.y = this.y;
        this.animatedSprite.width = this.w;
        this.animatedSprite.height = this.h;
        this.animatedSprite.anchor.set(0.5);
        this.animatedSprite.animationSpeed = 0.2;
        this.animatedSprite.play();
        this.app.stage.addChild(this.animatedSprite);
    }

    destroy() {
        this.animatedSprite.destroy({ children: true })
    }
}

export { Buff };
