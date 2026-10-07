// Aakash Academy AI Prompt Hub — Advanced Animated Application Logic

document.addEventListener('DOMContentLoaded', () => {
    // Dataset Reference
    const prompts = (typeof AAKASH_PROMPTS_DATA !== 'undefined' && AAKASH_PROMPTS_DATA.length > 0)
        ? AAKASH_PROMPTS_DATA
        : [];

    // State Variables
    let currentCategory = 'ALL';
    let searchQuery = '';
    let sortOption = 'default';
    let activePrompt = null;
    let favorites = JSON.parse(localStorage.getItem('aakash_favs') || '[]');

    // DOM References
    const gridEl = document.getElementById('prompts-grid');
    const marqueeTrack = document.getElementById('marquee-track');
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search-btn');
    const sortSelect = document.getElementById('sort-select');
    const noResultsEl = document.getElementById('no-results');
    const categoryBtns = document.querySelectorAll('.pill');
    const statTotalPrompts = document.getElementById('stat-total-prompts');
    const allCountEl = document.getElementById('all-count');
    const themeToggleBtn = document.getElementById('theme-toggle');

    // Modal References
    const modalOverlay = document.getElementById('prompt-modal');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalImage = document.getElementById('modal-image');
    const modalCat = document.getElementById('modal-cat');
    const modalTitle = document.getElementById('modal-title');
    const modalStats = document.getElementById('modal-stats');
    const modalPromptText = document.getElementById('modal-prompt-text');
    const modalCopyBtn = document.getElementById('modal-copy-btn');
    const modalCopyBtn2 = document.getElementById('modal-copy-btn-2');
    const modalFavBtn = document.getElementById('modal-fav-btn');
    const modalShareBtn = document.getElementById('modal-share-btn');
    
    const favCountEl = document.getElementById('fav-count');
    const pillFavCountEl = document.getElementById('pill-fav-count');
    const toastEl = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    const scrollTopBtn = document.getElementById('scroll-top-btn');

    // Initialize App
    if (statTotalPrompts) statTotalPrompts.textContent = prompts.length;
    if (allCountEl) allCountEl.textContent = prompts.length;
    updateFavBadges();
    initTheme();
    renderMarquee(prompts.slice(0, 20));
    renderGridWithSkeleton();

    // Theme Management
    function initTheme() {
        const saved = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', saved);
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const cur = document.documentElement.getAttribute('data-theme');
            const next = cur === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
        });
    }

    // Render Infinite Marquee Carousel
    function renderMarquee(list) {
        if (!marqueeTrack || list.length === 0) return;
        const items = [...list, ...list];
        marqueeTrack.innerHTML = items.map(item => `
            <div class="mq-card-item" onclick="openPromptModal('${item.id}')">
                <img src="${item.image}" alt="${escapeHtml(item.title)}" loading="lazy">
                <div class="mq-overlay">
                    <span class="mq-title">${escapeHtml(item.title)}</span>
                </div>
            </div>
        `).join('');
    }

    // Skeleton Screen Animation Loader (#24)
    function renderGridWithSkeleton() {
        if (!gridEl) return;
        // Inject 8 skeleton cards
        gridEl.innerHTML = Array(8).fill(0).map(() => `
            <div class="skeleton-card">
                <div class="skeleton-thumb"></div>
                <div class="skeleton-text" style="width: 40%;"></div>
                <div class="skeleton-text" style="width: 80%;"></div>
            </div>
        `).join('');

        // Render actual grid after short animation frame
        setTimeout(() => {
            renderGrid();
        }, 220);
    }

    // Render Prompts Grid with IntersectionObserver Scrollreveal (#2, #15)
    function renderGrid() {
        let filtered = prompts.filter(p => {
            if (currentCategory === 'FAVORITES') {
                if (!favorites.includes(p.id)) return false;
            } else if (currentCategory === 'Featured') {
                if (p.category !== 'Featured') return false;
            } else if (currentCategory !== 'ALL') {
                if (p.category.toLowerCase() !== currentCategory.toLowerCase()) return false;
            }

            if (searchQuery) {
                const q = searchQuery.toLowerCase();
                const matchTitle = p.title.toLowerCase().includes(q);
                const matchCat = p.category.toLowerCase().includes(q);
                return matchTitle || matchCat;
            }

            return true;
        });

        if (sortOption === 'name') {
            filtered.sort((a, b) => a.title.localeCompare(b.title));
        } else if (sortOption === 'popular') {
            filtered.sort((a, b) => parseInt(b.views) - parseInt(a.views));
        }

        if (filtered.length === 0) {
            gridEl.innerHTML = '';
            noResultsEl.style.display = 'block';
        } else {
            noResultsEl.style.display = 'none';
            gridEl.innerHTML = filtered.map((item, idx) => {
                const isFav = favorites.includes(item.id);
                return `
                <div class="card card-reveal" data-id="${item.id}" style="transition-delay: ${(idx % 12) * 0.04}s">
                    <div class="card-media">
                        <img src="${item.image}" alt="${escapeHtml(item.title)}" loading="lazy">
                        <span class="card-badge">⚡ UNLOCKED</span>
                        <button class="card-fav-btn ${isFav ? 'active' : ''}" onclick="toggleFav('${item.id}', event)">
                            ${isFav ? '❤️' : '🤍'}
                        </button>
                    </div>
                    <div class="card-content">
                        <span class="card-category">${escapeHtml(item.category)}</span>
                        <h3 class="card-title-text">${escapeHtml(item.title)}</h3>
                        <div class="card-bottom">
                            <span class="card-stats-text">👁️ ${item.views} | ❤️ ${item.likes}</span>
                            <button class="btn-card-action" onclick="openPromptModal('${item.id}')">View Prompt</button>
                        </div>
                    </div>
                </div>
            `}).join('');

            // Activate IntersectionObserver Parallax Scrollreveal
            setupScrollObserver();
            setupFaux3DTilt();
        }
    }

    // ScrollReveal Observer (#2)
    function setupScrollObserver() {
        const revealCards = document.querySelectorAll('.card-reveal');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });

        revealCards.forEach(card => observer.observe(card));
    }

    // Faux 3D Parallax Tilt Microinteraction (#14, #26)
    function setupFaux3DTilt() {
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                const tiltX = (y / rect.height) * -8;
                const tiltY = (x / rect.width) * 8;
                card.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateY(-6px) scale(1.02)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0) scale(1)';
            });
        });
    }

    // Category Pill Actions
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            categoryBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.getAttribute('data-cat');
            renderGridWithSkeleton();
        });
    });

    // Search Actions
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.trim();
            if (clearSearchBtn) clearSearchBtn.style.display = searchQuery ? 'block' : 'none';
            renderGrid();
        });
    }

    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', () => {
            searchInput.value = '';
            searchQuery = '';
            clearSearchBtn.style.display = 'none';
            renderGrid();
        });
    }

    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            sortOption = e.target.value;
            renderGrid();
        });
    }

    // Favorites Logic
    window.toggleFav = function(id, event) {
        if (event) event.stopPropagation();
        const idx = favorites.indexOf(id);
        if (idx >= 0) {
            favorites.splice(idx, 1);
            showToast("Removed from saved favorites");
        } else {
            favorites.push(id);
            showToast("Saved to favorites ❤️");
        }
        localStorage.setItem('aakash_favs', JSON.stringify(favorites));
        updateFavBadges();
        renderGrid();
        if (activePrompt && activePrompt.id === id) {
            updateModalFavState();
        }
    };

    function updateFavBadges() {
        if (favCountEl) favCountEl.textContent = favorites.length;
        if (pillFavCountEl) pillFavCountEl.textContent = favorites.length;
    }

    // Modal Operations
    window.openPromptModal = function(id) {
        const item = prompts.find(p => p.id === id);
        if (!item) return;

        activePrompt = item;
        modalImage.src = item.image;
        modalCat.textContent = item.category;
        modalTitle.textContent = item.title;
        modalStats.textContent = `👁️ ${item.views} views | ❤️ ${item.likes} likes`;
        modalPromptText.textContent = item.prompt_text;

        updateModalFavState();
        modalOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    function updateModalFavState() {
        if (!activePrompt || !modalFavBtn) return;
        const isFav = favorites.includes(activePrompt.id);
        modalFavBtn.innerHTML = isFav 
            ? `<svg width="14" height="14" viewBox="0 0 24 24" fill="#EC4899" stroke="#EC4899"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg> Saved in Favorites` 
            : `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg> Save to Favorites`;
    }

    if (modalFavBtn) {
        modalFavBtn.addEventListener('click', () => {
            if (activePrompt) window.toggleFav(activePrompt.id);
        });
    }

    function closeModal() {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = 'auto';
        activePrompt = null;
    }

    if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) closeModal();
        });
    }

    // Copy Prompt Functionality
    function copyPromptText() {
        if (!activePrompt) return;
        navigator.clipboard.writeText(activePrompt.prompt_text).then(() => {
            showToast("✨ Master Prompt Copied to Clipboard!");
        }).catch(() => {
            showToast("Copied text!");
        });
    }

    if (modalCopyBtn) modalCopyBtn.addEventListener('click', copyPromptText);
    if (modalCopyBtn2) modalCopyBtn2.addEventListener('click', copyPromptText);

    if (modalShareBtn) {
        modalShareBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(window.location.href);
            showToast("🔗 Page link copied to clipboard!");
        });
    }

    // Toast Banner
    function showToast(msg) {
        if (!toastEl) return;
        toastMessage.textContent = msg;
        toastEl.classList.add('active');
        setTimeout(() => {
            toastEl.classList.remove('active');
        }, 3000);
    }

    // Scroll to Top
    if (scrollTopBtn) {
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    window.resetFilters = function() {
        if (searchInput) searchInput.value = '';
        searchQuery = '';
        currentCategory = 'ALL';
        sortOption = 'default';
        if (clearSearchBtn) clearSearchBtn.style.display = 'none';
        categoryBtns.forEach(b => b.classList.remove('active'));
        if (categoryBtns[0]) categoryBtns[0].classList.add('active');
        renderGrid();
    };

    function escapeHtml(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
        );
    }
});
