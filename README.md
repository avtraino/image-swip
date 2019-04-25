# image-swip   

- Sorts and renames photos by date and event (e.g., `2018-12-17_11.20.14__Hiking-Trip.jpg`)
    - Date relies on DateTimeOriginal EXIF tag
    - Event relies on the name of the parent folder

## Get Started
### Requirements:
* Python 3.6.1 or later
* Pipenv
### Install:
```
git clone https://github.com/avtraino/image-swip.git
cd image-swip
pipenv install
```

### Usage:
First run to create folder structure:
```
pipenv run python3 image-swip.py
```
Folder structure:
```
image-swip/
└───Data/
│   └───Inbox/
│   └───Archive/
│   └───Problems/
```

#### Workflow
* Put event folders containing images in `/Inbox/`
    - Note: by design, image files placed directly in `/Inbox/` (without a parent folder) are not processed
* run `pipenv run python3 image-swip.py`

    
    
