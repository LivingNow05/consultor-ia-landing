with open("templates/automatizacion_whatsapp.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

old_script = """                function updateCalculator() {
                    if(!calcChats || !calcTicket) return;
                    const chats = parseInt(calcChats.value);
                    const ticket = parseInt(calcTicket.value);
                    
                    // Obtener la moneda actual que geo-personalization.js haya establecido (o 'USD' por defecto si aún no corre)
                    let currentCurrency = 'USD';
                    const currEl = document.querySelector('.dyn-currency');
                    if (currEl && currEl.textContent) currentCurrency = currEl.textContent.trim();
                    
                    valChats.textContent = chats;
                    valTicket.innerHTML = `<span class="dyn-currency">${currentCurrency}</span> ` + ticket.toLocaleString();
                    
                    const hoursSaved = Math.round((chats * 30 * 5) / 60);
                    resHours.textContent = hoursSaved.toLocaleString() + 'h';
                    
                    const leadsLostPerMonth = Math.round((chats * 30) * 0.20);
                    resLeads.textContent = "+" + leadsLostPerMonth.toLocaleString();
                    
                    const extraRevenue = Math.round(leadsLostPerMonth * 0.15 * ticket);
                    resRevenue.innerHTML = '<span id="dynamic-currency">USD</span> ' + extraRevenue.toLocaleString();
                }"""

new_script = """                function updateCalculator() {
                    if(!calcChats || !calcTicket) return;
                    const chats = parseInt(calcChats.value);
                    const ticket = parseInt(calcTicket.value);
                    
                    // Obtener la moneda actual que geo-personalization.js haya establecido (o 'USD' por defecto si aún no corre)
                    let currentCurrency = 'USD';
                    const currEl = document.querySelector('.dyn-currency');
                    if (currEl && currEl.textContent) currentCurrency = currEl.textContent.trim();
                    
                    valChats.textContent = chats;
                    valTicket.innerHTML = `<span class="dyn-currency">${currentCurrency}</span> ` + ticket.toLocaleString();
                    
                    const hoursSaved = Math.round((chats * 30 * 5) / 60);
                    resHours.textContent = hoursSaved.toLocaleString() + 'h';
                    
                    const leadsLostPerMonth = Math.round((chats * 30) * 0.20);
                    resLeads.textContent = "+" + leadsLostPerMonth.toLocaleString();
                    
                    const extraRevenue = Math.round(leadsLostPerMonth * 0.15 * ticket);
                    resRevenue.innerHTML = `<span class="dyn-currency">${currentCurrency}</span> ` + extraRevenue.toLocaleString();
                }"""

html = html.replace(old_script, new_script)

with open("templates/automatizacion_whatsapp.html", "w", encoding="utf-8") as f:
    f.write(html)
