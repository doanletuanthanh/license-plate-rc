const video = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const results = document.getElementById('results');

// Webcam setup
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => video.srcObject = stream)
  .catch(err => console.error("Webcam error:", err));

// Capture from webcam and send to FastAPI
document.getElementById("captureBtn").addEventListener("click", () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(blob => {
    const formData = new FormData();
    formData.append("file", blob, "frame.jpg");
    fetch('/recognize/', {
      method: "POST",
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      results.innerText = JSON.stringify(data, null, 2);
    });
  }, 'image/jpeg');
});

// Image upload form
document.getElementById("uploadForm").addEventListener("submit", e => {
  e.preventDefault();
  const formData = new FormData(e.target);
  fetch('/recognize/', {
    method: "POST",
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    results.innerText = JSON.stringify(data, null, 2);
  });
});
