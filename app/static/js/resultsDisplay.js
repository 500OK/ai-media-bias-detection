class ResultsDisplay {
    constructor() {
        this.resultsDiv = document.getElementById('results');
        this.contentDiv = document.getElementById('resultsContent');
        this.biasColors = [
            'bg-red-400', 'bg-blue-400', 'bg-green-400',
            'bg-yellow-400', 'bg-purple-400', 'bg-pink-400',
            'bg-indigo-400', 'bg-teal-400', 'bg-orange-400'
        ];
    }

    displayResults(data) {
        console.log('[DEBUG] Received data:', data);

        // Clear previous results
        this.contentDiv.innerHTML = '';

        // Handle extracted text
        if (data.extracted_text) {
            console.log('[DEBUG] Displaying extracted text');
            const textContainer = document.createElement('div');
            textContainer.className = 'mb-8 p-6 bg-white rounded-lg shadow-sm';
            textContainer.innerHTML = `
                <h3 class="text-lg font-semibold mb-4">Extracted Text</h3>
                <div class="text-gray-700 whitespace-pre-line">${data.extracted_text}</div>
            `;
            this.contentDiv.appendChild(textContainer);
        }

        // Handle analysis results
        const results = data.analysis?.results || [];
        console.log(`[DEBUG] Found ${results.length} bias results`);

        if (results.length === 0) {
            console.log('[DEBUG] No biases detected');
            this.contentDiv.innerHTML += `
                <div class="p-4 bg-green-100 border border-green-400 text-green-700 rounded">
                    No significant biases detected
                </div>`;
            return;
        }

        // Create distribution container
        console.log('[DEBUG] Creating bias analysis container');
        const distributionContainer = document.createElement('div');
        distributionContainer.className = 'mb-8 p-6 bg-white rounded-lg shadow-sm';
        distributionContainer.innerHTML = `
            <h3 class="text-lg font-semibold mb-4">Bias Analysis</h3>
            <div class="w-full h-4 bg-gray-200 rounded-full overflow-hidden mb-4">
                <div class="flex h-full" id="distributionBar"></div>
            </div>
            <div class="grid grid-cols-1 gap-4" id="distributionList"></div>
        `;
        this.contentDiv.appendChild(distributionContainer);

        // Create distribution bar segments
        console.log('[DEBUG] Creating distribution bar');
        const distributionBar = document.getElementById('distributionBar');
        results.forEach((result, index) => {
            console.log(`[DEBUG] Adding bar segment for ${result.bias_name} (${result.percentage}%)`);
            const barSegment = document.createElement('div');
            barSegment.className = `h-full ${this.biasColors[index % this.biasColors.length]}`;
            barSegment.style.width = `${result.percentage}%`;
            distributionBar.appendChild(barSegment);
        });

        // Display distribution percentages with descriptions
        console.log('[DEBUG] Creating bias list items');
        const distributionList = document.getElementById('distributionList');
        results.forEach((result, index) => {
            console.log(`[DEBUG] Adding list item for ${result.bias_name}`);
            const item = document.createElement('div');
            item.className = 'bg-gray-50 rounded-lg';
            item.innerHTML = `
                <div class="flex justify-between items-center p-3">
                    <div class="flex items-center gap-2">
                        <div class="w-3 h-3 rounded-full ${this.biasColors[index % this.biasColors.length]}"></div>
                        <span class="font-medium">${result.bias_name}</span>
                    </div>
                    <span class="font-bold ${this.getPercentageColor(result.percentage)}">${result.percentage}%</span>
                </div>
                <div class="px-3 pb-3 pl-8">
                    <p class="text-sm text-gray-600">${result.description}</p>
                </div>
            `;
            distributionList.appendChild(item);
        });

        console.log('[DEBUG] Results display completed');
    }

    getPercentageColor(percentage) {
        if (percentage >= 70) return 'text-red-600';
        if (percentage >= 50) return 'text-orange-600';
        return 'text-green-600';
    }

    clearResults() {
        this.contentDiv.innerHTML = '';
        this.resultsDiv.classList.add('hidden');
    }

    showLoading() {
        this.clearResults();
        this.resultsDiv.classList.remove('hidden');
        this.contentDiv.innerHTML = `
            <div class="flex justify-center items-center h-32">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
            </div>`;
    }

    displayError(message) {
        this.clearResults();
        this.resultsDiv.classList.remove('hidden');
        this.contentDiv.innerHTML = `
            <div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                ${message}
            </div>`;
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ResultsDisplay;
} 