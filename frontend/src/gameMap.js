import { Assets, TilingSprite } from "pixi.js";


class GameMap {
    constructor(app, settings) {
        this.app = app;
        this.texture = Assets.get('/assets/boundries_tile.png');
        this.settings = settings;
        this.map_settings = settings.map;
        this.set_boundries();
    }

    set_boundries() {
        
        const boundaries_thickness = this.map_settings.boundaries_thickness;
        const bases_tleft_bright_width = this.map_settings.bases_tleft_bright_width;
        const bases_tleft_bright_height = this.map_settings.bases_tleft_bright_height;
        const bases_bleft_tright_width = this.map_settings.bases_bleft_tright_width;
        const bases_bleft_tright_height = this.map_settings.bases_bleft_tright_height;
        const tank_height = this.settings.tank_height;

        const sprite1 = new TilingSprite({
            texture: this.texture,
            width: boundaries_thickness,
            height: this.app.screen.height,
        });
        
        const sprite2 = new TilingSprite({
            texture: this.texture,
            width: boundaries_thickness,
            height: this.app.screen.height,
            position: { x: this.app.screen.width - boundaries_thickness, y: 0 }
        });

        const sprite3 = new TilingSprite({
            texture: this.texture,
            width: this.app.screen.width,
            height: boundaries_thickness,
            position: { x: 0, y: 0 }
        });

        const sprite4 = new TilingSprite({
            texture: this.texture,
            width: this.app.screen.width,
            height: boundaries_thickness,
            position: { x: 0, y: this.app.screen.height - boundaries_thickness }
        });

        let x = this.map_settings.bases_tleft_x;
        let y = this.map_settings.bases_tleft_y;
        const base1 = new TilingSprite({
            texture: this.texture,
            width: bases_tleft_bright_width,
            height: bases_tleft_bright_height,
            position: { x: x - bases_tleft_bright_width/2, y: y - bases_tleft_bright_height/2 } // position is based on the center of the object somehow so i have to substract half the height to compensate
        });

        x = this.map_settings.bases_bright_x;
        y = this.map_settings.bases_bright_y;
        const base2 = new TilingSprite({
            texture: this.texture,
            width: bases_tleft_bright_width,
            height: bases_tleft_bright_height,
            position: { x: x - bases_tleft_bright_width/2, y: y - bases_tleft_bright_height/2 } 
        });

        const boundaries = [sprite1, sprite2, sprite3, sprite4, base1, base2];
        for (const boundary of boundaries) {
            this.app.stage.addChild(boundary);
        }
    }
}

export { GameMap };