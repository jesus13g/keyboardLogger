const socket = io();

socket.on('update', (data) => {
    // Mostrar métricas
    document.getElementById("metrics").innerHTML = `
        <p><strong>Palabras:</strong> ${data.words}</p>
        <p><strong>WPM total:</strong> ${data.wpm}</p>
        <p><strong>WPM (10s):</strong> ${data.wpm_10s}</p>
        <p><strong>WPM (30s):</strong> ${data.wpm_30s}</p>
        <p><strong>WPM (1min):</strong> ${data.wpm_60s}</p>
        <p><strong>Pausas:</strong> ${data.pauses}</p>
        <p><strong>Clic izquierdo:</strong> ${data.clicks_left}</p>
        <p><strong>Clic derecho:</strong> ${data.clicks_right}</p>
    `;

    // Resaltar tecla pulsada (usando "pressed" en lugar de "key")
    document.querySelectorAll(".key").forEach(k => k.classList.remove("active"));
    if (data.pressed) {
        const keyEl = document.querySelector(`.key[data-key="${data.pressed}"]`);
        if (keyEl) {
            keyEl.classList.add("active");
            setTimeout(() => {
                keyEl.classList.remove("active");
            }, 200);
        }
    }

    // Clic izquierdo
    if (!window.prevLeftClicks) window.prevLeftClicks = 0;
    if (data.clicks_left > window.prevLeftClicks) {
        const el = document.getElementById("left-click");
        el.classList.add("active");
        setTimeout(() => el.classList.remove("active"), 150);
    }
    window.prevLeftClicks = data.clicks_left;

    // Clic derecho
    if (!window.prevRightClicks) window.prevRightClicks = 0;
    if (data.clicks_right > window.prevRightClicks) {
        const el = document.getElementById("right-click");
        el.classList.add("active");
        setTimeout(() => el.classList.remove("active"), 150);
    }
    window.prevRightClicks = data.clicks_right;
});
