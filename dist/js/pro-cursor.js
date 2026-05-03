document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on non-touch devices
    if (window.matchMedia("(pointer: coarse)").matches) return;

    const cursor = document.createElement('div');
    cursor.classList.add('pro-cursor');
    document.body.appendChild(cursor);

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let cursorX = mouseX;
    let cursorY = mouseY;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animate() {
        // Smooth lerp follow
        cursorX += (mouseX - cursorX) * 0.2;
        cursorY += (mouseY - cursorY) * 0.2;

        cursor.style.transform = `translate3d(${cursorX}px, ${cursorY}px, 0) translate(-50%, -50%)`;

        requestAnimationFrame(animate);
    }
    animate();

    // Hover state for interactive elements
    const interactives = document.querySelectorAll('a, button, input, select, textarea, details, summary, .interactive');
    
    interactives.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.classList.add('hover');
        });
        el.addEventListener('mouseleave', () => {
            cursor.classList.remove('hover');
        });
    });
});
