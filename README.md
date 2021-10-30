This is our group's submission to the Tech4Good 2020 Hackathon, which we won third place overall.

We created a mandarin fluency evaluation app that provides a mandarin poem for the user to read, records the user's reading, and evaluates the user's mandarin fluency (through metrics such as phonetics, tone, flunecy, and completion) via a backend API.

The API we used is from 科大讯飞 here: https://www.xfyun.cn/doc/voiceservice/ise/API.html#全维度说明

The app's logic flow:
  1. Collect user information and store to a file
  2. Provide poems from which the user can choose to read from
  3. Record and store user's reading locally then upload to XunFei API
  4. Calculate and return fluency score
  6. Empty the storage files
