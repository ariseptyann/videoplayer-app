<template>
    <div class="video-container" ref="containerRef">
        <div v-if="isLoading" class="loading-spinner">
            <div class="spinner"></div>
        </div>

        <video
            v-show="!isLoading"
            ref="videoPlayer"
            class="video-player"
            @loadeddata="onVideoLoaded"
            @ended="onVideoEnd"
            @error="onVideoError"
            :controls="false"
        >
            <source :src="videoUrl" type="video/mp4">
        </video>
    </div>
</template>

<script>
export default {
    name: 'VideoPlayer',
    data() {
        return {
            videoUrl: '',
            isLoading: true,
            error: null
        }
    },
    async mounted() {
        try {
            const response = await fetch('http://localhost:8000/api/video-info')
            const data = await response.json()
            this.videoUrl = `http://localhost:8000${data.url}`
            
            // Request fullscreen saat komponen dimount
            document.documentElement.requestFullscreen()
                .then(() => {
                    // Setelah fullscreen, coba autoplay
                    this.attemptAutoplay()
                })
                .catch(err => {
                    console.warn('Fullscreen request failed:', err)
                    // Tetap coba autoplay meskipun fullscreen gagal
                    this.attemptAutoplay()
                })
        } catch (err) {
            this.error = 'Gagal memuat video'
            this.isLoading = false
        }
    },
    beforeUnmount() {
        // Keluar dari mode fullscreen saat komponen akan unmount
        if (document.fullscreenElement) {
            document.exitFullscreen()
        }
    },
    methods: {
        async attemptAutoplay() {
            try {
                const video = this.$refs.videoPlayer
                if (video) {
                    video.muted = false // Mute untuk memastikan autoplay berhasil
                    await video.play()
                }
            } catch (err) {
                console.warn('Autoplay failed:', err)
            }
        },
        
        onVideoLoaded() {
            this.isLoading = false
        },
        
        onVideoError(e) {
            console.error('Video error:', e)
            this.error = 'Terjadi kesalahan saat memutar video'
            this.isLoading = false
        },
        
        onVideoEnd() {
            // Exit fullscreen terlebih dahulu
            if (document.fullscreenElement) {
                // document.exitFullscreen()
                // .finally(() => {
                //     // Navigasi ke halaman QR
                //     this.$router.push('/qr')
                // })
                this.$router.push('/qr')
            } else {
                this.$router.push('/qr')
            }
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

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>