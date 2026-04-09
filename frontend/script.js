const BASE_URL = "http://127.0.0.1:5000";

let chart = null;

async function compileSchema() {
    const schema = document.getElementById("schema").value;
    const status = document.getElementById("compileStatus");

    status.innerText = "Compiling...";

    try {
        const res = await fetch(`${BASE_URL}/compile`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({schema: schema})
        });

        const data = await res.json();

        if (data.error) {
            status.innerText = `Error in ${data.phase} phase:\n${data.error}`;
        } else {
            document.getElementById("code").innerText = data.generated_code;
            status.innerText = "✅ Compilation successful";
        }

    } catch (err) {
        status.innerText = "❌ Backend connection failed";
    }
}

async function serializeData() {
    const status = document.getElementById("serializeStatus");
    status.innerText = "Serializing...";

    try {
        const schema = document.getElementById("schema").value;
        const fileInput = document.getElementById("jsonFile");
        const textarea = document.getElementById("jsonData");

        let jsonData = "";

        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];

            jsonData = await new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.onerror = () => reject("File read error");
                reader.readAsText(file);
            });

        } else {
            jsonData = textarea.value;
        }

        const res = await fetch(`${BASE_URL}/serialize`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                schema: schema,
                data: jsonData
            })
        });

        const data = await res.json();

        if (data.error) {
            status.innerText = `Error in ${data.phase} phase:\n${data.error}`;
        } else {
            document.getElementById("binary").innerText = data.binary_hex;

            document.getElementById("sizes").innerText =
                `JSON Size: ${data.json_size} bytes\nBinary Size: ${data.binary_size} bytes`;

            status.innerText = "✅ Serialization successful";

            // GRAPH
            const ctx = document.getElementById("sizeChart").getContext("2d");

            if (chart) chart.destroy();

            chart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: ["JSON", "Binary"],
                    datasets: [{
                        label: "Size (bytes)",
                        data: [data.json_size, data.binary_size]
                    }]
                }
            });
        }

    } catch (err) {
        status.innerText = " Something went wrong";
    }
}