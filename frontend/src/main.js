import {game} from "../src/game";

(async () => {
    await game.init();
    game.update();
})();