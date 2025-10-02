<template>
    <div class="qr-container">
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

        <!-- Scan Here -->
        <img
            src="@/assets/images/qr/scan-here.png"
            alt="Scan Here"
            class="scan-here"
        />

        <!-- Tempat QR -->
        <!-- <img
            src="@/assets/images/qr/tempat-qr.png"
            alt="Tempat QR"
            class="tempat-qr"
        /> -->

        <!-- QR Code Container -->
        <div class="qr-code-wrapper">
            <div v-if="loading" class="loading">
                <p>Loading QR Code...</p>
            </div>
            <div v-else-if="error" class="error">
                <p>{{ error }}</p>
            </div>
            <div v-else class="qr-code-container">
                <canvas id="qr-canvas"></canvas>
                <span class="corner tl"></span>
                <span class="corner tr"></span>
                <span class="corner bl"></span>
                <span class="corner br"></span>
                <!-- <p class="qr-subtitle">{{ qrData.title }}</p> -->
            </div>
        </div>

        <!-- HOME Button (uncomment jika perlu) -->
        <button
            class="home-btn"
            @click="$router.push('/')"
        >
            HOME
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
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import QRCode from 'qrcode'

const AUTO_RETURN_DELAY_MS = 99 * 60 * 1000 // 1 menit || ubah bagian depan untuk menit  atau belakang untuk detik
const QR_CANVAS_ID = 'qr-canvas'
const FALLBACK_QR = {
    url: 'https://ngobrolinhpv.com/',
    title: 'Scan untuk mengunjungi website'
}

export default {
    name: 'QRPage',
    setup() {
        const router = useRouter()
        const qrData = ref({ ...FALLBACK_QR })
        const loading = ref(true)
        const error = ref(null)
        let autoReturnTimer = null

        const clearAutoReturn = () => {
            if (autoReturnTimer) {
                clearTimeout(autoReturnTimer)
                autoReturnTimer = null
            }
        }

        const scheduleAutoReturn = () => {
            clearAutoReturn()
            autoReturnTimer = window.setTimeout(() => {
                router.replace('/')
            }, AUTO_RETURN_DELAY_MS)
        }

        const assignQrData = (payload) => {
            if (!payload?.url || typeof payload.url !== 'string' || !payload.url.trim()) {
                qrData.value = { ...FALLBACK_QR }
                return
            }

            qrData.value = {
                url: payload.url.trim(),
                title: payload.title ?? FALLBACK_QR.title
            }
        }

        const fetchQRData = async () => {
            try {
                const res = await fetch('/api/qr-data', { cache: 'no-store' })
                if (!res.ok) {
                    throw new Error(`Unexpected status ${res.status}`)
                }

                const data = await res.json()
                assignQrData(data)
            } catch (err) {
                console.warn('QR data fetch failed; using fallback payload.', err)
                assignQrData(null)
            }
        }

        const renderQr = async () => {
            const canvas = document.getElementById(QR_CANVAS_ID)
            if (!canvas) {
                return
            }

            const url = qrData.value.url
            if (!url) {
                throw new Error('No QR URL available for rendering')
            }

            const vh = window.innerHeight
            const is1080x1920 = window.innerWidth === 560 && window.innerHeight === 560

            // lebih besar di 1080×1920, tanpa cap 350
            const target = is1080x1920 ? vh * 0.48 : Math.min(vh * 0.35, 350)
            const size = Math.round(target)

            // render tajam di layar high-DPI
            const ratio = window.devicePixelRatio || 1
            canvas.width  = size * ratio
            canvas.height = size * ratio
            canvas.style.width  = size + 'px'
            canvas.style.height = size + 'px'

            await QRCode.toCanvas(canvas, url, {
                width: size * ratio,
                margin: 2,
                color: { dark: '#015f6d', light: '#00000000' },
                errorCorrectionLevel: 'M'
            })
        }

        const regenerateQr = async () => {
            try {
                await renderQr()
                error.value = null
            } catch (err) {
                console.error('Failed to generate QR code', err)
                error.value = 'Gagal membuat QR Code'
            }
        }

        const handleResize = () => {
            if (loading.value || error.value) {
                return
            }

            regenerateQr()
        }

        onMounted(async () => {
            await fetchQRData()
            loading.value = false
            await nextTick()
            await regenerateQr()
            window.addEventListener('resize', handleResize)
            scheduleAutoReturn()
        })

        onUnmounted(() => {
            window.removeEventListener('resize', handleResize)
            clearAutoReturn()
        })

        return {
            qrData,
            loading,
            error
        }
    }
}
</script>

<style scoped>
.qr-container {
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
    overflow: hidden;
    z-index: 0;
}

.cloud-image {
    width: 110%;
    height: 100%;
    object-fit: cover;
    margin-top: -38%;
    display: block;
}

.logo {
    width: auto;
    height: 10%;
    margin-top: 5%;
    object-fit: contain;
    z-index: 2;
}

.scan-here {
    width: 60%;
    height: auto;
    margin-top: -20%;
    object-fit: contain;
    z-index: 2;
}

/* QR Code Styling */
.qr-code-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -23%;
    z-index: 2;
    min-height: 40vh;
}

.qr-code-container {
    /* background: transparent;
    padding: 2rem;
    border-radius: 20px; 
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem; */
    position: relative;          /* penting */
    display: inline-block;       /* ukurannya mengikuti canvas */
    background: transparent;
    padding: 0;                  /* tanpa kotak putih */
    box-shadow: none;
    border: none;
}

#qr-canvas {
    display: block;
    border-radius: 10px;
}

/* ===== Corner style ===== */
.qr-code-container {
    position: relative;
    display: inline-block;
    background: transparent;
    --corner-size: 60px;   /* panjang sisi sudut */
    --thickness: 10px;     /* ketebalan garis */
    --radius: 0;        /* lengkung sudut */
    --color: #0a6a70;      /* warna teal */
    --inset: 0px;          /* kalau mau masuk ke dalam, ubah mis. 8px */
    --elbow-radius: 10px;
}

/* ===== Corner dengan balok, ujung RATA ===== */
.corner {
    position: absolute;
    width: 0; height: 0;
    z-index: 3;                /* di atas canvas */
    pointer-events: none;
}

/* tiap corner punya 2 balok: ::before (horizontal) & ::after (vertikal) */
.corner::before,
.corner::after {
    content: "";
    position: absolute;
    background: var(--color);
}


/* TOP-LEFT */
.corner.tl { top: var(--inset); left: var(--inset); }
.corner.tl::before { /* horizontal ke kanan */
    top: 0; left: 0; height: var(--thickness); width: var(--corner-size);
    border-top-left-radius: var(--elbow-radius);
}
.corner.tl::after {  /* vertikal ke bawah */
    top: 0; left: 0; width: var(--thickness); height: var(--corner-size);
    border-top-left-radius: var(--elbow-radius);
}

/* TOP-RIGHT */
.corner.tr { top: var(--inset); right: var(--inset); }
.corner.tr::before { /* horizontal ke kiri */
    top: 0; right: 0; height: var(--thickness); width: var(--corner-size);
    border-top-right-radius: var(--elbow-radius);
}
.corner.tr::after {  /* vertikal ke bawah */
    top: 0; right: 0; width: var(--thickness); height: var(--corner-size);
    border-top-right-radius: var(--elbow-radius);
}

/* BOTTOM-LEFT */
.corner.bl { bottom: var(--inset); left: var(--inset); }
.corner.bl::before { /* horizontal ke kanan */
    bottom: 0; left: 0; height: var(--thickness); width: var(--corner-size);
    border-bottom-left-radius: var(--elbow-radius);
}
.corner.bl::after {  /* vertikal ke atas */
    bottom: 0; left: 0; width: var(--thickness); height: var(--corner-size);
    border-bottom-left-radius: var(--elbow-radius);
}

/* BOTTOM-RIGHT */
.corner.br { bottom: var(--inset); right: var(--inset); }
.corner.br::before { /* horizontal ke kiri */
    bottom: 0; right: 0; height: var(--thickness); width: var(--corner-size);
    border-bottom-right-radius: var(--elbow-radius);
}
.corner.br::after {  /* vertikal ke atas */
    bottom: 0; right: 0; width: var(--thickness); height: var(--corner-size);
    border-bottom-right-radius: var(--elbow-radius);
}



/* .qr-subtitle {
    color: #004B3F;
    font-size: clamp(12px, 2vw, 18px);
    font-weight: 600;
    text-align: center;
    margin: 0;
    max-width: 300px;
} */

.loading,
.error {
    background: white;
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.loading p,
.error p {
    color: #004B3F;
    font-size: 18px;
    font-weight: 600;
    margin: 0;
}

.error p {
    color: #d32f2f;
}

/* HOME Button */
.home-btn {
    /* gradient */
    background-color: #f5f477;  /* fallback */
    background-image: linear-gradient(180deg, #f5f477 0%, #dddc23 100%);

    /* teks */
    font-family: "Raleway", system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    font-weight: 900;
    font-size: 42px;
    line-height: 1;              /* rapatkan vertikal */
    color: #004B3F;              /* kontras bagus di atas gradient kuning */

    /* tombol */
    border: none;
    border-radius: 25px;
    padding: 14px 42px;          /* lebih dekat ke tepi */
    cursor: pointer;
    transition: transform .2s ease, box-shadow .2s ease;
    margin-top: 22rem;
    z-index: 2;
    box-shadow: 0 6px 18px rgba(0,0,0,.2);
}

.home-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

.home-btn:active {
    transform: scale(0.98);
}

.background-illustration {
    position: absolute;
    bottom: -35%;
    left: 51%;
    transform: translateX(-50%);
    width: 167%;
    z-index: 1;
}

/* Media Query untuk tampilan landscape (laptop) */
@media (orientation: landscape) {
    .content-wrapper {
        height: 100vh;
        max-width: calc(100vh * 9/16);
        margin: 0 auto;
    }
}

/* Media Query untuk tampilan portrait (mobile/tablet) */
@media (orientation: portrait) {
    .content-wrapper {
        width: 100vw;
        height: 100vh;
    }
}

/* Untuk digital signage dengan resolusi tepat 1080x1920 */
@media (width: 1080px) and (height: 1920px) {
    .content-wrapper {
        width: 1080px;
        height: 1920px;
    }

    .cloud-wrapper {
        /* width: 1080px;
        height: 1920px;  */
        width: 125%;
        margin-left: -10%;
    }

    .cloud-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }

    .logo {
        height: 15%;
        margin-left: 5%;
        margin-top: -1%;
    }

    .scan-here {
        width: 80%;
        margin-top: -32%;
    }

    .qr-code-wrapper {
        margin-top: -27%;
        min-height: auto;
    }

    .qr-code-container {
        --corner-size: 90px;
        --thickness: 16px;
        --inset: 20px;
        --elbow-radius: 18px;
    }

    .home-btn {
        font-size: 48px;               /* atau responsif: clamp(28px, 5.2vw, 55px) */
        line-height: 1;
        padding: 20px 46px;
        margin-top: 29rem;
        cursor: pointer;
    }
}
</style>