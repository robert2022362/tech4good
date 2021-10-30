This is our group's submission to Tech4Good 2020 Hackathon. 
We created a mandarin fluency evaluation app that provides a mandarin poem for the user to read, records the user's reading, and evaluates the user's mandarin fluency (through metrics such as phonetics, tone, flunecy, and completion) via a backend API.
The API we used is from 科大讯飞 here: https://www.xfyun.cn/doc/voiceservice/ise/API.html#全维度说明

The app's logic flow:
Steps:
  1. collect users information --> to complete the e-map
  2. let users choose the poem they would like to read and start recording
  3. XunFei API and calculate a accuracy score
  4. print the accuracy
  5. empty the files
