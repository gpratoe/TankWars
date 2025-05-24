class BaseRepository {
    constructor() {
        this.entities = new Map();
    }

    create(id, data) {
        throw new Error("create must be implemented");
    }

    remove(id) {
        const entity = this.entities.get(id);
        if (entity?.destroy) entity.destroy();
        this.entities.delete(id);
    }

    get(id){
        return this.entities.get(id);
    }
}

export { BaseRepository };
