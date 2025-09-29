<template>
    <div class="video-container" ref="containerRef">
        <video
            v-if="videoUrl"
            ref="videoPlayer" :key="videoUrl"
            class="video-player"
            playsinline
            preload="auto"
            autoplay
            @loadeddata="onVideoLoaded"
            @ended="onVideoEnd"
            @error="onVideoError"
            :controls="false"
        >
            <source :src="videoUrl" type="video/mp4" />
        </video>

        <div v-if="isLoading" class="loading-spinner">
            <div class="spinner"></div>
        </div>

        <div v-if="error" class="video-error">
            <p>{{ error }}</p>
        </div>

        <div v-if="!isLoading && !error && playbackWarning" class="playback-warning">
            <p>{{ playbackWarning }}</p>
        </div>
    </div>
</template>

<script>
import { consumeAutoplayIntent } from '@/utils/audioUnlocker'

const API_BASE = (import.meta.env.VITE_API_BASE ?? 'http://localhost:8000').replace(/\/$/, '')

export default {
    name: 'VideoPlayer',
    data() {
        return {
            videoUrl: '',
            isLoading: true,
            error: null,
            playbackWarning: null,
            retryHandle: null,
            playbackRetryCount: 0,
            maxAutoplayRetries: 3,
            autoplayIntent: null
        }
    },
    async mounted() {
        this.autoplayIntent = consumeAutoplayIntent()
        if (this.autoplayIntent?.hasAudioUnlocked) {
            this.maxAutoplayRetries = 5
        }

        try {
            const response = await fetch(`${API_BASE}/api/video-info`, { cache: 'no-store' })
            if (!response.ok) {
                throw new Error(`Unexpected status ${response.status}`)
            }

            const data = await response.json()
            if (!data?.url) {
                throw new Error('Response missing url field')
            }

            const source = typeof data.url === 'string' && data.url.startsWith('http')
                ? data.url
                : `${API_BASE}${data.url}`

            this.videoUrl = source
        } catch (err) {
            console.error('Failed to load video metadata', err)
            this.error = 'Gagal memuat video'
            this.isLoading = false
        }
    },
    beforeUnmount() {
        if (this.retryHandle) {
            clearTimeout(this.retryHandle)
            this.retryHandle = null
        }
    },
    methods: {
        async attemptAutoplay() {
            const video = this.$refs.videoPlayer
            if (!video) {
                return
            }

            try {
                await video.play()
                this.playbackWarning = null
                this.playbackRetryCount = 0
                if (this.retryHandle) {
                    clearTimeout(this.retryHandle)
                    this.retryHandle = null
                }
            } catch (err) {
                console.warn('Autoplay failed:', err)
                if (this.playbackRetryCount < this.maxAutoplayRetries) {
                    this.playbackRetryCount += 1
                    this.retryHandle = setTimeout(() => {
                        this.retryHandle = null
                        this.attemptAutoplay()
                    }, 1000)
                } else {
                    const unlocked = this.autoplayIntent?.hasAudioUnlocked
                    this.playbackWarning = unlocked
                        ? 'Sedang menyiapkan audio, mohon tunggu...'
                        : 'Sentuh layar sekali untuk memulai video'
                }
            }
        },

        onVideoLoaded() {
            this.isLoading = false

            const video = this.$refs.videoPlayer
            if (video) {
                video.muted = false
                if (!video.hasAttribute('playsinline')) {
                    video.setAttribute('playsinline', '')
                }
            }

            this.attemptAutoplay()
        },

        onVideoError(event) {
            console.error('Video error:', event)
            this.error = 'Terjadi kesalahan saat memutar video'
            this.isLoading = false
        },

        onVideoEnd() {
            this.$router.push('/qr')
        }
    }
}
</script>

<style scoped>
    .video-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: black;
        z-index: 9999;
    }

    .video-player {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    .loading-spinner {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .spinner {
        width: 50px;
        height: 50px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    .video-error,
    .playback-warning {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.75);
        color: #f7f7f7;
        padding: 1.2rem 1.8rem;
        border-radius: 12px;
        text-align: center;
        max-width: 80%;
        font-size: 1.1rem;
        line-height: 1.4;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }

    .video-error {
        top: 50%;
        transform: translate(-50%, -50%);
    }

    .playback-warning {
        bottom: 6%;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>

