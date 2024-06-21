<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/6295/6295417.png" width="100" />
</p>
<p align="center">
    <h1 align="center">GITHUBCONTRI</h1>
</p>
<p align="center">
    <em>Code better, Contribute smarter with GithubContri!</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/kanav89/GithubContri?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/kanav89/GithubContri?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/kanav89/GithubContri?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/kanav89/GithubContri?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/JavaScript-F7DF1E.svg?style=flat&logo=JavaScript&logoColor=black" alt="JavaScript">
	<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=flat&logo=HTML5&logoColor=white" alt="HTML5">
	<img src="https://img.shields.io/badge/PostCSS-DD3A0A.svg?style=flat&logo=PostCSS&logoColor=white" alt="PostCSS">
	<img src="https://img.shields.io/badge/Autoprefixer-DD3735.svg?style=flat&logo=Autoprefixer&logoColor=white" alt="Autoprefixer">
	<img src="https://img.shields.io/badge/Bootstrap-7952B3.svg?style=flat&logo=Bootstrap&logoColor=white" alt="Bootstrap">
	<br>
	<img src="https://img.shields.io/badge/React-61DAFB.svg?style=flat&logo=React&logoColor=black" alt="React">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/Flask-000000.svg?style=flat&logo=Flask&logoColor=white" alt="Flask">
	<img src="https://img.shields.io/badge/JSON-000000.svg?style=flat&logo=JSON&logoColor=white" alt="JSON">
</p>
<hr>

##  Quick Links

> - [ Overview](#-overview)
> - [ Features](#-features)
> - [ Repository Structure](#-repository-structure)
> - [ Modules](#-modules)
> - [ Getting Started](#-getting-started)
>   - [ Installation](#-installation)
>   - [ Running GithubContri](#-running-GithubContri)
>   - [ Tests](#-tests)
> - [ Project Roadmap](#-project-roadmap)
> - [ Contributing](#-contributing)
> - [ License](#-license)
> - [ Acknowledgments](#-acknowledgments)

---

##  Overview

GithubContri is a project that fetches GitHub contributions data efficiently, orchestrates Flask app routing for handling API requests, and enhances user experience with dynamic elements in the frontend. The backend logic retrieves data from the GitHub API, while the React UI components facilitate OAuth login via Google, ensuring app security and enhanced performance. Testing functionalities and styling configurations with Tailwind CSS further elevate the quality and aesthetics of the project, contributing to a seamless user experience and robust functionality.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | This project has a modular architecture with a backend written in Flask to fetch GitHub contributions data. Dockerfile for containerization and front end in React with essential configurations for deployment. |
| 🔩 | **Code Quality**  | The codebase maintains good quality and style with clear separation of concerns between the backend and front end components. Consistent coding standards are followed. |
| 📄 | **Documentation** | There is extensive documentation with explanations of various components, their roles, and setup instructions. Code snippets are provided to help understand specific functionalities. |
| 🔌 | **Integrations**  | External dependencies include Flask, React libraries like react-bootstrap and react-datepicker, testing frameworks like Jest, and tools for styling like TailwindCSS and PostCSS. |
| 🧩 | **Modularity**    | The codebase is modular, enhancing reusability and maintainability. Components are well-organized and isolated, promoting easy extension and updates. |
| 🧪 | **Testing**       | Testing is done using Python for the backend and Jest for the front end. Test.py in the backend handles data manipulation and system interaction for quality control. |
| ⚡️  | **Performance**   | The project's efficiency and speed are well-maintained, ensuring optimal resource utilization. Flask backend routes API requests efficiently, and React components provide a smooth user experience. |
| 🛡️ | **Security**      | Measures for data protection and access control are not explicitly mentioned in the provided details. Proper validation and authentication protocols should be ensured for secure operation. |
| 📦 | **Dependencies**  | Key dependencies include Flask, React libraries, testing frameworks like Jest, and styling tools like TailwindCSS and PostCSS. The listed dependencies are crucial for project functionality. |


---

##  Repository Structure

```sh
└── GithubContri/
    ├── LICENSE
    ├── README.md
    └── githubapi
        ├── .vscode
        │   └── settings.json
        ├── backend
        │   ├── Dockerfile
        │   ├── main-Flask.py
        │   ├── main.py
        │   ├── requirements.txt
        │   └── test.py
        └── ui
            └── my-app
                ├── .gitignore
                ├── README.md
                ├── package-lock.json
                ├── package.json
                ├── postcss.config.js
                ├── public
                │   ├── favicon.ico
                │   ├── index.html
                │   ├── logo192.png
                │   ├── logo512.png
                │   ├── manifest.json
                │   └── robots.txt
                ├── src
                │   ├── App.css
                │   ├── App.js
                │   ├── App.test.js
                │   ├── gi.png
                │   ├── index.css
                │   ├── index.js
                │   ├── logo.svg
                │   ├── reportWebVitals.js
                │   └── setupTests.js
                └── tailwind.config.js
```

---

##  Modules

<details closed><summary>githubapi.backend</summary>

| File                                                                                                       | Summary                                                                                                                                                                                                                        |
| ---                                                                                                        | ---                                                                                                                                                                                                                            |
| [main.py](https://github.com/kanav89/GithubContri/blob/master/githubapi/backend/main.py)                   | Code Summary:** Fetching GitHub contributions data. **Architecture Role:** Backend logic for data retrieval.                                                                                                                   |
| [Dockerfile](https://github.com/kanav89/GithubContri/blob/master/githubapi/backend/Dockerfile)             | Dockerfile in githubapi/backend achieves containerizing Python Flask app for GitHubContri project, with essential configurations for deployment.**                                                                             |
| [main-Flask.py](https://github.com/kanav89/GithubContri/blob/master/githubapi/backend/main-Flask.py)       | Code Snippet Summary:**File `main-Flask.py` in `backend` orchestrates Flask app routing in GithubContri repo's architecture, crucial for handling API requests efficiently.                                                    |
| [requirements.txt](https://github.com/kanav89/GithubContri/blob/master/githubapi/backend/requirements.txt) | Code Summary:**`githubapi/backend/requirements.txt` manages dependencies for the Flask backend. Includes Flask, requests, datetime, argparse, and flask_restful for API functionality in the parent repository's architecture. |
| [test.py](https://github.com/kanav89/GithubContri/blob/master/githubapi/backend/test.py)                   | Code Summary:** **../githubapi/backend/test.py** utilizes Python for testing functionalities in the backend. It handles data manipulation and system interaction, enhancing quality control in the repository.                 |

</details>

<details closed><summary>githubapi.ui.my-app</summary>

| File                                                                                                             | Summary                                                                                                                                                                                                                             |
| ---                                                                                                              | ---                                                                                                                                                                                                                                 |
| [postcss.config.js](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/postcss.config.js)   | Code Summary:**`postcss.config.js` in `ui/my-app` utilizes plugins for tailwindCSS and autoprefixer to enhance styling in the UI components of the GithubContri repository.                                                         |
| [package.json](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/package.json)             | Code Summary**: `package.json` configures a React app, sets dependencies, scripts, and webpack options. Facilitates React app development with specified libraries and build processes within the GithubContri UI structure.        |
| [tailwind.config.js](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/tailwind.config.js) | Code Summary:**`tailwind.config.js` configures Tailwind CSS for React app styling. Specifies content sources and includes a custom plugin for enhanced styling features within the UI component.                                    |
| [package-lock.json](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/package-lock.json)   | Code snippet: main.pySummary: Implements core backend logic for handling API requests in the GithubContri repository. Manages communication with the GitHub API and processes user data. Key component of the backend architecture. |

</details>

<details closed><summary>githubapi.ui.my-app.public</summary>

| File                                                                                                          | Summary                                                                                                                                                                                             |
| ---                                                                                                           | ---                                                                                                                                                                                                 |
| [index.html](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/public/index.html)       | Code in githubapi/ui/my-app/public/index.html gives the root HTML structure for GitContri UI, defining metadata, resources, and build process instructions within the main repository architecture. |
| [manifest.json](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/public/manifest.json) | Code Summary** `manifest.json` configures a standalone React app's display, theme, and icons for GitHubContri's UI in the `githubapi` repository.                                                   |
| [robots.txt](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/public/robots.txt)       | Code snippet in robots.txt establishes crawling instructions for search engines in the parent repo's UI section.                                                                                    |

</details>

<details closed><summary>githubapi.ui.my-app.src</summary>

| File                                                                                                                 | Summary                                                                                                                                                                                                                                                    |
| ---                                                                                                                  | ---                                                                                                                                                                                                                                                        |
| [reportWebVitals.js](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/src/reportWebVitals.js) | Code Summary:** `reportWebVitals.js` monitors Core Web Vitals performance metrics in the UI app. The module imports `web-vitals` to retrieve and track metrics. It contributes to enhancing user experience and performance monitoring in the application. |
| [App.test.js](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/src/App.test.js)               | Code snippet in githubapi/ui/my-app/src/App.test.js verifies React app renders learn react link. Ensures expected UI element presence through automated testing. Integrates testing into React app development workflow.                                   |
| [setupTests.js](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/src/setupTests.js)           | Code Summary:**`setupTests.js` in `my-app/src` enhances Jest testing for DOM elements. It enables custom matchers like `toHaveTextContent`. More robust test assertions.                                                                                   |
| [App.js](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/src/App.js)                         | App.js in githubapi/ui/my-app/src:** Manages React UI components and OAuth login via Google. Enhances user experience with dynamic elements. Substantial for frontend functionality in the parent repository's architecture.                               |
| [App.css](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/src/App.css)                       | Summary: CSS file in githubapi/ui/my-app/src. Defines styling for React app components like full-page layout, buttons, headers. Enhances UI aesthetics and layout structure with Tailwind CSS.                                                             |
| [index.js](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/src/index.js)                     | Code snippet in githubapi/ui/my-app/src/index.js sets up Google OAuth provider for React app, rendering the main component. Enhances app security and user experience by enabling Google authentication.                                                   |
| [index.css](https://github.com/kanav89/GithubContri/blob/master/githubapi/ui/my-app/src/index.css)                   | Code Summary:** **Role:** Styling configuration for UI. **Features:** Define Tailwind CSS styles. **Impact:** Ensures consistent UI design.                                                                                                                |

</details>

---

##  Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **JavaScript**: `version x.y.z`

###  Installation

1. Clone the GithubContri repository:

```sh
git clone https://github.com/kanav89/GithubContri
```

2. Change to the project directory:

```sh
cd GithubContri
```

3. Install the dependencies:

```sh
npm install
```

###  Running GithubContri

Use the following command to run GithubContri:

```sh
node app.js
```

###  Tests

To execute tests, run:

```sh
npm test
```

---

##  Project Roadmap

- [X] `► INSERT-TASK-1`
- [ ] `► INSERT-TASK-2`
- [ ] `► ...`

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/kanav89/GithubContri/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/kanav89/GithubContri/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/kanav89/GithubContri/issues)**: Submit bugs found or log feature requests for Githubcontri.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone https://github.com/kanav89/GithubContri
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-quick-links)

---
