"use client";
import { useState } from "react";

export default function MedicalTerm() {
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfText, setPdfText] = useState("");
  const [definitions, setDefinitions] = useState({});
  const [selectedDefinition, setSelectedDefinition] = useState("");
  const [selectedWord, setSelectedWord] = useState("");
  const [selectedTerm, setSelectedTerm] = useState("");
  const [selectedImage, setSelectedImage] = useState(null);
  const [isWordHasImage, setIsWordHasImage] = useState(false);
  const [language, setLanguage] = useState("en");

  const handleFileChange = (e) => {
    setPdfFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!pdfFile) return;

    const formData = new FormData();
    formData.append("file", pdfFile);

    const response = await fetch("http://127.0.0.1:8000/api/v1/upload_pdf/", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (response.ok) {
      setPdfText(data.pdf_text);

      const highlightedWords = data.highlighted_words.reduce((acc, wordObj) => {
        acc[wordObj.term] = { hasImage: wordObj.has_image };
        return acc;
      }, {});
      setDefinitions(highlightedWords);
    } else {
      console.error(data.error);
    }
  };

  const fetchDefinition = async (word, language = "en") => {
    setSelectedWord(word);
    const response = await fetch(
      `http://127.0.0.1:8000/api/v1/get_definition/${word}?language=${language}`
    );
    const data = await response.json();
    if (response.ok) {
      setSelectedTerm(data.term);
      setDefinitions((prev) => ({
        ...prev,
        [word]: { ...prev[word], definition: data.definition },
      }));
      setSelectedDefinition(data.definition);

      const imageExtensions = ["jpg", "jpeg", "png", "gif"];
      let imagePath = null;
      for (const ext of imageExtensions) {
        try {
          const imageResponse = await fetch(`/${data.image}.${ext}`, {
            method: "HEAD",
          });
          if (imageResponse.ok) {
            imagePath = `/${data.image}.${ext}`;
            break;
          }
        } catch (error) {
          console.error(`Error fetching image with extension ${ext}:`, error);
        }
      }
      setSelectedImage(imagePath);
    } else {
      console.error(data.error);
    }
  };

  const handleWordClick = (word) => {
    if (definitions.hasOwnProperty(word)) {
      fetchDefinition(word, language);

      const hasImage = definitions[word]?.hasImage;
      setIsWordHasImage(hasImage || false);
    }
  };

  const handleLanguageChange = (e) => {
    const selectedLanguage = e.target.value;
    setLanguage(selectedLanguage);

    // Fetch the definition again if a term is selected
    if (selectedWord) {
      fetchDefinition(selectedWord, selectedLanguage);
    }
  };

  const getHighlightedText = (text, highlightedWords) => {
    const sortedWords = Object.keys(highlightedWords).sort(
      (a, b) => b.length - a.length
    );
    let highlightedText = text;

    sortedWords.forEach((word) => {
      const escapedWord = word.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
      const regex = new RegExp(`(?<!###)\\b${escapedWord}\\b(?!###)`, "gi");
      highlightedText = highlightedText.replace(regex, `###${word}###`);
    });

    return highlightedText.split(/(###.*?###)/g).map((part, index) => {
      if (part.startsWith("###") && part.endsWith("###")) {
        const word = part.slice(3, -3);
        const hasImage = highlightedWords[word]?.hasImage;
        const highlightColor = hasImage ? "bg-blue-300" : "bg-yellow-300";

        return (
          <span
            key={index}
            onClick={() => handleWordClick(word)}
            className={`mx-[2px] px-1 text-[14px] ${highlightColor} rounded-sm cursor-pointer`}
          >
            {word}{" "}
          </span>
        );
      } else {
        return <span key={index}>{part}</span>;
      }
    });
  };

  return (
    <div className="container mx-auto min-h-screen p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">
        PDF Upload and Medical Term Extractor
      </h1>

      {/* Upload Section */}
      <div className="flex justify-center mb-4">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="border border-gray-300 p-1 text-[14px] rounded"
        />
        <button
          className="bg-blue-500 text-white px-4 text-[14px] ml-2 rounded hover:bg-blue-700"
          onClick={handleUpload}
        >
          Upload PDF
        </button>
      </div>

      {/* Main Content: Left for PDF Text, Right for Definitions */}
      <div className="flex space-x-4">
        {/* Left Side: PDF Text Content */}
        {pdfText && (
          <div className="w-[60%] p-4 overflow-auto border border-black rounded-md">
            <div className="whitespace-pre-wrap">
              {getHighlightedText(pdfText, definitions)}
            </div>
          </div>
        )}
        {/* Right Side: Display Selected Word's Definition and Image */}
        {pdfText && (
          <div className="w-[40%] p-4 border border-black rounded-md">
            {language !== 'en' && <p className="text-[13px] font-semibold mb-3">
              {selectedWord ? selectedWord.charAt(0).toUpperCase() + selectedWord.slice(1) : ''}
            </p>}
            <h2 className="text-xl font-semibold mb-4">
              {selectedTerm ? selectedTerm.charAt(0).toUpperCase() + selectedTerm.slice(1) : ''}
            </h2>
            <div className="h-full">
              {selectedDefinition ? (
                <>
                  <p>{selectedDefinition}</p>
                  {selectedImage !== null && (
                    <div className="mt-4">
                      <img
                        src={selectedImage}
                        alt="Term illustration"
                        className="w-[100%] h-[400px] object-contain border rounded-md"
                      />
                    </div>
                  )}
                  {/* Language Selection */}
                  <div className="flex justify-start mt-4">
                    <label className="mr-2 text-[14px]">Select Language:</label>
                    <select
                      value={language}
                      onChange={handleLanguageChange}
                      className="border border-gray-300 p-1 text-[14px] rounded"
                    >
                      <option value="en">English</option>
                      <option value="ta">Tamil</option>
                      <option value="hi">Hindi</option>
                      <option value="ml">Malayalam</option>
                      <option value="te">Telugu</option>
                      {/* <option value="kn">Kannada</option> */}
                    </select>
                  </div>
                </>
              ) : (
                <div className="h-full flex justify-center items-center">
                  <p>Select a highlighted word to see its definition.</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
