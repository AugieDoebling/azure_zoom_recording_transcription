# Azure Zoom Recording Transcription
Python scripts to transcribe a Zoom meeting recording using Azure transcription

# Setting Up Azure Account
## Create Azure Account
Sign up for a Microsoft Azure account. If using a student account use your student email address - this will grant $100 credit.

## Get Student Credits
Follow student credentials workflow here:
https://aka.ms/startEDU

## Retrieving Azure Subscription Key
Follow steps laid out here to retrieve subscription keys. You may need to create a new resource to enable this
https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/overview#find-keys-and-region

# Install Required Pip Packages
Install packages listed in `requirements.py` using the following command
```
python -m pip install -r requirements.txt
```

# Using script
`azure_transcribe_videos.py` has several variables at the top of the script that need to be set for the script to function properly

### AZURE_SUBSCRIPTION_ID 
Retrive from instructions above

### AZURE_REGION
Azure region of subscription - formatted like `westus`

### VIDEO_INPUT_DIRECTORY
Directory to search for videos to transcribe. Script will convert any `.mp4` files in this directory

### OUTPUT_DIRECTORY
Directory to save transcription files to - directory is created if it does not exists
