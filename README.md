# Simple CRUD FastAPI Application
### Author: GiZano

## 🖊️ Summary 

<ol>
    <li><a href="#desc">Description</a></li>
    <li><a href="#container">Containerization</a></li>
    <li><a href="#api">API</a></li>
    <li><a href="#quickS">QuickStart</a></li>
    <li><a href="#addNTips">Additional Tips</a></li>
</ol>

## <p id="desc"> 📜 Description</p>

This is a simple containerized application I developed to learn how fastAPI works and how to use it in my future projects, alongside a database to retrieve and store data (in this case, SQLModel)

### Tutorial

To develop this project, I followed this <a href="https://www.youtube.com/watch?v=k5abZLzsQc0">tutorial</a>

## <p id="container">Containerization</p>

To make this application easier to be deployed and actually executed, it has been wrapped inside a docker container, which permits to run the application and expose the service by simply running the container image, without the need to download and install all the dependencies needed.

### 🐳 Docker Image

The pre-built Docker image is available on GitHub Container Registry:

```bash
docker pull ghcr.io/gizano/simple-fastapi-application:v1.0.0
```

### 📦  Image URL: https://github.com/users/GiZano/packages/container/package/simple-fastapi-application


## <p id="api">⚙️ API</p>

### Root




| Method | URL |
|--------|-----|
| GET | / |

#### Parameters
| Name | In | Description | Required |
|------|----|-------------|----------|

##### Response (200)
| Field | Type | Description |
|-------|------|-------------|

---

### Read Zones




| Method | URL |
|--------|-----|
| GET | /zones |

#### Parameters
| Name | In | Description | Required |
|------|----|-------------|----------|

##### Response (200)
| Field | Type | Description |
|-------|------|-------------|
| data | array |  |

---

### Read Zone




| Method | URL |
|--------|-----|
| GET | /zones/{id} |

#### Parameters
| Name | In | Description | Required |
|------|----|-------------|----------|
| id | path |  | Required |

##### Response (200)
| Field | Type | Description |
|-------|------|-------------|
| data | object |  |

##### Response (422)
| Field | Type | Description |
|-------|------|-------------|
| detail | array |  |

---

### Create Zone




| Method | URL |
|--------|-----|
| POST | /zones/{id} |

#### Parameters
| Name | In | Description | Required |
|------|----|-------------|----------|

##### Request Body
| Field | Type | Description | Required |
|-------|------|-------------|----------|
| name | string |  | Required |
| region | string |  | Optional |

##### Response (201)
| Field | Type | Description |
|-------|------|-------------|
| data | object |  |

##### Response (422)
| Field | Type | Description |
|-------|------|-------------|
| detail | array |  |

---

### Update Zone




| Method | URL |
|--------|-----|
| PUT | /zones/{id} |

#### Parameters
| Name | In | Description | Required |
|------|----|-------------|----------|
| id | path |  | Required |

##### Request Body
| Field | Type | Description | Required |
|-------|------|-------------|----------|
| name | string |  | Required |
| region | string |  | Optional |

##### Response (200)
| Field | Type | Description |
|-------|------|-------------|
| data | object |  |

##### Response (422)
| Field | Type | Description |
|-------|------|-------------|
| detail | array |  |

---

### Read Zone




| Method | URL |
|--------|-----|
| DELETE | /zones/{id} |

#### Parameters
| Name | In | Description | Required |
|------|----|-------------|----------|
| id | path |  | Required |

##### Response (204)
| Field | Type | Description |
|-------|------|-------------|

##### Response (422)
| Field | Type | Description |
|-------|------|-------------|
| detail | array |  |

---


## <p id="quickS"> 💻 Quick Start</p>

### Preliminary Setup

#### Linux / MacOS

```bash
# create project folder
mkdir <projectName>
# enter project folder
cd <projectName>
# create python virtual environment
python3 -m venv .venv
# enter the virtual environment
. .\.venv\bin\activate
# create gitignore file to ignore .venv folder in repository
echo ".venv" > .gitignore
# update pip (Python installer)
pip install --upgrade pip
# install fastapi (standard components)
pip install "fastapi[standard]"
# write all packets (and versions) inside a txt to be able to reconstruct the same environment if we have to open it on a different device
pip freeze > requirements.txt
# initialize git repository
git init
# add all files (except ignored in gitignore) in git repository
git add .
# save all created files in the repository
git commit -m "initial commit"
# create main source file
touch main.py
# open folder in VSC
code .
```

#### Windows
```bash
# create project folder
mkdir <projectName>
# enter project folder
cd <projectName>
# create python virtual environment
python3 -m venv .venv
# enter the virtual environmnent
.\venv\Scripts\activate
# create gitignore file to ignore .venv folder in repository
echo ".venv" > .gitignore 
# update pip (Python installer)
python.exe -m pip install --upgrade pip
# install fastapi (standard components)
pip install "fastapi[standard]"
# write all packets (and versions) inside a txt to be able to reconstruct the same environment if we have to open it on a different device
pip freeze > requirements.txt
# initialize git repository
git init
# add all files (except ignored in gitignore) in git repository
git add .
# save all created files in the repository
git commit -m "initial commit"
# create main source file
type nul > main.py
# open folder in VSC
code . 
```

## <p id="addTips"> 🔍 Additional Tips</p>

### Enable Strict Typing

(In VSC): <br>
\> Preferences: Open User Settings (JSON) <br>

Add following line:

```
python.analysis.typeCheckingMode: "strict"
```

### Add Pylance and Python extensions

### Open .venv on VSC Terminal

#### Linux / MacOS

In terminal:

```bash
. .\.venv\bin\activate
```

#### Windows

In terminal:

```bash
.\.venv\Scripts\activate
```

#### Run Code

In terminal:

```bash
fastapi dev main.py
```

**Full Changelog**: https://github.com/GiZano/simple-fastapi-application/compare/v1.0.0...v2.0.0