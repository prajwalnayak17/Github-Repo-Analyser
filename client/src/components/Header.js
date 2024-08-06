import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCodeBranch } from "@fortawesome/free-solid-svg-icons";
import { faGithub, faGitAlt } from "@fortawesome/free-brands-svg-icons";

const Header = () => {
  return (
    <header className="bg-gray-900 text-white p-6 rounded-b-lg shadow-lg">
      <h1 className="text-center text-4xl font-extrabold mb-2">
        GitHub Rep
        <span>
          <FontAwesomeIcon icon={faGithub} className="text-red-500 text-4xl" />
        </span>
        sitory Analyzer
      </h1>
      <div className="flex justify-center space-x-4 mb-4"></div>

      <p className="text-center text-xl font-medium text-gray-300 italic">
        <span>
          {" "}
          <FontAwesomeIcon icon={faGitAlt} className="text-red-400 text-2xl" />
        </span>
        nalyze,{" "}
        <span>
          <FontAwesomeIcon
            icon={faCodeBranch}
            className="text-blue-400 text-2xl"
          />
        </span>
        mprove, and{" "}
        <span>
          {" "}
          <FontAwesomeIcon
            icon={faGitAlt}
            className="text-yellow-400 text-2xl"
          />
        </span>
        ptimize your GitHub Repositories
      </p>
    </header>
  );
};

export default Header;
