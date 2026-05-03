INDUSTRY_DATA = {
    'Restaurantes': {
        'intro': 'Deja de perder reservas por no responder a tiempo. Tu asistente IA en {ciudad} gestiona mesas 24/7, responde dudas del menú al instante y evita los molestos no-shows. Recupera tu tiempo y llena tu negocio sin estrés. ¡{yes}!',
        'chat': {
            'user': '{greeting_user}, {you_verb_have} mesa para 4 hoy tipo 9? vamos con un perrito 🐶',
            'bot': '{greeting_bot} Sí, somos Pet Friendly. 🐾 Tenemos una mesa perfecta en la terraza. Confírmame a qué nombre la dejo agendada y la cargamos directo a nuestro sistema de reservas.'
        },
        'cards': [
            {'icon': 'fas fa-calendar-check', 'title': 'Reservas 24/7', 'desc': 'La IA toma reservas, verifica mesas disponibles y actualiza tu agenda automáticamente, de día o de noche.'},
            {'icon': 'fas fa-utensils', 'title': 'Menú Interactivo', 'desc': 'Responde al instante preguntas sobre alérgenos, opciones veganas o platos del día, guiando el antojo del cliente.'},
            {'icon': 'fas fa-bell', 'title': 'Anti No-Shows', 'desc': 'Envía recordatorios amigables horas antes de la reserva y gestiona cancelaciones para liberar mesas rápidamente.'},
            {'icon': 'fas fa-sync-alt', 'title': 'Fidelización', 'desc': 'Contacta a clientes que no visitan hace semanas con promociones automáticas para reactivar su consumo.'}
        ],
        'faqs': [
            {'q': '¿Cómo se conecta el bot con mi software de reservas actual?', 'a': 'Nos integramos vía API con plataformas como OpenTable, CoverManager o Meitre. El bot consulta disponibilidad en tiempo real y bloquea la mesa sin intervención humana.'},
            {'q': '¿El bot puede gestionar depósitos de seña para fechas especiales?', 'a': 'Absolutamente. El bot envía el link de pago (MercadoPago, Stripe) y no confirma la reserva en tu sistema hasta validar la transacción.'},
            {'q': '¿Qué pasa si el cliente pide algo muy específico fuera del menú?', 'a': 'La IA está entrenada con las reglas de tu restaurante. Si hay un pedido que requiere autorización, escala el chat a tu recepcionista silenciosamente.'}
        ]
    },
    'Salones de Belleza': {
        'intro': 'Llena la agenda de tu salón en {ciudad} mientras trabajas. Tu agente IA responde tarifas, toma citas 24/7 y envía recordatorios para que tus sillones nunca estén vacíos. Factura más {money}, organizando menos.',
        'chat': {
            'user': '{greeting_user}, a q hora {you_verb_have} libre mañana para balayage y corte?',
            'bot': '{greeting_bot} 💇‍♀️ Tengo un espacio a las 15:30 hs con nuestra colorista principal. ¿Te guardo el turno? Queda bloqueado en nuestra agenda.'
        },
        'cards': [
            {'icon': 'fas fa-calendar-alt', 'title': 'Agenda Inteligente', 'desc': 'Coordina citas complejas que requieren diferentes tiempos (ej. color + corte) cruzando disponibilidad de estilistas.'},
            {'icon': 'fas fa-images', 'title': 'Cotización Visual', 'desc': 'La IA analiza fotos de referencia que manda el cliente para dar un rango de precio aproximado y tiempo de sesión.'},
            {'icon': 'fas fa-stopwatch', 'title': 'Cero Huecos', 'desc': 'Si un cliente cancela, la IA notifica automáticamente a la lista de espera para rellenar ese horario.'},
            {'icon': 'fas fa-heart', 'title': 'Seguimiento', 'desc': 'Escribe al mes para recordar el retoque de raíz o el mantenimiento de uñas, impulsando la recurrencia.'}
        ],
        'faqs': [
            {'q': '¿Puede el bot agendar citas con profesionales específicos?', 'a': 'Sí. La IA lee la disponibilidad individual de cada estilista desde herramientas como Fresha o Google Calendar y coordina los tiempos exactos.'},
            {'q': '¿Cómo maneja la IA los tratamientos que varían de precio según el largo?', 'a': 'Entrenamos al bot para pedir una foto o preguntar el largo actual, ofreciendo un rango estimado y aclarando que el valor final se confirma en el salón.'},
            {'q': '¿Se puede configurar el cobro de señas para tratamientos caros?', 'a': 'Totalmente. La IA envía el enlace de pago y retiene el turno por un tiempo límite (ej. 30 min). Si no se paga, lo libera automáticamente.'}
        ]
    },
    'Clínicas Dentales': {
        'intro': 'Deja de perder pacientes en {ciudad} por demoras al responder. Implementamos IA que filtra urgencias, coordina turnos con tus especialistas y envía recordatorios 24/7. Digitaliza tu clínica y aumenta tu {money}.',
        'chat': {
            'user': '{greeting_user}, se me cayó un bracket, {you_verb_have} turno de urgencia hoy??',
            'bot': '{greeting_bot} Entiendo la molestia. Tenemos un espacio a las 16:00 hs con el especialista. ¿Me confirmas tu DNI para agendarte directo en el sistema?'
        },
        'cards': [
            {'icon': 'fas fa-tooth', 'title': 'Triage Inicial', 'desc': 'La IA filtra urgencias dentales frente a consultas estéticas y prioriza la asignación de turnos inmediatos.'},
            {'icon': 'fas fa-calendar-plus', 'title': 'Agendamiento', 'desc': 'Se sincroniza con el calendario de tus doctores (Dentalink, Google) y ofrece los horarios exactos disponibles.'},
            {'icon': 'fas fa-file-medical', 'title': 'Pre-Evaluación', 'desc': 'Solicita información básica previa al turno, agilizando el tiempo en sala de espera de tu clínica.'},
            {'icon': 'fas fa-clock', 'title': 'Recordatorios', 'desc': 'Reduce inasistencias enviando recordatorios automáticos por WhatsApp pidiendo confirmación o reagendamiento.'}
        ],
        'faqs': [
            {'q': '¿Se integra con mi software de gestión odontológica?', 'a': 'Sí, sincronizamos la IA mediante API con plataformas como Dentalink, Odonto o tu CRM actual, asegurando doble vía de información.'},
            {'q': '¿Cómo gestiona la IA la confidencialidad médica?', 'a': 'Usamos la API Oficial de Meta (encriptación extremo a extremo) y la IA solo solicita datos de triage básico, sin almacenar historias clínicas.'},
            {'q': '¿Puede la IA explicar procedimientos o presupuestos?', 'a': 'La IA responde dudas frecuentes sobre implantes, ortodoncia, etc. Para presupuestos exactos, invita al paciente a una consulta presencial de diagnóstico.'}
        ]
    },
    'Hoteles y Hostales': {
        'intro': 'Tu recepción virtual en {ciudad} nunca duerme. Automatiza reservas, consultas de habitaciones y servicios adicionales al instante. Brinda un servicio {cool} desde WhatsApp y escala la ocupación de tu hotel.',
        'chat': {
            'user': '{greeting_user}, necesito saber si {you_verb_have} habitación doble del 15 al 18 y el precio porfa.',
            'bot': '{greeting_bot} Sí, tenemos habitaciones dobles disponibles para esas fechas. El total es $150 USD. ¿{you_verb_want} que te envíe el link de reserva?'
        },
        'cards': [
            {'icon': 'fas fa-bed', 'title': 'Disponibilidad 24/7', 'desc': 'Cruza datos con tu PMS para confirmar fechas libres y concretar reservas a cualquier hora del día.'},
            {'icon': 'fas fa-concierge-bell', 'title': 'Concierge Virtual', 'desc': 'Responde sobre horarios de desayuno, WiFi, check-in, check-out y tours, sin molestar a la recepción.'},
            {'icon': 'fas fa-credit-card', 'title': 'Pagos Seguros', 'desc': 'Genera y envía enlaces de pago automáticos para confirmar reservas de manera rápida y sin fricción.'},
            {'icon': 'fas fa-plane-arrival', 'title': 'Up-selling', 'desc': 'Ofrece traslados al aeropuerto, upgrade de habitación o cenas románticas antes de la llegada del huésped.'}
        ],
        'faqs': [
            {'q': '¿Se conecta con nuestro Channel Manager (Cloudbeds, SiteMinder)?', 'a': 'Por supuesto. La IA lee la disponibilidad en tiempo real y bloquea la habitación, evitando overbooking.'},
            {'q': '¿Puede la IA atender huéspedes en varios idiomas?', 'a': 'Sí, la IA detecta automáticamente el idioma del usuario (inglés, portugués, etc.) y le responde con la misma naturalidad que en español.'},
            {'q': '¿El bot puede hacer pre check-in por WhatsApp?', 'a': 'Totalmente. La IA puede solicitar los datos, foto del pasaporte y horario de llegada antes de que el huésped pise el hotel.'}
        ]
    },
    'Inmobiliarias': {
        'intro': 'Filtra prospectos y coordina visitas en automático. Tu IA captura propiedades, cruza requisitos en tiempo real y agenda a los interesados ideales en {ciudad}. Acelera tus cierres inmobiliarios y multiplica tu {money}.',
        'chat': {
            'user': '{greeting_user}, el dpto de 2 ambientes de la calle Mitre sigue disponible? aceptan mascotas?',
            'bot': '{greeting_bot} Sí, sigue disponible y es Pet Friendly 🐾. ¿Cumples con los requisitos de garantía? Si es así, te agendamos una visita.'
        },
        'cards': [
            {'icon': 'fas fa-filter', 'title': 'Filtro de Leads', 'desc': 'Pre-califica automáticamente preguntando por garantías, ingresos y número de personas antes de coordinar visita.'},
            {'icon': 'fas fa-home', 'title': 'Match de Propiedades', 'desc': 'Si la propiedad consultada ya se alquiló, la IA sugiere opciones similares en la misma zona de forma instantánea.'},
            {'icon': 'fas fa-calendar-check', 'title': 'Agenda de Visitas', 'desc': 'Sincroniza con el calendario de tus asesores comerciales para fijar citas en las propiedades sin idas y vueltas.'},
            {'icon': 'fas fa-file-contract', 'title': 'Envío de Fichas', 'desc': 'Comparte brochures, videos y detalles técnicos de los inmuebles directamente en el chat del cliente.'}
        ],
        'faqs': [
            {'q': '¿Cómo se conecta con mi CRM inmobiliario (Tokko, EasyBroker)?', 'a': 'Usamos APIs para que la IA lea el inventario actualizado. Cada nuevo lead pre-calificado se inyecta directamente en tu pipeline.'},
            {'q': '¿El bot puede atender captación de propiedades (propietarios)?', 'a': 'Sí. Identifica si el usuario quiere comprar/alquilar o si es un propietario que quiere tasar/vender su inmueble, y dispara el flujo correspondiente.'},
            {'q': '¿Qué pasa si la IA se equivoca en un precio?', 'a': 'La IA no inventa precios. Siempre extrae la información en tiempo real de tu base de datos o feed XML. Si la propiedad no tiene precio público, solicita el contacto para un asesor.'}
        ]
    },
    'Gimnasios': {
        'intro': 'Inscribe nuevos socios a las 3 AM. Tu bot de WhatsApp responde tarifas de tu gimnasio en {ciudad}, envía links de pago y gestiona cobros atrasados. Aumenta tu retención y genera más {money} sin esfuerzo humano.',
        'chat': {
            'user': '{greeting_user}, q cuesta el pase libre y hay q pagar inscripcion?',
            'bot': '{greeting_bot} El pase libre cuesta $30.000/mes. Solo por esta semana la inscripción está 100% bonificada. 💪 ¿{you_verb_want} que te pase el link de registro para aprovecharlo?'
        },
        'cards': [
            {'icon': 'fas fa-dumbbell', 'title': 'Venta de Planes', 'desc': 'Explica diferencias entre planes, horarios de clases y envía pasarelas de pago para inscribir socios automáticamente.'},
            {'icon': 'fas fa-money-bill-wave', 'title': 'Gestión de Morosos', 'desc': 'Detecta pagos atrasados y envía recordatorios amables con el link de pago para recuperar cuotas vencidas.'},
            {'icon': 'fas fa-calendar-alt', 'title': 'Reserva de Clases', 'desc': 'Permite a los socios reservar su cupo en spinning o crossfit conectándose con el software de tu gimnasio.'},
            {'icon': 'fas fa-clipboard-list', 'title': 'Onboarding', 'desc': 'Da la bienvenida a los nuevos socios, enviándoles el reglamento, rutinas iniciales y tips de alimentación.'}
        ],
        'faqs': [
            {'q': '¿Se puede integrar con mi software de gestión deportiva (Evo, CrossHero)?', 'a': 'Sí, la IA se conecta por API para altas automáticas, control de accesos y verificación del estado de pago del socio.'},
            {'q': '¿Cómo maneja la IA la venta cruzada (suplementos, personal trainer)?', 'a': 'El bot puede identificar necesidades durante el onboarding y enviar promos de proteínas o sesiones personalizadas con un link de compra directo.'},
            {'q': '¿Puede la IA enviar recordatorios a los que abandonan (churn)?', 'a': 'Exacto. Si el sistema detecta que un usuario lleva 3 semanas sin ir, la IA le envía un mensaje motivacional automático.'}
        ]
    },
    'Veterinarias': {
        'intro': 'Tu guardia 24/7 no puede perder llamadas. Nuestra IA en {ciudad} prioriza urgencias veterinarias, agenda baños, vacunas y da seguimiento post-operatorio. Cuida a tus pacientes de 4 patas eficientemente. ¡{cool}!',
        'chat': {
            'user': '{greeting_user}, mi perrito está respirando raro, {you_verb_have} guardia a esta hora?',
            'bot': '{greeting_bot} Sí, la guardia está abierta. 🚨 Por favor, {come_verb} directo a la clínica. Nuestro veterinario de turno ya está avisado.'
        },
        'cards': [
            {'icon': 'fas fa-ambulance', 'title': 'Triage de Urgencias', 'desc': 'Distingue entre un simple corte de uñas y una emergencia vital, derivando al médico de guardia sin demoras.'},
            {'icon': 'fas fa-syringe', 'title': 'Carnet Virtual', 'desc': 'Avisa proactivamente cuándo toca la próxima desparasitación o vacuna anual, asegurando el regreso del cliente.'},
            {'icon': 'fas fa-calendar-check', 'title': 'Turnos Automáticos', 'desc': 'Gestiona la agenda de peluquería, clínica y cirugías, respetando los tiempos de cada área.'},
            {'icon': 'fas fa-heartbeat', 'title': 'Post-Consulta', 'desc': 'A las 48hs de una visita o cirugía, envía un mensaje automático preguntando por el estado y evolución de la mascota.'}
        ],
        'faqs': [
            {'q': '¿Cómo diferencia la IA una urgencia de una consulta normal?', 'a': 'Se entrena al bot con palabras clave (ej: "sangre", "ahogando", "atropellado"). Si detecta peligro, omite flujos de venta y envía dirección y alerta inmediata.'},
            {'q': '¿La IA puede leer fotos de las mascotas?', 'a': 'Actualmente, puede recibir fotos (ej: ver una erupción) y derivarla al veterinario con un contexto detallado, pero por ética profesional no da diagnósticos clínicos automáticos.'},
            {'q': '¿Se integra con mi historial clínico digital?', 'a': 'Sí. Si tu software lo permite, el bot registra las interacciones del dueño directo en el perfil de la mascota.'}
        ]
    },
    'Talleres Automotrices': {
        'intro': 'No pares de trabajar bajo el auto por contestar el celular. Tu asistente IA en {ciudad} entrega presupuestos básicos, da turnos de mantenimiento y notifica cuando el vehículo está listo. ¡{yes}! Todo automático.',
        'chat': {
            'user': '{greeting_user}, el auto me hace un ruido raro al frenar. {you_verb_have} turno para mirarlo?',
            'bot': '{greeting_bot} Suena a que necesitas una revisión de frenos. 🚗 Tenemos un hueco mañana a las 10:00 am. ¿Me pasas la marca y modelo de tu auto para agendarte?'
        },
        'cards': [
            {'icon': 'fas fa-car-crash', 'title': 'Recepción de Casos', 'desc': 'Recibe fotos y audios del problema del vehículo, catalogando el tipo de servicio que necesita (mecánica, chapa, eléctrica).'},
            {'icon': 'fas fa-calendar-alt', 'title': 'Asignación de Elevador', 'desc': 'Cruza horarios y capacidad del taller para agendar revisiones sin saturar a los mecánicos.'},
            {'icon': 'fas fa-check-circle', 'title': 'Avisos de Entrega', 'desc': 'Cuando terminas el service, el bot avisa automáticamente al cliente que puede pasar a retirar y envía el costo.'},
            {'icon': 'fas fa-oil-can', 'title': 'Mantenimiento Preventivo', 'desc': 'Calcula fechas por kilometraje y escribe a los meses para recordar que toca cambio de aceite y filtros.'}
        ],
        'faqs': [
            {'q': '¿El bot puede cotizar repuestos exactos?', 'a': 'El bot da presupuestos estimados de mano de obra o servicios estándar (ej. Service de 10.000km). Para fallas complejas, solicita datos y escala al mecánico experto.'},
            {'q': '¿Cómo le aviso a la IA que el auto ya está listo?', 'a': 'Con nuestra plataforma o tu CRM, simplemente cambias el estado del vehículo a "Listo" y la IA dispara el mensaje final al cliente automáticamente.'},
            {'q': '¿Se puede enviar presupuestos formales en PDF?', 'a': 'Sí. La IA puede generar y enviar presupuestos formales o capturar la aceptación del cliente (aprobación) de los arreglos adicionales requeridos.'}
        ]
    },
    'Spas y Centros de Estética': {
        'intro': 'Vende relajación de manera inteligente. La IA agenda masajes, depilación y envía Gift Cards en automático en {ciudad}. Cuida de tus pacientes mientras la inteligencia artificial cuida de tus reservas y tu {money}.',
        'chat': {
            'user': '{greeting_user}!! quería ver promos para el día de la madre, un día de spa o algo asi',
            'bot': '{greeting_bot} 🌸 Tenemos 3 promos hermosas. El "Pack Mamá Relax" es el más elegido. Incluye masaje e hidratación. ¿Te gustaría que te pase el folleto digital para que lo veas?'
        },
        'cards': [
            {'icon': 'fas fa-spa', 'title': 'Venta de Tratamientos', 'desc': 'Recomienda tratamientos según el tipo de piel o dolor del paciente, funcionando como un asesor comercial 24/7.'},
            {'icon': 'fas fa-gift', 'title': 'Venta de Vouchers', 'desc': 'Cierra ventas de Gift Cards de madrugada, generando links de pago y enviando el voucher digital instantáneo.'},
            {'icon': 'fas fa-calendar-day', 'title': 'Reservas Optimizadas', 'desc': 'Coordina citas considerando la disponibilidad de cabinas y del profesional específico que requiere el tratamiento.'},
            {'icon': 'fas fa-comments', 'title': 'Protocolos Previos', 'desc': 'Envía indicaciones (ej. "no tomar sol 48hs antes de la depilación láser") y consentimientos informados automáticos.'}
        ],
        'faqs': [
            {'q': '¿La IA se integra con mi agenda de especialistas?', 'a': 'Sí, nos integramos con Fresha, Google Calendar, entre otros. Consideramos la disponibilidad de las salas/equipos y del terapeuta al mismo tiempo.'},
            {'q': '¿Qué hace si un tratamiento requiere evaluación previa presencial?', 'a': 'La IA está programada para identificar tratamientos invasivos o específicos y su objetivo principal será agendar esa primera cita de diagnóstico.'},
            {'q': '¿Puede hacer campañas de reactivación (ej. a pacientes de botox)?', 'a': 'Claro. A los 4-6 meses de la aplicación, la IA puede contactar proactivamente recordando el retoque, multiplicando la recurrencia.'}
        ]
    },
    'Academias y Cursos': {
        'intro': 'Convierte prospectos en alumnos sin esfuerzo. Tu bot en {ciudad} comparte temarios, costos y links de inscripción las 24hs. Escala tus matrículas y genera más {money} al instante.',
        'chat': {
            'user': '{greeting_user}, info del curso de marketing? empieza la prox semana vdd?',
            'bot': '{greeting_bot} Así es, inicia el próximo martes a las 19:00 hs. 🎓 Modalidad 100% online y queda grabado. ¿{you_verb_want} que te pase el PDF con el temario completo?'
        },
        'cards': [
            {'icon': 'fas fa-graduation-cap', 'title': 'Matrícula 24/7', 'desc': 'Cierra inscripciones enviando formularios y procesando pagos fuera del horario de oficina comercial.'},
            {'icon': 'fas fa-book-open', 'title': 'Entrega de Temarios', 'desc': 'Envía brochures en PDF, detalles de la malla curricular y certificaciones según el curso consultado.'},
            {'icon': 'fas fa-question-circle', 'title': 'Soporte al Alumno', 'desc': 'Responde automáticamente dudas de alumnos activos sobre contraseñas de campus, faltas y horarios.'},
            {'icon': 'fas fa-bullhorn', 'title': 'Nutrición de Leads', 'desc': 'Hace seguimiento al lead que preguntó pero no compró, ofreciendo descuentos o avisando del cierre de cupos.'}
        ],
        'faqs': [
            {'q': '¿Se integra con mi LMS (Moodle, Hotmart, Thinkific)?', 'a': 'Sí, podemos conectar la IA con plataformas educativas para generar accesos, consultar el estado del pago o enviar recordatorios de clases.'},
            {'q': '¿La IA puede atender a diferentes países con precios distintos?', 'a': 'Totalmente. La IA detecta el código de país del usuario (+54, +57, +34) y entrega la información con la moneda local y horarios correspondientes.'},
            {'q': '¿Cómo gestiona dudas muy técnicas sobre un curso avanzado?', 'a': 'Si la pregunta excede el conocimiento del prospecto (ej. dudas sobre un módulo específico de Python), escala el chat a un coordinador académico.'}
        ]
    }
}
