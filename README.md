Spotify-Youtube-Downloader
==============================

Easily download all songs of your spotify playlist from youtube with this repo.

How to:
-----

- In the projects terminal, install the requirements using "pip install -r requirements"
- Create a .env with the variables "id" and "secret" (for help see "https://medium.com/@michaelmiller0998/extracting-song-data-from-spotify-using-spotipy-167728d0a924")
- In the projects terminal, run "streamlit run app.py"
- If your browser is not opening automatically, visit "http://localhost:8501"
- Simply paste a Spotify playlist link. 
- It then scrapes the top 5 Youtube Videos for each Song.
- Then you are asked to manually select the youtube video, you want to download
- The videos are then automatically downloaded to the "songs" directory as m4a-format


Project Organization
------------
```
├── README.md           <- The top-level README for developers using this project
│
├── requirements.txt    <- The requirements file for building the environment
│
├── .gitignore          <- Files to be ignored when uploading the repository
│
├── app.py             <- starting page of streamlit
│
├── .env                <- environment variables: OPENAI_API_KEY, CHAT_MODEL and EMBEDDING_MODEL
│
├── .streamlit          <- streamlit options directory
│  └── config.toml                     <- streamlit ui design options
│
├── venv                <- virtual environment
│  └── ...                             <- python packages
│
├── songs
│  └── ...                             <- Your downloaded songs
│
├── data
│  └── pictures                        <- pcitures for UI
│
└── scripts
   └── html_template.py                <- html/css for streamlit

```
--------
