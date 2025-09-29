<template>
    <div class="home-container">
        <div class="content-wrapper">
            <!-- Awan Background dengan wrapper -->
            <div class="cloud-wrapper">
                <img 
                    src="@/assets/images/home/awan.png" 
                    alt="Cloud" 
                    class="cloud-image"
                />
            </div>

            <!-- Logo HDV -->
            <img 
                src="@/assets/images/home/logo.png" 
                alt="HDV Logo" 
                class="logo"
            />

            <!-- Text Action -->
            <img 
                src="@/assets/images/home/your-action.png" 
                alt="Your Action" 
                class="action-image"
            />

            <!-- Get Started Button -->
            <button 
                class="get-started-btn"
                @click="startVideo"
            >
                GET STARTED
            </button>

            <!-- Background Illustration -->
            <img 
                src="@/assets/images/home/illustrasi-full.png" 
                alt="Background" 
                class="background-illustration"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: 'HomePage',
    methods: {
        startVideo() {
            this.$router.push('/video')
        }
    }
}
</script>

<style scoped>
.home-container {
    background-color: #ebe2d1;
    min-height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    overflow: hidden;
}

.content-wrapper {
    aspect-ratio: 9/16;
    height: 100vh;
    max-width: calc(100vh * 9/16);
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    overflow: hidden;
}

.cloud-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    aspect-ratio: 392.63/395;
    /* Tambahkan overflow hidden agar bagian bawah tidak terlihat */
    overflow: hidden;
}

.cloud-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    /* Geser ke atas setengah dari tinggi container */
    margin-top: -39%;
    display: block;
}

.logo {
    width: auto;
    height: 12%;
    margin-top: 0%;
    object-fit: contain;
    z-index: 2;
}

.action-image {
    width: 80%;
    height: auto;
    margin-top: -13%;
    margin-bottom: 5%;
    object-fit: contain;
    z-index: 2;
}

.background-illustration {
    position: absolute;
    bottom: -35%;
    left: 51%;
    transform: translateX(-50%);
    width: 167%;
    z-index: 1;
    /* margin-top: -48px; */
}

.get-started-btn {
    background: #004B3F;
    color: #dddc23;
    border: none;
    border-radius: 30px;
    padding: 1.2rem 4rem;
    font-size: 1.8vw;
    font-weight: 900;
    cursor: pointer;
    transition: transform 0.2s ease;
    margin-top: -100px;
    z-index: 2;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.get-started-btn:hover {
    transform: scale(1.05);
}

/* Media Query untuk tampilan landscape (laptop) */
@media (orientation: landscape) {
    .content-wrapper {
        height: 100vh;
        max-width: calc(100vh * 9/16);
        margin: 0 auto;
    }

    .action-image {
        width: 70%;
    }

    .get-started-btn {
        font-size: 1.5vw;
    }
}

/* Media Query untuk tampilan portrait (mobile/tablet) */
@media (orientation: portrait) {
    .content-wrapper {
        width: 100vw;
        height: 100vh;
    }

    .action-image {
        width: 90%;
    }

    .get-started-btn {
        font-size: 3.5vw;
    }
}

/* Untuk digital signage dengan resolusi tepat 1080x1920 */
@media (width: 1080px) and (height: 1920px) {
    .content-wrapper {
        width: 1080px;
        height: 1920px;
    }

    .cloud-wrapper {
        width: 1080px;
        height: 1920px; /* Sesuaikan nilai ini sesuai kebutuhan */
    }

    .cloud-image {
        width: 1080px;
        /* Sesuaikan nilai margin-top jika perlu untuk resolusi spesifik */
        margin-top: -73%; /* Setengah dari tinggi asli gambar awan */
    }

    .logo {
        /* width: auto; */
        height: 10%;
        margin-top: 5%;
        /* object-fit: contain;
        z-index: 2; */
    }

    .action-image {
        width: 60%;
        margin-top: -5%;
        /* margin-top: -13%; */
        /* margin-bottom: 5%; */
    }

    .get-started-btn {
        font-size: 36px;
        padding: 1.5rem 5rem;
        margin-top: -10%;
    }
}
</style>