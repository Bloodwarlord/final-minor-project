// 













const video = document.getElementById("video");
const prediction = document.getElementById("prediction");
const confidence = document.getElementById("confidence");
let isCapturing = false;
let captureInterval;

// Access the device camera and stream to the video element
if (video) {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      video.srcObject = stream;
    })
    .catch((error) => console.error("Error accessing the webcam:", error));
} else {
  console.error("Video element not found.");
}

// Function to start capturing frames
function startCapturing() {
  if (isCapturing) return; // Prevent multiple intervals
  isCapturing = true;
  captureInterval = setInterval(captureAndSendFrame, 200); // Capture every 200ms (adjust as needed)
}

// Function to stop capturing frames
function stopCapturing() {
  isCapturing = false;
  clearInterval(captureInterval);
}

// Function to capture a frame and send it to the backend
function captureAndSendFrame() {
  if (video && video.srcObject) {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      const formData = new FormData();
      formData.append("image", blob, "frame.jpg");

      fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (prediction && confidence) {
            prediction.innerText = `Prediction: ${data.prediction}`;
            confidence.innerText = `Confidence: ${data.confidence.toFixed(2)}`;
          }
        })
        .catch((error) => console.log("Error:", error));
    });
  } else {
    console.error("Cannot capture image: video stream not available.");
  }
}

// Attach start and stop functions to buttons
document.getElementById("captureButton").addEventListener("click", startCapturing);
document.getElementById("stopButton").addEventListener("click", stopCapturing);
