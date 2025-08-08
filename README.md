# MotiMate

> **Your daily dose of motivation — fully automated.**  
MotiMate creates and posts motivational videos to Instagram Reels using AI-generated quotes, aesthetic backgrounds, and smart styling — all on autopilot.

---

## **BETA NOTICE**
**This is a beta release.** Expect bugs, Instagram API quirks, and limitations:  
- Uses **Instagram’s Private API** via [instagrapi](https://github.com/adw0rd/instagrapi) — may break anytime if Instagram changes things.  
- **Private API use may violate Instagram’s Terms of Service** — use at your own risk.   
- Designed for **1 post/day**. Not tested for higher frequency.  

---

## Features
- **Motivational Quote Generation** – AI-generated or custom quotes.  
- **Dynamic Backgrounds** – Fetches aesthetic vertical videos from Pexels.  
- **Smart Styling** – Picks text color based on video background for better visibility.  
- **Random Fonts** – Uses varied fonts for fresh daily designs.  
- **Quote + Author Split** – Author appears at the bottom, styled separately.  
- **Auto Instagram Upload** – Posts directly to Reels.

---

## Example Output
_"Be your own reason to keep going"_  
Author automatically positioned for a clean, cinematic look.  

![Example Reel](assets/example.gif) 

---

## Installation

Method 1


Method 2 

#### 1. Prerequisites
	•	Python 3.11+
	•	pip (latest version)
	•	Ollama (for local LLM models) → Install guide
After installing, pull your model:
```
ollama pull phi
```


#### 1. Clone the repo
```bash
git clone https://github.com/yourusername/motimate.git
cd motimatepipreqs . --force
```
Create & Activate a Virtual Environment (Recommended)
```
# Create virtual environment
python3 -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```
#### 2. Install Dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```


#### 3. Set up Environment Variables
```
OLLAMA_HOST=your_local_ollama_server
OLLAMA_MODEL=your_local_model_name
PEXELS_API_KEY=your_pexels_api_key
IG_USERNAME=your_instagram_username
IG_PASSWORD=your_instagram_password
```

#### 4. Run MotiMate
```
python src/main.py
```