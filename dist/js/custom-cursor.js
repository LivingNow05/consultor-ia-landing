
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on non-touch devices
    if (window.matchMedia("(pointer: coarse)").matches) return;

    const dot = document.createElement('div');
    dot.classList.add('custom-cursor-dot');
    document.body.appendChild(dot);

    const aura = document.createElement('div');
    aura.classList.add('custom-cursor-aura');
    document.body.appendChild(aura);

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let dotX = mouseX;
    let dotY = mouseY;
    let auraX = mouseX;
    let auraY = mouseY;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animate() {
        // Dot follows instantly
        dotX += (mouseX - dotX) * 1;
        dotY += (mouseY - dotY) * 1;
        
        // Aura has a springy delay
        auraX += (mouseX - auraX) * 0.15;
        auraY += (mouseY - auraY) * 0.15;

        dot.style.transform = `translate3d(${dotX}px, ${dotY}px, 0) translate(-50%, -50%)`;
        aura.style.transform = `translate3d(${auraX}px, ${auraY}px, 0) translate(-50%, -50%)`;

        requestAnimationFrame(animate);
    }
    animate();

    // Add hover effects to all interactive elements
    const interactives = document.querySelectorAll('a, button, input, select, textarea, details, summary, .interactive');
    
    interactives.forEach(el => {
        el.addEventListener('mouseenter', () => {
            aura.classList.add('hover');
            dot.classList.add('hover');
        });
        el.addEventListener('mouseleave', () => {
            aura.classList.remove('hover');
            dot.classList.remove('hover');
        });
    });
});
