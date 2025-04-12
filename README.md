# Niagara Package Installer (npi)

**Niagara Package Installer** (npi) is a lightweight, developer-friendly CLI tool that helps you easily install and manage Niagara Framework software packages from custom repositories or Git sources.

---

## 🚀 Features

- Install Niagara packages in one command
- Simplifies package management workflows
- Designed to be bootstrap-friendly with minimal setup

---

## 📦 Installation

### 🔧 Prerequisites

Make sure you have the following installed:

- [PowerShell 7 (pwsh7)](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell)
- [Git](https://git-scm.com/downloads)
- [uv (by astral-sh)](https://astral.sh/blog/uv-the-python-pkg-manager/)

Install `uv` and `git` using `winget`:

```pwsh
winget install astral-sh.uv git.git
```

### 🧰 Installing `npi`

Use `uv` to install the tool from Git:

```pwsh
uv tool install git+https://<your_repo_url>
```

After installing the tool, run the following command to add `uv` tools to your PATH:

```pwsh
uv tool update-shell
```

> **Note:** Then **restart your shell** to apply the changes.

Once installed and the shell is restarted, `npi` should be available in your terminal.

---

## 🔧 Basic Usage

### Install a package

```pwsh
npi install vykonPro
```

---

## 📖 Commands (More Coming Soon)

- `npi install <package>` — Installs the specified Niagara package
- `npi list` — Lists available packages (future feature)
- `npi search <keyword>` — Searches for a package (future feature)

---

## 🛠 Example Workflow

```pwsh
# Install Niagara Pro package
npi install vykonPro

# (future)
npi search bacnet
npi list
```

---

## ❓FAQ

**Q: Does this replace Workbench?**  
A: No, it's a tool to streamline installation and management workflows, especially helpful for headless or scripted environments.

**Q: Is `uv` required?**  
A: Yes, it's used for bootstrapping and dependency management.

---

## 📌 License
MIT License. See `LICENSE` file for details.

---

## 👷‍♂️ Contributing
Want to help improve `npi`? PRs and issues welcome!

---

## 🔗 Links

- UV Documentation: https://astral.sh/blog/uv-the-python-pkg-manager/
- Niagara Framework (Tridium): https://www.tridium.com/

---

Crafted with ❤️ for building smarter automation tools.
