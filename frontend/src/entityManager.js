import { BulletRepository } from './bulletRepository.js'
import { TankRepository } from './tankRepository.js'
import { BuffRepository } from './buffRepository.js'

class EntityManager {
    constructor(app, settings, player_id) {
        this.repos = new Map();
        this.repos.set('tank', new TankRepository(app, settings, player_id));
        this.repos.set('bullet', new BulletRepository(app, settings, player_id));
        this.repos.set('buff', new BuffRepository(app));
    }

    add(type, id, data) {
        this.repos.get(type)?.create(id, data);
    }

    remove(type, id) {
        this.repos.get(type)?.remove(id);
    }

    setStates(states) {
        this.repos.forEach((repo, type) => {
            const plural_type = type + 's';
            if (states[plural_type]){
                repo.setStates(states[plural_type])
            }
        });
    }

    updateEntities() {
        this.repos.forEach((repo, type) => {
            repo.updateAll();
        });
    }

    get(type, id) {
        return this.repos.get(type).get(id);
    }
}

export { EntityManager };
