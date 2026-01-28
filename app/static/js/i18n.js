// ===== SISTEMA DE IDIOMAS MULTILINGÜE GLOBAL =====
let translations = {};
let currentLanguage = localStorage.getItem('language') || 'es';

// Almacenar textos originales para poder traducir dinámicamente
let originalContent = {
    experience_titles: {},
    experience_companies: {},
    experience_descriptions: {},
    education_degrees: {},
    education_institutions: {},
    education_fields: {},
    education_descriptions: {},
    skill_categories: {}
};

// ===== CARGAR TRADUCCIONES DESDE JSON =====
async function loadTranslations() {
    try {
        const response = await fetch('/static/translations.json');
        translations = await response.json();
        
        // Primero guardar contenido original (que viene del servidor en español)
        storeOriginalContent();
        console.log('💾 Contenido original guardado');
        
        // Luego aplicar el idioma guardado
        // Si es español, no hace nada porque ya está en español
        // Si es otro idioma, traduce
        if (currentLanguage !== 'es') {
            applyLanguage(currentLanguage);
        } else {
            // Para español, solo actualizar selector y disparar evento
            updateLanguageSelector(currentLanguage);
            document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: currentLanguage } }));
        }
        
        updateSkillBars();
        console.log('✅ Traducciones cargadas correctamente');
    } catch (error) {
        console.error('❌ Error cargando traducciones:', error);
    }
}

// ===== GUARDAR CONTENIDO ORIGINAL =====
function storeOriginalContent() {
    // Guardar títulos de experiencias
    document.querySelectorAll('.timeline-title').forEach((el, idx) => {
        const text = el.textContent.trim();
        if (text && !originalContent.experience_titles[idx]) {
            originalContent.experience_titles[idx] = text;
        }
    });
    
    // Guardar empresas
    document.querySelectorAll('.timeline-company').forEach((el, idx) => {
        const text = el.textContent.trim();
        if (text && !originalContent.experience_companies[idx]) {
            originalContent.experience_companies[idx] = text;
        }
    });
    
    // Guardar descripciones de experiencias
    document.querySelectorAll('.timeline-description').forEach((el, idx) => {
        const text = el.textContent.trim();
        if (text && !originalContent.experience_descriptions[idx]) {
            originalContent.experience_descriptions[idx] = text;
        }
    });
    
    // Guardar grados educativos
    document.querySelectorAll('.education-card h3').forEach((el, idx) => {
        const text = el.textContent.trim();
        if (text && !originalContent.education_degrees[idx]) {
            originalContent.education_degrees[idx] = text;
        }
    });
    
    // Guardar instituciones
    document.querySelectorAll('.education-institution').forEach((el, idx) => {
        const text = el.textContent.trim();
        if (text && !originalContent.education_institutions[idx]) {
            originalContent.education_institutions[idx] = text;
        }
    });
    
    // Guardar campos de estudio
    document.querySelectorAll('.education-card').forEach((card, idx) => {
        const fieldDiv = card.querySelector('div[style*="color: var(--text-muted)"]');
        if (fieldDiv) {
            const text = fieldDiv.textContent.trim();
            if (text && !originalContent.education_fields[idx]) {
                originalContent.education_fields[idx] = text;
            }
        }
    });
    
    // Guardar descripciones educativas
    document.querySelectorAll('.education-card p').forEach((el, idx) => {
        const text = el.textContent.trim();
        if (text && !originalContent.education_descriptions[idx]) {
            originalContent.education_descriptions[idx] = text;
        }
    });
    
    // Guardar categorías de skills
    document.querySelectorAll('.skill-category-title').forEach((el, idx) => {
        const text = el.textContent.trim();
        if (text && !originalContent.skill_categories[idx]) {
            originalContent.skill_categories[idx] = text;
        }
    });
    
    console.log('💾 Contenido original guardado');
}

// ===== OBTENER TRADUCCIÓN ANIDADA =====
function getTranslation(key) {
    const keys = key.split('.');
    let translation = translations[currentLanguage];
    
    for (let k of keys) {
        if (translation && translation[k]) {
            translation = translation[k];
        } else {
            return key;
        }
    }
    
    return translation;
}

// ===== APLICAR IDIOMA A TODA LA PÁGINA =====
function applyLanguage(lang) {
    currentLanguage = lang;
    localStorage.setItem('language', lang);
    
    console.log('🔄 Aplicando idioma:', lang);
    
    // Actualizar atributo de idioma en HTML
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    
    // Traducir todos los elementos con data-i18n
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = getTranslation(key);
        
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            if (element.hasAttribute('placeholder')) {
                element.placeholder = translation;
            } else {
                element.value = translation;
            }
        } else if (element.hasAttribute('title')) {
            element.title = translation;
        } else {
            element.innerHTML = translation;
        }
    });
    
    // Traducir placeholders con data-i18n-placeholder
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        const translation = getTranslation(key);
        element.placeholder = translation;
    });
    
    // Actualizar selector de idioma
    updateLanguageSelector(lang);
    
    // Manejar contenido de BD
    if (lang === 'es') {
        // Restaurar contenido original español
        console.log('🇪🇸 Restaurando español original...');
        
        document.querySelectorAll('.timeline-title').forEach((el, idx) => {
            if (originalContent.experience_titles[idx]) {
                el.textContent = originalContent.experience_titles[idx];
            }
        });
        
        document.querySelectorAll('.timeline-company').forEach((el, idx) => {
            if (originalContent.experience_companies[idx]) {
                el.textContent = originalContent.experience_companies[idx];
            }
        });
        
        document.querySelectorAll('.timeline-description').forEach((el, idx) => {
            if (originalContent.experience_descriptions[idx]) {
                el.textContent = originalContent.experience_descriptions[idx];
            }
        });
        
        document.querySelectorAll('.education-card h3').forEach((el, idx) => {
            if (originalContent.education_degrees[idx]) {
                el.textContent = originalContent.education_degrees[idx];
            }
        });
        
        document.querySelectorAll('.education-institution').forEach((el, idx) => {
            if (originalContent.education_institutions[idx]) {
                el.textContent = originalContent.education_institutions[idx];
            }
        });
        
        document.querySelectorAll('.education-card').forEach((card, idx) => {
            const fieldDiv = card.querySelector('div[style*="color: var(--text-muted)"]');
            if (fieldDiv && originalContent.education_fields[idx]) {
                fieldDiv.textContent = originalContent.education_fields[idx];
            }
        });
        
        document.querySelectorAll('.education-card p').forEach((el, idx) => {
            if (originalContent.education_descriptions[idx]) {
                el.textContent = originalContent.education_descriptions[idx];
            }
        });
        
        document.querySelectorAll('.skill-category-title').forEach((el, idx) => {
            if (originalContent.skill_categories[idx]) {
                el.textContent = originalContent.skill_categories[idx];
            }
        });
        
        console.log('✅ Español restaurado completamente');
    } else {
        // Traducir a otro idioma
        translateDatabaseContent(lang);
    }
    
    // Disparar evento personalizado
    document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
}

// ===== CAMBIAR IDIOMA GLOBAL =====
function changeLanguage(lang) {
    console.log('🌍 Cambiando idioma a:', lang);
    
    // Siempre llamar a applyLanguage para actualizar todo correctamente
    applyLanguage(lang);
}

// ===== TRADUCIR CONTENIDO DE BASE DE DATOS =====
function translateDatabaseContent(lang) {
    try {
        const bdTranslations = translations[lang]?.bd_translations || {};
        
        if (!bdTranslations || Object.keys(bdTranslations).length === 0) {
            console.log('⚠️ No hay traducciones de BD para idioma:', lang);
            return;
        }
        
        console.log('🔄 Traduciendo contenido de BD para idioma:', lang);
        
        // Función auxiliar para traducir elementos
        function translateElements(selector, storageKey, translationMap) {
            const elements = document.querySelectorAll(selector);
            elements.forEach((el, idx) => {
                // Obtener el texto original guardado (en español)
                const originalText = originalContent[storageKey]?.[idx];
                
                if (originalText && translationMap[originalText]) {
                    const translated = translationMap[originalText];
                    console.log(`✅ ${storageKey} traducido: "${originalText}" → "${translated}"`);
                    el.textContent = translated;
                } else {
                    console.log(`⚠️ No se encontró traducción para: "${originalText}"`);
                }
            });
        }
        
        // Traducir títulos de experiencias
        if (bdTranslations.experience_titles) {
            console.log('📝 Traduciendo títulos de experiencias...');
            translateElements('.timeline-title', 'experience_titles', bdTranslations.experience_titles);
        }
        
        // Traducir empresas
        if (bdTranslations.experience_companies) {
            console.log('📝 Traduciendo empresas...');
            translateElements('.timeline-company', 'experience_companies', bdTranslations.experience_companies);
        }
        
        // Traducir descripciones de experiencias
        if (bdTranslations.experience_descriptions) {
            console.log('📝 Traduciendo descripciones de experiencias...');
            translateElements('.timeline-description', 'experience_descriptions', bdTranslations.experience_descriptions);
        }
        
        // Traducir grados educativos
        if (bdTranslations.education_degrees) {
            console.log('📚 Traduciendo grados educativos...');
            translateElements('.education-card h3', 'education_degrees', bdTranslations.education_degrees);
        }
        
        // Traducir instituciones educativas
        if (bdTranslations.education_institutions) {
            console.log('📚 Traduciendo instituciones...');
            translateElements('.education-institution', 'education_institutions', bdTranslations.education_institutions);
        }
        
        // Traducir campos de estudio
        if (bdTranslations.education_fields) {
            console.log('📚 Traduciendo campos de estudio...');
            document.querySelectorAll('.education-card').forEach((card, idx) => {
                const fieldDiv = card.querySelector('div[style*="color: var(--text-muted)"]');
                if (fieldDiv) {
                    const originalText = originalContent.education_fields[idx];
                    if (originalText && bdTranslations.education_fields[originalText]) {
                        const translated = bdTranslations.education_fields[originalText];
                        console.log(`✅ Campo traducido: "${originalText}" → "${translated}"`);
                        fieldDiv.textContent = translated;
                    }
                }
            });
        }
        
        // Traducir descripciones educativas
        if (bdTranslations.education_descriptions) {
            console.log('📚 Traduciendo descripciones de educación...');
            translateElements('.education-card p', 'education_descriptions', bdTranslations.education_descriptions);
        }
        
        // Traducir categorías de skills
        if (bdTranslations.skill_categories) {
            console.log('⚙️ Traduciendo categorías de skills...');
            translateElements('.skill-category-title', 'skill_categories', bdTranslations.skill_categories);
        }
        
        console.log('✅ Traducción de contenido de BD completada');
        
    } catch (error) {
        console.error('❌ Error traduciendo contenido de BD:', error);
    }
}

// ===== ACTUALIZAR SELECTOR DE IDIOMA =====
function updateLanguageSelector(lang) {
    const languageButtons = document.querySelectorAll('.language-btn');
    languageButtons.forEach(btn => {
        if (btn.getAttribute('data-lang') === lang) {
            btn.classList.add('active');
            btn.style.opacity = '1';
            btn.style.transform = 'scale(1.1)';
        } else {
            btn.classList.remove('active');
            btn.style.opacity = '0.6';
            btn.style.transform = 'scale(1)';
        }
    });
}

// ===== ACTUALIZAR BARRAS DE PROGRESO =====
function updateSkillBars() {
    const skillProgressElements = document.querySelectorAll('.skill-progress');
    let maxWidth = 0;
    
    skillProgressElements.forEach(element => {
        const widthValue = parseInt(element.style.width);
        if (widthValue > maxWidth) {
            maxWidth = widthValue;
        }
    });
    
    maxWidth = Math.max(maxWidth, 100);
    
    skillProgressElements.forEach(element => {
        const originalWidth = parseInt(element.style.width);
        element.style.width = originalWidth + '%';
    });
}

// ===== EVENT LISTENERS =====
document.addEventListener('languageChanged', (e) => {
    console.log('✅ Evento de cambio de idioma detectado:', e.detail.language);
    updateSkillBars();
});

document.addEventListener('DOMContentLoaded', () => {
    console.log('📖 Inicializando sistema de idiomas...');
    
    // Cargar traducciones
    loadTranslations();
    
    // Configurar event listeners en botones de idioma
    document.querySelectorAll('.language-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const lang = this.getAttribute('data-lang');
            if (lang) {
                changeLanguage(lang);
            }
        });
    });
    
    console.log('✅ Sistema de idiomas listo');
});

