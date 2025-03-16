import { Assets, TilingSprite } from "pixi.js";


class GameMap {
    constructor(app) {
        this.app = app;
        this.texture = Assets.get('/assets/boundries_tile.png');

        
        this.set_boundries();
    }

    set_boundries() {
        const sprite1 = new TilingSprite({
            texture: this.texture,
            width: 20,
            height: this.app.screen.height,
        });
        
        const sprite2 = new TilingSprite({
            texture: this.texture,
            width: 20,
            height: this.app.screen.height,
            position: { x: this.app.screen.width - 20, y: 0 }
        });

        const sprite3 = new TilingSprite({
            texture: this.texture,
            width: this.app.screen.width,
            height: 20,
            position: { x: 0, y: 0 }
        });

        const sprite4 = new TilingSprite({
            texture: this.texture,
            width: this.app.screen.width,
            height: 20,
            position: { x: 0, y: this.app.screen.height - 20 }
        });

        this.app.stage.addChild(sprite1);
        this.app.stage.addChild(sprite2);
        this.app.stage.addChild(sprite3);
        this.app.stage.addChild(sprite4);
    }
}

export { GameMap };