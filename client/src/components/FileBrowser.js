import React, { useState } from "react";
import { FaFolder, FaFile } from "react-icons/fa"; // Import icons for folders and files

const FileBrowser = ({ fileStructure, onSelect, repoName }) => {
  // Initialize the state to keep track of expanded folders
  const [expandedFolders, setExpandedFolders] = useState({});

  // Handle folder toggle
  const handleToggle = (path) => {
    setExpandedFolders((prev) => ({
      ...prev,
      [path]: !prev[path],
    }));
  };

  // Render files and folders recursively
  const renderFiles = (structure, path = "") => {
    return Object.entries(structure).map(([name, content]) => {
      const currentPath = path ? `${path}/${name}` : name;
      if (content === null) {
        return (
          <div
            key={currentPath}
            onClick={() => onSelect({ path: currentPath })}
            className="cursor-pointer hover:bg-gray-700 p-2 flex items-center"
          >
            <FaFile className="mr-2" /> {name}
          </div>
        );
      } else {
        return (
          <div key={currentPath}>
            <div
              className="font-bold p-2 flex items-center cursor-pointer text-yellow-400 hover:bg-yellow-200"
              onClick={() => handleToggle(currentPath)}
            >
              <FaFolder className="mr-2" /> {name}
            </div>
            <div
              className={`ml-4 ${
                expandedFolders[currentPath] === false ? "hidden" : ""
              }`}
            >
              {renderFiles(content, currentPath)}
            </div>
          </div>
        );
      }
    });
  };

  return (
    <div className="bg-gray-800 p-4 text-white rounded-lg shadow-md">
      {/* Display the repository name */}
      {repoName && <div className="text-lg font-semibold mb-4">{repoName}</div>}
      {/* Render the file structure */}
      <div>{renderFiles(fileStructure)}</div>
    </div>
  );
};

export default FileBrowser;
