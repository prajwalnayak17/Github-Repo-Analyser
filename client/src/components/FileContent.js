import React, { useState, useEffect } from "react";
import axios from "axios";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { twilight } from "react-syntax-highlighter/dist/esm/styles/prism";

const FileContent = ({ content, fileName, filePath }) => {
  const [analysisResult, setAnalysisResult] = useState({});
  const [loading, setLoading] = useState(false);
  const [expandedComments, setExpandedComments] = useState({});

  // Reset analysis data when a new file is selected
  useEffect(() => {
    setAnalysisResult({});
    setExpandedComments({});
  }, [fileName, filePath]);

  const handleAnalyze = () => {
    setLoading(true); // Show loading state

    axios
      .post("/api/analyze-file/", {
        fileName,
        filePath,
        content,
      })
      .then((response) => {
        setAnalysisResult(response.data.analysis); // Update with actual field from response
      })
      .catch((error) => {
        console.error("Error analyzing file:", error);
        setAnalysisResult({ error: "Error analyzing file." });
      })
      .finally(() => {
        setLoading(false); // Hide loading state
      });
  };

  const toggleComment = (lineNumber) => {
    setExpandedComments((prev) => ({
      ...prev,
      [lineNumber]: !prev[lineNumber],
    }));
  };

  const renderComments = () => {
    const comments = [];

    Object.keys(analysisResult).forEach((key) => {
      const lineRange = key.split("-").map((num) => parseInt(num, 10));
      let startLine = lineRange[0];
      let endLine = "";
      if (lineRange[2]) {
        startLine = lineRange[1];
        endLine = lineRange[2];
        comments.push({ startLine, endLine, comment: analysisResult[key] });
      } else {
        endLine = lineRange[1] || startLine;
        comments.push({ startLine, endLine, comment: analysisResult[key] });
      }
    });

    comments.sort((a, b) => a.startLine - b.startLine);

    return comments.map(({ startLine, endLine, comment }) => {
      const isExpanded = expandedComments[startLine];
      const displayComment = isExpanded || comment.length <= 100;

      return (
        <div key={startLine} className="mb-2">
          <div className="font-bold text-yellow-300 text-lg">
            {startLine === endLine
              ? `Line ${startLine}:`
              : `Lines ${startLine} - ${endLine}:`}
          </div>
          <div
            className="text-base cursor-pointer"
            style={{ maxWidth: "300px", overflow: "hidden" }}
            onClick={() => toggleComment(startLine)}
          >
            {displayComment ? comment : comment.substring(0, 100) + "..."}
          </div>
        </div>
      );
    });
  };

  return (
    <div className="p-4">
      <div className="flex items-center mb-4">
        <h2 className="text-xl font-bold mr-2">{fileName}</h2>
        <button
          onClick={handleAnalyze}
          className="flex items-center p-2 bg-violet-500 text-white rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
          disabled={loading}
        >
          <span
            className="mr-2 text-yellow-300"
            role="img"
            aria-label="twinkle"
          >
            ✨
          </span>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      <div className="mb-4 text-gray-500">
        <strong>Path:</strong> {filePath}
      </div>
      <div className="flex">
        <div className="flex-1 max-w-3xl rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <SyntaxHighlighter
              language="javascript" // or "python" or any language you need
              style={twilight}
              customStyle={{ margin: 0, padding: 0, borderRadius: "4px" }}
              showLineNumbers={true} // Enable line numbers
              lineNumberStyle={{ color: "#888", paddingRight: "10px" }} // Style for line numbers
            >
              {content}
            </SyntaxHighlighter>
          </div>
        </div>
        <div className="ml-4 w-1/3 bg-gray-700 p-4 rounded-lg overflow-y-auto">
          <h3 className="text-2xl font-bold mb-2 text-purple-300">Analysis</h3>
          <div>{renderComments()}</div>
        </div>
      </div>
    </div>
  );
};

export default FileContent;
