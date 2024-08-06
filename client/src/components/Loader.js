import React from "react";

const Loader = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full space-y-4">
      <div className="flex items-center justify-center space-x-2">
        <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent border-solid rounded-full animate-spin"></div>
        <span className="text-xl font-semibold text-gray-700">
          Analyzing your repository with AI ✨✨✨
        </span>
      </div>
    </div>
  );
};

export default Loader;
