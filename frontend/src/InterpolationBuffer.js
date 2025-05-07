/** 
 * This code was taken and slightly modified from the following repository:
 * https://github.com/hathora/interpolation-buffer
 * The comments were added by me, to help understand the code and how it works.
 */

import createMedianFilter from "moving-median";

export class InterpolationBuffer {
    constructor(restingState, updateRate, interpolate){
        this.restingState = restingState;   // Initial state, used if there's nothing in the buffer
        this.updateRate = updateRate;       // Rate in ms of how often the server sends updates (also known as tickRate)
        this.interpolate = interpolate;     // Interpolation function to use

        this.clientStartTime = undefined;            // Time when the client received the first state from server
        this.offsetMedian = createMedianFilter(100); // Smoothens the difference between server and client time
        this.buffer = [];                            // Buffer of states
    }

    enqueue(state){
        // updatedAt is an artificial timestamp that tells us when the state was created, we shift it
        // by the offset between the server and client time, so that we can generate a delay and interpolate
        // smoothly between states. We could also just use the original server timestamp and substract from
        // 'now'. Maybe that would be even better, as it would be more intuitive.
        const now = Date.now();
        const updatedAt = state.timestamp;

        if (this.buffer.length === 0 && this.clientStartTime === undefined){
            this.clientStartTime = now;
        }

        const offset = this.offsetMedian(now - updatedAt);
        const roundedOffset = Math.ceil(offset / (this.updateRate / 2)) * (this.updateRate / 2);

        this.buffer.push({
            state,
            updatedAt: updatedAt + roundedOffset + this.updateRate,
        });
    }

    getInterpolatedState(now){
        if (this.buffer.length === 0){
            this.clientStartTime = undefined;
            return this.restingState;
        }

        const last = this.buffer[this.buffer.length - 1];
        if (last.updatedAt <= now){
            // if 'now' is grater than the last updatedAt, it means we are "ahead" of time (remember updatedAt is shifted)
            // so we would generate more delay by interpolating between the states that are left in the buffer. So we just
            // jump to the last state and reset the buffer.
            this.restingState = last.state;
            this.clientStartTime = last.updatedAt;
            this.buffer = [];
            return  this.restingState;
        }

        for (let i = this.buffer.length - 1; i>=0; i--){
            // Basically we are looking for the last state that is older than 'now'.
            // Due to the last 'if' we know that the last state is 'forward in time' than 'now',
            // so we look for the last state that is 'behind in time' from 'now', and discard everything 'older'.
            // This allows us to maintain our artificial delay consistent.

            if(this.buffer[i].updatedAt <= now){
                this.clientStartTime = undefined;
                this.buffer.splice(0, i); // <- Perú es clave
                return this.interp(this.buffer[0], this.buffer[1], now);
            }
        }

        // If we get here, it means that there's no states that are 'behind' now, so everything is 'ahead' in time.
        // So we just interpolate between the first state and the resting state.
        // This can happen when the app just started, or after emptying the buffer, or if i'm using a smaller delay
        // than i should, or if there's a lot of lag and the updatedAt gets placed in the future due to the calculation
        // of the offset.
        return this.interp(
            {state: this.restingState, updatedAt: this.clientStartTime ?? now},
             this.buffer[0],
             now,
            );

    }

    interp(from, to, now){
        // dt calculates the percentage of time elapsed between 'from' and 'to' with respect to now.
        // Basically telling us at which point in time we are (now) between the 'creation' of the two states,
        // remember that updatedAt is shifted, so 'now' is simulated to be "behind" in time.
        // This allow us to know how much closer to one of the states we should be, so we can interpolate accordingly.

        // Keep in mind that if dt is < 0, then 'now' is behind 'from', so we should interpolate from restingstate.
        // If dt is > 1, then 'now' is ahead of 'to', so we should snap to 'to' and reset the buffer.
        // And if dt is between 0 and 1, then we should interpolate between 'from' and 'to'.
        // All of this is taken cared of in the getInterpolatedState method. 
        
        const dt = (now - from.updatedAt) / (to.updatedAt - from.updatedAt);
        return this.interpolate(from.state, to.state, dt);
    }



}