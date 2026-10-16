import requests

url = "https://formsubmit.co/ajax/rohit.bcastudent25.30916@cimage.in"
headers = {
    "Origin": "https://syncpulse-ai.vercel.app",
    "Referer": "https://syncpulse-ai.vercel.app/",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
data = {
    "_subject": "SyncPulse AI - Official Admin 6-Digit OTP",
    "Admin Email": "rohit.bcastudent25.30916@cimage.in",
    "Security OTP": "739201",
    "_template": "box",
    "Message": "Your 6-Digit Admin Verification OTP is: 739201. Please enter this code on the SyncPulse AI Command Center."
}

res = requests.post(url, headers=headers, json=data)
print("FormSubmit status:", res.status_code)
print("FormSubmit response:", res.text)
