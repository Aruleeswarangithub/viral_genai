const form = document.getElementById("generateForm");
const statusBadge = document.getElementById("statusBadge");
const jobIdText = document.getElementById("jobIdText");
const generatedText = document.getElementById("generatedText");
const enhancedPrompt = document.getElementById("enhancedPrompt");
const imageContainer = document.getElementById("imageContainer");

let poller = null;

function setStatus(status) {
    statusBadge.textContent = status;

    statusBadge.className = "badge";
    if (status === "queued") statusBadge.classList.add("text-bg-warning");
    else if (status === "processing") statusBadge.classList.add("text-bg-info");
    else if (status === "completed") statusBadge.classList.add("text-bg-success");
    else if (status === "failed") statusBadge.classList.add("text-bg-danger");
    else statusBadge.classList.add("text-bg-secondary");
}

async function pollStatus(jobId) {
    poller = setInterval(async () => {
        const res = await fetch(`/api/status/${jobId}`);
        const data = await res.json();

        setStatus(data.status || "unknown");
        generatedText.textContent = data.generated_text || "No text found";
        enhancedPrompt.textContent = data.enhanced_prompt || "No prompt found";

        if (data.status === "completed") {
            clearInterval(poller);
            imageContainer.innerHTML = `
                <img src="${data.image_url}" alt="Generated asset" class="generated-image mb-3" />
                <div class="small text-muted">Final asset URL loaded successfully.</div>
            `;
        }
    }, 2000);
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (poller) clearInterval(poller);

    imageContainer.innerHTML = `<p class="text-muted mb-0">Waiting for image generation...</p>`;
    setStatus("submitting");
    jobIdText.textContent = "";

    const payload = {
        brand_name: document.getElementById("brand_name").value,
        persona: document.getElementById("persona").value,
        platform: document.getElementById("platform").value,
        product_brief: document.getElementById("product_brief").value
    };

    const res = await fetch("/api/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    generatedText.textContent = data.generated_text || "No text generated";
    enhancedPrompt.textContent = data.enhanced_prompt || "No prompt generated";
    setStatus(data.status || "queued");
    jobIdText.textContent = `Job ID: ${data.job_id}`;

    pollStatus(data.job_id);
});
