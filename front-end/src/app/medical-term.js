"use client";
import { useState } from 'react';

export default function MedicalTerm() {
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfText, setPdfText] = useState('');
  const [definitions, setDefinitions] = useState([]); // Store the definitions
  const [selectedDefinition, setSelectedDefinition] = useState(''); // To display selected word's definition

  const handleFileChange = (e) => {
    setPdfFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!pdfFile) return;

    const formData = new FormData();
    formData.append('file', pdfFile);

    const response = await fetch('http://localhost:8000/upload_pdf', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    if (response.ok) {
      setPdfText(data.pdf_text);
      setDefinitions(data.definitions); 
    } else {
      console.error(data.error);
    }
  };

  // Check if a word has a definition
  const getDefinitionForWord = (word) => {
    const term = definitions.find((def) => def.term.toLowerCase() === word.toLowerCase());
    return term ? term.definition : null;
  };

  // Handle click on a highlighted word
  const handleWordClick = (word) => {
    const definition = getDefinitionForWord(word);
    setSelectedDefinition(definition || 'No definition found');
  };

  return (
    <div className="container mx-auto min-h-screen p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">PDF Upload and Medical Term Extractor</h1>

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
              {pdfText.split(' ').map((word, index) => {
                const definition = getDefinitionForWord(word);
                return (
                  <span
                    key={index}
                    onClick={() => definition && handleWordClick(word)}
                    className={`mx-[2px] px-1 text-[14px] ${definition ? 'bg-yellow-300 rounded-sm cursor-pointer' : ''
                      }`}
                  >
                    {word}{' '}
                  </span>
                );
              })}
            </div>
          </div>
        )}
        {/* Right Side: Display Selected Word's Definition */}
        {pdfText && (
          <div className="w-[40%] p-4 border border-black rounded-md">
            <h2 className="text-xl font-semibold mb-4">Term Definition</h2>
            <div className="h-full">
              {selectedDefinition ? (
                <p>{selectedDefinition}</p>
              ) : (
                <div className='h-full flex justify-center items-center'>
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
