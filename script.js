const CONFIG = {
    repo: 'zhang-lecheng/daily-paper',
    dataBranch: 'data',
    baseUrl: 'https://raw.githubusercontent.com/zhang-lecheng/daily-paper/data/'
};

const elements = {
    dateInput: document.getElementById('dateSelect'),
    aiFilter: document.getElementById('aiFilter'),
    paperList: document.getElementById('paperList'),
    searchInput: document.getElementById('searchInput'),
    categoryBar: document.getElementById('categoryBar'),
    perturbationFilter: document.getElementById('perturbationFilter')
};

let allPapers = [];
let availableDates = [];
let currentCategory = 'All';

async function fetchData(path) {
    // Attempt to fetch from GitHub raw if possible (production)
    try {
        const response = await fetch(CONFIG.baseUrl + path);
        if (response.ok) return await response.json();
    } catch (e) { }

    // Fallback to local (for local development/testing)
    const response = await fetch(`data/${path}`);
    return await response.json();
}

async function init() {
    try {
        availableDates = await fetchData('available_dates.json');

        flatpickr(elements.dateInput, {
            enable: availableDates,
            defaultDate: availableDates[0],
            dateFormat: "Y-m-d",
            onChange: (selectedDates, dateStr) => {
                loadPapers(dateStr);
            }
        });

        if (availableDates.length > 0) {
            loadPapers(availableDates[0]);
        }
    } catch (e) {
        console.error("Initialization failed", e);
        elements.paperList.innerHTML = `<div class="loading">Failed to load data. Please check connection.</div>`;
    }
}

async function loadPapers(date) {
    elements.paperList.innerHTML = `<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading papers for ${date}...</div>`;
    try {
        allPapers = await fetchData(`${date}.json`);
        currentCategory = 'All';
        renderCategories();
        renderPapers();
    } catch (e) {
        console.error("Load failed", e);
        elements.paperList.innerHTML = `<div class="loading">No papers found for ${date}.</div>`;
    }
}

function renderCategories() {
    const cats = new Set(['All']);
    allPapers.forEach(p => {
        if (p.primary_category) cats.add(p.primary_category);
    });

    elements.categoryBar.innerHTML = Array.from(cats).map(cat => `
        <div class="category-pill ${currentCategory === cat ? 'active' : ''}" 
             onclick="setCategory('${cat}')">
            ${cat}
        </div>
    `).join('');
}

window.setCategory = (cat) => {
    currentCategory = cat;
    renderCategories();
    renderPapers();
};

function renderPapers() {
    const showOnlyAI = elements.aiFilter.checked;
    const showOnlyPerturb = elements.perturbationFilter.checked;
    const query = elements.searchInput.value.toLowerCase();

    const filtered = allPapers.filter(p => {
        const matchesAI = !showOnlyAI || p.is_ai4science;
        const matchesPerturb = !showOnlyPerturb || p.is_perturbation;
        const matchesCat = currentCategory === 'All' || p.primary_category === currentCategory;
        const matchesSearch = p.title.toLowerCase().includes(query) ||
            p.summary.toLowerCase().includes(query);
        return matchesAI && matchesPerturb && matchesCat && matchesSearch;
    });

    if (filtered.length === 0) {
        elements.paperList.innerHTML = `<div class="loading">No papers match your criteria.</div>`;
        return;
    }

    elements.paperList.innerHTML = filtered.map((paper, index) => `
        <div class="paper-card ${paper.is_ai4science ? 'ai4science-card' : ''}">
            <div class="paper-header">
                <span class="paper-index">${index + 1}</span>
                <div class="paper-title">
                    <a href="${paper.url}" target="_blank">${paper.title}</a>
                </div>
            </div>
            <div class="paper-authors">${paper.authors.join(', ')}</div>
            <div class="paper-meta">
                <span class="meta-item"><i class="far fa-clock"></i> ${paper.published}</span>
                <span class="meta-item"><i class="fas fa-tag"></i> ${paper.primary_category}</span>
            </div>
            <div class="paper-tags">
                ${paper.is_ai4science ? '<span class="tag"><i class="fas fa-microscope"></i> AI4Science</span>' : ''}
                ${paper.is_perturbation ? '<span class="tag perturbation"><i class="fas fa-vial"></i> Perturbation Prediction</span>' : ''}
            </div>
            ${paper.reasoning ? `
                <div class="ai-reason">
                    <span class="reason-label"><i class="fas fa-robot"></i> AI Insight</span>
                    ${paper.reasoning}
                </div>
            ` : ''}
        </div>
    `).join('');
}

elements.aiFilter.addEventListener('change', renderPapers);
elements.perturbationFilter.addEventListener('change', renderPapers);
elements.searchInput.addEventListener('input', renderPapers);

init();
