import { useState } from "react";
import FooterNav from "../components/FooterNav";
import { FilePreviewSuccess, FilePreviewError } from "../components/FilePreview";
import { ToastSuccess, ToastError } from "../components/Toast";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [toast, setToast] = useState(null);
  const [error, setError] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    if (
      !selectedFile.name.endsWith(".tf") &&
      !selectedFile.name.endsWith(".json")
    ) {
      setError(true);
      setToast("error");
      return;
    }

    setFile(selectedFile);
    setError(false);
    setToast("success");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100 flex flex-col">

      {/* 🔹 HEADER */}
      <header className="bg-white shadow-sm px-8 py-5 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-indigo-600">CloudScan</h1>
          <p className="text-sm text-gray-500">
            AI-Powered Cloud Misconfiguration Analyzer
          </p>
        </div>
        <span className="material-symbols-outlined text-indigo-500 text-3xl">
          security
        </span>
      </header>

      {/* 🔹 MAIN CONTENT */}
      <main className="flex-grow flex items-center justify-center px-4">
        <div className="max-w-2xl w-full bg-white rounded-2xl shadow-xl p-10">

          {/* Title */}
          <h2 className="text-3xl font-semibold text-gray-800 mb-2">
            Upload Configuration
          </h2>
          <p className="text-gray-500 mb-8">
            Upload Terraform or JSON configuration files to scan for
            privacy and security misconfigurations.
          </p>

          {/* Upload Box */}
          <label
            htmlFor="fileUpload"
            className="flex flex-col items-center justify-center border-2 border-dashed border-indigo-300 rounded-xl p-10 cursor-pointer hover:border-indigo-500 hover:bg-indigo-50 transition-all duration-300"
          >
            <span className="material-symbols-outlined text-6xl text-indigo-400 mb-4">
              cloud_upload
            </span>
            <p className="font-medium text-gray-700">
              Click to upload or drag & drop
            </p>
            <p className="text-sm text-gray-500 mt-1">
              Supported: .tf, .json
            </p>

            <input
              id="fileUpload"
              type="file"
              className="hidden"
              onChange={handleFileChange}
            />
          </label>

          {/* File Preview */}
          <div className="mt-6">
            {file && !error && <FilePreviewSuccess />}
            {error && <FilePreviewError />}
          </div>

          {/* Scan Button */}
          <button
            className="mt-8 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl transition transform hover:scale-105 hover:shadow-lg"
          >
            Scan Configuration
          </button>
        </div>
      </main>

      {/* Toast */}
      {toast === "success" && <ToastSuccess />}
      {toast === "error" && <ToastError />}

      {/* Footer */}
      <FooterNav />
    </div>
  );
}
