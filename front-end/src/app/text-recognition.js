"use client";
import { useState } from "react";

export default function TextRecognition() {
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a file to upload");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

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
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-[50%] w-full space-y-8 bg-white p-8 rounded-lg shadow-lg">
        <h2 className="text-center text-3xl font-extrabold text-gray-900">Upload Image for OCR</h2>
        <p className="text-center text-sm text-gray-600">Upload an image file to extract text using OCR.</p>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="file-upload" className="block text-sm font-medium text-gray-700">
                Choose File
              </label>
              <input
                id="file-upload"
                name="file"
                type="file"
                accept="image/*,.pdf"
                onChange={handleFileChange}
                className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {loading ? "Processing..." : "Upload"}
            </button>
          </div>
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
  );
}
