// frontend logic for opportunity portal

// State
let allOpportunities = [];
let deleteTargetId = null;

// DOM Elements
const grid = document.getElementById("opportunities-grid");
const loadingSpinner = document.getElementById("loading-spinner");
const emptyState = document.getElementById("empty-state");
const resultsCount = document.getElementById("results-count");
const searchInput = document.getElementById("search-input");
const departmentFilter = document.getElementById("department-filter");
const statusFilter = document.getElementById("status-filter");
const resetFiltersBtn = document.getElementById("reset-filters-btn");
const emptyStateResetBtn = document.getElementById("empty-state-reset-btn");

// Metric Elements
const metricTotal = document.getElementById("metric-total");
const metricOpen = document.getElementById("metric-open");
const metricClosed = document.getElementById("metric-closed");

// Modals
const createModal = document.getElementById("create-modal");
const editModal = document.getElementById("edit-modal");
const detailsModal = document.getElementById("details-modal");
const deleteModal = document.getElementById("delete-modal");

// Forms
const createForm = document.getElementById("create-form");
const editForm = document.getElementById("edit-form");
const createErrorBanner = document.getElementById("create-error");
const editErrorBanner = document.getElementById("edit-error");


// Notification Toast System
function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transition = "opacity 0.3s ease";
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}


// Modal Controls
function openModal(modal) {
    if (modal) modal.style.display = "flex";
}

function closeModal(modal) {
    if (modal) modal.style.display = "none";
}

// Global modal close triggers
document.querySelectorAll("[data-close]").forEach((btn) => {
    btn.addEventListener("click", () => {
        const targetId = btn.getAttribute("data-close");
        const targetModal = document.getElementById(targetId);
        closeModal(targetModal);
    });
});

window.addEventListener("click", (e) => {
    if (e.target.classList.contains("modal-overlay")) {
        closeModal(e.target);
    }
});


// Fetch and Render Opportunities (GET /api/opportunities)
async function loadOpportunities() {
    loadingSpinner.style.display = "block";
    grid.innerHTML = "";
    emptyState.style.display = "none";

    try {
        const res = await fetch("/api/opportunities");
        const result = await res.json();

        if (!res.ok || !result.success) {
            throw new Error(result.error || "Failed to load opportunities");
        }

        allOpportunities = result.data || [];
        updateMetrics(allOpportunities);
        renderFilteredOpportunities();
    } catch (err) {
        console.error("Error loading opportunities:", err);
        showToast(`Could not load data: ${err.message}`, "error");
        loadingSpinner.style.display = "none";
    }
}

function updateMetrics(items) {
    const total = items.length;
    const openCount = items.filter((item) => item.status === "Open").length;
    const closedCount = items.filter((item) => item.status === "Closed").length;

    metricTotal.textContent = total;
    metricOpen.textContent = openCount;
    metricClosed.textContent = closedCount;
}

function renderFilteredOpportunities() {
    loadingSpinner.style.display = "none";

    const query = searchInput.value.trim().toLowerCase();
    const dept = departmentFilter.value;
    const status = statusFilter.value;

    const filtered = allOpportunities.filter((item) => {
        const matchesQuery =
            !query ||
            item.title.toLowerCase().includes(query) ||
            item.faculty_name.toLowerCase().includes(query) ||
            item.research_area.toLowerCase().includes(query);

        const matchesDept = !dept || item.department === dept;
        const matchesStatus = !status || item.status === status;

        return matchesQuery && matchesDept && matchesStatus;
    });

    resultsCount.textContent = `Showing ${filtered.length} of ${allOpportunities.length} opportunities`;

    if (filtered.length === 0) {
        grid.innerHTML = "";
        emptyState.style.display = "block";
        return;
    }

    emptyState.style.display = "none";
    grid.innerHTML = filtered.map(createOpportunityCardHtml).join("");

    attachCardEventListeners();
}

function createOpportunityCardHtml(opp) {
    const isClosed = opp.status === "Closed";
    const statusClass = isClosed ? "badge-closed" : "badge-open";
    const toggleTargetStatus = isClosed ? "Open" : "Closed";
    const toggleBtnLabel = isClosed ? "Mark Open" : "Mark Closed";

    return `
        <article class="opportunity-card" data-id="${opp.id}">
            <div>
                <div class="card-top">
                    <h3 class="card-title">${escapeHtml(opp.title)}</h3>
                    <span class="badge ${statusClass}">${opp.status}</span>
                </div>
                <div class="card-area">${escapeHtml(opp.research_area)}</div>
                <div class="card-faculty">
                    Supervisor: <strong>${escapeHtml(opp.faculty_name)}</strong> &bull; ${escapeHtml(opp.department)}
                </div>
                <p class="card-desc-snippet">${escapeHtml(opp.description)}</p>
                
                <div class="card-meta-row">
                    <div class="meta-chip">Positions: <span>${opp.positions_available}</span></div>
                    <div class="meta-chip">Deadline: <span>${opp.deadline}</span></div>
                </div>
            </div>

            <div class="card-actions">
                <div class="card-actions-left">
                    <button class="btn btn-outline btn-sm action-view" data-id="${opp.id}">View Details</button>
                    <button class="btn btn-secondary btn-sm action-edit" data-id="${opp.id}">Edit</button>
                    <button class="btn btn-outline btn-sm action-toggle" data-id="${opp.id}" data-target-status="${toggleTargetStatus}">
                        ${toggleBtnLabel}
                    </button>
                </div>
                <button class="btn btn-danger btn-sm action-delete" data-id="${opp.id}" data-title="${escapeHtml(opp.title)}">Delete</button>
            </div>
        </article>
    `;
}

function attachCardEventListeners() {
    // View Details
    document.querySelectorAll(".action-view").forEach((btn) => {
        btn.addEventListener("click", () => openDetailsView(btn.getAttribute("data-id")));
    });

    // Edit
    document.querySelectorAll(".action-edit").forEach((btn) => {
        btn.addEventListener("click", () => openEditView(btn.getAttribute("data-id")));
    });

    // Toggle Status
    document.querySelectorAll(".action-toggle").forEach((btn) => {
        btn.addEventListener("click", () => {
            const id = btn.getAttribute("data-id");
            const targetStatus = btn.getAttribute("data-target-status");
            toggleOpportunityStatus(id, targetStatus);
        });
    });

    // Delete
    document.querySelectorAll(".action-delete").forEach((btn) => {
        btn.addEventListener("click", () => {
            const id = btn.getAttribute("data-id");
            const title = btn.getAttribute("data-title");
            promptDeleteOpportunity(id, title);
        });
    });
}


// Single Opportunity Details View (GET /api/opportunities/:id)
async function openDetailsView(id) {
    try {
        const res = await fetch(`/api/opportunities/${id}`);
        const result = await res.json();

        if (!res.ok || !result.success) {
            throw new Error(result.error || "Opportunity not found");
        }

        const data = result.data;
        document.getElementById("details-id").textContent = `#${data.id}`;
        document.getElementById("details-title").textContent = data.title;
        document.getElementById("details-faculty").textContent = data.faculty_name;
        document.getElementById("details-department").textContent = data.department;
        document.getElementById("details-area").textContent = data.research_area;
        document.getElementById("details-positions").textContent = data.positions_available;
        document.getElementById("details-deadline").textContent = data.deadline;
        document.getElementById("details-skills").textContent = data.required_skills;
        document.getElementById("details-description").textContent = data.description;

        const badge = document.getElementById("details-status-badge");
        badge.textContent = data.status;
        badge.className = `badge ${data.status === "Closed" ? "badge-closed" : "badge-open"}`;

        const editShortcutBtn = document.getElementById("details-edit-shortcut-btn");
        editShortcutBtn.onclick = () => {
            closeModal(detailsModal);
            openEditView(data.id);
        };

        openModal(detailsModal);
    } catch (err) {
        showToast(`Failed to load details: ${err.message}`, "error");
    }
}


// Create Research Opportunity (POST /api/opportunities)
document.getElementById("open-create-modal-btn").addEventListener("click", () => {
    createForm.reset();
    createErrorBanner.style.display = "none";
    openModal(createModal);
});

createForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    createErrorBanner.style.display = "none";

    const payload = {
        title: document.getElementById("create-title").value.trim(),
        faculty_name: document.getElementById("create-faculty").value.trim(),
        department: document.getElementById("create-dept").value,
        research_area: document.getElementById("create-area").value.trim(),
        positions_available: parseInt(document.getElementById("create-positions").value, 10),
        deadline: document.getElementById("create-deadline").value,
        status: document.getElementById("create-status").value,
        required_skills: document.getElementById("create-skills").value.trim(),
        description: document.getElementById("create-desc").value.trim()
    };

    // Client-side validation check
    for (const [key, val] of Object.entries(payload)) {
        if (!val || (typeof val === "string" && !val.trim())) {
            createErrorBanner.textContent = `Please fill in the required field: ${key.replace("_", " ")}`;
            createErrorBanner.style.display = "block";
            return;
        }
    }

    const submitBtn = document.getElementById("create-submit-btn");
    submitBtn.disabled = true;
    submitBtn.textContent = "Publishing...";

    try {
        const res = await fetch("/api/opportunities", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const result = await res.json();

        if (res.status === 201 && result.success) {
            showToast("Research opportunity published successfully!", "success");
            closeModal(createModal);
            createForm.reset();
            loadOpportunities();
        } else {
            createErrorBanner.textContent = result.error || "Failed to create opportunity.";
            createErrorBanner.style.display = "block";
            showToast(result.error || "Validation error.", "error");
        }
    } catch (err) {
        createErrorBanner.textContent = `Server connection error: ${err.message}`;
        createErrorBanner.style.display = "block";
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Publish Opportunity";
    }
});


// Edit Research Opportunity (PUT /api/opportunities/:id)
async function openEditView(id) {
    editForm.reset();
    editErrorBanner.style.display = "none";

    try {
        const res = await fetch(`/api/opportunities/${id}`);
        const result = await res.json();

        if (!res.ok || !result.success) {
            throw new Error(result.error || "Failed to load record");
        }

        const data = result.data;
        document.getElementById("edit-id").value = data.id;
        document.getElementById("edit-title").value = data.title;
        document.getElementById("edit-faculty").value = data.faculty_name;
        document.getElementById("edit-dept").value = data.department;
        document.getElementById("edit-area").value = data.research_area;
        document.getElementById("edit-positions").value = data.positions_available;
        document.getElementById("edit-deadline").value = data.deadline;
        document.getElementById("edit-status").value = data.status;
        document.getElementById("edit-skills").value = data.required_skills;
        document.getElementById("edit-desc").value = data.description;

        openModal(editModal);
    } catch (err) {
        showToast(`Could not open editor: ${err.message}`, "error");
    }
}

editForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    editErrorBanner.style.display = "none";

    const id = document.getElementById("edit-id").value;
    const payload = {
        title: document.getElementById("edit-title").value.trim(),
        faculty_name: document.getElementById("edit-faculty").value.trim(),
        department: document.getElementById("edit-dept").value,
        research_area: document.getElementById("edit-area").value.trim(),
        positions_available: parseInt(document.getElementById("edit-positions").value, 10),
        deadline: document.getElementById("edit-deadline").value,
        status: document.getElementById("edit-status").value,
        required_skills: document.getElementById("edit-skills").value.trim(),
        description: document.getElementById("edit-desc").value.trim()
    };

    const submitBtn = document.getElementById("edit-submit-btn");
    submitBtn.disabled = true;
    submitBtn.textContent = "Saving...";

    try {
        const res = await fetch(`/api/opportunities/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const result = await res.json();

        if (res.status === 200 && result.success) {
            showToast("Opportunity updated successfully!", "success");
            closeModal(editModal);
            loadOpportunities();
        } else {
            editErrorBanner.textContent = result.error || "Failed to update opportunity.";
            editErrorBanner.style.display = "block";
            showToast(result.error || "Update error.", "error");
        }
    } catch (err) {
        editErrorBanner.textContent = `Connection error: ${err.message}`;
        editErrorBanner.style.display = "block";
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Save Changes";
    }
});


// Toggle Opportunity Status (PUT /api/opportunities/:id)
async function toggleOpportunityStatus(id, newStatus) {
    try {
        const res = await fetch(`/api/opportunities/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: newStatus })
        });
        const result = await res.json();

        if (res.status === 200 && result.success) {
            showToast(`Status changed to ${newStatus}`, "success");
            loadOpportunities();
        } else {
            showToast(result.error || "Could not toggle status", "error");
        }
    } catch (err) {
        showToast(`Request failed: ${err.message}`, "error");
    }
}


// Delete Research Opportunity (DELETE /api/opportunities/:id)
function promptDeleteOpportunity(id, title) {
    deleteTargetId = id;
    document.getElementById("delete-target-title").textContent = `"${title}"`;
    openModal(deleteModal);
}

document.getElementById("confirm-delete-btn").addEventListener("click", async () => {
    if (!deleteTargetId) return;

    const btn = document.getElementById("confirm-delete-btn");
    btn.disabled = true;
    btn.textContent = "Deleting...";

    try {
        const res = await fetch(`/api/opportunities/${deleteTargetId}`, {
            method: "DELETE"
        });
        const result = await res.json();

        if (res.status === 200 && result.success) {
            showToast("Research opportunity deleted successfully.", "success");
            closeModal(deleteModal);
            deleteTargetId = null;
            loadOpportunities();
        } else {
            showToast(result.error || "Failed to delete opportunity", "error");
        }
    } catch (err) {
        showToast(`Request failed: ${err.message}`, "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "Delete Opportunity";
    }
});


// Filter & Search Controls Listeners
searchInput.addEventListener("input", renderFilteredOpportunities);
departmentFilter.addEventListener("change", renderFilteredOpportunities);
statusFilter.addEventListener("change", renderFilteredOpportunities);

function resetFilters() {
    searchInput.value = "";
    departmentFilter.value = "";
    statusFilter.value = "";
    renderFilteredOpportunities();
}

resetFiltersBtn.addEventListener("click", resetFilters);
emptyStateResetBtn.addEventListener("click", resetFilters);


// Utility to sanitize HTML output
function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Initial Data Load on Page Ready
document.addEventListener("DOMContentLoaded", loadOpportunities);
