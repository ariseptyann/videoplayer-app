const AudioContextCtor = window.AudioContext || window.webkitAudioContext;
let audioContext = null;

export async function ensureAudioUnlocked() {
    if (!AudioContextCtor) {
        return false;
    }

    if (!audioContext) {
        audioContext = new AudioContextCtor();
    }

    if (audioContext.state === "suspended") {
        try {
            await audioContext.resume();
        } catch (err) {
            console.warn("Failed to resume AudioContext", err);
        }
    }

    return audioContext.state === "running";
}

export function markAutoplayIntent(metadata = {}) {
    try {
        const payload = {
            ts: Date.now(),
            ...metadata
        };
        sessionStorage.setItem("video-autoplay-intent", JSON.stringify(payload));
    } catch (err) {
        console.warn("Unable to persist autoplay intent", err);
    }
}

export function consumeAutoplayIntent(maxAgeMs = 60000) {
    try {
        const raw = sessionStorage.getItem("video-autoplay-intent");
        if (!raw) {
            return null;
        }

        sessionStorage.removeItem("video-autoplay-intent");
        const payload = JSON.parse(raw);

        if (!payload?.ts || Date.now() - payload.ts > maxAgeMs) {
            return null;
        }

        return payload;
    } catch (err) {
        console.warn("Unable to read autoplay intent", err);
        return null;
    }
}
