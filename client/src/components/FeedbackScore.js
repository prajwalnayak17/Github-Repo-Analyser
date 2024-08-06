import React from "react";

const FeedbackScore = ({ feedback, score, hash }) => {
  // Determine the color class based on the score
  const getScoreColorClass = (score) => {
    if (score < 5) {
      return "bg-red-500 text-white";
    } else if (score >= 5 && score < 8) {
      return "bg-yellow-500 text-black";
    } else {
      return "bg-green-500 text-white";
    }
  };

  const scoreColorClass = getScoreColorClass(score);

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-900">
      <div className="max-w-3xl w-full p-6 bg-gray-800 rounded-lg shadow-lg">
        <h1 className="text-4xl font-bold mb-4 text-blue-400">Analysis</h1>
        <div className="mb-4 text-lg">
          <strong> Based on latest commit:</strong>{" "}
          <span className="text-blue-300"> #{hash}</span>
        </div>
        <div className="mb-4">
          <strong className="text-lg">Score:</strong>{" "}
          <span className={`inline-block p-2 rounded font-bold text-xl ${scoreColorClass}`}>
            {score}
          </span>
        </div>
        <div>
          <strong className="text-2xl text-blue-400">Feedback:</strong> <br />
          <br />
          <pre className="whitespace-pre-wrap text-lg text-gray-300">
            {feedback}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default FeedbackScore;
