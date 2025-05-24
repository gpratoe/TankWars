import { BaseRepository } from './baseRepository.js'
import { Tank } from './tank.js'

class TankRepository extends BaseRepository {
    constructor(app, settings, player_id) {
        super();
        this.app = app;
        this.settings = settings;
        this.player_id = player_id;
    }

    create(id, tankData) {
        const isLocal = this.player_id == id;
        const tank = new Tank(
            id,
            tankData.name,
            tankData.color,
            tankData.x,
            tankData.y,
            this.settings.tank.width,
            this.settings.tank.height,
            tankData.angle,
            this.app,
            isLocal,
            this.settings.update_rate
        );
        this.entities.set(id, tank);
    }

    setStates(tanksState) {
        for (const id in tanksState) {
            const state = tanksState[id];
            if (state.is_dead) {
                this.remove(Number(id));
            }
            else if (this.entities.has(Number(id))){
                this.entities.get(Number(id)).set_state(state);
            }
        }
    }

    updateAll() {
        this.entities.forEach((tank, id) => {
            tank.update()
        })
    }
}

export { TankRepository };
