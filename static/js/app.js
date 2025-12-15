// Main application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initAnimations();
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize cluster interactions
    initClusterInteractions();
    
    // Initialize module filter
    initModuleFilter();
    
    // Re-initialize after HTMX swaps (if HTMX is available)
    if (typeof htmx !== 'undefined') {
        document.body.addEventListener('htmx:afterSwap', function() {
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
            initAnimations();
        });
    }
});

// Animate elements on page load
function initAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('animate-slide-up');
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    animatedElements.forEach(el => observer.observe(el));
}

// Initialize tooltips
function initTooltips() {
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    
    tooltipTriggers.forEach(trigger => {
        trigger.addEventListener('mouseenter', function() {
            showTooltip(this);
        });
        
        trigger.addEventListener('mouseleave', function() {
            hideTooltip(this);
        });
    });
}

function showTooltip(element) {
    const tooltipText = element.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip absolute bg-gray-800 text-white text-sm px-3 py-2 rounded shadow-lg z-50';
    tooltip.textContent = tooltipText;
    tooltip.id = 'active-tooltip';
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
    tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
}

function hideTooltip(element) {
    const tooltip = document.getElementById('active-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// Cluster interactions
function initClusterInteractions() {
    const clusterItems = document.querySelectorAll('.cluster-item');
    
    clusterItems.forEach(item => {
        item.addEventListener('click', function() {
            this.classList.toggle('expanded');
            const details = this.querySelector('.cluster-details');
            if (details) {
                details.classList.toggle('hidden');
            }
        });
    });
}

// Module filter
function initModuleFilter() {
    const filterButtons = document.querySelectorAll('[data-module-filter]');
    const clusterItems = document.querySelectorAll('[data-module]');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filterValue = this.getAttribute('data-module-filter');
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active', 'bg-blue-600', 'text-white'));
            this.classList.add('active', 'bg-blue-600', 'text-white');
            
            // Filter clusters
            clusterItems.forEach(item => {
                const itemModule = item.getAttribute('data-module');
                if (filterValue === 'all' || itemModule === filterValue) {
                    item.style.display = 'block';
                    item.classList.add('animate-fade-in');
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}

// Priority tier helpers
function getPriorityBadge(tier, count) {
    const badges = {
        'tier_1': { emoji: '🔥🔥🔥', text: 'TOP PRIORITY', class: 'badge-tier-1' },
        'tier_2': { emoji: '🔥🔥', text: 'HIGH PRIORITY', class: 'badge-tier-2' },
        'tier_3': { emoji: '🔥', text: 'MEDIUM PRIORITY', class: 'badge-tier-3' },
        'tier_4': { emoji: '✓', text: 'LOW PRIORITY', class: 'badge-tier-4' }
    };
    
    const badge = badges[tier] || badges['tier_4'];
    return `<span class="${badge.class}">${badge.emoji} ${badge.text} (${count}x)</span>`;
}

// Export to PDF
function exportToPDF(subjectId) {
    window.location.href = `/reports/${subjectId}/pdf/`;
}

// Copy cluster text
function copyClusterText(element) {
    const text = element.closest('.cluster-item').querySelector('.cluster-topic').textContent;
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg text-white z-50 animate-slide-up ${
        type === 'success' ? 'bg-green-500' : 
        type === 'error' ? 'bg-red-500' : 
        'bg-blue-500'
    }`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('animate-fade-out');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Search functionality
function initSearch() {
    const searchInput = document.getElementById('cluster-search');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const clusters = document.querySelectorAll('.cluster-item');
        
        clusters.forEach(cluster => {
            const text = cluster.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                cluster.style.display = 'block';
                cluster.classList.add('animate-fade-in');
            } else {
                cluster.style.display = 'none';
            }
        });
    });
}

// Initialize search if search box exists
if (document.getElementById('cluster-search')) {
    initSearch();
}

// Smooth scroll to section
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Toggle dark mode (future enhancement)
function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
}

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.documentElement.classList.add('dark');
}
