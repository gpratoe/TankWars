import { BaseRepository } from './baseRepository.js'
import { Bullet } from './bullet.js'

class BulletRepository extends BaseRepository {
    constructor(app, settings, player_id) {
        super();
        this.app = app;
        this.settings = settings;
        this.player_id = player_id;
    }

    create(id, bulletData) {
        const is_local = this.player_id == bulletData.owner_id;
        const bullet = new Bullet(
            id,
            bulletData.x,
            bulletData.y,
            bulletData.direction,
            bulletData.damage,
            bulletData.speed,
            this.app,
            is_local,
            this.settings.update_rate
        );
        this.entities.set(id, bullet);
    }

    setStates(bulletsState){
        for (const id in bulletsState) {
            const state = bulletsState[id];
            if (state.is_dead) {
                this.remove(id);
            }
            else if (this.entities.has(id)) {
                this.entities.get(id).set_state(state);
            }
            else {
                this.create(id, state);
            }
        }
    }

    updateAll() {
        this.entities.forEach((bullet, id) => {
            bullet.update();
        })
    }
}

export { BulletRepository };
