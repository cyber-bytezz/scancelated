"use client";
import { useState, useRef } from "react";

export default function TextRecognitionCamera() {
  const [extractedText, setExtractedText] = useState("");
  const [loading, setLoading] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [cameraOn, setCameraOn] = useState(false);
  const [captured, setCaptured] = useState(false);

  // Turn on the camera
  const startCamera = async () => {
    setCameraOn(true);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    } catch (error) {
      console.error("Error accessing camera:", error);
    }
  };

  // Capture the image from the video stream
  const captureImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    const context = canvas.getContext("2d");

    // Ensure the video stream is loaded
    if (video.videoWidth && video.videoHeight) {
      // Set canvas dimensions to match the video feed
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      // Draw the current frame of the video onto the canvas
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      console.log("captured!")
      setCaptured(true); // Mark the image as captured
    } else {
      console.error("Video stream not ready yet.");
    }
  };

  // Handle form submission to upload the captured image
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!captured) {
      alert("Please capture an image first!");
      return;
    }

    const canvas = canvasRef.current;

    // Convert canvas to Blob to send as a file
    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append("file", blob, "captured-image.png");

      setLoading(true);

      try {
        const response = await fetch("http://localhost:8000/upload/", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        setExtractedText(data.extracted_text);
      } catch (error) {
        console.error("Error uploading file:", error);
      } finally {
        setLoading(false);
      }
    });
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-lg">
        <h2 className="text-center text-3xl font-extrabold text-gray-900">Capture Image for OCR</h2>
        <p className="text-center text-sm text-gray-600">Take a picture and extract text using OCR.</p>

        <div className="mt-4 flex flex-col items-center space-y-4">
          {cameraOn ? (
            <>
              <video ref={videoRef} autoPlay className="w-full h-auto rounded-md" />
              <button
                className="mt-2 px-4 py-2 bg-indigo-600 text-white rounded-md"
                onClick={captureImage}
              >
                Capture Image
              </button>
              <canvas ref={canvasRef} className="hidden" />
            </>
          ) : (
            <button
              className="px-4 py-2 bg-indigo-600 text-white rounded-md"
              onClick={startCamera}
            >
              Start Camera
            </button>
          )}

          <form className="mt-4 space-y-6" onSubmit={handleSubmit}>
            <button
              type="submit"
              className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md"
            >
              {loading ? "Processing..." : "Upload & Recognize"}
            </button>
          </form>

          {extractedText && (
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-900">Extracted Text:</h3>
              <div className="bg-gray-100 rounded-md p-4 mt-2 text-sm text-gray-700">
                <pre className="whitespace-pre-wrap">{extractedText}</pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
