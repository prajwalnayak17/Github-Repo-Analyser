import React, { useState } from "react";
import axios from "axios";
import FileBrowser from "../components/FileBrowser";
import FileContent from "../components/FileContent";
import Header from "../components/Header";
import Loader from "../components/Loader";
import FeedbackScore from "../components/FeedbackScore";

const HomePage = () => {
  const [fileStructure, setFileStructure] = useState({});
  const [selectedFileContent, setSelectedFileContent] = useState("");
  const [selectedFileName, setSelectedFileName] = useState("");
  const [selectedFilePath, setSelectedFilePath] = useState("");
  const [repoUrl, setRepoUrl] = useState("");
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [score, setScore] = useState(0);
  const [hash, setHash] = useState("");
  const [analysisDone, setAnalysisDone] = useState(false); // Track if analysis is done
  const [showFileBrowser, setShowFileBrowser] = useState(false); // Track if file browser should be shown
  const [repoName, setRepoName] = useState(""); // New state for repository name

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true); // Show loader

    // Fetch file structure from the backend
    axios
      .post("/api/repo/", { url: repoUrl, context })
      .then((response) => {
        setFileStructure(response.data.file_structure);
        setFeedback(response.data.feedback);
        setScore(response.data.score);
        setHash(response.data.last_commit_hash);
        setRepoName(repoUrl.split("/").pop().replace(".git", "")); // Set repository name
        setSelectedFileContent(""); // Clear content on new fetch
        setAnalysisDone(true); // Mark analysis as done
        setShowFileBrowser(false); // Hide file browser until "Analyze Files" is clicked
      })
      .catch((error) => {
        console.error("Error fetching file structure:", error);
      })
      .finally(() => {
        setLoading(false); // Hide loader
      });
  };

  const handleFileSelect = (file) => {
    setSelectedFilePath(file.path);
    setSelectedFileName(file.path.split("/").pop()); // Extract file name from path

    // Fetch file content from the backend
    axios
      .get(
        `api/file/${repoName}/${encodeURIComponent(
          file.path
        )}`
      )
      .then((response) => {
        setSelectedFileContent(response.data.content);
      })
      .catch((error) => {
        console.error("Error fetching file content:", error);
      });
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-900 text-white">
      <Header />
      <div className="flex-1 flex items-center justify-center p-4">
        <div
          className={`w-full max-w-3xl p-6 rounded-lg shadow-lg transition-all duration-500 ${
            analysisDone ? "border-glow" : "border-animated"
          }`}
        >
          <form onSubmit={handleSubmit} className="flex space-x-4">
            <input
              type="text"
              placeholder="GitHub Repo SSH URL"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              className="p-3 border rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 flex-grow"
              required
            />
            <input
              type="text"
              placeholder="Context (Optional)"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              className="p-3 border rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 flex-grow"
            />
            <button
              type="submit"
              className="p-3 bg-purple-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              ✨ Analyze
            </button>
          </form>
        </div>
      </div>
      {loading ? (
        <div className="flex-1 flex items-center justify-center">
          <Loader />
        </div>
      ) : analysisDone && !showFileBrowser ? (
        <div className="flex flex-col items-center justify-center p-4">
          {feedback && (
            <FeedbackScore feedback={feedback} score={score} hash={hash} />
          )}
          <button
            onClick={() => setShowFileBrowser(true)}
            className="p-3 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 mt-4"
          >
            Analyze Files
          </button>
        </div>
      ) : showFileBrowser && fileStructure ? (
        <div className="flex h-full">
          <div
            className="file-browser-container bg-gray-900 text-white max-h-screen custom-scrollbar"
            style={{ flex: "0 0 300px", overflowY: "auto" }}
          >
            <FileBrowser
              fileStructure={fileStructure}
              onSelect={handleFileSelect}
              repoName={repoName} // Pass the repoName to FileBrowser
            />
          </div>
          <div
            style={{ width: "2px", backgroundColor: "gray" }} // White line separator
          />
          <div className="flex-1 overflow-y-auto max-h-screen custom-scrollbar">
            <FileContent
              content={selectedFileContent}
              fileName={selectedFileName}
              filePath={selectedFilePath}
              context={context} // Pass context to FileContent
            />
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default HomePage;
