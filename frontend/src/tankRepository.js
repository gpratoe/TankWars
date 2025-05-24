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
        id = Number(id);
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
        for (let id in tanksState) {
            const state = tanksState[id];
            id = Number(id);
            if (state.is_dead) {
                this.remove(id);
            }
            else if (this.entities.has(id)){
                this.entities.get(id).set_state(state);
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
