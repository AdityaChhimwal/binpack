// Pre-defined schemas for the dropdown
const presets = {
    player: `struct Player {\n    int health;\n    string[20] name;\n    int score;\n}`,
    exam: `struct Exam {\n    string[30] student_name;\n    int roll_number;\n    int total_marks;\n    string[10] student_id;\n}`
};

// DOM Elements
const schemaInput = document.getElementById('schema-input');
const presetSelect = document.getElementById('schema-presets');
const generateBtn = document.getElementById('btn-generate');
const dynamicForm = document.getElementById('dynamic-form');

// Set initial value
schemaInput.value = presets.player;

// Handle dropdown changes
presetSelect.addEventListener('change', (e) => {
    schemaInput.value = presets[e.target.value];
});

// A mini-parser specifically for the browser demo
function parseSchemaForDemo(text) {
    const fields = [];
    // This regex looks for: (int or string) (optional [size]) (name) ;
    const regex = /(int|string)(?:\[(\d+)\])?\s+([a-zA-Z_]\w*)\s*;/g;
    let match;
    
    while ((match = regex.exec(text)) !== null) {
        fields.push({
            type: match[1],
            length: match[2] ? parseInt(match[2]) : 4, // Ints are 4 bytes
            name: match[3]
        });
    }
    return fields;
}

// Generate the UI
generateBtn.addEventListener('click', () => {
    const fields = parseSchemaForDemo(schemaInput.value);
    
    if (fields.length === 0) {
        dynamicForm.innerHTML = '<p style="color:red;">Could not parse schema. Check syntax!</p>';
        return;
    }

    // Build the form HTML
    dynamicForm.innerHTML = '';
    fields.forEach(field => {
        const div = document.createElement('div');
        div.className = 'form-group';
        
        const label = document.createElement('label');
        label.innerText = `${field.name} (${field.type}${field.type === 'string' ? `[${field.length}]` : ''})`;
        
        const input = document.createElement('input');
        input.type = field.type === 'int' ? 'number' : 'text';
        input.id = `input-${field.name}`;
        input.dataset.name = field.name; // Save metadata on the element
        input.dataset.type = field.type;
        input.dataset.length = field.length;
        
        // Every time the user types, recalculate the sizes
        input.addEventListener('input', calculateSizes);
        
        div.appendChild(label);
        div.appendChild(input);
        dynamicForm.appendChild(div);
    });

    calculateSizes(); // Initial calculation
});

// The Core Math Logic
function calculateSizes() {
    const inputs = dynamicForm.querySelectorAll('input');
    if (inputs.length === 0) return;

    let jsonData = {};
    let binSize = 0;

    inputs.forEach(input => {
        // 1. Build JSON Object
        let val = input.value;
        if (input.dataset.type === 'int') {
            val = parseInt(val) || 0; 
        }
        jsonData[input.dataset.name] = val;

        // 2. Calculate BinPack size (It's strictly fixed based on schema!)
        binSize += parseInt(input.dataset.length); 
    });

    // Calculate JSON size by turning the object into a string and measuring it
    const jsonString = JSON.stringify(jsonData);
    const jsonSize = new Blob([jsonString]).size; // Gets exact byte size

    updateGraph(jsonSize, binSize);
}

// Update the visuals
function updateGraph(jsonSize, binSize) {
    document.getElementById('json-bytes').innerText = jsonSize;
    document.getElementById('bin-bytes').innerText = binSize;

    // Calculate percentages for the CSS width (make JSON the 100% baseline)
    const max = Math.max(jsonSize, binSize, 1); // Avoid division by zero
    
    document.getElementById('bar-json').style.width = `${(jsonSize / max) * 100}%`;
    document.getElementById('bar-bin').style.width = `${(binSize / max) * 100}%`;

    // Calculate Savings
    const savings = ((jsonSize - binSize) / jsonSize) * 100;
    const savingsText = document.getElementById('savings-text');
    
    if (savings > 0) {
        savingsText.innerText = `Bandwidth Saved: ${savings.toFixed(1)}%!`;
        savingsText.style.color = '#28a745';
    } else {
        savingsText.innerText = `JSON is smaller here! (Type more data)`;
        savingsText.style.color = '#dc3545';
    }
}