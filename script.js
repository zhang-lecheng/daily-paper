const dateSelect = document.getElementById('dateSelect');
const aiFilter = document.getElementById('aiFilter');
const paperList = document.getElementById('paperList');

let allPapers = [];

async function init() {
    try {
        const response = await fetch('data/available_dates.json');
        const dates = await response.json();

        dateSelect.innerHTML = dates.map(date => `<option value="${date}">${date}</option>`).join('');

        if (dates.length > 0) {
            loadPapers(dates[0]);
        }
    } catch (e) {
        console.error("Failed to load dates", e);
        paperList.innerHTML = `<div class="loading">Failed to load dates. Please check if data is available.</div>`;
    }
}

async function loadPapers(date) {
    paperList.innerHTML = `<div class="loading">Loading papers for ${date}...</div>`;
    try {
        const response = await fetch(`data/${date}.json`);
        allPapers = await response.json();
        renderPapers();
    } catch (e) {
        console.error("Failed to load papers", e);
        paperList.innerHTML = `<div class="loading">Failed to load papers for this date.</div>`;
    }
}

function renderPapers() {
    const showOnlyAI = aiFilter.checked;
    const filtered = showOnlyAI ? allPapers.filter(p => p.ai4science) : allPapers;

    if (filtered.length === 0) {
        paperList.innerHTML = `<div class="loading">No papers found matching the filter.</div>`;
        return;
    }

    paperList.innerHTML = filtered.map(paper => `
        <div class="paper-card">
            <div class="paper-title">
                <a href="${paper.url}" target="_blank">${paper.title}</a>
            </div>
            <div class="paper-authors">${paper.authors.join(', ')} • ${paper.published}</div>
            <div class="paper-tags">
                ${paper.ai4science ? '<span class="tag">AI4Science</span>' : ''}
                ${paper.perturbation ? '<span class="tag perturbation">Perturbation Prediction</span>' : ''}
            </div>
            ${paper.ai4science ? `
                <div class="ai-reason">
                    <span class="reason-label">AI Analysis</span>
                    ${paper.reason}
                </div>
            ` : ''}
        </div>
    `).join('');
}

dateSelect.addEventListener('change', (e) => loadPapers(e.target.value));
aiFilter.addEventListener('change', renderPapers);

init();
