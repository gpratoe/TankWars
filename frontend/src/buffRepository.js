import { BaseRepository } from './baseRepository.js'
import { Buff } from './buff.js'

class BuffRepository extends BaseRepository {
    constructor(app) {
        super();
        this.app = app;
    }

    create(id, buffData) {
        const buff = new Buff(
            id,
            buffData.x,
            buffData.y,
            this.app,
        );
        this.entities.set(id, buff);
    }

    setStates(buffStates) {
        for (let id in buffStates) {
            const state = buffStates[id];
            id = Number(id);
            console.log(state);
            if (this.entities.has(id)) {
                if (state.taken) {
                    this.remove(id);
                }
            }
            else {
                this.create(id, state);
            }
        }
    }

    updateAll() {
        return
    }
}

export { BuffRepository };
